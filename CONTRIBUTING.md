# Contributing to Python ExamDiff Pro

Thank you for your interest in contributing to Python ExamDiff Pro! This document provides guidelines and instructions for contributing.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/python-examdiff.git
   cd python-examdiff
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements.txt[dev]  # Development dependencies
   ```

3. **Run tests** to ensure everything works:
   ```bash
   pytest tests/ -v
   ```

## Coding Standards

### Python Style

- Follow **PEP 8** style guidelines
- Use **type hints** for all function parameters and return values
- Write **docstrings** for all classes and functions (Google style)
- Maximum line length: **120 characters**

### Code Quality

- Write **clean, readable code**
- Add **comments** for complex logic
- Use **meaningful variable names**
- Keep functions **focused and small** (ideally < 50 lines)

### Example

```python
def compare_files(
    file1_path: str,
    file2_path: str,
    options: Optional[Dict[str, Any]] = None
) -> ComparisonResult:
    """
    Compare two files and return the differences.
    
    Args:
        file1_path: Path to the first file
        file2_path: Path to the second file
        options: Optional comparison options
        
    Returns:
        ComparisonResult object containing the differences
        
    Raises:
        FileNotFoundError: If either file doesn't exist
        IOError: If there's an error reading the files
    """
    # Implementation here
    pass
```

## Testing

- Write **tests** for all new features
- Ensure all **existing tests pass**
- Aim for **>80% code coverage**
- Use **pytest** for testing

### Running Tests

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test file
pytest tests/test_myers.py -v
```

## Commit Messages

Use clear, descriptive commit messages:

- **Format**: `type: brief description`
- **Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
- **Example**: `feat: add three-way merge support`

## Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** (if applicable)
5. **Create a pull request** with a clear description

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests pass
```

## Areas for Contribution

- **Bug fixes**: Check open issues
- **New features**: Discuss in issues first
- **Documentation**: Improve README, add examples
- **Tests**: Increase test coverage
- **Plugins**: Create useful plugins
- **Performance**: Optimize slow operations

## Questions?

- Open an **issue** for questions
- Check existing **issues** and **discussions**
- Review the **codebase** for examples

Thank you for contributing! 🎉
