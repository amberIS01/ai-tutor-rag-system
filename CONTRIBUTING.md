# Contributing Guide

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 14+
- Docker & Docker Compose (optional)

### Local Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-tutor-rag-system
```

2. **Setup backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements_dev.txt
```

3. **Setup frontend**
```bash
cd frontend
# Frontend doesn't require installation, just needs a web server
```

## Development Workflow

### Running Tests
```bash
cd backend
pytest tests/ -v
```

### Code Formatting
```bash
cd backend
black .
isort .
```

### Linting
```bash
cd backend
flake8 . --max-line-length=100
mypy . --ignore-missing-imports
```

### Running the Application
```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend (in another terminal)
cd frontend
python -m http.server 5500
```

## Making Changes

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
- Write clean, well-documented code
- Add tests for new functionality
- Update documentation as needed

3. **Run tests and linting**
```bash
make test
make lint
```

4. **Commit your changes**
```bash
git add .
git commit -m "feat: your feature description"
```

## Commit Message Convention

We follow Conventional Commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `test:` for tests
- `refactor:` for code refactoring
- `perf:` for performance improvements
- `ci:` for CI/CD changes
- `config:` for configuration changes

## Pull Request Process

1. Push your branch to the repository
2. Create a Pull Request with a descriptive title
3. Include a description of your changes
4. Ensure all tests pass
5. Request review from maintainers

## Code Style

- Use type hints in Python
- Follow PEP 8 style guide
- Keep functions small and focused
- Write descriptive variable names
- Add docstrings to functions and classes

## Testing Guidelines

- Write unit tests for all new features
- Aim for >80% code coverage
- Use pytest for Python testing
- Mock external dependencies
- Test both success and error cases

## Reporting Issues

When reporting bugs, please include:
- Description of the issue
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, etc.)

## Questions?

Feel free to open an issue or contact the maintainers.
