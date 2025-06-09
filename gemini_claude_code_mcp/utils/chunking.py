"""Context chunking utilities for processing large codebases."""

import re

import tiktoken

from gemini_claude_code_mcp.config.settings import settings
from gemini_claude_code_mcp.utils.logging import get_logger

logger = get_logger(__name__)

# Initialize tokenizer for counting tokens
tokenizer = tiktoken.get_encoding('cl100k_base')


def count_tokens(text: str) -> int:
    """Count the number of tokens in a text."""
    return len(tokenizer.encode(text))


def find_code_boundaries(content: str, language: str) -> list[tuple[int, int]]:
    """Find natural code boundaries (functions, classes, etc.) in the content."""
    boundaries: list[tuple[int, int]] = []

    # Language-specific patterns for finding code boundaries
    patterns = {
        'python': [
            (r'^class\s+\w+.*?:', re.MULTILINE),
            (r'^def\s+\w+.*?:', re.MULTILINE),
            (r'^async\s+def\s+\w+.*?:', re.MULTILINE),
        ],
        'javascript': [
            (r'^function\s+\w+\s*\(', re.MULTILINE),
            (r'^const\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>', re.MULTILINE),
            (r'^class\s+\w+', re.MULTILINE),
            (r'^export\s+(?:default\s+)?(?:function|class|const)', re.MULTILINE),
        ],
        'typescript': [
            (r'^function\s+\w+\s*\(', re.MULTILINE),
            (r'^const\s+\w+\s*=\s*(?:async\s*)?\(.*?\)\s*=>', re.MULTILINE),
            (r'^class\s+\w+', re.MULTILINE),
            (r'^export\s+(?:default\s+)?(?:function|class|const|interface|type)', re.MULTILINE),
            (r'^interface\s+\w+', re.MULTILINE),
            (r'^type\s+\w+', re.MULTILINE),
        ],
        'java': [
            (r'^(?:public|private|protected)?\s*class\s+\w+', re.MULTILINE),
            (r'^(?:public|private|protected)?\s*(?:static\s+)?(?:final\s+)?\w+\s+\w+\s*\(', re.MULTILINE),
        ],
        'cpp': [
            (r'^class\s+\w+', re.MULTILINE),
            (r'^struct\s+\w+', re.MULTILINE),
            (r'^\w+(?:\s+\w+)*\s+\w+\s*\(', re.MULTILINE),
        ],
    }

    # Get patterns for the language, default to common patterns
    lang_patterns = patterns.get(language.lower(), patterns.get('python', []))

    for pattern, flags in lang_patterns:
        for match in re.finditer(pattern, content, flags):
            line_num = content[: match.start()].count('\n')
            boundaries.append((line_num, match.start()))

    # Sort boundaries by line number
    boundaries.sort(key=lambda x: x[0])

    return boundaries


def get_language_from_extension(filename: str) -> str:
    """Get programming language from file extension."""
    ext_to_lang = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'cpp',
        '.h': 'cpp',
        '.hpp': 'cpp',
        '.cs': 'csharp',
        '.go': 'go',
        '.rs': 'rust',
        '.rb': 'ruby',
        '.php': 'php',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.scala': 'scala',
        '.r': 'r',
        '.m': 'objc',
        '.mm': 'objc',
    }

    for ext, lang in ext_to_lang.items():
        if filename.endswith(ext):
            return lang

    return 'text'


