"""Project summarization tool for analyzing codebases."""

from pathlib import Path
from typing import Any

from fastmcp import FastMCP

from gemini_claude_code_mcp.models.context import AnalysisRequest, ChunkingStrategy, FilePattern
from gemini_claude_code_mcp.services.file_collector import FileCollector
from gemini_claude_code_mcp.services.large_context_analyzer import LargeContextAnalyzer
from gemini_claude_code_mcp.utils.chunking import count_tokens
from gemini_claude_code_mcp.utils.logging import get_logger

logger = get_logger(__name__)


def register_summarize_project_tool(mcp: FastMCP[Any]):
    """Register the summarize_project tool with the MCP server."""

    @mcp.tool()
    async def summarize_project(  # type: ignore
        directory_path: str,
        focus_areas: list[str] | None,
        include_patterns: list[str] | None,
        exclude_patterns: list[str] | None,
    ) -> dict[str, Any]:
        """Generate a comprehensive summary of a project/codebase.

        This tool analyzes an entire project directory and provides a multi-level summary including:
        - Project structure and organization
        - Technology stack and dependencies
        - Main components and their purposes
        - Architecture patterns and design decisions
        - Key APIs and interfaces

        Args:
            directory_path: Absolute path to the project directory
            focus_areas: Optional list of specific areas to focus on (e.g., ["authentication", "api", "database"])
            include_patterns: Optional file patterns to include (e.g., ["*.py", "src/**/*.js"])
            exclude_patterns: Optional file patterns to exclude beyond defaults

        Returns:
            Dictionary containing:
            - overview: High-level project summary
            - structure: Directory structure analysis
            - tech_stack: Detected technologies and frameworks
            - components: Main components and their descriptions
            - architecture: Architectural patterns and decisions
            - statistics: Project statistics (file counts, sizes, etc.)
        """
        try:
            # Validate directory path
            project_path = Path(directory_path).resolve()
            if not project_path.exists():
                return {
                    'error': f'Directory not found: {directory_path}',
                    'status': 'failed',
                }

            if not project_path.is_dir():
                return {
                    'error': f'Path is not a directory: {directory_path}',
                    'status': 'failed',
                }

            logger.info(f'Starting project summary for: {project_path}')

            # Initialize services
            file_collector = FileCollector()
            analyzer = LargeContextAnalyzer()

            # Prepare file pattern
            file_pattern = FilePattern(
                include=include_patterns or [],
                exclude=exclude_patterns or [],
                respect_gitignore=True,
            )

            # Collect files
            logger.info('Collecting project files...')
            collected_files = await file_collector.collect_files(str(project_path), file_pattern)

            if not collected_files:
                return {
                    'error': 'No files found matching the specified patterns',
                    'status': 'failed',
                }

            logger.info(f'Collected {len(collected_files)} files')

            # Generate project structure
            structure = _generate_project_structure(project_path, collected_files)

            # Prepare analysis query
            focus_context = ''
            if focus_areas:
                focus_context = f'\nPay special attention to these areas: {", ".join(focus_areas)}'

            analysis_query = f"""Analyze this codebase and provide a comprehensive project summary including:
            1. **Overview**: A high-level description of what this project does and its main purpose
            2. **Technology Stack**: List all detected programming languages, frameworks, libraries, and tools
            3. **Architecture**: Identify architectural patterns, design decisions, and project organization
            4. **Main Components**: List and describe the main components, modules, or services
            5. **Key Features**: Identify the key features and functionalities implemented
            6. **Dependencies**: Note important external dependencies and integrations
            7. **Code Quality**: Comment on code organization, patterns, and best practices observed
            {focus_context}
            Provide a structured, detailed summary that would help a developer quickly understand this codebase."""

            # Combine file contents for analysis
            combined_content = _combine_file_contents(collected_files, project_path)
            total_tokens = count_tokens(combined_content)

            logger.info(f'Total content tokens: {total_tokens}')

            # Create analysis request
            analysis_request = AnalysisRequest(
                query=analysis_query,
                content=combined_content,
                chunking_strategy=ChunkingStrategy.CODE_AWARE,
                context_metadata={
                    'project_path': str(project_path),
                    'file_count': len(collected_files),
                },
            )

            # Analyze with LargeContextAnalyzer
            logger.info('Analyzing project content...')
            analysis_result = await analyzer.analyze(analysis_request)

            # Generate statistics
            statistics = _generate_statistics(collected_files)

            # Parse the analysis response into structured sections
            structured_summary = _parse_analysis_response(analysis_result.response or 'No analysis available')

            return {
                'status': 'success',
                'project_path': str(project_path),
                'overview': structured_summary.get('overview', 'No overview available'),
                'structure': structure,
                'tech_stack': structured_summary.get('tech_stack', {}),
                'architecture': structured_summary.get('architecture', {}),
                'components': structured_summary.get('components', []),
                'key_features': structured_summary.get('key_features', []),
                'dependencies': structured_summary.get('dependencies', []),
                'code_quality': structured_summary.get('code_quality', {}),
                'statistics': statistics,
                'analysis_details': {
                    'files_analyzed': len(collected_files),
                    'total_tokens': total_tokens,
                    'used_gemini': analysis_result.used_gemini,
                    'chunks_processed': analysis_result.chunks_processed,
                },
            }

        except Exception as e:
            logger.error(f'Error summarizing project: {e}', exc_info=True)
            return {
                'error': f'Failed to summarize project: {str(e)}',
                'status': 'failed',
            }


