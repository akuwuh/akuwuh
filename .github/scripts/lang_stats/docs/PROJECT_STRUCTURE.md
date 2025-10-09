##🏗️ Project Structure

This document describes the professional Python project structure following Domain-Driven Design principles.

## Directory Layout

```
lang_stats/                          # Main package
│
├── __init__.py                      # Public API exports
│
├── domain/                          # 🎯 DOMAIN LAYER
│   ├── __init__.py                  # Core business logic & entities
│   ├── language_stat.py             # LanguageStat entity (immutable)
│   └── stats_collection.py          # StatsCollection aggregate
│
├── infrastructure/                  # 🔌 INFRASTRUCTURE LAYER
│   ├── __init__.py                  # External services & adapters
│   └── github_client.py             # GitHub API client
│
├── rendering/                       # 🎨 PRESENTATION LAYER
│   ├── __init__.py                  # Visualization engines
│   ├── progress_bar.py              # Progress bar renderer
│   ├── text.py                      # Text-based renderer
│   └── svg/                         # SVG rendering subsystem
│       ├── __init__.py
│       ├── renderer.py              # Main SVG orchestrator
│       └── patterns.py              # SVG pattern generators
│
├── core/                            # 💼 APPLICATION LAYER
│   ├── __init__.py                  # Services & coordination
│   ├── config.py                    # Configuration management
│   └── service.py                   # LanguageStatsService
│
├── utils/                           # 🛠️ UTILITIES
│   ├── __init__.py                  # Shared utilities
│   ├── text_utils.py                # Text processing
│   └── file_utils.py                # File operations
│
├── extrusion_styles/                # 🎲 PLUGGABLE STRATEGIES
│   ├── __init__.py                  # Strategy implementations
│   ├── base.py                      # ExtrusionStyle ABC
│   ├── style1_back_box.py           # Back box style
│   ├── style2_connected.py          # Connected style
│   ├── factory.py                   # Style factory
│   └── README.md                    # Style documentation
│
├── legacy/                          # 📦 LEGACY (backward compat)
│   ├── generator.py                 # Old generate_language_stats()
│   ├── svg_generator.py             # Old generate_language_stats_svg()
│   ├── formatter.py                 # Old formatters
│   ├── box_drawer.py                # Old box drawing
│   ├── html_converter.py            # Old HTML converter
│   └── readme_updater.py            # Old README updater
│
├── ARCHITECTURE.md                  # Architecture documentation
├── REFACTORING_SUMMARY.md           # Refactoring details
└── PROJECT_STRUCTURE.md             # This file

../                                  # Project root
├── requirements.txt                 # Python dependencies
├── setup.py                         # Setup script
└── pyproject.toml                   # Modern Python project config
```

## Layer Responsibilities

### 🎯 Domain Layer (`domain/`)

**Purpose**: Core business logic and entities

**Responsibilities**:
- Define domain entities (`LanguageStat`)
- Define aggregates (`StatsCollection`)
- Enforce business rules and invariants
- Pure Python, no external dependencies

**Key Classes**:
- `LanguageStat`: Immutable value object representing a language stat
- `StatsCollection`: Aggregate managing collection of stats

**Rules**:
- ✅ No dependencies on other layers
- ✅ Immutable entities where possible
- ✅ Rich domain models with behavior
- ❌ No I/O operations
- ❌ No framework dependencies

### 🔌 Infrastructure Layer (`infrastructure/`)

**Purpose**: External services and adapters

**Responsibilities**:
- Interact with external APIs (GitHub)
- Handle authentication and rate limiting
- Convert external data to domain models
- Manage network errors

**Key Classes**:
- `GitHubClient`: GitHub API adapter

**Rules**:
- ✅ Depends on domain layer
- ✅ Handles all I/O
- ✅ Converts DTOs to domain objects
- ❌ No business logic
- ❌ No rendering logic

### 🎨 Presentation Layer (`rendering/`)

