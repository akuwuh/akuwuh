`
# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.
``

## Overview
- This repo is a profile README with lightweight automation.
- Executable code in-repo: `assets/convert.py` (standalone Python script to convert Unicode braille art into a tightly-cropped SVG).
- CI uses GitHub Actions to fetch and run the external `lang-stats` package from `akuwuh/re-po` to generate `langs-mono-*.svg` and keep `README.md` in sync.

## Commands

### Braille → SVG generator (local)
- Edit defaults in `assets/convert.py` if needed:
  - `SRC_PATH` (input text file with braille), `OUT_PATH` (output SVG), sizing and style constants.
  - Note: paths are currently absolute to this machine; switch to relative paths if running elsewhere.
- Run:

```bash
python3 assets/convert.py
```

### Generate language stats locally (mirrors CI workflow)
Option A: Clone the external repo into `./re-po` (matches CI layout) and install the package:

```bash
# from repo root
git clone https://github.com/akuwuh/re-po.git re-po
cd re-po/packages/py-core
pip install -r requirements.txt
pip install -e .
```

Then run the generator from the repo root (set env vars as desired):

```bash
# from repo root
GITHUB_TOKEN={{GITHUB_TOKEN}} \
OUTPUT_MODE=vector \
USE_GRAPHICAL_BARS=true \
SVG_THEME=light \
python3 re-po/packages/py-core/generate_langs.py
```

Option B: Install the package directly from GitHub (no local clone):

```bash
pip install "git+https://github.com/akuwuh/re-po.git#subdirectory=packages/py-core"
```

Programmatic usage example (from the external package docs):

```python
from lang_stats import LanguageStatsService, RenderConfig

service = LanguageStatsService(username="yourusername")
config = RenderConfig.default_light()
svg = service.generate_svg(config=config)
```

Notes:
- `GITHUB_TOKEN` is required for API access (in CI it uses `secrets.METRICS_TOKEN` or falls back to `secrets.GITHUB_TOKEN`).
- Outputs are `langs-mono-*.svg` in repo root; `README.md` references these files for light/dark themes.

## CI and automation
- Workflow: `.github/workflows/langs-mono.yml`
  - Triggers: scheduled (`0 6 * * *`), manual dispatch, and `push` to `main` (ignores changes to `langs-mono-*.svg` and `README.md`).
  - Steps:
    1) Checkout this repo.
    2) Setup Python 3.x.
    3) Checkout `akuwuh/re-po` into `./re-po`.
    4) Install `lang-stats` from `re-po/packages/py-core` (requirements + editable install).
    5) Run `python re-po/packages/py-core/generate_langs.py` with env:
       - `GITHUB_TOKEN` (secret), `GITHUB_ACTOR` (owner), `OUTPUT_MODE` (`text` or `vector`), `USE_GRAPHICAL_BARS` (for vector), `SVG_THEME` (`light` or `dark`).
    6) Commit and push changes to `README.md` and `langs-mono-*.svg` if modified.

## Structure at a glance (high level)
- `README.md`: Presentation; embeds generated `langs-mono-*.svg` and `assets/braille-*.svg` via light/dark `<picture>` sources.
- `.github/workflows/langs-mono.yml`: Orchestrates generation of language stat SVGs via the external `re-po` package and commits results.
- `assets/convert.py`: Pure-stdlib utility to convert braille blocks into uniformly spaced SVG (adjust constants at top for size/theme/paths).

## Notes for agents
- There is no project-level build, lint, or test tooling configured in this repo.
- When updating `assets/convert.py`, prefer relative paths under `assets/` to avoid machine-specific absolute paths.
- If language stat assets or README sections drift, re-run the local generation commands above or trigger the CI workflow.
