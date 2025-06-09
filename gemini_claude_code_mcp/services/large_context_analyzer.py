"""Large context analyzer service for processing files that exceed Claude's context window."""

import asyncio
import hashlib
import json
from collections.abc import Coroutine
from typing import Any

from cachetools import TTLCache

from gemini_claude_code_mcp.config.settings import settings
from gemini_claude_code_mcp.models.context import AnalysisRequest, AnalysisResult, ChunkingStrategy
from gemini_claude_code_mcp.services.gemini import gemini_text_to_text
from gemini_claude_code_mcp.utils.chunking import count_tokens, smart_chunk_content
from gemini_claude_code_mcp.utils.logging import get_logger

logger = get_logger(__name__)


class LargeContextAnalyzer:
    """Service for analyzing large contexts using Gemini's extended context window."""

    def __init__(self):
        self.cache: TTLCache[str, AnalysisResult] = TTLCache(
            maxsize=settings.cache_max_size, ttl=settings.cache_ttl_seconds
        )
        self.claude_limit = settings.context_limits.claude_max_tokens
        self.gemini_limit = settings.context_limits.gemini_max_tokens

    def needs_large_context_processing(self, content: str) -> bool:
        """Check if content exceeds Claude's context limit."""
        token_count = count_tokens(content)
        logger.debug(f'Content has {token_count} tokens (Claude limit: {self.claude_limit})')
        return token_count > self.claude_limit

    async def analyze(self, request: AnalysisRequest) -> AnalysisResult:
        """Analyze content, automatically using Gemini for large contexts."""
        cache_key = self._generate_cache_key(request)

        # Check cache first
        if cache_key in self.cache:
            logger.info('Returning cached analysis result')
            return self.cache[cache_key]

        total_tokens = count_tokens(request.content)

        if not self.needs_large_context_processing(request.content):
            # Content fits in Claude's context, no need for Gemini
            logger.info(f"Content fits in Claude's context ({total_tokens} tokens)")
            result = AnalysisResult(
                query=request.query,
                content=request.content,
                total_tokens=total_tokens,
                chunks_processed=0,
                used_gemini=False,
                response=None,
            )
            self.cache[cache_key] = result
            return result

        # Process with Gemini
        logger.info(f'Processing large context ({total_tokens} tokens) with Gemini')

        # Use appropriate chunking strategy
        if request.chunking_strategy == ChunkingStrategy.CODE_AWARE:
            # Use existing chunking utility
            filename = request.context_metadata.get('filename', 'content.txt')
            chunks = smart_chunk_content(
                request.content,
                filename,
                chunk_size=self.gemini_limit - 1000,  # Leave room for prompts
            )
        else:
            # For simple chunking, just split by size
            chunks = self._simple_chunk_by_size(request.content)
        response = await self._process_chunks_with_gemini(chunks, request.query)

        result = AnalysisResult(
            query=request.query,
            content=request.content,
            total_tokens=total_tokens,
            chunks_processed=len(chunks),
            used_gemini=True,
            response=response,
        )

        self.cache[cache_key] = result
        return result

    def _simple_chunk_by_size(self, content: str) -> list[tuple[str, int, int]]:
        """Simple chunking by token count, returns format compatible with smart_chunk_content."""
        chunks: list[tuple[str, int, int]] = []
        lines = content.split('\n')
        current_chunk = []
        current_tokens = 0
        chunk_limit = self.gemini_limit - 1000  # Leave room for prompts
        start_line = 0

        for i, line in enumerate(lines):
            line_tokens = count_tokens(line + '\n')

            if current_tokens + line_tokens > chunk_limit and current_chunk:
                chunk_text = '\n'.join(current_chunk)
                chunks.append((chunk_text, start_line, i - 1))
                current_chunk = [line]
                current_tokens = line_tokens
                start_line = i
            else:
                current_chunk.append(line)
                current_tokens += line_tokens

        if current_chunk:
            chunk_text = '\n'.join(current_chunk)
            chunks.append((chunk_text, start_line, len(lines) - 1))

        return chunks

    async def _process_chunks_with_gemini(
        self,
        chunks: list[tuple[str, int, int]],  # (chunk_text, start_line, end_line)
        query: str,
    ) -> str:
        """Process chunks through Gemini and aggregate responses."""
        if not chunks:
            return 'No content to analyze'

        # For single chunk, process directly
        if len(chunks) == 1:
            chunk_text, start_line, end_line = chunks[0]
            prompt = (
                f'Analyze the following code/content and answer this query: {query}\n\n'
                f'Content:\n{chunk_text}\n\n'
                f'Provide a comprehensive answer based on the content above.'
            )

            result = await gemini_text_to_text(prompt)
            return result or 'No response from Gemini'

        # For multiple chunks, process in parallel with context
        chunk_responses: list[str | None] = []
        tasks: list[Coroutine[Any, Any, str | None]] = []

        for i, (chunk_text, start_line, end_line) in enumerate(chunks):
            prompt = (
                f'You are analyzing part {i + 1} of {len(chunks)} of a larger codebase.\n'
                f'Query: {query}\n\n'
                f'Content (lines {start_line}-{end_line}):\n'
                f'{chunk_text}\n\n'
                f'Analyze this section and provide findings relevant to the query.\n'
                f'Note any references to other parts that might be in other chunks.'
            )

            tasks.append(gemini_text_to_text(prompt))

        chunk_responses = await asyncio.gather(*tasks)

        # Aggregate responses
        findings = '\n\n'.join([f'Part {i + 1}: {resp}' for i, resp in enumerate(chunk_responses) if resp])

        aggregation_prompt = (
            f'You analyzed a large codebase in {len(chunks)} parts for this query: {query}\n\n'
            f'Here are the findings from each part:\n\n'
            f'{findings}\n\n'
            f'Synthesize these findings into a comprehensive answer. '
            f'Resolve any cross-references between parts and provide a cohesive response.'
        )

        final_result = await gemini_text_to_text(aggregation_prompt)
        return final_result or 'No response from Gemini'

    def _generate_cache_key(self, request: AnalysisRequest) -> str:
        """Generate a cache key for the request."""
        key_data = {
            'query': request.query,
            'content_hash': hashlib.sha256(request.content.encode()).hexdigest(),
            'strategy': request.chunking_strategy.value,
        }
        return hashlib.sha256(json.dumps(key_data).encode()).hexdigest()
