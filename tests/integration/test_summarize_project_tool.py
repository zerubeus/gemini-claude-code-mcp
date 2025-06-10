"""Integration test for summarize_project tool."""

import json
from pathlib import Path
from typing import Any

import pytest
from fastmcp import Client, FastMCP
from syrupy.assertion import SnapshotAssertion

from gemini_claude_code_mcp.tools.summarize_project_tool import register_summarize_project_tool


@pytest.fixture
def mcp_server() -> FastMCP[Any]:
    """Create MCP server with summarize_project tool registered."""
    server: FastMCP[Any] = FastMCP('TestServer')
    register_summarize_project_tool(server)
    return server


@pytest.fixture
def test_project_dir(tmp_path: Path) -> Path:
    """Create a minimal test project structure."""
    # Create project structure
    project_dir = tmp_path / 'test_project'
    project_dir.mkdir()

    # Create some Python files
    src_dir = project_dir / 'src'
    src_dir.mkdir()

    # Main module
    main_py_content = """\"\"\"Main module for test project.\"\"\"

    from typing import List


    class Calculator:
        \"\"\"Simple calculator class for testing.\"\"\"

        def add(self, a: int, b: int) -> int:
            \"\"\"Add two numbers.\"\"\"
            return a + b

        def multiply(self, a: int, b: int) -> int:
            \"\"\"Multiply two numbers.\"\"\"
            return a * b


    def process_items(items: List[str]) -> List[str]:
        \"\"\"Process a list of items.\"\"\"
        return [item.upper() for item in items]


    if __name__ == "__main__":
        calc = Calculator()
        print(calc.add(5, 3))
    """
    (src_dir / 'main.py').write_text(main_py_content)

    # Utils module
    utils_py_content = """\"\"\"Utility functions for the project.\"\"\"

    import json
    from pathlib import Path


    def load_config(config_path: str) -> dict:
        \"\"\"Load configuration from JSON file.\"\"\"
        with open(config_path, 'r') as f:
            return json.load(f)


    def save_data(data: dict, output_path: str) -> None:
        \"\"\"Save data to JSON file.\"\"\"
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)


    def format_path(path: str) -> Path:
        \"\"\"Convert string path to Path object.\"\"\"
        return Path(path).resolve()
    """
    (src_dir / 'utils.py').write_text(utils_py_content)

    # Create tests directory
    tests_dir = project_dir / 'tests'
    tests_dir.mkdir()

    test_main_content = """\"\"\"Tests for main module.\"\"\"

    from src.main import Calculator, process_items


    def test_calculator_add():
        calc = Calculator()
        assert calc.add(2, 3) == 5


    def test_process_items():
        items = ['hello', 'world']
        result = process_items(items)
        assert result == ['HELLO', 'WORLD']
    """
    (tests_dir / 'test_main.py').write_text(test_main_content)

    # Create configuration files
    pyproject_content = """[project]
    name = "test-project"
    version = "0.1.0"
    description = "A test project for integration testing"
    dependencies = [
        "pytest>=7.0.0",
    ]

    [build-system]
    requires = ["setuptools>=61.0"]
    build-backend = "setuptools.build_meta"
    """
    (project_dir / 'pyproject.toml').write_text(pyproject_content)

    readme_content = """# Test Project

    This is a minimal test project for integration testing the summarize_project tool.

    ## Features

    - Simple calculator implementation
    - Utility functions for file operations
    - Basic test suite

    ## Usage

    ```python
    from src.main import Calculator

    calc = Calculator()
    result = calc.add(10, 20)
    ```
    """
    (project_dir / 'README.md').write_text(readme_content)

    # Add .gitignore
    gitignore_content = """__pycache__/
    *.pyc
    .pytest_cache/
    """
    (project_dir / '.gitignore').write_text(gitignore_content)

    return project_dir


