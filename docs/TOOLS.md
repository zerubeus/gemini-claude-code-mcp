# MCP Tools Documentation

## summarize_project

Generate a comprehensive summary of a project/codebase using Gemini's large context capabilities.

### Description

This tool analyzes an entire project directory and provides a multi-level summary including:

- Project structure and organization
- Technology stack and dependencies
- Main components and their purposes
- Architecture patterns and design decisions
- Key APIs and interfaces

When the codebase exceeds Claude's context limit, it automatically uses Google Gemini's 1M token context window for analysis.

### Parameters

| Parameter          | Type         | Required | Description                                                                               |
| ------------------ | ------------ | -------- | ----------------------------------------------------------------------------------------- |
| `directory_path`   | string       | Yes      | Absolute path to the project directory                                                    |
| `focus_areas`      | list[string] | No       | Optional list of specific areas to focus on (e.g., ["authentication", "api", "database"]) |
| `include_patterns` | list[string] | No       | Optional file patterns to include (e.g., ["*.py", "src/**/*.js"])                         |
| `exclude_patterns` | list[string] | No       | Optional file patterns to exclude beyond defaults                                         |

### Response Format

```json
{
  "status": "success",
  "project_path": "/path/to/project",
  "overview": "High-level project summary text",
  "structure": {
    "name": "project",
    "type": "directory",
    "children": {
      "src": {
        "type": "directory",
        "children": {
          "main.py": {
            "type": "file",
            "language": "python",
            "size": 1234,
            "tokens": 250
          }
        }
      }
    }
  },
  "tech_stack": {
    // Technology stack information
  },
  "architecture": {
    // Architecture patterns and decisions
  },
  "components": [
    // List of main components
  ],
  "key_features": [
    // List of key features
  ],
  "dependencies": [
    // External dependencies
  ],
  "code_quality": {
    // Code quality observations
  },
  "statistics": {
    "total_files": 42,
    "total_size_bytes": 123456,
    "total_size_mb": 0.12,
    "total_tokens": 5000,
    "languages": {
      "python": 30,
      "javascript": 10,
      "markdown": 2
    },
    "file_types": {
      ".py": 30,
      ".js": 10,
      ".md": 2
    }
  },
  "analysis_details": {
    "files_analyzed": 42,
    "total_tokens": 5000,
    "used_gemini": false,
    "chunks_processed": 0
  }
}
```

### Example Usage

```python
# Summarize a Python project
result = await summarize_project(
    directory_path="/Users/john/my-python-project",
    focus_areas=["database", "api"],
    include_patterns=["*.py", "*.md"],
    exclude_patterns=["tests/*", "docs/*"]
)

# Summarize a JavaScript project
result = await summarize_project(
    directory_path="/Users/jane/react-app",
    focus_areas=["components", "state management"],
    include_patterns=["src/**/*.js", "src/**/*.jsx"]
)
```

### Notes

- The tool automatically respects `.gitignore` files unless configured otherwise
- Files larger than 10MB are skipped to avoid memory issues
- When content exceeds Claude's context limit (~200k tokens), it automatically switches to Gemini
- The analysis uses code-aware chunking to maintain context boundaries
- Results are cached for 1 hour to improve performance on repeated queries

## generate_doc_for_specific_folder

_[Documentation pending implementation]_
