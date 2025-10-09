"""
Language Statistics Generator for GitHub README

A professional, modular system for generating beautiful language statistics
visualizations with 3D box effects. Built with Domain-Driven Design principles.

Architecture:
    - domain/         : Core business logic and entities
    - infrastructure/ : External services (GitHub API)
    - rendering/      : Visualization engines (SVG, text)
    - core/           : Application services and configuration
    - utils/          : Shared utilities
    - extrusion_styles/ : Pluggable 3D rendering strategies

Example usage:
    >>> from lang_stats import LanguageStatsService, RenderConfig
    >>> 
    >>> service = LanguageStatsService(github_token="your_token", username="yourusername")
    >>> config = RenderConfig.default_light()
    >>> svg = service.generate_svg(config=config)
    >>> print(svg)
"""

__version__ = '3.0.0'  # Complete DDD refactoring

# Core service (recommended API)
from .core import LanguageStatsService, RenderConfig, ThemeColors

# Domain models (for advanced usage)
from .domain import LanguageStat, StatsCollection

# Rendering engines
from .rendering import SVGRenderer, TextRenderer

# Extrusion styles (for customization)
from . import extrusion_styles

# Legacy compatibility (backward compatible)
# Note: Legacy imports disabled to avoid circular dependencies
# If you need old API, import directly from legacy module:
# from lang_stats.legacy import generate_language_stats, generate_language_stats_svg

__all__ = [
    # Main API (recommended)
    'LanguageStatsService',
    'RenderConfig',
    'ThemeColors',
    
    # Domain models
    'LanguageStat',
    'StatsCollection',
    
    # Renderers
    'SVGRenderer',
    'TextRenderer',
    
    # Extrusion styles
    'extrusion_styles',
    
]
