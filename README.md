# 🔄 Gemini-Claude Code MCP Server

## 🔮 Enable Claude Code to Harness Gemini for Ultra-Large Context Workloads 🧠⚡

Let Claude tap into Gemini's extended context window for smarter, bigger, and faster code reasoning.

## 🎯 Project Overview

This MCP (Model Context Protocol) server bridges Claude Code with Google's Gemini models, enabling Claude to leverage Gemini's massive context window (up to 1M tokens) for processing large codebases, extensive documentation, and complex multi-file analysis tasks that would otherwise exceed Claude's native context limits.

### Key Benefits

- **🚀 Extended Context**: Access Gemini's 2M token context window for massive codebases
- **🧠 Hybrid Intelligence**: Combine Claude's reasoning with Gemini's large-scale processing
- **⚡ Performance**: Offload context-heavy operations to Gemini while keeping Claude responsive
- **🔧 Seamless Integration**: Works directly within Claude Code via MCP protocol

## 🏗️ Architecture

### System Components

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│   Claude Code   │ <-----> │   MCP Server     │ <-----> │  Gemini API     │
│                 │   MCP   │                  │  HTTP   │                 │
│  (Reasoning &   │         │  (Bridge Layer)  │         │ (Large Context  │
│   Execution)    │         │                  │         │   Processing)   │
└─────────────────┘         └──────────────────┘         └─────────────────┘
```

### Core Modules

1. **MCP Server** (`mcp_server/server.py`)

   - Handles MCP protocol communication with Claude Code
   - Routes requests between Claude and Gemini
   - Manages session state and context switching

2. **Gemini Service** (`services/gemini_manager.py`)

   - Manages Gemini API connections using the [Google AI Python SDK](https://ai.google.dev/gemini-api/docs)
   - Handles context chunking and streaming
   - Optimizes token usage and caching

3. **Context Tools** (`tools/`)
   - `analyze_large_context`: Process entire repositories or documentation sets
   - `summarize_codebase`: Generate intelligent summaries of large projects
   - `cross_file_analysis`: Analyze dependencies and relationships across many files
   - `context_search`: Search through massive contexts efficiently
   - `code_generation`: Generate code with full project context awareness

## 🛠️ Technical Implementation

### MCP Tools Available

#### 1. `analyze_large_context`

Processes large amounts of code or documentation that exceed Claude's context window.

```json
{
  "name": "analyze_large_context",
  "parameters": {
    "files": ["array of file paths or patterns"],
    "query": "analysis query or task",
    "model": "gemini-1.5-pro-002" // optional, defaults to best available
  }
}
```

#### 2. `summarize_codebase`

Creates intelligent summaries of entire codebases.

```json
{
  "name": "summarize_codebase",
  "parameters": {
    "path": "/path/to/codebase",
    "focus_areas": ["optional areas of interest"],
    "detail_level": "high|medium|low"
  }
}
```

#### 3. `cross_file_analysis`

Analyzes relationships and dependencies across multiple files.

```json
{
  "name": "cross_file_analysis",
  "parameters": {
    "files": ["file patterns"],
    "analysis_type": "dependencies|interfaces|data_flow|security"
  }
}
```

#### 4. `context_search`

Search through massive contexts using Gemini's understanding.

```json
{
  "name": "context_search",
  "parameters": {
    "query": "search query",
    "scope": "codebase|documentation|all",
    "semantic": true // use semantic search vs keyword
  }
}
```

#### 5. `code_generation`

Generate code with full project context awareness.

```json
{
  "name": "code_generation",
  "parameters": {
    "task": "generation task description",
    "context_files": ["relevant files for context"],
    "style_guide": "optional style preferences"
  }
}
```

### Context Management Strategy

1. **Smart Chunking**: Automatically splits large contexts into manageable chunks
2. **Context Caching**: Caches processed contexts to avoid redundant API calls
3. **Progressive Loading**: Loads context progressively based on relevance
4. **Token Optimization**: Intelligently manages token usage across both models

## 📦 Installation

### Prerequisites

- Python 3.11+
- Claude Code with MCP support
- Google Cloud account with Gemini API access
- Google AI Python SDK (installed automatically with dependencies)

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/gemini-claude-code-mpc.git
   cd gemini-claude-code-mpc
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Configure API credentials**

   ```bash
   # Set up Gemini API key
   export GOOGLE_API_KEY="your-gemini-api-key"

   # Or use Google Cloud authentication
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/service-account.json"
   ```

4. **Configure Claude Code**
   Add to your Claude Code settings:
   ```json
   {
     "mcpServers": {
       "gemini-claude-code-mcp": {
         "command": "uvx",
         "args": ["gemini-claude-code-mcp"]
         "env": {
           "GOOGLE_API_KEY": "your-gemini-api-key",
       }
     }
   }
   ```

## 🚀 Usage Examples

### Example 1: Analyzing a Large Codebase

```markdown
Claude: "Use Gemini to analyze the entire React codebase and identify performance bottlenecks"

The MCP server will:

1. Gather all relevant files from the React codebase
2. Send them to Gemini for analysis
3. Return structured insights about performance issues
```

### Example 2: Cross-Repository Analysis

```markdown
Claude: "Compare the authentication implementations across our microservices"

The MCP server will:

1. Collect auth-related code from multiple repositories
2. Use Gemini to analyze patterns and differences
3. Provide comprehensive comparison results
```

### Example 3: Documentation Generation

```markdown
Claude: "Generate comprehensive API documentation for this entire project"

The MCP server will:

1. Scan all code files for API endpoints and interfaces
2. Use Gemini to understand the full context
3. Generate detailed, context-aware documentation
```

## 🔧 Configuration

### Environment Variables

- `GOOGLE_API_KEY`: Gemini API key
- `GEMINI_MODEL`: Model to use (default: gemini-1.5-pro-002)
- `MAX_CONTEXT_SIZE`: Maximum context size in tokens (default: 2000000)
- `CACHE_ENABLED`: Enable context caching (default: true)
- `CACHE_TTL`: Cache time-to-live in seconds (default: 3600)

### Advanced Configuration

Create a `config.yaml` file:

```yaml
gemini:
  model: gemini-1.5-pro-002
  max_tokens: 2000000
  temperature: 0.1

cache:
  enabled: true
  ttl: 3600
  max_size: 1GB

processing:
  chunk_size: 100000
  overlap: 1000
  parallel_chunks: 4
```

## 📚 SDK Documentation

This project uses the official Google AI Python SDK for Gemini. For detailed information about the SDK:

- [Google AI Python SDK Documentation](https://ai.google.dev/gemini-api/docs)
- [SDK GitHub Repository](https://github.com/google/generative-ai-python)
- [API Reference](https://ai.google.dev/api/python/google/generativeai)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup

```bash
# Install development dependencies
uv sync

# Run tests
pytest

# Run linting
ruff check .

# Format code
ruff check --fix .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built on [FastMCP](https://gofastmcp.com/)
- Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Designed for [Claude Code](https://claude.ai/code)
