# 📦 Scripts Moved to Re-Po

This directory previously contained the `lang-stats` package. 

## 🚚 New Location

All code has been migrated to: **[akuwuh/re-po](https://github.com/akuwuh/re-po)**

```
akuwuh/re-po/packages/py-core/
├── lang_stats/          # Main package (DDD architecture)
├── docs/                # All documentation
├── generate_langs.py    # Main script
├── requirements.txt
├── setup.py
└── pyproject.toml
```

## 🔄 Migration Details

The migration preserved full git history using `git-filter-repo`. The code now lives in a dedicated repository for better organization and reusability.

## 📖 Documentation

- **Package Documentation**: [re-po/packages/py-core/docs/](https://github.com/akuwuh/re-po/tree/main/packages/py-core/docs)
- **DDD Guide**: [DDD_RESPONSIBILITIES.md](https://github.com/akuwuh/re-po/blob/main/packages/py-core/lang_stats/docs/DDD_RESPONSIBILITIES.md)
- **Quick Start**: [README_NEW_ARCHITECTURE.md](https://github.com/akuwuh/re-po/blob/main/packages/py-core/lang_stats/docs/README_NEW_ARCHITECTURE.md)

## 🚀 Usage in Workflows

The workflow now pulls from the re-po repository:

```yaml
- name: Checkout re-po (lang-stats package)
  uses: actions/checkout@v3
  with:
    repository: akuwuh/re-po
    path: re-po

- name: Install lang-stats package
  run: |
    cd re-po/packages/py-core
    pip install -r requirements.txt
    pip install -e .
```

See `.github/workflows/langs-mono.yml` for the full workflow.

## 📦 Installing the Package

### From GitHub
```bash
pip install git+https://github.com/akuwuh/re-po.git#subdirectory=packages/py-core
```

### For Development
```bash
git clone https://github.com/akuwuh/re-po.git
cd re-po/packages/py-core
pip install -e ".[dev]"
```

## 💻 Using the Package

```python
from lang_stats import LanguageStatsService, RenderConfig

service = LanguageStatsService(username="yourusername")
config = RenderConfig.default_light()
svg = service.generate_svg(config=config)
```

---

**Migrated**: October 2025  
**New Repo**: [akuwuh/re-po](https://github.com/akuwuh/re-po)  
**Package Path**: `packages/py-core/`

