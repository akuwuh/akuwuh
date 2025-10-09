# Git Ignore Configuration

## 📁 Files Created

Three `.gitignore` files have been strategically placed to ensure proper version control hygiene:

### 1. Project Root: `.gitignore`
**Location**: `/Users/cute/Documents/vsc/akuwuh/.gitignore`

**Purpose**: Main project-level gitignore for the entire repository

**Covers**:
- Python cache and bytecode files
- Virtual environments (venv, env, .venv)
- Distribution and packaging artifacts
- Testing artifacts (pytest, coverage)
- IDE configurations (VSCode, IntelliJ)
- OS-specific files (macOS .DS_Store, Windows Thumbs.db)
- Type checker caches (mypy, pytype, pyre)
- Node modules (if applicable)
- Environment variable files

### 2. Scripts Level: `.github/scripts/.gitignore`
**Location**: `/Users/cute/Documents/vsc/akuwuh/.github/scripts/.gitignore`

**Purpose**: Script-specific ignores for the scripts directory

**Covers**:
- Python-specific files
- Test output directory (`test_output/`)
- Build artifacts
- Temporary files
- Development logs

### 3. Package Level: `.github/scripts/lang_stats/.gitignore`
**Location**: `/Users/cute/Documents/vsc/akuwuh/.github/scripts/lang_stats/.gitignore`

**Purpose**: Package-specific ignores for the lang_stats module

**Covers**:
- Package cache files
- Testing artifacts
- Type checking cache
- Build files
- IDE configurations

## ✅ What's Ignored

### Python Files
```
__pycache__/              # Python cache directories
*.py[cod]                 # Compiled Python files (.pyc, .pyo, .pyd)
*$py.class                # Java-style class files
*.so                      # Shared object files
.Python                   # Python binary
```

### Virtual Environments
```
venv/                     # Standard venv
env/                      # Alternative env
.venv/                    # Hidden venv
ENV/                      # Capital ENV
*.bak/                    # Backup environments
```

### Distribution & Packaging
```
build/                    # Build output
dist/                     # Distribution files
*.egg-info/               # Egg metadata
*.egg                     # Egg files
wheels/                   # Wheel files
sdist/                    # Source distributions
```

### Testing
```
.pytest_cache/            # Pytest cache
.coverage                 # Coverage data
htmlcov/                  # Coverage HTML reports
.tox/                     # Tox environments
.hypothesis/              # Hypothesis testing
```

### Type Checking
```
.mypy_cache/              # Mypy cache
.pytype/                  # Pytype cache
.pyre/                    # Pyre cache
dmypy.json                # DMPy data
```

### IDEs & Editors
```
.vscode/                  # Visual Studio Code
.idea/                    # IntelliJ IDEA / PyCharm
*.swp                     # Vim swap files
*.swo                     # Vim swap files
*~                        # Backup files
.DS_Store                 # macOS finder info
```

### Environment & Secrets
```
.env                      # Environment variables
.env.local                # Local environment
.env.*.local              # Environment overrides
```

### Project-Specific
```
test_output/              # Test output files
*.log                     # Log files
*.tmp                     # Temporary files
temp/                     # Temp directory
```

## 🧹 Cleanup Performed

The following cleanup was automatically performed:

1. ✅ Removed all `__pycache__/` directories
2. ✅ Deleted all `*.pyc` files
3. ✅ Deleted all `*.pyo` files

## 🔍 Verification

To verify gitignore is working:

```bash
# Check if specific files are ignored
git check-ignore -v .github/scripts/test_output/sample_dark.svg
git check-ignore -v .github/scripts/lang_stats/__pycache__

# See what's being tracked
git status --short

# List all ignored files
git status --ignored
```

## 📋 Best Practices

### DO Commit
- ✅ Source code (`.py` files)
- ✅ Configuration templates (`.example` files)
- ✅ Documentation (`.md` files)
- ✅ Requirements files (`requirements.txt`)
- ✅ Setup files (`setup.py`, `pyproject.toml`)
- ✅ Test files (`test_*.py`)
- ✅ Gitignore files (`.gitignore`)

