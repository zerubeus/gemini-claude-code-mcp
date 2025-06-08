"""Context models for managing large code contexts."""

from datetime import datetime
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class FileContent(BaseModel):
    """Model for file content with metadata."""
    
    path: Path = Field(description="File path")
    content: str = Field(description="File content")
    size: int = Field(description="File size in bytes")
    modified: datetime = Field(description="Last modified timestamp")
    language: Optional[str] = Field(default=None, description="Programming language")
    encoding: str = Field(default="utf-8", description="File encoding")


class ContextChunk(BaseModel):
    """Model for a chunk of context."""
    
    id: str = Field(description="Unique chunk identifier")
    content: str = Field(description="Chunk content")
    token_count: int = Field(description="Number of tokens in chunk")
    files: list[str] = Field(description="Files included in this chunk")
    start_index: int = Field(description="Start index in original context")
    end_index: int = Field(description="End index in original context")
    overlap_previous: Optional[str] = Field(
        default=None,
        description="ID of previous chunk with overlap"
    )
    overlap_next: Optional[str] = Field(
        default=None,
        description="ID of next chunk with overlap"
    )


class AnalysisRequest(BaseModel):
    """Model for analysis request."""
    
    files: list[str] = Field(description="Files or patterns to analyze")
    query: str = Field(description="Analysis query")
    model: str = Field(default="gemini-2.0-flash-exp", description="Model to use")
    max_chunks: Optional[int] = Field(
        default=None,
        description="Maximum number of chunks to process"
    )
    include_dependencies: bool = Field(
        default=True,
        description="Include file dependencies in context"
    )


class AnalysisResult(BaseModel):
    """Model for analysis result."""
    
    query: str = Field(description="Original query")
    response: str = Field(description="Analysis response")
    chunks_processed: int = Field(description="Number of chunks processed")
    total_tokens: int = Field(description="Total tokens processed")
    files_analyzed: list[str] = Field(description="Files that were analyzed")
    model_used: str = Field(description="Gemini model used")
    processing_time: float = Field(description="Processing time in seconds")
    cached: bool = Field(default=False, description="Whether result was cached")


class CodebaseSnapshot(BaseModel):
    """Model for codebase snapshot."""
    
    path: Path = Field(description="Root path of codebase")
    total_files: int = Field(description="Total number of files")
    total_size: int = Field(description="Total size in bytes")
    languages: dict[str, int] = Field(
        description="Language distribution (language -> file count)"
    )
    structure: dict = Field(description="Directory structure")
    generated_at: datetime = Field(
        default_factory=datetime.now,
        description="Snapshot generation timestamp"
    )