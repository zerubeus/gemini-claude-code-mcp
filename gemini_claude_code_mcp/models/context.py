"""Context models for managing large code contexts."""

from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ChunkingStrategy(str, Enum):
    """Strategy for chunking large content."""

    SIMPLE = 'simple'
    CODE_AWARE = 'code_aware'
    SEMANTIC = 'semantic'


class FileContent(BaseModel):
    """Model for file content with metadata."""

    path: Path = Field(description='File path')
    content: str = Field(description='File content')
    size: int = Field(description='File size in bytes')
    modified: datetime = Field(description='Last modified timestamp')
    language: str | None = Field(default=None, description='Programming language')
    encoding: str = Field(default='utf-8', description='File encoding')


class ContextChunk(BaseModel):
    """Model for a chunk of context."""

    content: str = Field(description='Chunk content')
    start_line: int = Field(description='Start line number in original content')
    end_line: int = Field(description='End line number in original content')
    token_count: int = Field(description='Number of tokens in chunk')
    metadata: dict[str, Any] = Field(default_factory=dict, description='Additional metadata')


class AnalysisRequest(BaseModel):
    """Model for analysis request."""

    query: str = Field(description='Analysis query')
    content: str = Field(description='Content to analyze')
    chunking_strategy: ChunkingStrategy = Field(default=ChunkingStrategy.CODE_AWARE, description='Chunking strategy')
    context_metadata: dict[str, Any] = Field(default_factory=dict, description='Additional context metadata')


class AnalysisResult(BaseModel):
    """Model for analysis result."""

    query: str = Field(description='Original query')
    content: str = Field(description='Original content')
    total_tokens: int = Field(description='Total tokens processed')
    chunks_processed: int = Field(description='Number of chunks processed')
    used_gemini: bool = Field(description='Whether Gemini was used')
    response: str | None = Field(description='Analysis response')
    metadata: dict[str, Any] = Field(default_factory=dict, description='Additional metadata')


class FilePattern(BaseModel):
    """Pattern for matching files."""

    include: list[str] = Field(default_factory=list, description='Patterns to include')
    exclude: list[str] = Field(default_factory=list, description='Patterns to exclude')
    respect_gitignore: bool = Field(default=True, description='Respect .gitignore files')


class CollectedFile(BaseModel):
    """Represents a collected file with metadata."""

    path: str = Field(description='Absolute file path')
    relative_path: str = Field(description='Relative file path')
    content: str = Field(description='File content')
    size: int = Field(description='File size in bytes')
    token_count: int = Field(description='Token count')
    language: str | None = Field(default=None, description='Programming language')
    relevance_score: float = Field(default=0.0, description='Relevance score')


class CodebaseSnapshot(BaseModel):
    """Model for codebase snapshot."""

    path: Path = Field(description='Root path of codebase')
    total_files: int = Field(description='Total number of files')
    total_size: int = Field(description='Total size in bytes')
    languages: dict[str, int] = Field(description='Language distribution (language -> file count)')
    structure: dict[str, Any] = Field(description='Directory structure')
    generated_at: datetime = Field(default_factory=datetime.now, description='Snapshot generation timestamp')
