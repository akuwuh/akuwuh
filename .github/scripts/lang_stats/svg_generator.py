"""
SVG generator for language statistics with 3D box effect
"""

from .config import (
    LEFT_PADDING,
    RIGHT_PADDING,
    EXTRUSION_INDENT_LEVEL_1,
    EXTRUSION_INDENT_LEVEL_2,
    PROGRESS_BAR_BLOCKS,
    FILLED_BLOCK,
    EMPTY_BLOCK,
    LANG_NAME_WIDTH
)
from .formatter import generate_progress_bar
from .extrusion_styles import ExtrusionStyleFactory


# SVG Configuration
CHAR_WIDTH = 9.6  # Width of monospace character in pixels
CHAR_HEIGHT = 20  # Height of line in pixels
LINE_SPACING = 4  # Additional spacing between lines
FONT_SIZE = 16
FONT_FAMILY = "'Courier New', Courier, monospace"

# 3D Box Configuration
BOX_PADDING_X = 20  # Horizontal padding inside box
BOX_PADDING_Y = 15  # Vertical padding inside box
EXTRUSION_DEPTH_X = 15  # Horizontal depth of 3D extrusion
EXTRUSION_DEPTH_Y = 15  # Vertical depth of 3D extrusion
STROKE_WIDTH = 2  # Width of border lines
CORNER_RADIUS = 0  # Radius for rounded corners
EXTRUSION_STYLE = 1  # 1 = back box (no diagonals), 2 = connected extrusion (with diagonals)

# Colors for light and dark themes
COLORS_LIGHT = {
    'text': '#000000',
    'border': '#000000',
    'bg': 'transparent',
    'filled_bar': '#000000',
    'empty_bar': '#d0d7de'
}

COLORS_DARK = {
    'text': '#FFFFFF',
    'border': '#FFFFFF',
    'bg': 'transparent',
    'filled_bar': '#FFFFFF',
    'empty_bar': '#d0d7de'
}


def escape_xml(text):
    """Escape XML special characters"""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def draw_3d_box_borders(x, y, width, height, extrude_x, extrude_y, stroke_width, color, style=1):
    """
    Draw 3D box borders using the specified extrusion style.
    
    This function uses the ExtrusionStyleFactory to create the appropriate
    style renderer and delegates the rendering to it.
    
    Args:
        x, y: Top-left corner of front face
        width, height: Dimensions of front face
        extrude_x, extrude_y: Extrusion depth
        stroke_width: Line thickness
        color: Border color
        style: Style number (1, 2, etc.)
        
    Returns:
        List of SVG path/line elements
    """
    extrusion_style = ExtrusionStyleFactory.create(style, stroke_width, CORNER_RADIUS)
    return extrusion_style.render(x, y, width, height, extrude_x, extrude_y, color)


def calculate_text_width(text):
    """Calculate approximate width of text in pixels"""
    return len(text) * CHAR_WIDTH


def draw_box_line(x, y, text):
    """Generate SVG text element for a single line"""
    return f'<text x="{x}" y="{y}" class="box-text">{escape_xml(text)}</text>'


def format_lang_line(lang_name, percentage, show_bar_placeholder=True):
    """Format a single language line with proper spacing"""
    lang_display = lang_name.ljust(LANG_NAME_WIDTH)
    percent_str = f'{percentage:5.1f} %'
    
    if show_bar_placeholder:
        # Add space for progress bar
        return f'{lang_display}  {" " * PROGRESS_BAR_BLOCKS}  {percent_str}'
    else:
        # For text-based bars
        bar = generate_progress_bar(percentage)
        return f'{lang_display}  {bar}  {percent_str}'


