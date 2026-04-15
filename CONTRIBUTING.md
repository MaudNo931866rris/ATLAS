# Contributing to ATLAS

Thank you for your interest in contributing to ATLAS! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

Before opening an issue:

1. Search existing issues to avoid duplicates
2. Check the [troubleshooting guide](docs/TROUBLESHOOTING.md)
3. Gather relevant information:
   - ATLAS version/commit hash
   - Operating system and version
   - GPU model and driver version
   - Output of `kubectl get pods`
   - Relevant logs

When opening an issue:

1. Use a clear, descriptive title
2. Describe the expected vs actual behavior
3. Provide steps to reproduce
4. Include logs and configuration (remove secrets!)

### Suggesting Features

Feature requests are welcome! Please:

1. Describe the use case and problem you're solving
2. Explain how your feature would work
3. Consider implementation complexity and trade-offs

### Pull Requests

#### Before You Start

1. Check existing issues/PRs for similar changes
2. For major changes, open an issue first to discuss
3. Fork the repository and create a feature branch

#### Development Setup

```bash
# Clone your fork
git clone https://github.com/<your-username>/atlas.git
cd atlas

# Create feature branch
git checkout -b feature/your-feature-name

# Copy configuration
cp .env.example .env
# Edit .env if you need to change model path or ports

# Run tests before making changes
python tests/validate_tests.py
```

#### Making Changes

1. Follow existing code style and patterns
2. Write tests for new functionality
3. Update documentation as needed
4. Keep commits focused and atomic
5. Write clear commit messages

#### Commit Message Format

```
component: short description (50 chars max)

Longer description if needed. Explain what and why,
not how (the code shows how).

Fixes #123
```

Examples:
- `geometric-lens: add project caching for faster queries`
- `sandbox: increase default timeout to 90s`
- `docs: add GPU troubleshooting section`

#### Submitting

1. Ensure all tests pass: `python tests/validate_tests.py`
2. Update CHANGELOG.md if applicable
3. Push to your fork
4. Open a pull request with:
   - Clear title and description
   - Link to related issues
   - Test results

#### Code Review

- Address review feedback promptly
- Explain your decisions when disagreeing
- Request re-review after making changes

## Code Style

### Python

- Follow PEP 8
- Use type hints for function signatures
- Document public functions with docstrings
- Maximum line length: 100 characters

```python
def process_chunk(
    content: str,
    file_path: str,
    start_line: int,
) -> dict[str, Any]:
    """
    Process a code chunk for vector storage.

    Args:
        content: The chunk text content
        file_path: Source file path
        start_line: Starting line number

    Returns:
        Dictionary with chunk metadata and embedding
    """
    ...
```

### Bash

- Use shellcheck for linting
- Quote variables: `"$var"` not `$var`
- Use `[[` for conditionals instead of `[`
- Always set `set -euo pipefail` at the top of scripts