### DON'T Commit
- ❌ Cache files (`__pycache__/`, `*.pyc`)
- ❌ Virtual environments (`venv/`, `.venv/`)
- ❌ Build artifacts (`dist/`, `build/`)
- ❌ IDE configurations (`.vscode/`, `.idea/`)
- ❌ Environment files (`.env`)
- ❌ OS files (`.DS_Store`, `Thumbs.db`)
- ❌ Test outputs (`test_output/`)
- ❌ Logs (`*.log`)
- ❌ Personal credentials or tokens

## 🚀 Usage

### Adding to Git

The gitignore files themselves should be committed:

```bash
git add .gitignore
git add .github/scripts/.gitignore
git add .github/scripts/lang_stats/.gitignore
git commit -m "Add comprehensive .gitignore files for Python project"
```

### Creating Environment File

Create a template for environment variables:

```bash
# Create .env.example (this gets committed)
cat << EOF > .env.example
# GitHub API Token (get from https://github.com/settings/tokens)
GITHUB_TOKEN=your_token_here

# GitHub Username
GITHUB_USERNAME=yourusername
EOF

# Create your actual .env (this is ignored)
cp .env.example .env
# Edit .env with your real credentials
```

### Checking Ignored Files

```bash
# See all ignored files
git status --ignored --short

# Check if a specific file is ignored
git check-ignore -v path/to/file

# Show all .gitignore rules applying to a file
git check-ignore -v -n path/to/file
```

## 🔧 Customization

### Adding Custom Ignores

To add project-specific ignores, edit the appropriate `.gitignore`:

```bash
# For project-wide ignores
echo "my_custom_file.txt" >> .gitignore

# For scripts-specific ignores
echo "custom_script_output/" >> .github/scripts/.gitignore

# For package-specific ignores
echo "deprecated_modules/" >> .github/scripts/lang_stats/.gitignore
```

### Unignoring Files

To force-track an ignored file:

```bash
git add -f path/to/ignored/file
```

To create an exception in `.gitignore`:

```
# Ignore all .log files
*.log

# But track this specific one
!important.log
```

## 📦 Integration with Development Tools

### Pre-commit Hook (Optional)

Create `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Check for sensitive data
if git diff --cached --name-only | grep -q "\.env$"; then
    echo "ERROR: Attempting to commit .env file!"
    exit 1
fi

# Check for large files
find . -size +10M | grep -v ".git" | while read file; do
    if git diff --cached --name-only | grep -q "$file"; then
        echo "ERROR: Large file detected: $file"
        exit 1
    fi
done
```

### VSCode Settings

Add to `.vscode/settings.json` (optional):

```json
{
  "files.watcherExclude": {
    "**/__pycache__/**": true,
    "**/.pytest_cache/**": true,
    "**/.mypy_cache/**": true,
    "**/venv/**": true
  },
  "search.exclude": {
    "**/__pycache__": true,
    "**/.pytest_cache": true,
    "**/.mypy_cache": true,
    "**/venv": true
  }
}
```

## 🎯 Summary

✅ **Three-tier gitignore strategy** covering:
  - Project root (comprehensive)
  - Scripts directory (script-specific)
  - Package directory (package-specific)

✅ **Complete coverage** of:
  - Python artifacts
  - Development tools
  - Build outputs
  - Testing files
  - IDE configurations
  - OS-specific files

✅ **Clean repository** with:
  - No cache files
  - No build artifacts
  - No sensitive data
  - Professional structure

## 📚 Resources

- [GitHub's Python .gitignore template](https://github.com/github/gitignore/blob/main/Python.gitignore)
- [Git Documentation - gitignore](https://git-scm.com/docs/gitignore)
- [Python Packaging Guide](https://packaging.python.org/en/latest/)

---

**Status**: ✅ Complete  
**Last Updated**: October 2025  
**Coverage**: Comprehensive

