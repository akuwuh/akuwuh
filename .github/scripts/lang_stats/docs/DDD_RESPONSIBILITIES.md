# 🎯 Domain-Driven Design: Clear Responsibilities

## Project Structure (CLEAN!)

```
lang_stats/                        📦 MAIN PACKAGE
│
├── __init__.py                    🚪 Public API Entry Point
│
├── 🎯 domain/                     PURE BUSINESS LOGIC
│   ├── __init__.py
│   ├── language_stat.py           ↳ Single language statistic
│   └── stats_collection.py        ↳ Collection of statistics
│
├── 🔌 infrastructure/             EXTERNAL WORLD
│   ├── __init__.py
│   └── github_client.py           ↳ GitHub API adapter
│
├── 🎨 rendering/                  VISUALIZATION
│   ├── __init__.py
│   ├── progress_bar.py            ↳ Progress bar rendering
│   ├── text.py                    ↳ Text output
│   └── svg/                       ↳ SVG subsystem
│       ├── __init__.py
│       ├── renderer.py            ↳ SVG orchestrator
│       └── patterns.py            ↳ SVG patterns
│
├── 💼 core/                       APPLICATION SERVICES
│   ├── __init__.py
│   ├── config.py                  ↳ Configuration management
│   └── service.py                 ↳ Main service API
│
├── 🛠️ utils/                      SHARED UTILITIES
│   ├── __init__.py
│   ├── text_utils.py              ↳ Text processing
│   └── file_utils.py              ↳ File operations
│
├── 🎲 extrusion_styles/           RENDERING STRATEGIES
│   ├── __init__.py
│   ├── base.py                    ↳ Strategy interface
│   ├── style1_back_box.py         ↳ Back box strategy
│   ├── style2_connected.py        ↳ Connected strategy
│   ├── factory.py                 ↳ Strategy factory
│   └── README.md                  ↳ Style docs
│
├── 📚 docs/                       DOCUMENTATION
│   ├── DDD_RESPONSIBILITIES.md    ↳ This file
│   ├── README_NEW_ARCHITECTURE.md ↳ Quick start
│   ├── PROJECT_STRUCTURE.md       ↳ Detailed structure
│   ├── ARCHITECTURE.md            ↳ Architecture
│   ├── COMPLETE_REFACTORING.md    ↳ Refactoring details
│   ├── REFACTORING_SUMMARY.md     ↳ Summary
│   └── README.md                  ↳ Original docs
│
└── 📦 legacy/                     DEPRECATED (v4.0.0)
    ├── __init__.py
    ├── box_drawer.py              ↳ Old box drawing
    ├── config.py                  ↳ Old configuration
    ├── fetcher.py                 ↳ Old data fetching
    ├── formatter.py               ↳ Old formatting
    ├── generator.py               ↳ Old generator
    ├── html_converter.py          ↳ Old HTML converter
    ├── readme_updater.py          ↳ Old README updater
    └── svg_generator.py           ↳ Old SVG generator
```

---

## 📋 Layer Responsibilities

### 🎯 DOMAIN LAYER (`domain/`)

**What It Does**: Core business logic - the heart of your application

**Files**:
- `language_stat.py` - Defines what a language statistic IS
- `stats_collection.py` - Manages a collection of statistics

**Responsibilities**:
- ✅ Define business entities (`LanguageStat`)
- ✅ Define aggregates (`StatsCollection`)
- ✅ Enforce business rules (percentages must sum to 100%)
- ✅ Validate data integrity
- ✅ Provide domain operations (get top language, filter by threshold)

**Rules**:
- ❌ NO external dependencies (requests, etc.)
- ❌ NO I/O operations
- ❌ NO rendering logic
- ❌ NO infrastructure concerns
- ✅ Pure Python business logic only

**Example**:
```python
# domain/language_stat.py
@dataclass(frozen=True)
class LanguageStat:
    """A single language statistic - immutable value object"""
    name: str
    percentage: float
    bytes: int = 0
    
    def __post_init__(self):
        # Enforce business rules
        if not 0 <= self.percentage <= 100:
            raise ValueError("Percentage must be 0-100")
```

---

### 🔌 INFRASTRUCTURE LAYER (`infrastructure/`)

**What It Does**: Talks to the outside world (APIs, databases, files)

**Files**:
- `github_client.py` - Fetches data from GitHub API

**Responsibilities**:
- ✅ Interact with external APIs (GitHub)
- ✅ Handle authentication and tokens
- ✅ Manage network requests
- ✅ Convert external data → domain objects
- ✅ Handle errors and retries