def _generate_project_structure(project_path: Path, collected_files: list[Any]) -> dict[str, Any]:
    """Generate a hierarchical representation of the project structure."""
    structure: dict[str, Any] = {'name': project_path.name, 'type': 'directory', 'children': {}}

    for file in collected_files:
        relative_path = Path(file.relative_path)
        parts = relative_path.parts

        current: dict[str, Any] = structure['children']
        for part in parts[:-1]:
            if part not in current:
                current[part] = {'type': 'directory', 'children': {}}
            current = current[part]['children']

        # Add the file
        filename = parts[-1]
        current[filename] = {
            'type': 'file',
            'language': file.language,
            'size': file.size,
            'tokens': file.token_count,
        }

    return structure


def _combine_file_contents(collected_files: list[Any], project_path: Path) -> str:
    """Combine file contents with metadata headers."""
    combined_parts: list[str] = []

    # Add project overview
    combined_parts.append(f'# Project: {project_path.name}')
    combined_parts.append(f'# Path: {project_path}')
    combined_parts.append(f'# Total Files: {len(collected_files)}')
    combined_parts.append('\n---\n')

    # Add each file with header
    for file in collected_files:
        header = f'\n### File: {file.relative_path}\n'
        header += f'Language: {file.language or "unknown"}\n'
        header += f'Size: {file.size} bytes | Tokens: {file.token_count}\n'
        header += '```\n'

        combined_parts.append(header)
        combined_parts.append(file.content)
        combined_parts.append('\n```\n')

    return '\n'.join(combined_parts)


def _generate_statistics(collected_files: list[Any]) -> dict[str, Any]:
    """Generate project statistics."""
    stats: dict[str, Any] = {
        'total_files': len(collected_files),
        'total_size_bytes': sum(f.size for f in collected_files),
        'total_tokens': sum(f.token_count for f in collected_files),
        'languages': {},
        'file_types': {},
    }

    # Count by language
    for file in collected_files:
        lang = file.language or 'unknown'
        if lang not in stats['languages']:
            stats['languages'][lang] = 0
        stats['languages'][lang] += 1

        # Count by extension
        ext = Path(file.relative_path).suffix or 'no_extension'
        if ext not in stats['file_types']:
            stats['file_types'][ext] = 0
        stats['file_types'][ext] += 1

    # Sort languages by count
    stats['languages'] = dict(sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True))

    # Add human-readable size
    size_mb = stats['total_size_bytes'] / (1024 * 1024)
    stats['total_size_mb'] = round(size_mb, 2)

    return stats


def _parse_analysis_response(response: str) -> dict[str, Any]:
    """Parse the analysis response into structured sections."""
    # This is a simple parser that looks for markdown sections
    # In production, you might want to use a more sophisticated approach

    sections: dict[str, Any] = {
        'overview': '',
        'tech_stack': {},
        'architecture': {},
        'components': [],
        'key_features': [],
        'dependencies': [],
        'code_quality': {},
    }

    current_section: str | None = None
    current_content: list[str] = []

    lines = response.split('\n')

    for line in lines:
        # Check for section headers
        if line.startswith('**Overview**') or line.startswith('1. **Overview**'):
            current_section = 'overview'
            current_content = []
        elif line.startswith('**Technology Stack**') or line.startswith('2. **Technology Stack**'):
            current_section = 'tech_stack'
            current_content = []
        elif line.startswith('**Architecture**') or line.startswith('3. **Architecture**'):
            current_section = 'architecture'
            current_content = []
        elif line.startswith('**Main Components**') or line.startswith('4. **Main Components**'):
            current_section = 'components'
            current_content = []
        elif line.startswith('**Key Features**') or line.startswith('5. **Key Features**'):
            current_section = 'key_features'
            current_content = []
        elif line.startswith('**Dependencies**') or line.startswith('6. **Dependencies**'):
            current_section = 'dependencies'
            current_content = []
        elif line.startswith('**Code Quality**') or line.startswith('7. **Code Quality**'):
            current_section = 'code_quality'
            current_content = []
        elif current_section:
            # Add content to current section
            if line.strip():
                current_content.append(line.strip())

    # Process collected content
    if 'overview' in sections:
        sections['overview'] = '\n'.join(current_content).strip()

    # For now, return the full response in overview if parsing fails
    if not any(sections.values()):
        sections['overview'] = response

    return sections
