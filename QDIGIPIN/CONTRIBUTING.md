# Contributing to Q-DIGIPIN India

Thank you for your interest in contributing to Q-DIGIPIN India! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. **Clear title** describing the bug
2. **Steps to reproduce** the issue
3. **Expected behavior** vs actual behavior
4. **QGIS version** and operating system
5. **Screenshots** if applicable
6. **Error messages** or logs

### Suggesting Features

Feature requests are welcome! Please create an issue with:

1. **Clear description** of the feature
2. **Use case** explaining why it's needed
3. **Proposed implementation** (if you have ideas)
4. **Examples** from other tools (if applicable)

### Pull Requests

1. **Fork** the repository
2. **Create a branch** for your feature (`git checkout -b feature/amazing-feature`)
3. **Make your changes** following our coding standards
4. **Write tests** for new functionality
5. **Update documentation** as needed
6. **Commit your changes** (`git commit -m 'Add amazing feature'`)
7. **Push to branch** (`git push origin feature/amazing-feature`)
8. **Open a Pull Request**

## Development Setup

### Prerequisites

- QGIS 3.0 or higher
- Python 3.6+
- Git

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/Sakyasingh1/Q-DIGIPIN-India.git
cd Q-DIGIPIN-India

# Create symbolic link to QGIS plugins directory (Linux/Mac)
ln -s $(pwd) ~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/QDIGIPIN

# Or copy to plugins directory (Windows)
# Copy to: C:\Users\<username>\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\
```

### Running Tests

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_encoding.py

# Run with coverage
python -m pytest --cov=core tests/
```

## Coding Standards

### Python Style

- Follow **PEP 8** style guide
- Use **4 spaces** for indentation
- Maximum line length: **100 characters**
- Use **docstrings** for all functions and classes

### Example

```python
def encode_coordinates(lat, lon, precision=10):
    """
    Encode coordinates to DIGIPIN code.
    
    Args:
        lat (float): Latitude in decimal degrees
        lon (float): Longitude in decimal degrees
        precision (int): Precision level (1-10)
        
    Returns:
        str: DIGIPIN code
        
    Raises:
        ValueError: If coordinates are out of range
    """
    # Implementation here
    pass
```

### Naming Conventions

- **Classes**: PascalCase (`DigipinEncoder`)
- **Functions**: snake_case (`encode_coordinates`)
- **Constants**: UPPER_CASE (`DEFAULT_PRECISION`)
- **Private methods**: _leading_underscore (`_validate_input`)

### Documentation

- Add docstrings to all public functions and classes
- Update README.md for new features
- Update user_guide.md for user-facing changes
- Add examples for complex features

### Commit Messages

Use clear, descriptive commit messages:

```
Add batch encoding feature

- Implement batch processing for multiple points
- Add progress bar for user feedback
- Include error handling for invalid coordinates
```

## Testing Guidelines

### Unit Tests

- Write tests for all new functions
- Test edge cases and error conditions
- Aim for >80% code coverage

### Integration Tests

- Test complete workflows
- Test with real QGIS layers
- Test processing algorithms

### Test Structure

```python
class TestFeatureName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass
    
    def test_normal_case(self):
        """Test normal operation"""
        pass
    
    def test_edge_case(self):
        """Test edge cases"""
        pass
    
    def test_error_handling(self):
        """Test error conditions"""
        pass
```

## Project Structure

```
QDIGIPIN/
├── core/              # Core functionality
├── gui/               # User interface
├── processing/        # Processing algorithms
├── resources/         # Icons and assets
├── tests/             # Test suite
└── docs/              # Documentation
```

## Release Process

1. Update version in `metadata.txt`
2. Update `CHANGELOG.md`
3. Run full test suite
4. Create git tag (`v1.0.0`)
5. Build plugin package
6. Submit to QGIS plugin repository

## Questions?

If you have questions about contributing:

- Open an issue on GitHub
- Email: sakyasingh@example.com
- Check existing issues and pull requests

## License

By contributing, you agree that your contributions will be licensed under the GPL v3 License.

---

Thank you for contributing to Q-DIGIPIN India! 🎉