**Rules**:
- ❌ NO business logic
- ❌ NO rendering concerns
- ✅ Convert DTOs to domain models
- ✅ All I/O happens here

**Example**:
```python
# infrastructure/github_client.py
class GitHubClient:
    """Adapter for GitHub API"""
    
    def fetch_language_stats(self, username: str) -> StatsCollection:
        # 1. Fetch from API (infrastructure concern)
        repos = self._fetch_user_repos(username)
        
        # 2. Convert to domain objects
        stats = self._calculate_percentages(language_bytes)
        
        # 3. Return domain aggregate
        return StatsCollection(stats)
```

---

### 🎨 RENDERING LAYER (`rendering/`)

**What It Does**: Turns domain objects into visual output

**Files**:
- `svg/renderer.py` - Main SVG orchestrator
- `svg/patterns.py` - SVG pattern generation
- `text.py` - Text-based rendering
- `progress_bar.py` - Progress bar generation

**Responsibilities**:
- ✅ Render domain objects as SVG
- ✅ Render domain objects as text
- ✅ Generate visual elements
- ✅ Apply styling and themes
- ✅ Create progress bars

**Rules**:
- ❌ NO business logic
- ❌ NO data fetching
- ❌ NO I/O (except returning strings)
- ✅ Pure rendering logic only

**Example**:
```python
# rendering/svg/renderer.py
class SVGRenderer:
    """Renders statistics as SVG"""
    
    def render(self, stats: StatsCollection) -> str:
        # Takes domain object, returns SVG string
        # NO business logic - just visualization
        return svg_string
```

---

### 💼 CORE LAYER (`core/`)

**What It Does**: Application services - orchestrates everything

**Files**:
- `service.py` - Main application service
- `config.py` - Configuration management

**Responsibilities**:
- ✅ Coordinate between layers
- ✅ Manage configuration
- ✅ Provide high-level API
- ✅ Handle workflows
- ✅ Compose operations

**Rules**:
- ❌ NO rendering details
- ❌ NO data access details
- ❌ NO business logic
- ✅ Orchestration only

**Example**:
```python
# core/service.py
class LanguageStatsService:
    """Main application service"""
    
    def generate_svg(self, config: RenderConfig) -> str:
        # 1. Fetch data (infrastructure)
        stats = self.github_client.fetch_language_stats()
        
        # 2. Render (presentation)
        renderer = SVGRenderer(config)
        svg = renderer.render(stats)
        
        # 3. Return result
        return svg
```

---

### 🛠️ UTILS LAYER (`utils/`)

**What It Does**: Shared helper functions

**Files**:
- `text_utils.py` - Text processing utilities
- `file_utils.py` - File system utilities

**Responsibilities**:
- ✅ Text escaping and formatting
- ✅ File I/O helpers
- ✅ Common algorithms
- ✅ Reusable functions

**Rules**:
- ❌ NO layer-specific logic
- ❌ NO state management
- ✅ Pure functions preferred
- ✅ Reusable across all layers

**Example**:
```python
# utils/text_utils.py
def escape_xml(text: str) -> str:
    """Pure function - no side effects"""
    return text.replace('&', '&amp;').replace('<', '&lt;')
```

---

### 🎲 EXTRUSION STYLES (`extrusion_styles/`)

**What It Does**: Pluggable 3D rendering strategies

**Files**:
- `base.py` - Strategy interface
- `style1_back_box.py` - Back box implementation
- `style2_connected.py` - Connected implementation
- `factory.py` - Style creation

**Responsibilities**:
- ✅ Define rendering strategies
- ✅ Implement style variations
- ✅ Factory for style creation
- ✅ Self-contained rendering

**Rules**:
- ❌ NO business logic
- ❌ NO data access
- ✅ Strategy pattern
- ✅ Easily extensible

**Example**:
```python
# extrusion_styles/style1_back_box.py
class BackBoxExtrusion(ExtrusionStyle):
    """Strategy for back box style"""
    
    def render(self, x, y, width, height, ...) -> List[str]:
        # Returns SVG elements for this specific style
        return [front_box, back_box]
```

---

### 📦 LEGACY (`legacy/`)

**What It Does**: Old code kept for backward compatibility

**Status**: ⚠️ DEPRECATED - Will be removed in v4.0.0

**Files**: All old monolithic scripts

**Responsibilities**:
- ✅ Maintain backward compatibility
- ✅ Redirect to new architecture where possible

**Rules**:
- ❌ DO NOT USE FOR NEW CODE
- ❌ DO NOT MODIFY (unless critical bug)
- ✅ Migrate to new API when possible

---