def smart_chunk_content(
    content: str,
    filename: str,
    chunk_size: int | None = None,
    overlap_size: int | None = None,
) -> list[tuple[str, int, int]]:
    """Chunk content intelligently, respecting code boundaries.

    Returns list of (chunk_text, start_line, end_line) tuples.
    """
    if chunk_size is None:
        chunk_size = settings.processing.chunk_size
    if overlap_size is None:
        overlap_size = settings.processing.overlap

    # If content is small enough, return as single chunk
    total_tokens = count_tokens(content)
    if total_tokens <= chunk_size:
        lines = content.split('\n')
        return [(content, 0, len(lines) - 1)]

    logger.debug(f'Chunking {filename} with {total_tokens} tokens into chunks of {chunk_size}')

    # Get language and find code boundaries
    language = get_language_from_extension(filename)
    boundaries = find_code_boundaries(content, language)

    lines = content.split('\n')
    chunks: list[tuple[str, int, int]] = []
    current_chunk_lines: list[str] = []
    current_chunk_start = 0
    current_tokens = 0

    for i, line in enumerate(lines):
        line_tokens = count_tokens(line + '\n')

        # Check if adding this line would exceed chunk size
        if current_tokens + line_tokens > chunk_size and current_chunk_lines:
            # Find the best boundary to split at
            best_boundary = i

            # Look for nearby code boundaries
            for boundary_line, _ in boundaries:
                if current_chunk_start < boundary_line <= i:
                    # Check if splitting at this boundary keeps us under the limit
                    test_chunk = '\n'.join(lines[current_chunk_start:boundary_line])
                    if count_tokens(test_chunk) <= chunk_size:
                        best_boundary = boundary_line

            # Create chunk up to the best boundary
            chunk_end = best_boundary - 1
            chunk_text = '\n'.join(current_chunk_lines[: chunk_end - current_chunk_start + 1])
            chunks.append((chunk_text, current_chunk_start, chunk_end))

            # Start new chunk with overlap
            overlap_start = max(0, chunk_end - overlap_size // (line_tokens or 1))
            current_chunk_start = overlap_start
            current_chunk_lines = lines[overlap_start : i + 1]
            current_tokens = count_tokens('\n'.join(current_chunk_lines))
        else:
            current_chunk_lines.append(line)
            current_tokens += line_tokens

    # Add the last chunk
    if current_chunk_lines:
        chunk_text = '\n'.join(current_chunk_lines)
        chunks.append((chunk_text, current_chunk_start, len(lines) - 1))

    logger.info(f'Created {len(chunks)} chunks from {filename}')
    return chunks


def merge_chunk_responses(responses: list[str], overlap_size: int | None = None) -> str:
    """Merge responses from multiple chunks, handling overlaps intelligently."""
    if not responses:
        return ''

    if len(responses) == 1:
        return responses[0]

    if overlap_size is None:
        overlap_size = settings.processing.overlap

    merged = responses[0]

    for i in range(1, len(responses)):
        current_response = responses[i]

        # Try to find overlapping content
        overlap_found = False

        # Look for common lines at the boundary
        merged_lines = merged.split('\n')
        current_lines = current_response.split('\n')

        # Try different overlap sizes
        for overlap_check in range(min(len(merged_lines), len(current_lines), 10), 0, -1):
            if merged_lines[-overlap_check:] == current_lines[:overlap_check]:
                # Found overlap, merge without duplication
                merged = '\n'.join(merged_lines + current_lines[overlap_check:])
                overlap_found = True
                break

        if not overlap_found:
            # No overlap found, append with separator
            merged += '\n\n---\n\n' + current_response

    return merged


def prepare_chunked_context(
    files_content: list[tuple[str, str]],  # List of (filename, content) tuples
    query: str,
    max_context_size: int | None = None,
) -> list[tuple[str, str]]:
    """Prepare chunked context from multiple files for processing.

    Returns list of (context_description, context_content) tuples.
    """
    if max_context_size is None:
        max_context_size = settings.gemini.max_tokens

    # Reserve tokens for the query and response
    query_tokens = count_tokens(query)
    reserved_tokens = query_tokens + settings.gemini.max_output_tokens + 1000  # Buffer
    available_tokens = max_context_size - reserved_tokens

    logger.debug(f'Available tokens for context: {available_tokens}')

    all_chunks: list[tuple[str, str]] = []

    # Process each file
    for filename, content in files_content:
        file_chunks = smart_chunk_content(content, filename)
        for chunk_text, start_line, end_line in file_chunks:
            chunk_desc = f'{filename} (lines {start_line + 1}-{end_line + 1})'
            all_chunks.append((chunk_desc, chunk_text))

    # Group chunks into contexts that fit within token limits
    contexts: list[tuple[str, str]] = []
    current_context_parts: list[tuple[str, str]] = []
    current_context_tokens = 0

    for chunk_desc, chunk_text in all_chunks:
        chunk_tokens = count_tokens(chunk_text)

        if current_context_tokens + chunk_tokens > available_tokens and current_context_parts:
            # Create context from current parts
            context_desc = f'Context with {len(current_context_parts)} parts'
            context_content = '\n\n'.join([f'### {desc}\n\n{text}' for desc, text in current_context_parts])
            contexts.append((context_desc, context_content))

            # Start new context
            current_context_parts = [(chunk_desc, chunk_text)]
            current_context_tokens = chunk_tokens
        else:
            current_context_parts.append((chunk_desc, chunk_text))
            current_context_tokens += chunk_tokens

    # Add remaining context
    if current_context_parts:
        context_desc = f'Context with {len(current_context_parts)} parts'
        context_content = '\n\n'.join([f'### {desc}\n\n{text}' for desc, text in current_context_parts])
        contexts.append((context_desc, context_content))

    logger.info(f'Prepared {len(contexts)} contexts from {len(files_content)} files')
    return contexts
