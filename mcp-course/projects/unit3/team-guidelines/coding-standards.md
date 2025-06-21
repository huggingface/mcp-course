# Coding Standards

## Python
- Use type hints for all function arguments and return values
- Follow PEP 8 style guide
- Maximum line length: 100 characters
- Use descriptive variable names
- Prefer f-strings over .format() or % formatting

## Git Commits
- Use conventional commit format: type(scope): description
- Types: feat, fix, docs, style, refactor, test, chore
- Keep commit messages under 72 characters
- Reference issue numbers when applicable (e.g., "Fixes #123")

## Code Organization
- One class per file for major components
- Group related functionality into modules
- Use __init__.py to control public API
- Keep functions under 50 lines when possible

## Testing
- All new features must include tests
- Maintain >80% test coverage
- Use pytest for Python tests
- Test edge cases and error conditions
- Mock external dependencies

## Documentation
- All public functions need docstrings
- Use Google-style docstrings
- Include usage examples for complex functions
- Keep README files up to date