## 🔄 Data Flow

```
USER REQUEST
    ↓
┌─────────────────────────────┐
│  core/service.py            │ ← YOU START HERE
│  LanguageStatsService       │
└────────┬────────────────────┘
         │
         ├──→ infrastructure/github_client.py
         │    ↓ Fetch data from API
         │    ↓ Convert to domain objects
         │    ↓
         │    └──→ domain/stats_collection.py
         │         └──→ domain/language_stat.py
         │              (Pure business objects)
         │
         └──→ rendering/svg/renderer.py
              ├──→ extrusion_styles/factory.py
              │    └──→ style1 or style2
              │
              ├──→ rendering/svg/patterns.py
              │
              ├──→ rendering/progress_bar.py
              │
              └──→ utils/text_utils.py
                   
    ↓
SVG OUTPUT
```

---

## 🎯 Single Responsibility Examples

### ✅ GOOD: Each file has ONE job

**domain/language_stat.py**
- Job: Define what a language stat IS
- Does: Validates data, provides properties
- Doesn't: Fetch data, render, configure

**infrastructure/github_client.py**
- Job: Talk to GitHub API
- Does: HTTP requests, authentication, error handling
- Doesn't: Business logic, rendering, configuration

**rendering/svg/renderer.py**
- Job: Render SVG output
- Does: Generate SVG strings, coordinate rendering
- Doesn't: Fetch data, business validation, I/O

**core/service.py**
- Job: Orchestrate the workflow
- Does: Coordinate layers, manage config
- Doesn't: Rendering details, data access details

### ❌ BAD: Old monolithic approach

**Old generator.py** (LEGACY)
- Mixed concerns: fetching + formatting + rendering
- Hard to test
- Difficult to modify
- No clear responsibility

---

## 🚀 Usage Guide

### For Simple Use Cases

```python
# Use the service layer - it handles everything
from lang_stats import LanguageStatsService, RenderConfig

service = LanguageStatsService(username="user")
svg = service.generate_svg()  # Easy!
```

### For Advanced Use Cases

```python
# Use components directly for more control
from lang_stats.infrastructure import GitHubClient
from lang_stats.rendering.svg import SVGRenderer
from lang_stats.core import RenderConfig

# 1. Fetch (infrastructure layer)
client = GitHubClient(token="...")
stats = client.fetch_language_stats("user")

# 2. Render (presentation layer)
config = RenderConfig.custom(extrusion_style=2)
renderer = SVGRenderer(config)
svg = renderer.render(stats)
```

### For Testing

```python
# Mock at layer boundaries
from unittest.mock import Mock
from lang_stats.domain import StatsCollection, LanguageStat

# Create test data (domain objects)
test_stats = StatsCollection([
    LanguageStat("Python", 50.0),
    LanguageStat("TypeScript", 50.0)
])

# Test renderer in isolation
renderer = SVGRenderer(config)
result = renderer.render(test_stats)  # No API calls!
```

---

## 📊 Responsibility Matrix

| Layer | Fetches Data | Business Logic | Renders | I/O | Orchestrates |
|-------|--------------|----------------|---------|-----|--------------|
| **domain/** | ❌ | ✅ | ❌ | ❌ | ❌ |
| **infrastructure/** | ✅ | ❌ | ❌ | ✅ | ❌ |
| **rendering/** | ❌ | ❌ | ✅ | ❌ | ❌ |
| **core/** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **utils/** | ❌ | ❌ | ❌ | Maybe | ❌ |
| **extrusion_styles/** | ❌ | ❌ | ✅ | ❌ | ❌ |

---

## 🎓 Summary

### Each Layer Has ONE Job:

1. **domain/** = What things ARE (business entities)
2. **infrastructure/** = Talk to external world (APIs)
3. **rendering/** = Make things visible (SVG, text)
4. **core/** = Coordinate everything (orchestration)
5. **utils/** = Helper functions (pure utilities)
6. **extrusion_styles/** = Pluggable strategies (rendering styles)
7. **legacy/** = Old code (deprecated)

### Golden Rules:

- ✅ **Each file** has a single, clear purpose
- ✅ **Each layer** has distinct responsibilities
- ✅ **Dependencies** flow in one direction
- ✅ **Testing** is easy (isolated components)
- ✅ **Changes** are localized (modify one layer)

### This is TRUE Domain-Driven Design! 🎯

No more mixed concerns.  
No more "everything in one file".  
Clean, professional, maintainable code.

---

**Version**: 3.0.0  
**Status**: ✅ Production Ready  
**Architecture**: Domain-Driven Design (DDD)