def generate_svg_3d_box(content_lines, theme='light'):
    """
    Generate SVG with 3D box effect
    
    Args:
        content_lines: List of content strings
        theme: 'light' or 'dark'
        
    Returns:
        SVG string
    """
    if not content_lines:
        return ""
    
    colors = COLORS_LIGHT if theme == 'light' else COLORS_DARK
    
    max_content_length = max(len(line) for line in content_lines)
    inner_width = LEFT_PADDING + max_content_length + RIGHT_PADDING
    
    # Build box lines (same as text version)
    box_lines = []
    
    # Top border
    box_lines.append('┌' + '─' * inner_width + '┐')
    
    # Content lines with right extrusion
    for i, content in enumerate(content_lines):
        padded_content = f'{" " * LEFT_PADDING}{content}'.ljust(inner_width)
        indent = ' ' * EXTRUSION_INDENT_LEVEL_1
        
        if i == 0:
            box_lines.append(f'{indent}│{padded_content}├─┐')
        else:
            box_lines.append(f'{indent}│{padded_content}│ │')
    
    # Bottom border with 3D effect
    indent_1 = ' ' * EXTRUSION_INDENT_LEVEL_1
    indent_2 = ' ' * EXTRUSION_INDENT_LEVEL_2
    box_lines.append(f'{indent_1}└┬' + '─' * (inner_width - 1) + '┘ │')
    box_lines.append(f'{indent_2}└' + '─' * (inner_width + 1) + '┘')
    
    # Calculate SVG dimensions
    max_line_width = max(len(line) for line in box_lines)
    svg_width = max_line_width * CHAR_WIDTH + 20
    svg_height = len(box_lines) * (CHAR_HEIGHT + LINE_SPACING) + 20
    
    # Generate SVG
    svg_parts = []
    svg_parts.append(f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append('  <style>')
    svg_parts.append(f'    .box-text {{ font-family: {FONT_FAMILY}; font-size: {FONT_SIZE}px; fill: {colors["text"]}; white-space: pre; }}')
    svg_parts.append('  </style>')
    
    # Add text elements for each line
    y_pos = CHAR_HEIGHT + 10
    for line in box_lines:
        svg_parts.append(f'  {draw_box_line(10, y_pos, line)}')
        y_pos += CHAR_HEIGHT + LINE_SPACING
    
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)


