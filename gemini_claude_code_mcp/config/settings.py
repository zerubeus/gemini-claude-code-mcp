"""Configuration settings for Gemini-Claude Code MCP server."""

from typing import Literal, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeminiSettings(BaseSettings):
    """Settings for Google Gemini API."""

    api_key: str = Field(default='', description='Google API key for Gemini')
    model: str = Field(default='gemini-2.0-flash-exp', description='Default Gemini model to use')
    max_tokens: int = Field(default=2000000, description='Maximum context size in tokens')
    temperature: float = Field(default=0.1, ge=0.0, le=2.0, description='Temperature for generation')
    timeout: int = Field(default=300, description='API timeout in seconds')
    max_output_tokens: int = Field(default=1000, ge=1, le=2000000, description='Maximum output tokens per request')

    @field_validator('model')
    @classmethod
    def validate_model(cls, v: str) -> str:
        """Validate that the model is a supported Gemini model."""
        valid_models = [
            'gemini-2.0-flash-exp',
            'gemini-1.5-pro',
            'gemini-1.5-pro-002',
            'gemini-1.5-flash',
            'gemini-1.5-flash-002',
            'gemini-1.5-flash-8b',
            'gemini-2.5-pro-preview-06-05',  # Add newer model
        ]
        if v not in valid_models:
            raise ValueError(f'Model must be one of {valid_models}')
        return v


class CacheSettings(BaseSettings):
    """Settings for context caching."""

    enabled: bool = Field(default=True, description='Enable context caching')
    ttl: int = Field(default=3600, description='Cache time-to-live in seconds')
    max_size_gb: float = Field(default=1.0, description='Maximum cache size in GB')
    eviction_policy: Literal['lru', 'lfu', 'fifo'] = Field(default='lru', description='Cache eviction policy')


class ProcessingSettings(BaseSettings):
    """Settings for context processing."""

    chunk_size: int = Field(default=100000, description='Size of context chunks in tokens')
    overlap: int = Field(default=1000, description='Overlap between chunks in tokens')
    parallel_chunks: int = Field(default=4, ge=1, le=10, description='Number of chunks to process in parallel')
    file_extensions: list[str] = Field(
        default=[
            '.py',
            '.js',
            '.ts',
            '.jsx',
            '.tsx',
            '.java',
            '.cpp',
            '.c',
            '.h',
            '.hpp',
            '.cs',
            '.go',
            '.rs',
            '.rb',
            '.php',
            '.swift',
            '.kt',
            '.scala',
            '.r',
            '.m',
            '.mm',
            '.md',
            '.txt',
            '.json',
            '.yaml',
            '.yml',
            '.toml',
            '.xml',
            '.html',
            '.css',
            '.scss',
        ],
        description='File extensions to include in analysis',
    )
    ignore_patterns: list[str] = Field(
        default=[
            '__pycache__',
            '.git',
            '.venv',
            'node_modules',
            '.pytest_cache',
            '*.pyc',
            '*.pyo',
            '*.egg-info',
            'dist',
            'build',
            '.DS_Store',
        ],
        description='Patterns to ignore during file traversal',
    )


class LoggingSettings(BaseSettings):
    """Settings for logging configuration."""

    level: Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] = Field(default='INFO', description='Logging level')
    format: str = Field(
        default='%(asctime)s - %(name)s - %(levelname)s - %(message)s', description='Log message format'
    )
    file: Optional[str] = Field(default=None, description='Log file path (None for stdout only)')
    max_file_size_mb: int = Field(default=10, description='Maximum log file size in MB')
    backup_count: int = Field(default=5, description='Number of backup log files to keep')


class ContextLimits(BaseSettings):
    """Context size limits for different models."""

    claude_max_tokens: int = Field(default=200000, description='Claude max context tokens')
    gemini_max_tokens: int = Field(default=2000000, description='Gemini max context tokens')


class Settings(BaseSettings):
    """Main settings for the MCP server."""

    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', env_nested_delimiter='__', extra='ignore'
    )

    # Sub-settings
    gemini: GeminiSettings = Field(default_factory=GeminiSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    processing: ProcessingSettings = Field(default_factory=ProcessingSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    context_limits: ContextLimits = Field(default_factory=ContextLimits)

    # Server settings
    server_name: str = Field(default='gemini-claude-code', description='MCP server name')
    server_version: str = Field(default='0.1.0', description='MCP server version')

    # Performance settings
    max_concurrent_requests: int = Field(default=10, ge=1, le=50, description='Maximum concurrent requests to handle')
    request_timeout: int = Field(default=600, description='Request timeout in seconds')

    # Security settings
    rate_limit_requests: int = Field(default=100, description='Maximum requests per minute')
    rate_limit_window: int = Field(default=60, description='Rate limit window in seconds')

    # Cache settings (for LargeContextAnalyzer)
    cache_max_size: int = Field(default=100, description='Max number of cached analysis results')
    cache_ttl_seconds: int = Field(default=3600, description='Cache TTL in seconds')


# Create a singleton settings instance
settings = Settings()
