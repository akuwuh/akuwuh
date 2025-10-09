# Extrusion Styles Module

This module provides a flexible, extensible architecture for rendering 3D box extrusion effects in SVG.

## Architecture

The module follows **Domain-Driven Design** principles with clear separation of concerns:

```
extrusion_styles/
├── base.py              # Abstract base class defining the interface
├── style1_back_box.py   # Style 1: Back box implementation
├── style2_connected.py  # Style 2: Connected extrusion implementation
├── factory.py           # Factory pattern for style instantiation
└── __init__.py          # Public API exports
```

## Design Patterns

### Strategy Pattern
Each extrusion style is a separate strategy that can be swapped at runtime without changing client code.

### Factory Pattern
The `ExtrusionStyleFactory` provides a centralized way to create style instances, making it easy to add new styles.

### Template Method Pattern
The base class defines the overall rendering workflow (`render()`), while subclasses implement specific steps (`render_front_face()`, `render_extrusion()`).

## Available Styles

### Style 1: Back Box Extrusion
**Class:** `BackBoxExtrusion`

Creates a clean, layered look by drawing a box behind the main box without diagonal connection lines.

**Use case:** When you want a simple, uncluttered 3D effect.

### Style 2: Connected Extrusion
**Class:** `ConnectedExtrusion`

Shows visible right and bottom faces with diagonal lines connecting front to back, creating a true 3D perspective.

**Use case:** When you want a more realistic 3D box appearance.

## Usage

### Basic Usage

```python
from extrusion_styles import ExtrusionStyleFactory

# Create a style instance
style = ExtrusionStyleFactory.create(
    style_number=1,
    stroke_width=2.0,
    corner_radius=0
)

# Render the 3D box
svg_elements = style.render(
    x=10, y=10,
    width=200, height=100,
    extrude_x=15, extrude_y=15,
    color='#000000'
)
```

### Adding a New Style

1. Create a new class extending `ExtrusionStyle`:

```python
# style3_custom.py
from .base import ExtrusionStyle

class CustomExtrusion(ExtrusionStyle):
    def render_front_face(self, x, y, width, height, color):
        # Your implementation
        pass
    
    def render_extrusion(self, x, y, width, height, extrude_x, extrude_y, color):
        # Your implementation
        pass
```

2. Register it with the factory:

```python
from extrusion_styles import ExtrusionStyleFactory
from .style3_custom import CustomExtrusion

ExtrusionStyleFactory.register_style(3, CustomExtrusion)
```

3. Use it:

```python
style = ExtrusionStyleFactory.create(3, stroke_width=2.0)
```

## Benefits of This Architecture

1. **Separation of Concerns**: Each style is isolated in its own module
2. **Open/Closed Principle**: Open for extension (new styles), closed for modification
3. **Single Responsibility**: Each class has one clear purpose
4. **Easy Testing**: Each style can be tested independently
5. **Maintainability**: Changes to one style don't affect others
6. **Extensibility**: New styles can be added without modifying existing code

## API Reference

### `ExtrusionStyle` (Abstract Base Class)

#### Methods

- `render(x, y, width, height, extrude_x, extrude_y, color)` → `List[str]`
  - Renders complete 3D box
  - Returns list of SVG element strings

- `render_front_face(x, y, width, height, color)` → `str` (abstract)
  - Renders the front face
  - Must be implemented by subclasses

- `render_extrusion(x, y, width, height, extrude_x, extrude_y, color)` → `List[str]` (abstract)
  - Renders the extrusion effect
  - Must be implemented by subclasses

### `ExtrusionStyleFactory`

#### Methods

- `create(style_number, stroke_width, corner_radius=0)` → `ExtrusionStyle`
  - Creates an extrusion style instance
  - Raises `ValueError` if style not found

- `register_style(style_number, style_class)` → `None`
  - Registers a new style class

- `available_styles()` → `List[int]`
  - Returns list of available style numbers

## Examples

### Switching Styles Dynamically

```python
from extrusion_styles import ExtrusionStyleFactory

for style_num in ExtrusionStyleFactory.available_styles():
    style = ExtrusionStyleFactory.create(style_num, stroke_width=2)
    elements = style.render(10, 10, 200, 100, 15, 15, '#000')
    print(f"Style {style_num}: {len(elements)} SVG elements")
```

### Custom Configuration

```python
# Create with custom stroke width and rounded corners
style = ExtrusionStyleFactory.create(
    style_number=1,
    stroke_width=3.5,
    corner_radius=5
)
```

