"""
SVG pattern generators
"""


class CheckeredPatternGenerator:
    """
    Generates checkered pattern for SVG.
    """
    
    def __init__(self, bar_height: int = 12, num_squares: int = 6):
        """
        Initialize pattern generator.
        
        Args:
            bar_height: Height of the bar in pixels
            num_squares: Number of squares vertically
        """
        self.bar_height = bar_height
        self.num_squares = num_squares
        self.pattern_size = (bar_height / num_squares) * 2  # 2 squares per pattern
        self.square_size = self.pattern_size / 2
    
    def generate(self, pattern_id: str, fill_color: str) -> str:
        """
        Generate SVG pattern definition.
        
        Args:
            pattern_id: Unique ID for the pattern
            fill_color: Color for filled squares
            
        Returns:
            SVG pattern definition string
        """
        return f'''<pattern id="{pattern_id}" x="0" y="0" width="{self.pattern_size}" height="{self.pattern_size}" patternUnits="userSpaceOnUse">
      <rect width="{self.square_size}" height="{self.square_size}" x="0" y="0" fill="none" />
      <rect width="{self.square_size}" height="{self.square_size}" x="{self.square_size}" y="0" fill="{fill_color}" />
      <rect width="{self.square_size}" height="{self.square_size}" x="0" y="{self.square_size}" fill="{fill_color}" />
      <rect width="{self.square_size}" height="{self.square_size}" x="{self.square_size}" y="{self.square_size}" fill="none" />
    </pattern>'''