def generate_svg_with_vector_borders(lang_stats, theme='light'):
    """
    Generate SVG with true vector borders and graphical progress bars
    
    Args:
        lang_stats: List of tuples [(language_name, percentage), ...]
        theme: 'light' or 'dark'
        
    Returns:
        SVG string with vector-drawn 3D box and graphical progress bars
    """
    if not lang_stats:
        return ""
    
    colors = COLORS_LIGHT if theme == 'light' else COLORS_DARK
    
    # Calculate content dimensions
    max_text_width = 0
    content_data = []
    
    for lang_name, percentage in lang_stats:
        line_text = format_lang_line(lang_name, percentage, show_bar_placeholder=True)
        text_width = calculate_text_width(line_text)
        max_text_width = max(max_text_width, text_width)
        content_data.append({
            'lang_name': lang_name,
            'percentage': percentage,
            'text': line_text,
            'filled_blocks': round((percentage / 100) * PROGRESS_BAR_BLOCKS)
        })
    
    # Box dimensions
    box_width = max_text_width + (BOX_PADDING_X * 2)
    box_height = len(lang_stats) * (CHAR_HEIGHT + LINE_SPACING) + (BOX_PADDING_Y * 2)
    
    # SVG dimensions (including extrusion)
    svg_width = box_width + EXTRUSION_DEPTH_X + 40
    svg_height = box_height + EXTRUSION_DEPTH_Y + 40
    
    # Starting positions
    box_x = 20
    box_y = 20
    
    # Build SVG
    svg_parts = []
    svg_parts.append(f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">')
    svg_parts.append('  <defs>')
    svg_parts.append('    <!-- Checkered pattern for empty bar (░ effect) -->')
    # Bar height is 12px, 6 squares = 2px per square, pattern repeats every 4px (2 squares)
    pattern_size = 4
    square_size = 2
    svg_parts.append(f'    <pattern id="checkered-pattern-{theme}" x="0" y="0" width="{pattern_size}" height="{pattern_size}" patternUnits="userSpaceOnUse">')
    svg_parts.append(f'      <rect width="{square_size}" height="{square_size}" x="0" y="0" fill="none" />')
    svg_parts.append(f'      <rect width="{square_size}" height="{square_size}" x="{square_size}" y="0" fill="{colors["text"]}" />')
    svg_parts.append(f'      <rect width="{square_size}" height="{square_size}" x="0" y="{square_size}" fill="{colors["text"]}" />')
    svg_parts.append(f'      <rect width="{square_size}" height="{square_size}" x="{square_size}" y="{square_size}" fill="none" />')
    svg_parts.append('    </pattern>')
    svg_parts.append('    <style>')
    svg_parts.append(f'      .lang-text {{ font-family: {FONT_FAMILY}; font-size: {FONT_SIZE}px; fill: {colors["text"]}; }}')
    svg_parts.append(f'      .bar-filled {{ fill: {colors["filled_bar"]}; }}')
    svg_parts.append(f'      .bar-empty {{ fill: url(#checkered-pattern-{theme}); }}')
    svg_parts.append('    </style>')
    svg_parts.append('  </defs>')
    svg_parts.append('')
    
    # Draw 3D box borders
    svg_parts.append('  <!-- 3D Box Borders -->')
    svg_parts.append('  <g id="box-borders">')
    border_paths = draw_3d_box_borders(
        box_x, box_y, box_width, box_height,
        EXTRUSION_DEPTH_X, EXTRUSION_DEPTH_Y,
        STROKE_WIDTH, colors['border'], EXTRUSION_STYLE
    )
    for path in border_paths:
        svg_parts.append(f'    {path}')
    svg_parts.append('  </g>')
    svg_parts.append('')
    
    # Draw content (text and progress bars)
    svg_parts.append('  <!-- Language Statistics -->')
    svg_parts.append('  <g id="content">')
    
    y_pos = box_y + BOX_PADDING_Y + CHAR_HEIGHT
    bar_x_offset = BOX_PADDING_X + (LANG_NAME_WIDTH + 2) * CHAR_WIDTH
    
    for i, data in enumerate(content_data):
        # Draw language name
        lang_text = data['lang_name'].ljust(LANG_NAME_WIDTH)
        svg_parts.append(f'    <text x="{box_x + BOX_PADDING_X}" y="{y_pos}" class="lang-text">{escape_xml(lang_text)}</text>')
        
        # Draw progress bar
        bar_y = y_pos - CHAR_HEIGHT + 6
        bar_width = PROGRESS_BAR_BLOCKS * CHAR_WIDTH * 0.95
        bar_height = 12  # Divisible by 6 for perfect checkerboard pattern
        
        filled_width = data['filled_blocks'] * CHAR_WIDTH * 0.95
        empty_width = bar_width - filled_width
        
        # Filled portion
        if filled_width > 0:
            svg_parts.append(f'    <rect x="{box_x + bar_x_offset}" y="{bar_y}" width="{filled_width}" height="{bar_height}" class="bar-filled" />')
        
        # Empty portion
        if empty_width > 0:
            svg_parts.append(f'    <rect x="{box_x + bar_x_offset + filled_width}" y="{bar_y}" width="{empty_width}" height="{bar_height}" class="bar-empty" />')
        
        # Draw percentage
        percent_str = f'{data["percentage"]:5.1f} %'
        percent_x = box_x + bar_x_offset + bar_width + (2 * CHAR_WIDTH)
        svg_parts.append(f'    <text x="{percent_x}" y="{y_pos}" class="lang-text">{percent_str}</text>')
        
        y_pos += CHAR_HEIGHT + LINE_SPACING
    
    svg_parts.append('  </g>')
    svg_parts.append('</svg>')
    
    return '\n'.join(svg_parts)


def generate_language_stats_svg(lang_stats, use_3d=True, use_graphical_bars=True, theme='light', use_vector_borders=True):
    """
    Main entry point for SVG generation
    
    Args:
        lang_stats: List of tuples [(language_name, percentage), ...]
        use_3d: If True, use 3D box (currently always 3D in SVG mode)
        use_graphical_bars: If True, use graphical rectangles for bars; if False, use text characters
        theme: 'light' or 'dark'
        use_vector_borders: If True, use SVG paths/lines for borders; if False, use text characters
        
    Returns:
        SVG string
        
    Note:
        use_vector_borders=True provides the best alignment and customization.
        Set to False to use text-based Unicode box-drawing characters.
        The use_3d parameter is currently always enabled in SVG mode.
    """
    # Note: use_3d is kept for API compatibility but always uses 3D in SVG mode
    _ = use_3d
    
    # Use vector borders for perfect alignment (recommended)
    if use_vector_borders and use_graphical_bars:
        return generate_svg_with_vector_borders(lang_stats, theme)
    
    # Fallback to text-based rendering
    if use_graphical_bars:
        return generate_svg_with_bars(lang_stats, theme)
    else:
        # Format with text-based bars
        from .formatter import format_content_lines
        content_lines = format_content_lines(lang_stats)
        return generate_svg_3d_box(content_lines, theme)

