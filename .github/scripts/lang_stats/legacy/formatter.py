"""
Content formatting for language statistics
"""

from .config import LANG_NAME_WIDTH, PROGRESS_BAR_BLOCKS, FILLED_BLOCK, EMPTY_BLOCK


def generate_progress_bar(percentage, total_blocks=PROGRESS_BAR_BLOCKS):
    """
    Generate filled and empty blocks based on percentage
    
    Args:
        percentage: Percentage value (0-100)
        total_blocks: Total number of blocks in the bar
        
    Returns:
        String of filled and empty block characters
    """
    filled_blocks = round((percentage / 100) * total_blocks)
    empty_blocks = total_blocks - filled_blocks
    return FILLED_BLOCK * filled_blocks + EMPTY_BLOCK * empty_blocks


def format_content_lines(lang_stats):
    """
    Format language statistics into content lines
    
    Args:
        lang_stats: List of tuples [(language_name, percentage), ...]
        
    Returns:
        List of formatted content strings
    """
    content_lines = []
    for lang_name, percentage in lang_stats:
        # Pad language name to fixed width
        lang_display = lang_name.ljust(LANG_NAME_WIDTH)
        
        # Generate progress bar
        bar_string = generate_progress_bar(percentage)
        
        # Format percentage with padding
        percent_str = f'{percentage:5.1f} %'
        
        # Combine: "TypeScript    ████████████░░░░░░░░░░░░░  29.5 %"
        line = f'{lang_display} {bar_string}  {percent_str}'
        content_lines.append(line)
    
    return content_lines
