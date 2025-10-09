"""
Progress bar rendering utilities
"""

from typing import Tuple


class ProgressBarRenderer:
    """
    Renders progress bars in various formats.
    """
    
    def __init__(self, total_blocks: int = 25, filled_char: str = '█', empty_char: str = '░'):
        """
        Initialize progress bar renderer.
        
        Args:
            total_blocks: Total number of blocks in bar
            filled_char: Character for filled portion
            empty_char: Character for empty portion
        """
        self.total_blocks = total_blocks
        self.filled_char = filled_char
        self.empty_char = empty_char
    
    def render_text(self, percentage: float) -> str:
        """
        Render text-based progress bar.
        
        Args:
            percentage: Progress percentage (0-100)
            
        Returns:
            Progress bar string
        """
        filled_blocks = round((percentage / 100) * self.total_blocks)
        empty_blocks = self.total_blocks - filled_blocks
        return self.filled_char * filled_blocks + self.empty_char * empty_blocks
    
    def render_svg_rects(self, percentage: float, x: float, y: float,
                        total_width: float, height: float,
                        filled_color: str, empty_color: str) -> Tuple[str, str]:
        """
        Render SVG rectangles for progress bar.
        
        Args:
            percentage: Progress percentage (0-100)
            x, y: Starting position
            total_width: Total bar width
            height: Bar height
            filled_color: Color for filled portion
            empty_color: Color/pattern for empty portion
            
        Returns:
            Tuple of (filled_rect, empty_rect) SVG strings
        """
        filled_width = (percentage / 100) * total_width
        empty_width = total_width - filled_width
        
        filled_rect = ''
        empty_rect = ''
        
        if filled_width > 0:
            filled_rect = f'<rect x="{x}" y="{y}" width="{filled_width}" height="{height}" fill="{filled_color}" />'
        
        if empty_width > 0:
            empty_rect = f'<rect x="{x + filled_width}" y="{y}" width="{empty_width}" height="{height}" fill="{empty_color}" />'
        
        return filled_rect, empty_rect

