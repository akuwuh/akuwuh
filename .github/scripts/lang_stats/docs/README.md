# Language Stats Generator

A flexible language statistics generator that supports both text-based and vector (SVG) output modes with 3D box effects.

## Features

- **Dual Output Modes**: Choose between text-based HTML or vector SVG output
- **3D Extrusion Effect**: Visual depth with border extrusion
- **Progress Bars**: Language usage visualization with customizable styles
- **Theme Support**: Light and dark themes for SVG mode
- **Configurable**: Easily customize via config or environment variables

## Output Modes

### Text Mode (Default)
Generates HTML with Unicode box-drawing characters and text-based progress bars.

**Advantages:**
- Lightweight
- Works everywhere
- No external dependencies
- Classic terminal aesthetic

**Example:**
```
┌──────────────────────────────────────────────────────┐
  │  TypeScript     █████████░░░░░░░░░░░░░░░░   34.3 %   ├─┐
  │  Python         ████████░░░░░░░░░░░░░░░░░   33.6 %   │ │
  └┬─────────────────────────────────────────────────────┘ │
   └───────────────────────────────────────────────────────┘
```

### Vector Mode (SVG)
Generates scalable vector graphics with graphical progress bars.

**Advantages:**
- Crisp rendering at any size
- Graphical progress bars (rectangles)
- Better accessibility
- Modern appearance
- Theme-aware (light/dark)

**Example:**
Same visual appearance but rendered as true vector graphics with smooth, scalable bars.

## Configuration

### Method 1: Config File
Edit `.github/scripts/lang_stats/config.py`:

```python
OUTPUT_MODE = 'vector'  # Options: 'text', 'vector'
USE_GRAPHICAL_BARS = True  # For vector mode: use rectangles vs text chars
SVG_THEME = 'light'  # Options: 'light', 'dark'
```

### Method 2: Environment Variables
Set environment variables (takes precedence over config):

```bash
export OUTPUT_MODE=vector
export USE_GRAPHICAL_BARS=true
export SVG_THEME=light
```

### Method 3: GitHub Actions Variables
Configure in GitHub repository settings → Settings → Secrets and variables → Actions → Variables:

- `OUTPUT_MODE`: `text` or `vector`
- `USE_GRAPHICAL_BARS`: `true` or `false`
- `SVG_THEME`: `light` or `dark`

## Usage

### In GitHub Actions
The workflow automatically reads from GitHub Actions variables or uses defaults:

```yaml
- name: Generate language stats
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    OUTPUT_MODE: ${{ vars.OUTPUT_MODE || 'text' }}
    USE_GRAPHICAL_BARS: ${{ vars.USE_GRAPHICAL_BARS || 'true' }}
    SVG_THEME: ${{ vars.SVG_THEME || 'light' }}
  run: python .github/scripts/generate_langs.py
```

### Manual Usage
```bash
# Using text mode (default)
python .github/scripts/generate_langs.py

# Using vector mode
OUTPUT_MODE=vector python .github/scripts/generate_langs.py

# Using vector mode with dark theme
OUTPUT_MODE=vector SVG_THEME=dark python .github/scripts/generate_langs.py

# Using vector mode with text-based bars
OUTPUT_MODE=vector USE_GRAPHICAL_BARS=false python .github/scripts/generate_langs.py
```

### Programmatic Usage
```python
from lang_stats.generator import generate_language_stats

lang_stats = [
    ('TypeScript', 34.3),
    ('Python', 33.6),
    ('C', 21.4)
]

# Text mode
html_output = generate_language_stats(lang_stats, use_3d=True, output_mode='text')

# Vector mode (light theme)
svg_output = generate_language_stats(
    lang_stats, 
    use_3d=True, 
    output_mode='vector',
    use_graphical_bars=True,
    svg_theme='light'
)

# Vector mode (dark theme)
svg_dark = generate_language_stats(
    lang_stats,
    use_3d=True,
    output_mode='vector', 
    use_graphical_bars=True,
    svg_theme='dark'
)
```

## Module Structure

```
lang_stats/
├── __init__.py           # Package initialization
├── config.py             # Configuration constants
├── fetcher.py            # GitHub API data fetching
├── formatter.py          # Content formatting
├── box_drawer.py         # Text-based box drawing
├── html_converter.py     # HTML conversion utilities
├── svg_generator.py      # SVG generation (NEW!)
├── generator.py          # Main orchestration
└── readme_updater.py     # README.md updater
```

## Configuration Options

### General
- `MAX_LANGUAGES`: Maximum number of languages to display (default: 5)
- `LANG_NAME_WIDTH`: Fixed width for language names (default: 14)
- `PROGRESS_BAR_BLOCKS`: Total blocks in progress bar (default: 25)

### Box Drawing
- `LEFT_PADDING`: Spaces to left of content (default: 2)
- `RIGHT_PADDING`: Spaces to right of content (default: 3)
- `EXTRUSION_INDENT_LEVEL_1`: First extrusion indent (default: 2)
- `EXTRUSION_INDENT_LEVEL_2`: Second extrusion indent (default: 3)

### Output
- `OUTPUT_MODE`: `'text'` or `'vector'` (default: `'text'`)
- `USE_GRAPHICAL_BARS`: `True` or `False` (default: `True`)
- `SVG_THEME`: `'light'` or `'dark'` (default: `'light'`)

### Language Filtering
- `EXCLUDED_LANGUAGES`: List of languages to exclude (e.g., `['JavaScript', 'HTML', 'CSS']`)

## Customization Examples

### Change to Vector Mode Globally
```python
# config.py
OUTPUT_MODE = 'vector'
USE_GRAPHICAL_BARS = True
SVG_THEME = 'light'
```

### Use Dark Theme in Vector Mode
```python
# config.py
OUTPUT_MODE = 'vector'
SVG_THEME = 'dark'
```

### Keep Text-Based Bars in Vector Mode
```python
# config.py
OUTPUT_MODE = 'vector'
USE_GRAPHICAL_BARS = False  # Use text characters instead of rectangles
```

### Show More Languages
```python
# config.py
MAX_LANGUAGES = 10  # Show top 10 languages
```

## Tips

1. **Vector mode** is recommended for:
   - Better rendering on high-DPI displays
   - Clean scaling across different screen sizes
   - Modern, polished appearance

2. **Text mode** is recommended for:
   - Classic terminal aesthetic
   - Minimal file size
   - Maximum compatibility

3. **Use environment variables** for:
   - Testing different modes without changing code
   - Per-environment configuration
   - CI/CD flexibility

4. **GitHub Actions Variables** are ideal for:
   - Easy switching between modes via GitHub UI
   - No code changes required
   - Per-repository configuration

## Troubleshooting

### Vector output looks misaligned
- Adjust `CHAR_WIDTH` in `svg_generator.py` (default: 9.6)
- Ensure monospace font is used

### Bars don't match percentages
- Check `PROGRESS_BAR_BLOCKS` calculation in `formatter.py`
- Verify rounding logic in `generate_progress_bar()`

### Colors not showing correctly
- Verify theme setting (`'light'` or `'dark'`)
- Check color definitions in `svg_generator.py`

### Mode not changing
- Environment variables take precedence over config
- Check variable spelling and case sensitivity
- Verify GitHub Actions variables are set correctly

## Contributing

When adding new features:
1. Maintain consistency between text and vector modes
2. Update both `box_drawer.py` and `svg_generator.py`
3. Add configuration options to `config.py`
4. Update this README
5. Test both output modes

## License

Part of the akuwuh profile repository.

