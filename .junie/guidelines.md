# Python Development Guidelines

This document outlines the standard practices and guidelines for Python development in this project.

## Python Defaults

- Use Python 3.13+ for all development
- Follow PEP 8 style guidelines
- Use type hints whenever possible
- Limit line length to 88 characters (Black default)
- Use docstrings for all public modules, functions, classes, and methods
- Use f-strings for string formatting
- Use pathlib instead of os.path for file operations
- Prefer context managers (with statements) when dealing with resources
- Use virtual environments for development

## Development Process

- After every feature, create tests that test the feature
- If the tests do not succeed, fix them before moving onto another task
- Once the tests succeed, run Black on the changed files and then commit them to git before moving on to another task
- Write meaningful commit messages that describe the changes made
- Keep commits focused on a single logical change
- Run linters and type checkers before committing

## Granularity

- Break larger features down to smaller steps
- Implement, test, and commit them step by step
- Each step should be a complete, working unit
- Ensure each step has appropriate test coverage
- Keep pull requests small and focused

## Environment

- Use uv as package manager
- If a test fails, check that you are using the project's environment
- Install packages when necessary
- Keep dependencies up to date
- Document all dependencies in pyproject.toml
- Use consistent dependency versions across development environments
- Key dependencies include:
  - FastAPI for the API framework
  - Playwright for browser automation and XSS testing
  - pytest for testing
  - uvicorn for serving the API

## Code Quality

- Write self-documenting code with clear variable and function names
- Avoid complex nested structures
- Keep functions and methods small and focused
- Use appropriate design patterns
- Write unit tests for all functionality
- Aim for high test coverage
- Use assertions and proper error handling

## Project Structure

- Source code is organized in the `src/` directory under the `xss_validator` package
- Example scripts demonstrating usage are in the `examples/` directory
- Utility and performance testing scripts are in the `scripts/` directory
- Tests are located in the `tests/` directory
- Documentation is maintained in the `docs/` directory
