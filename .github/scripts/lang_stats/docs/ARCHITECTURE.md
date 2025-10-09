# Lang Stats Architecture

This document describes the architecture of the language statistics generator following Domain-Driven Design principles.

## Overview

The system generates language statistics visualizations with configurable 3D box effects. The architecture is modular, extensible, and follows SOLID principles.

## Project Structure

```
lang_stats/
├── __init__.py                    # Package entry point
├── config.py                      # Configuration constants
├── fetcher.py                     # GitHub API data fetching
├── formatter.py                   # Text formatting utilities
├── generator.py                   # Main orchestration logic
├── svg_generator.py               # SVG rendering orchestrator
├── html_converter.py              # HTML conversion utilities
├── box_drawer.py                  # Text-based box drawing
├── readme_updater.py              # README file updating
└── extrusion_styles/              # 3D extrusion rendering (new)
    ├── __init__.py                # Style exports
    ├── base.py                    # Abstract base class
    ├── style1_back_box.py         # Style 1 implementation
    ├── style2_connected.py        # Style 2 implementation
    ├── factory.py                 # Factory pattern
    └── README.md                  # Style documentation
```

## Domain Model

### Bounded Contexts

1. **Data Fetching Context** (`fetcher.py`)
   - Responsibility: Fetch language statistics from GitHub API
   - Domain entities: Language stats, repository data
   - External dependency: GitHub API

2. **Formatting Context** (`formatter.py`, `html_converter.py`)
   - Responsibility: Format data for display
   - Domain entities: Progress bars, percentages, text layout

3. **Rendering Context** (`svg_generator.py`, `extrusion_styles/`)
   - Responsibility: Generate visual representations
   - Domain entities: SVG elements, 3D boxes, extrusion styles
   - **Key abstraction**: `ExtrusionStyle` strategy pattern

4. **Generation Context** (`generator.py`)
   - Responsibility: Orchestrate the entire workflow
   - Coordinates between contexts

## Key Design Patterns

### 1. Strategy Pattern (Extrusion Styles)

Different extrusion rendering strategies are encapsulated as separate classes implementing a common interface:

```python
ExtrusionStyle (ABC)
    ├── BackBoxExtrusion (Style 1)
    └── ConnectedExtrusion (Style 2)
```

**Benefits:**
- Easy to add new styles without modifying existing code
- Each style is independently testable
- Runtime style selection

### 2. Factory Pattern

The `ExtrusionStyleFactory` creates style instances based on configuration:

```python
style = ExtrusionStyleFactory.create(style_number=1, stroke_width=2)
```

**Benefits:**
- Centralized style creation logic
- Type-safe style instantiation
- Runtime registration of new styles

### 3. Template Method Pattern

The `ExtrusionStyle` base class defines the rendering workflow:

```python
def render(self, x, y, width, height, extrude_x, extrude_y, color):
    elements = []
    elements.append(self.render_front_face(...))  # Hook method
    elements.extend(self.render_extrusion(...))   # Hook method
    return elements
```

**Benefits:**
- Consistent rendering workflow
- Subclasses only implement specific steps
- DRY principle

## SOLID Principles

### Single Responsibility Principle (SRP)
- ✅ Each style class has ONE job: render its specific extrusion type
- ✅ Factory has ONE job: create style instances
- ✅ `svg_generator.py` orchestrates, doesn't implement styles

### Open/Closed Principle (OCP)
- ✅ Open for extension: Add new styles by creating new classes
- ✅ Closed for modification: Existing styles don't change when adding new ones

### Liskov Substitution Principle (LSP)
- ✅ Any `ExtrusionStyle` subclass can be used interchangeably
- ✅ All styles implement the same interface

### Interface Segregation Principle (ISP)
- ✅ `ExtrusionStyle` interface is minimal and focused
- ✅ Clients only depend on methods they use

### Dependency Inversion Principle (DIP)
- ✅ `svg_generator.py` depends on `ExtrusionStyle` abstraction
- ✅ Concrete styles are injected via factory

## Data Flow

```
User Request
    ↓
generate_language_stats()
    ↓
fetch_language_stats()  →  GitHub API
    ↓
generate_language_stats_svg()
    ↓
ExtrusionStyleFactory.create(style_number)
    ↓
ExtrusionStyle.render()  →  SVG Elements
    ↓
Assembled SVG Output
    ↓
File System / README
```

## Configuration

Configuration is centralized in `config.py` and `svg_generator.py`:

- `EXTRUSION_STYLE`: Select style (1, 2, etc.)
- `EXTRUSION_DEPTH_X/Y`: Control 3D depth
- `STROKE_WIDTH`: Border thickness
- `CORNER_RADIUS`: Rounded corners

## Extensibility

### Adding a New Extrusion Style

1. **Create new style class:**
   ```python
   # extrusion_styles/style3_isometric.py
   from .base import ExtrusionStyle
   
   class IsometricExtrusion(ExtrusionStyle):
       def render_front_face(self, ...):
           # Implementation
       
       def render_extrusion(self, ...):
           # Implementation
   ```

2. **Register in factory:**
   ```python
   # In extrusion_styles/__init__.py
   from .style3_isometric import IsometricExtrusion
   ```

3. **Update factory registry:**
   ```python
   # extrusion_styles/factory.py
   _styles = {
       1: BackBoxExtrusion,
       2: ConnectedExtrusion,
       3: IsometricExtrusion  # Add here
   }
   ```

4. **Use it:**
   ```python
   EXTRUSION_STYLE = 3  # In svg_generator.py
   ```

## Testing Strategy

### Unit Tests
- Test each style independently
- Mock SVG generation
- Verify output format

### Integration Tests
- Test factory creation
- Test style switching
- Test with real data

### Example Test Structure
```python
def test_back_box_extrusion():
    style = BackBoxExtrusion(stroke_width=2)
    elements = style.render(0, 0, 100, 50, 10, 10, '#000')
    assert len(elements) == 2  # Front + back
    assert 'rect' in elements[0]
    assert 'rect' in elements[1]
```

## Performance Considerations

- **Lazy instantiation**: Styles created only when needed
- **Minimal memory**: Each style is stateless after configuration
- **SVG efficiency**: Paths optimized for minimal file size

## Future Enhancements

### Potential New Styles
1. **Style 3: Isometric** - True isometric projection
2. **Style 4: Shadow** - Drop shadow instead of extrusion
3. **Style 5: Gradient** - Gradient-filled extrusion
4. **Style 6: Wireframe** - Wireframe-only 3D effect

### Additional Features
- Configurable line styles (dashed, dotted)
- Animated SVG transitions
- Multiple color schemes per style
- Auto-selection based on theme

## Migration Guide

### From Old to New Architecture

**Before:**
```python
# Styles were hardcoded in draw_3d_box_borders()
paths = draw_3d_box_borders(x, y, w, h, ex, ey, sw, color, style=1)
```

**After:**
```python
# Styles are modular and extensible
from extrusion_styles import ExtrusionStyleFactory

style = ExtrusionStyleFactory.create(1, stroke_width=2)
paths = style.render(x, y, w, h, ex, ey, color)
```

**Benefits:**
- Better separation of concerns
- Easier to test
- Simpler to extend
- Follows DDD principles

## References

- **Domain-Driven Design**: Eric Evans
- **Design Patterns**: Gang of Four
- **SOLID Principles**: Robert C. Martin
- **Clean Architecture**: Robert C. Martin

