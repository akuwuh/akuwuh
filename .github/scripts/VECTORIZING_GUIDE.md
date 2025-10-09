# Vectorizing Module - Quick Start Guide

## 🎨 Overview

The language stats generator now supports **two output modes**:

1. **Text Mode** (default): HTML with Unicode box-drawing characters
2. **Vector Mode** (new): SVG with scalable vector graphics

Both modes produce identical visual appearance with 3D extrusion effects and progress bars.

## 🚀 Quick Setup

### Switch to Vector Mode

**Option 1: Config File** (Permanent)
```python
# Edit .github/scripts/lang_stats/config.py
OUTPUT_MODE = 'vector'  # Change from 'text' to 'vector'
```

**Option 2: Environment Variable** (Temporary/Testing)
```bash
OUTPUT_MODE=vector python .github/scripts/generate_langs.py
```

**Option 3: GitHub Actions** (Recommended for Production)
1. Go to your repository → Settings → Secrets and variables → Actions → Variables
2. Click "New repository variable"
3. Add: `OUTPUT_MODE` = `vector`

## ⚙️ Configuration Options

### Available Settings

| Variable | Options | Default | Description |
|----------|---------|---------|-------------|
| `OUTPUT_MODE` | `text`, `vector` | `text` | Output format type |
| `USE_GRAPHICAL_BARS` | `true`, `false` | `true` | Use rectangles vs text chars in vector mode |
| `SVG_THEME` | `light`, `dark` | `light` | Color scheme for vector mode |

### Examples

**Vector mode with dark theme:**
```bash
OUTPUT_MODE=vector SVG_THEME=dark python .github/scripts/generate_langs.py
```

**Vector mode with text-based bars:**
```bash
OUTPUT_MODE=vector USE_GRAPHICAL_BARS=false python .github/scripts/generate_langs.py
```

## 📊 Output Comparison

### Text Mode Output
```
┌──────────────────────────────────────────────────────┐
  │  TypeScript     █████████░░░░░░░░░░░░░░░░   34.3 %   ├─┐
  │  Python         ████████░░░░░░░░░░░░░░░░░   33.6 %   │ │
  └┬─────────────────────────────────────────────────────┘ │
   └───────────────────────────────────────────────────────┘
```
- Uses Unicode characters
- Lightweight (~1KB)
- Classic terminal look

### Vector Mode Output
```svg
<svg width="596" height="212">
  <!-- Scalable vector graphics with graphical bars -->
</svg>
```
- True vector graphics
- Crisp at any size (~2KB)
- Modern appearance
- Graphical progress bars

## 🧪 Testing

Run the test script to verify both modes:
```bash
python .github/scripts/test_output_modes.py
```

This will:
- ✅ Test all output modes
- ✅ Generate sample files
- ✅ Verify functionality
- ✅ Show preview of each mode

## 🔧 Troubleshooting

### Vector output not showing in README?
- Make sure you've committed and pushed the changes
- GitHub Actions must run to update the README
- Check workflow logs for errors

### Bars look misaligned?
- Adjust `CHAR_WIDTH` in `svg_generator.py` (default: 9.6)
- Try values between 9.0 and 10.5

### Want to switch back to text mode?
```bash
# Just change the config or env var back
OUTPUT_MODE=text python .github/scripts/generate_langs.py
```

## 🎯 Recommended Usage

**Use Vector Mode when:**
- You want crisp rendering on all displays
- Modern, polished appearance is important
- You have many languages to display
- You want graphical progress bars

**Use Text Mode when:**
- You prefer classic terminal aesthetic
- Minimal file size is important
- Maximum compatibility is needed

## 📝 GitHub Actions Setup

Update your workflow to use vector mode:

```yaml
- name: Generate language stats
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    OUTPUT_MODE: 'vector'  # ← Add this
    SVG_THEME: 'light'     # ← Optional
  run: python .github/scripts/generate_langs.py
```

Or use repository variables for easier switching:

```yaml
- name: Generate language stats
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    OUTPUT_MODE: ${{ vars.OUTPUT_MODE || 'text' }}
    USE_GRAPHICAL_BARS: ${{ vars.USE_GRAPHICAL_BARS || 'true' }}
    SVG_THEME: ${{ vars.SVG_THEME || 'light' }}
  run: python .github/scripts/generate_langs.py
```

## 📚 API Usage

### Python API

```python
from lang_stats.generator import generate_language_stats

stats = [
    ('TypeScript', 34.3),
    ('Python', 33.6),
    ('C', 21.4)
]

# Text mode
text_output = generate_language_stats(stats, output_mode='text')

# Vector mode (light)
svg_light = generate_language_stats(
    stats, 
    output_mode='vector',
    use_graphical_bars=True,
    svg_theme='light'
)

# Vector mode (dark)
svg_dark = generate_language_stats(
    stats,
    output_mode='vector',
    svg_theme='dark'
)
```

## 🎨 Customization

### Colors (Vector Mode)

Edit `svg_generator.py`:

```python
COLORS_LIGHT = {
    'text': '#24292f',      # Main text color
    'border': '#24292f',    # Border color
    'filled_bar': '#24292f', # Filled bar color
    'empty_bar': '#d0d7de'  # Empty bar color
}

COLORS_DARK = {
    'text': '#c9d1d9',
    'border': '#c9d1d9',
    'filled_bar': '#c9d1d9',
    'empty_bar': '#30363d'
}
```

### Dimensions

```python
CHAR_WIDTH = 9.6   # Adjust for font width
CHAR_HEIGHT = 20   # Line height
FONT_SIZE = 16     # Font size in pixels
```

## 🔥 Features

- ✨ **Identical Visual Output**: Both modes look the same
- 🎨 **3D Extrusion**: Visual depth effect maintained
- 📊 **Progress Bars**: Graphical (vector) or text-based
- 🌓 **Light/Dark Themes**: For vector mode
- 🔧 **Flexible Configuration**: Config file, env vars, or GitHub Actions
- 🧪 **Fully Tested**: Comprehensive test suite included
- 📝 **Well Documented**: Complete API documentation

## 💡 Tips

1. **Start with text mode** to ensure everything works, then switch to vector
2. **Use repository variables** in GitHub Actions for easy switching
3. **Test locally first** before deploying to production
4. **Check sample outputs** in the test_output folder
5. **Both modes** preserve the same 3D effect and bar functionality

## 📦 What's New

### v2.0.0 - Vectorizing Module
- ➕ Added SVG vector output mode
- ➕ Graphical progress bars with rectangles
- ➕ Light and dark theme support
- ➕ Flexible configuration system
- ➕ Complete test suite
- 📝 Comprehensive documentation

## 🔗 Files Modified

- ✅ `svg_generator.py` - New SVG generation module
- ✅ `generator.py` - Updated to support both modes
- ✅ `config.py` - Added output mode configuration
- ✅ `generate_langs.py` - Added environment variable support
- ✅ `langs-mono.yml` - Updated workflow with mode selection
- ✅ `__init__.py` - Updated package exports

## 🤝 Contributing

When adding features:
1. Maintain consistency between text and vector modes
2. Update both rendering engines
3. Add tests for new functionality
4. Update documentation

---

**Ready to use!** Switch to vector mode and enjoy crisp, scalable language statistics! 🚀

