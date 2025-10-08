"""
HTML conversion utilities for GitHub README
"""


def convert_to_html(lines):
    """
    Convert box drawing to HTML with proper spacing
    
    Args:
        lines: List of box drawing strings
        
    Returns:
        HTML string wrapped in <div> and <samp> tags
    """
    html_lines = []
    for line in lines:
        # Replace spaces with &nbsp; to preserve alignment in HTML
        html_line = line.replace(' ', '&nbsp;')
        html_lines.append(html_line)
    
    # Wrap in centered div with samp tag
    stats_html = '<br>\n'.join(html_lines)
    return f'<div align="center">\n<samp>\n{stats_html}\n</samp>\n</div>'
