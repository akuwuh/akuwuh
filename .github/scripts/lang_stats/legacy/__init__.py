"""
Legacy modules - deprecated, kept for backward compatibility only.

⚠️ DO NOT USE THESE MODULES FOR NEW CODE!
⚠️ Use the new DDD architecture instead.

These modules are kept only to ensure backward compatibility with existing code.
They will be removed in version 4.0.0.

For new code, use:
    from lang_stats import LanguageStatsService, RenderConfig

See docs/README_NEW_ARCHITECTURE.md for migration guide.
"""

# Legacy imports (will be removed in v4.0.0)
from .generator import generate_language_stats
from .svg_generator import generate_language_stats_svg

__all__ = [
    'generate_language_stats',
    'generate_language_stats_svg'
]