**Purpose**: Visualization and output generation

**Responsibilities**:
- Render domain models as SVG
- Render domain models as text
- Generate progress bars
- Apply styling and themes

**Key Classes**:
- `SVGRenderer`: Main SVG orchestrator
- `TextRenderer`: Text-based output
- `ProgressBarRenderer`: Progress bar generation
- `CheckeredPatternGenerator`: SVG patterns

**Rules**:
- ✅ Depends on domain and core layers
- ✅ Pure rendering logic
- ❌ No business logic
- ❌ No I/O operations

### 💼 Application Layer (`core/`)

**Purpose**: Application services and orchestration

**Responsibilities**:
- Coordinate between layers
- Manage configuration
- Provide high-level API
- Handle workflows

**Key Classes**:
- `LanguageStatsService`: Main application service
- `RenderConfig`: Configuration management
- `ThemeColors`: Color schemes

**Rules**:
- ✅ Orchestrates other layers
- ✅ Manages transactions/workflows
- ✅ Provides public API
- ❌ No rendering details
- ❌ No data access details

### 🛠️ Utilities (`utils/`)

**Purpose**: Shared utilities and helpers

**Responsibilities**:
- Text processing
- File operations
- Common algorithms

**Key Functions**:
- `escape_xml()`: XML escaping
- `calculate_text_width()`: Text measurements
- `ensure_directory()`: File system helpers

**Rules**:
- ✅ Pure functions when possible
- ✅ Reusable across layers
- ❌ No layer-specific logic
- ❌ No state management

### 🎲 Extrusion Styles (`extrusion_styles/`)

**Purpose**: Pluggable 3D rendering strategies

**Responsibilities**:
- Define extrusion rendering interface
- Implement style variations
- Factory pattern for style creation

**Key Classes**:
- `ExtrusionStyle`: Abstract base class
- `BackBoxExtrusion`: Style 1
- `ConnectedExtrusion`: Style 2
- `ExtrusionStyleFactory`: Style factory

**Rules**:
- ✅ Strategy pattern
- ✅ Easily extensible
- ✅ Self-contained modules
- ❌ No cross-style dependencies

## Dependency Flow

```
┌─────────────────────────────────────────────┐
│           Public API (__init__.py)          │
└──────────────────┬──────────────────────────┘
                   │
      ┌────────────┴────────────┐
      │                         │
      v                         v
┌─────────────┐          ┌─────────────┐
│    Core     │─────────>│  Rendering  │
│  (Service)  │          │             │
└─────┬───────┘          └──────┬──────┘
      │                         │
      │    ┌────────────┐       │
      └───>│   Domain   │<──────┘
      │    └────────────┘       │
      │                         │
      v                         v
┌─────────────┐          ┌─────────────┐
│Infrastructure│         │   Utils     │
└─────────────┘          └─────────────┘
                              ^
                              │
                    ┌─────────┴─────────┐
                    │  Extrusion Styles │
                    └───────────────────┘
```

**Rules**:
- Core depends on: Domain, Infrastructure, Rendering
- Rendering depends on: Domain, Utils, Extrusion Styles
- Infrastructure depends on: Domain
- Domain depends on: Nothing (pure)
- Utils depends on: Nothing (pure)

## Module Organization Principles

### 1. **Separation of Concerns**
Each module has a single, well-defined responsibility.

### 2. **Dependency Inversion**
High-level modules don't depend on low-level modules. Both depend on abstractions.

### 3. **Interface Segregation**
Clients only depend on methods they use.

### 4. **Open/Closed Principle**
Open for extension (new styles, renderers), closed for modification.

### 5. **Single Responsibility**
Each class/module has one reason to change.

## Usage Examples

### Simple Usage (Service API)

```python
from lang_stats import LanguageStatsService, RenderConfig

# Create service
service = LanguageStatsService(
    github_token="your_token",
    username="yourusername"
)

# Generate SVG
config = RenderConfig.default_light()
svg = service.generate_svg(config=config)
print(svg)
```