@pytest.mark.asyncio
async def test_summarize_project_basic(
    mcp_server: FastMCP[Any], test_project_dir: Path, snapshot: SnapshotAssertion
) -> None:
    """Test basic project summarization with real Gemini API."""
    async with Client(mcp_server) as client:
        result = await client.call_tool(
            'summarize_project',
            {
                'directory_path': str(test_project_dir),
            },
        )

        # Extract the response
        assert hasattr(result[0], 'text'), 'Result should have text attribute'
        assert hasattr(result[0], 'text'), 'Result should have text attribute'
        response = json.loads(result[0].text)  # type: ignore  # type: ignore

        # Verify structure
        assert response['status'] == 'success'
        assert response['project_path'] == str(test_project_dir)
        assert 'overview' in response
        assert 'structure' in response
        assert 'statistics' in response
        assert 'analysis_details' in response

        # Verify statistics are accurate
        stats = response['statistics']
        assert stats['total_files'] == 3  # main.py, utils.py, test_main.py (only .py files by default)
        assert stats['languages']['python'] == 3

        # Verify structure
        structure = response['structure']
        assert structure['name'] == 'test_project'
        assert 'src' in structure['children']
        assert 'main.py' in structure['children']['src']['children']
        assert 'utils.py' in structure['children']['src']['children']

        # Create a deterministic snapshot by removing variable data
        snapshot_data = {
            'status': response['status'],
            'structure': response['structure'],
            'statistics': response['statistics'],
            'has_overview': bool(response.get('overview')),
            'has_tech_stack': bool(response.get('tech_stack')),
            'has_architecture': bool(response.get('architecture')),
            'has_components': bool(response.get('components')),
            'analysis_details': {
                'files_analyzed': response['analysis_details']['files_analyzed'],
                'used_gemini': response['analysis_details']['used_gemini'],
            },
        }

        # Compare with snapshot
        assert snapshot_data == snapshot


@pytest.mark.asyncio
async def test_summarize_project_with_focus_areas(
    mcp_server: FastMCP[Any], test_project_dir: Path, snapshot: SnapshotAssertion
) -> None:
    """Test project summarization with focus areas."""
    async with Client(mcp_server) as client:
        result = await client.call_tool(
            'summarize_project',
            {
                'directory_path': str(test_project_dir),
                'focus_areas': ['testing', 'calculator'],
                'include_patterns': ['*.py'],
            },
        )

        assert hasattr(result[0], 'text'), 'Result should have text attribute'
        response = json.loads(result[0].text)  # type: ignore

        assert response['status'] == 'success'
        assert response['statistics']['total_files'] == 3  # Only Python files

        # Create snapshot data
        snapshot_data = {
            'status': response['status'],
            'files_analyzed': response['analysis_details']['files_analyzed'],
            'total_files': response['statistics']['total_files'],
            'languages': response['statistics']['languages'],
        }

        assert snapshot_data == snapshot


@pytest.mark.asyncio
async def test_summarize_project_invalid_directory(mcp_server: FastMCP[Any]) -> None:
    """Test error handling for invalid directory."""
    async with Client(mcp_server) as client:
        result = await client.call_tool(
            'summarize_project',
            {
                'directory_path': '/non/existent/directory',
            },
        )

        assert hasattr(result[0], 'text'), 'Result should have text attribute'
        response = json.loads(result[0].text)  # type: ignore

        assert response['status'] == 'failed'
        assert 'error' in response
        assert 'Directory not found' in response['error']


@pytest.mark.asyncio
async def test_summarize_project_empty_directory(mcp_server: FastMCP[Any], tmp_path: Path) -> None:
    """Test handling of empty directory."""
    empty_dir = tmp_path / 'empty_project'
    empty_dir.mkdir()

    async with Client(mcp_server) as client:
        result = await client.call_tool(
            'summarize_project',
            {
                'directory_path': str(empty_dir),
            },
        )

        assert hasattr(result[0], 'text'), 'Result should have text attribute'
        response = json.loads(result[0].text)  # type: ignore

        assert response['status'] == 'failed'
        assert 'No files found' in response['error']


