"""File collector service for discovering and loading files."""

import fnmatch
import os
from collections.abc import AsyncIterator
from pathlib import Path

import aiofiles
from git import InvalidGitRepositoryError, Repo

from gemini_claude_code_mcp.config.settings import settings
from gemini_claude_code_mcp.models.context import CollectedFile, FilePattern
from gemini_claude_code_mcp.utils.chunking import count_tokens, get_language_from_extension
from gemini_claude_code_mcp.utils.logging import get_logger

logger = get_logger(__name__)


class FileCollector:
    """Service for collecting files based on patterns."""

    def __init__(self):
        self.supported_extensions = set(settings.processing.file_extensions)
        self.ignore_patterns = set(settings.processing.ignore_patterns)

    async def collect_files(self, root_path: str, pattern: FilePattern) -> list[CollectedFile]:
        """Collect files matching the pattern from root path."""
        root = Path(root_path).resolve()

        if not root.exists():
            raise ValueError(f'Path does not exist: {root}')

        # Get gitignore patterns if requested
        gitignore_patterns: set[str] = set()
        if pattern.respect_gitignore:
            gitignore_patterns = self._load_gitignore_patterns(root)

        # Combine all ignore patterns
        all_ignore_patterns = self.ignore_patterns | gitignore_patterns | set(pattern.exclude)

        # Collect files
        collected_files: list[CollectedFile] = []
        async for file_path in self._discover_files(root, pattern.include, all_ignore_patterns):
            try:
                collected_file = await self._load_file(file_path, root)
                if collected_file:
                    collected_files.append(collected_file)
            except Exception as e:
                logger.warning(f'Failed to load file {file_path}: {e}')

        logger.info(f'Collected {len(collected_files)} files from {root}')
        return collected_files

    async def _discover_files(
        self, root: Path, include_patterns: list[str], ignore_patterns: set[str]
    ) -> AsyncIterator[Path]:
        """Discover files matching patterns."""
        # If no include patterns, include all supported files
        if not include_patterns:
            include_patterns = [f'**/*{ext}' for ext in self.supported_extensions]

        # Use asyncio to walk directory tree
        for dirpath, dirnames, filenames in os.walk(root):
            current_dir = Path(dirpath)

            # Filter out ignored directories
            dirnames[:] = [
                d for d in dirnames if not any(self._matches_pattern(d, pattern) for pattern in ignore_patterns)
            ]

            # Check files
            for filename in filenames:
                file_path = current_dir / filename
                relative_path = file_path.relative_to(root)

                # Skip if matches ignore pattern
                if any(self._matches_pattern(str(relative_path), pattern) for pattern in ignore_patterns):
                    continue

                # Check if matches include pattern
                if any(self._matches_pattern(str(relative_path), pattern) for pattern in include_patterns):
                    yield file_path

    async def _load_file(self, file_path: Path, root: Path) -> CollectedFile | None:
        """Load a file and create CollectedFile object."""
        try:
            # Get file stats
            stat = file_path.stat()

            # Skip very large files (>10MB)
            if stat.st_size > 10 * 1024 * 1024:
                logger.warning(f'Skipping large file: {file_path} ({stat.st_size} bytes)')
                return None

            # Read file content
            async with aiofiles.open(file_path, encoding='utf-8', errors='ignore') as f:  # type: ignore
                content = await f.read()

            # Count tokens
            token_count = count_tokens(content)

            # Detect language
            language = get_language_from_extension(str(file_path))

            return CollectedFile(
                path=str(file_path),
                relative_path=str(file_path.relative_to(root)),
                content=content,
                size=stat.st_size,
                token_count=token_count,
                language=language,
                relevance_score=0.0,  # Will be set by relevance scoring
            )

        except Exception as e:
            logger.error(f'Error loading file {file_path}: {e}')
            return None

    def _load_gitignore_patterns(self, root: Path) -> set[str]:
        """Load patterns from .gitignore files."""
        patterns: set[str] = set()

        try:
            repo = Repo(root)
            # Get patterns from git's exclude info
            for item in repo.ignored(root):
                patterns.add(str(Path(item).relative_to(root)))
        except InvalidGitRepositoryError:
            # Not a git repo, check for .gitignore file
            gitignore_path = root / '.gitignore'
            if gitignore_path.exists():
                with open(gitignore_path) as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            patterns.add(line)

        return patterns

    def _matches_pattern(self, path: str, pattern: str) -> bool:
        """Check if path matches pattern."""
        # Handle glob patterns
        if '*' in pattern or '?' in pattern or '[' in pattern:
            return fnmatch.fnmatch(path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern)
        # Handle directory patterns
        elif pattern.endswith('/'):
            return path.startswith(pattern) or os.path.basename(path) == pattern[:-1]
        # Handle exact matches
        else:
            return pattern in path or os.path.basename(path) == pattern

    async def score_relevance(self, files: list[CollectedFile], query: str) -> list[CollectedFile]:
        """Score files by relevance to query."""
        # Simple keyword-based scoring for now
        query_terms = set(query.lower().split())

        for file in files:
            score = 0.0
            content_lower = file.content.lower()
            path_lower = file.relative_path.lower()

            # Score based on query terms in content
            for term in query_terms:
                score += content_lower.count(term) * 0.1

            # Bonus for terms in filename
            for term in query_terms:
                if term in path_lower:
                    score += 5.0

            # Normalize by file size
            if file.token_count > 0:
                score = score / (file.token_count / 1000)

            file.relevance_score = min(score, 100.0)  # Cap at 100

        # Sort by relevance
        files.sort(key=lambda f: f.relevance_score, reverse=True)

        return files