### Advanced Usage (Direct Components)

```python
from lang_stats.infrastructure import GitHubClient
from lang_stats.rendering.svg import SVGRenderer
from lang_stats.core import RenderConfig

# Fetch data
client = GitHubClient(token="your_token")
stats = client.fetch_language_stats("yourusername")

# Render
config = RenderConfig.custom(extrusion_style=2, theme='dark')
renderer = SVGRenderer(config)
svg = renderer.render(stats)
```

### Custom Extrusion Style

```python
from lang_stats.extrusion_styles import ExtrusionStyle, ExtrusionStyleFactory

# Define custom style
class IsometricExtrusion(ExtrusionStyle):
    def render_front_face(self, ...):
        # Your implementation
        pass
    
    def render_extrusion(self, ...):
        # Your implementation
        pass

# Register
ExtrusionStyleFactory.register_style(3, IsometricExtrusion)

# Use
config = RenderConfig.custom(extrusion_style=3)
```

## Testing Strategy

### Unit Tests
```
tests/
├── domain/                 # Test domain logic
├── infrastructure/         # Test API clients (mocked)
├── rendering/              # Test renderers
├── core/                   # Test services
└── extrusion_styles/       # Test styles
```

### Integration Tests
```
tests/integration/
├── test_end_to_end.py     # Full workflow
└── test_api_integration.py # Real API calls
```

## Migration Guide

### From Old API

**Before:**
```python
from lang_stats import generate_language_stats_svg
svg = generate_language_stats_svg(stats, theme='light')
```

**After (recommended):**
```python
from lang_stats import LanguageStatsService, RenderConfig
service = LanguageStatsService(username="user")
config = RenderConfig.default_light()
svg = service.generate_svg(config=config)
```

**After (backward compatible):**
```python
from lang_stats import generate_language_stats_svg  # Still works!
svg = generate_language_stats_svg(stats, theme='light')
```

## Benefits of This Structure

### For Development
- 🚀 **Fast iteration**: Change one layer without affecting others
- 🧪 **Easy testing**: Each layer tested independently
- 📚 **Clear contracts**: Interfaces define expectations
- 🔍 **Easy debugging**: Clear boundaries isolate issues

### For Maintenance
- ✏️ **Easy to modify**: Changes localized to specific modules
- ➕ **Easy to extend**: Add features without breaking existing code
- 🔧 **Easy to refactor**: Clean dependencies enable safe refactoring
- 📖 **Easy to understand**: Clear structure and documentation

### For Scalability
- 🏗️ **Modular**: Add new renderers, styles, or data sources easily
- 🔄 **Reusable**: Components can be used in different contexts
- 🎯 **Focused**: Each module has a clear purpose
- 💪 **Robust**: Strong separation prevents side effects

## Future Enhancements

### Potential Additions

1. **New Renderers**
   - HTML5 Canvas renderer
   - PNG/Image renderer
   - PDF renderer

2. **New Data Sources**
   - GitLab integration
   - Bitbucket integration
   - Local repository scanning

3. **New Features**
   - Caching layer
   - Analytics/tracking
   - Real-time updates
   - Custom themes

4. **Developer Tools**
   - CLI tool
   - Web dashboard
   - VS Code extension

## Conventions

### Naming
- Classes: `PascalCase`
- Functions/methods: `snake_case`
- Constants: `UPPER_CASE`
- Private: `_leading_underscore`

### File Organization
- One class per file (when possible)
- Related classes in same module
- Tests mirror source structure

### Documentation
- Docstrings for all public APIs
- Type hints for all functions
- README in each major module
- Architecture docs at root

## Conclusion

This structure provides a solid foundation for a professional Python project that:
- Is maintainable and scalable
- Follows industry best practices
- Enables independent development of features
- Provides clear APIs for users

The architecture supports current needs while allowing for future growth without major restructuring.