@pytest.fixture
def large_test_project_dir(tmp_path: Path) -> Path:
    """Create a large test project that exceeds Claude's context limit."""
    project_dir = tmp_path / 'large_test_project'
    project_dir.mkdir()

    # Create many Python files with substantial content
    src_dir = project_dir / 'src'
    src_dir.mkdir()

    # Generate enough content to exceed 200k tokens but stay under 1M
    # Each file will have ~15000 tokens, so we need about 15 files to get ~225k tokens
    large_file_content = """
# This is a large file with substantial content to test Gemini integration
""" + '\n'.join(
        [
            f"""
class Component{i}:
    '''A complex component with many methods and substantial documentation.
    
    This component handles various operations including data processing,
    validation, transformation, and persistence. It implements multiple
    design patterns and integrates with various external services.
    '''
    
    def __init__(self, config: dict):
        '''Initialize the component with configuration.
        
        Args:
            config: Configuration dictionary containing all necessary parameters
                   for initializing this component including database connections,
                   API endpoints, timeout values, and feature flags.
        '''
        self.config = config
        self.data = []
        self.cache = {{}}
        self.connections = []
        self.validators = []
        self.transformers = []
        self.handlers = []
        self.middleware = []
        self.plugins = []
        self.listeners = []
        self.observers = []
    
    def process_data(self, input_data: list) -> list:
        '''Process input data through multiple transformation stages.
        
        This method implements a complex data processing pipeline that includes:
        - Data validation and sanitization
        - Type conversion and normalization
        - Business logic application
        - Error handling and recovery
        - Performance optimization
        - Caching and memoization
        - Logging and monitoring
        
        Args:
            input_data: Raw input data to be processed
            
        Returns:
            Processed data ready for consumption
        '''
        # Extensive processing logic here
        result = []
        for item in input_data:
            # Validate
            if not self._validate(item):
                continue
            
            # Transform
            transformed = self._transform(item)
            
            # Apply business logic
            processed = self._apply_business_logic(transformed)
            
            # Cache results
            self._cache_result(item, processed)
            
            result.append(processed)
        
        return result
    
    def _validate(self, item: Any) -> bool:
        '''Validate an item against all registered validators.'''
        for validator in self.validators:
            if not validator.validate(item):
                return False
        return True
    
    def _transform(self, item: Any) -> Any:
        '''Transform an item through all registered transformers.'''
        result = item
        for transformer in self.transformers:
            result = transformer.transform(result)
        return result
    
    def _apply_business_logic(self, item: Any) -> Any:
        '''Apply complex business logic to the item.'''
        # Simulate complex processing
        result = item
        for handler in self.handlers:
            result = handler.handle(result)
        return result
    
    def _cache_result(self, key: Any, value: Any) -> None:
        '''Cache the processing result for future use.'''
        self.cache[str(key)] = value
    
    # Add many more methods to increase token count...
    {
                ' '.join(
                    [
                        f'''
    def method_{j}(self, param{j}: Any) -> Any:
        """Another method with documentation to increase token count.
        
        This method performs operation {j} on the input parameter and returns
        the processed result after applying various transformations and validations.
        """
        return param{j}
    '''
                        for j in range(50)  # Increased methods per class
                    ]
                )
            }
"""
            for i in range(10)  # Generate more classes per file
        ]
    )

    # Create 15 files to exceed token limit but stay under Gemini's limit
    for i in range(15):
        file_path = src_dir / f'component_{i}.py'
        file_path.write_text(large_file_content)

    return project_dir


@pytest.mark.asyncio
async def test_summarize_large_project_uses_gemini(
    mcp_server: FastMCP[Any], large_test_project_dir: Path, snapshot: SnapshotAssertion
) -> None:
    """Test that large projects trigger Gemini usage."""
    async with Client(mcp_server) as client:
        result = await client.call_tool(
            'summarize_project',
            {
                'directory_path': str(large_test_project_dir),
            },
        )

        assert hasattr(result[0], 'text'), 'Result should have text attribute'
        response = json.loads(result[0].text)  # type: ignore

        assert response == snapshot

        # Verify the request succeeded
        assert response['status'] == 'success'

        # Most importantly: verify Gemini was actually used!
        assert response['analysis_details']['used_gemini'] is True
        assert response['analysis_details']['chunks_processed'] > 0

        # Verify we processed a large number of files
        assert response['statistics']['total_files'] == 15
        assert response['analysis_details']['total_tokens'] > 200000  # Exceeds Claude's limit
        assert response['analysis_details']['total_tokens'] < 1000000  # But stays under Gemini's limit
