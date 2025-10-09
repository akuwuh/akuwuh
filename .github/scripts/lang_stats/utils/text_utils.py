"""
Text processing utilities
"""


def escape_xml(text: str) -> str:
    """
    Escape XML/HTML special characters.
    
    Args:
        text: Input text
        
    Returns:
        Escaped text safe for XML/HTML
    """
    return (text
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def calculate_text_width(text: str, char_width: float = 9.6) -> float:
    """
    Calculate approximate pixel width of monospace text.
    
    Args:
        text: Input text
        char_width: Width of a single character in pixels
        
    Returns:
        Approximate width in pixels
    """
    return len(text) * char_width


def truncate_text(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate text to maximum length with suffix.
    
    Args:
        text: Input text
        max_length: Maximum length (including suffix)
        suffix: Suffix to append if truncated
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def pad_text(text: str, width: int, align: str = 'left', fill: str = ' ') -> str:
    """
    Pad text to specified width.
    
    Args:
        text: Input text
        width: Target width
        align: Alignment ('left', 'right', 'center')
        fill: Fill character
        
    Returns:
        Padded text
    """
    if align == 'left':
        return text.ljust(width, fill)
    elif align == 'right':
        return text.rjust(width, fill)
    elif align == 'center':
        return text.center(width, fill)
    else:
        raise ValueError(f"Invalid alignment: {align}")

