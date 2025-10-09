"""
Main generator that orchestrates the stats generation
"""

from .formatter import format_content_lines
from .box_drawer import draw_3d_border, draw_simple_border
from .html_converter import convert_to_html
from .svg_generator import generate_language_stats_svg
from .config import OUTPUT_MODE, USE_GRAPHICAL_BARS, USE_VECTOR_BORDERS, SVG_THEME


def generate_language_stats(lang_stats, use_3d=True, output_mode=None, use_graphical_bars=None, use_vector_borders=None, svg_theme=None):
    """
    Generate WakaTime-style language stats as HTML or SVG
    
    Args:
        lang_stats: List of tuples [(language_name, percentage), ...]
        use_3d: If True, use 3D box; if False, use simple border
        output_mode: 'text' or 'vector' (defaults to config.OUTPUT_MODE)
        use_graphical_bars: Use graphical bars in SVG mode (defaults to config.USE_GRAPHICAL_BARS)
        use_vector_borders: Use SVG paths for borders in vector mode (defaults to config.USE_VECTOR_BORDERS)
        svg_theme: 'light' or 'dark' for SVG mode (defaults to config.SVG_THEME)
        
    Returns:
        HTML string or SVG string with formatted stats
    """
    # Use config defaults if not specified
    if output_mode is None:
        output_mode = OUTPUT_MODE
    if use_graphical_bars is None:
        use_graphical_bars = USE_GRAPHICAL_BARS
    if use_vector_borders is None:
        use_vector_borders = USE_VECTOR_BORDERS
    if svg_theme is None:
        svg_theme = SVG_THEME
    
    if output_mode == 'vector':
        # Generate SVG
        svg_content = generate_language_stats_svg(
            lang_stats, 
            use_3d=use_3d, 
            use_graphical_bars=use_graphical_bars,
            use_vector_borders=use_vector_borders,
            theme=svg_theme
        )
        # Wrap SVG in div for README
        return f'<div align="center">\n{svg_content}\n</div>'
    else:
        # Generate text-based HTML (original behavior)
        content_lines = format_content_lines(lang_stats)
        
        # Draw border (3D or simple)
        if use_3d:
            box_lines = draw_3d_border(content_lines)
        else:
            box_lines = draw_simple_border(content_lines)
        
        # Convert to HTML
        return convert_to_html(box_lines)
