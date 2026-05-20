# Contributing to PromptFix

Welcome to PromptFix! We appreciate your interest in contributing to this project. This guide will help you get started.

## 🎯 How to Contribute

There are many ways to contribute to PromptFix:

### 1. Report Bugs
- Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.md)
- Include detailed steps to reproduce
- Provide error logs and environment information

### 2. Suggest Features
- Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.md)
- Explain the use case and expected behavior
- Consider alternatives and priority

### 3. Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Add tests if applicable
- Submit a Pull Request

### 4. Documentation
- Improve existing documentation
- Add usage examples
- Translate documentation to other languages

### 5. Community Support
- Answer questions in Discussions
- Help other users with issues
- Share your use cases

## 📋 Getting Started

### Prerequisites
- Python 3.8+
- Git
- DeepSeek API Key (for testing)

### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/jacksong-source/promptfix.git
cd promptfix

# Install dependencies
pip install -e .

# Install development dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/
```

## 🔧 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Add docstrings for public functions
- Keep code clean and readable

### Testing
- Add tests for new features
- Ensure existing tests pass
- Maintain test coverage above 80%

### Commit Messages
- Use descriptive commit messages
- Follow conventional commits format:
  - `feat: add new feature`
  - `fix: resolve bug`
  - `docs: update documentation`
  - `refactor: improve code structure`
  - `test: add test cases`

### Pull Request Process
1. Create a descriptive PR title
2. Explain the changes in the description
3. Link related issues
4. Ensure all tests pass
5. Request review from maintainers

## 📁 Project Structure

```
promptfix/
├── promptfix/           # Source code
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── config.py       # Configuration
│   ├── detector.py     # Detection logic
│   └── transformer.py  # Prompt transformation
├── tests/              # Test suite
│   └── test_promptfix.py
├── .github/            # GitHub configurations
│   └── ISSUE_TEMPLATE/
├── .env.example        # Environment variables template
├── pyproject.toml      # Package configuration
├── README.md           # Main documentation
├── README_CN.md        # Chinese documentation
└── CONTRIBUTING.md     # This file
```

## 🎨 Good First Issues

Looking for ways to get started? Check for issues labeled with:
- `good first issue` - Beginner-friendly tasks
- `help wanted` - Tasks that need community help

## 📝 License

By contributing to PromptFix, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## 🙋 Need Help?

If you have questions or need assistance:
- 📝 [Open an Issue](https://github.com/jacksong-source/promptfix/issues)
- 💬 [Start a Discussion](https://github.com/jacksong-source/promptfix/discussions)
- 📧 Email: 15011462616@163.com

Thank you for contributing to PromptFix! 🚀