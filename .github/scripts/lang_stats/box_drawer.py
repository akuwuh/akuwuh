"""
Box drawing utilities for creating bordered content
"""

from .config import (
    LEFT_PADDING,
    RIGHT_PADDING,
    EXTRUSION_INDENT_LEVEL_1,
    EXTRUSION_INDENT_LEVEL_2
)


def draw_simple_border(content_lines):
    """
    Draw a simple box border without extrusion
    
    Args:
        content_lines: List of content strings
        
    Returns:
        List of box drawing strings
    """
    if not content_lines:
        return []
    
    max_content_length = max(len(line) for line in content_lines)
    inner_width = LEFT_PADDING + max_content_length + RIGHT_PADDING
    
    lines = []
    
    # Top border
    lines.append('┌' + '─' * inner_width + '┐')
    
    # Content lines
    for content in content_lines:
        padded = f'{" " * LEFT_PADDING}{content}'.ljust(inner_width)
        lines.append(f'│{padded}│')
    
    # Bottom border
    lines.append('└' + '─' * inner_width + '┘')
    
    return lines


def draw_3d_border(content_lines):
    """
    Draw a 3D box with extrusion effect
    
    Args:
        content_lines: List of content strings
        
    Returns:
        List of box drawing strings with 3D effect
    """
    if not content_lines:
        return []
    
    max_content_length = max(len(line) for line in content_lines)
    inner_width = LEFT_PADDING + max_content_length + RIGHT_PADDING
    
    lines = []
    
    # Top border (no left indent)
    lines.append('┌' + '─' * inner_width + '┐')
    
    # Content lines with right extrusion
    for i, content in enumerate(content_lines):
        # Pad content: LEFT_PADDING spaces + content + fill to inner_width
        padded_content = f'{" " * LEFT_PADDING}{content}'.ljust(inner_width)
        
        # Add left indent and borders
        indent = ' ' * EXTRUSION_INDENT_LEVEL_1
        
        if i == 0:
            # First line: start right extrusion with ├─┐
            lines.append(f'{indent}│{padded_content}├─┐')
        else:
            # Other lines: continue right extrusion with │ │
            lines.append(f'{indent}│{padded_content}│ │')
    
    # Bottom border with 3D effect
    indent_1 = ' ' * EXTRUSION_INDENT_LEVEL_1
    indent_2 = ' ' * EXTRUSION_INDENT_LEVEL_2
    
    # First bottom line: └┬ with (inner_width - 1) dashes + right extrusion
    lines.append(f'{indent_1}└┬' + '─' * (inner_width - 1) + '┘ │')
    
    # Second bottom line: └ with (inner_width + 2) dashes
    lines.append(f'{indent_2}└' + '─' * (inner_width + 2) + '┘')
    
    return lines
