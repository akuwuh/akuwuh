"""
Text-based rendering
"""

from typing import List
from ..domain import StatsCollection
from ..utils import pad_text


class TextRenderer:
    """
    Renders language statistics as text-based output.
    """
    
    def __init__(self, lang_name_width: int = 15, progress_bar_blocks: int = 25):
        """
        Initialize text renderer.
        
        Args:
            lang_name_width: Width for language name column
            progress_bar_blocks: Number of blocks in progress bar
        """
        self.lang_name_width = lang_name_width
        self.progress_bar_blocks = progress_bar_blocks
    
    def render(self, stats: StatsCollection) -> List[str]:
        """
        Render statistics as list of text lines.
        
        Args:
            stats: Language statistics collection
            
        Returns:
            List of formatted text lines
        """
        lines = []
        
        for stat in stats:
            lang_display = pad_text(stat.name, self.lang_name_width, align='left')
            
            filled_blocks = round((stat.percentage / 100) * self.progress_bar_blocks)
            empty_blocks = self.progress_bar_blocks - filled_blocks
            progress_bar = '█' * filled_blocks + '░' * empty_blocks
            
            percent_str = f'{stat.percentage:5.1f} %'
            
            line = f'{lang_display}  {progress_bar}  {percent_str}'
            lines.append(line)
        
        return lines

