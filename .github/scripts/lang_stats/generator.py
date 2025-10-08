"""
Main generator that orchestrates the stats generation
"""

from .formatter import format_content_lines
from .box_drawer import draw_3d_border, draw_simple_border
from .html_converter import convert_to_html


def generate_language_stats(lang_stats, use_3d=True):
    """
    Generate WakaTime-style language stats as HTML
    
    Args:
        lang_stats: List of tuples [(language_name, percentage), ...]
        use_3d: If True, use 3D box; if False, use simple border
        
    Returns:
        HTML string with formatted stats
    """
    # Format content
    content_lines = format_content_lines(lang_stats)
    
    # Draw border (3D or simple)
    if use_3d:
        box_lines = draw_3d_border(content_lines)
    else:
        box_lines = draw_simple_border(content_lines)
    
    # Convert to HTML
    return convert_to_html(box_lines)
