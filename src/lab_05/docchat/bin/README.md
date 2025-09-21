# DocChat Development Scripts

This directory contains development scripts for the DocChat project.

## Scripts

### `./bin/lint`

A comprehensive linting and formatting script using Ruff.

#### Usage

```bash
# Basic linting
./bin/lint                      # Lint current directory
./bin/lint app.py config/      # Lint specific files/directories

# Auto-fix issues
./bin/lint --fix               # Lint and auto-fix issues
./bin/lint --fix app.py        # Fix specific file

# Code formatting
./bin/lint --format            # Format code only
./bin/lint --format config/    # Format specific directory

# Combined operations
./bin/lint --all               # Lint and format
./bin/lint --all --fix         # Lint with auto-fix and format

# CI/CD mode
./bin/lint --check             # Check only, exit with error if issues found
./bin/lint --check --verbose   # Verbose output for debugging
```

#### Options

- `-h, --help`: Show help message
- `-f, --fix`: Automatically fix issues where possible
- `-c, --check`: Check only, exit with error code if issues found
- `-v, --verbose`: Verbose output
- `--format`: Run ruff format (code formatting) only
- `--all`: Run all checks (lint + format)

#### Features

- 🔍 **Comprehensive linting** using Ruff
- 🔧 **Auto-fix** common issues with `--fix`
- 🎨 **Code formatting** with Ruff formatter
- 🚦 **CI/CD ready** with `--check` mode
- 🌈 **Colored output** for better readability
- 📊 **Summary reporting** of all operations
- ⚡ **Fast execution** using UV package manager

#### Examples

```bash
# Quick development cycle
./bin/lint --all --fix

# Before committing (CI check)
./bin/lint --check

# Fix specific file issues
./bin/lint --fix app.py

# Format entire codebase
./bin/lint --format .
```

#### Integration with IDE

You can integrate this script with your IDE or editor:

**VS Code**: Add to tasks.json
```json
{
    "label": "Lint with Ruff",
    "type": "shell",
    "command": "./bin/lint",
    "args": ["--all", "--fix"],
    "group": "build"
}
```

**Pre-commit hook**:
```bash
#!/bin/sh
./bin/lint --check
```

## Adding New Scripts

When adding new development scripts:

1. Make them executable: `chmod +x bin/script-name`
2. Add proper shebang: `#!/usr/bin/env bash`
3. Include help functionality with `-h/--help`
4. Use consistent error handling and colored output
5. Document in this README