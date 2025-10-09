"""
Configuration management
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class ThemeColors:
    """Color scheme for a theme"""
    text: str
    border: str
    bg: str
    filled_bar: str
    empty_bar: str
    
    @staticmethod
    def light() -> 'ThemeColors':
        """Get light theme colors"""
        return ThemeColors(
            text='#000000',
            border='#000000',
            bg='transparent',
            filled_bar='#000000',
            empty_bar='#d0d7de'
        )
    
    @staticmethod
    def dark() -> 'ThemeColors':
        """Get dark theme colors"""
        return ThemeColors(
            text='#FFFFFF',
            border='#FFFFFF',
            bg='transparent',
            filled_bar='#FFFFFF',
            empty_bar='#d0d7de'
        )
    
    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary"""
        return {
            'text': self.text,
            'border': self.border,
            'bg': self.bg,
            'filled_bar': self.filled_bar,
            'empty_bar': self.empty_bar
        }


@dataclass
class RenderConfig:
    """
    Configuration for rendering language statistics.
    
    Centralizes all rendering parameters in one place.
    """
    
    # Typography
    font_family: str = "'Courier New', Courier, monospace"
    font_size: int = 16
    char_width: float = 9.6
    char_height: int = 20
    line_spacing: int = 4
    
    # Layout
    lang_name_width: int = 15
    progress_bar_blocks: int = 25
    left_padding: int = 1
    right_padding: int = 1
    
    # 3D Box
    box_padding_x: int = 20
    box_padding_y: int = 15
    extrusion_depth_x: int = 15
    extrusion_depth_y: int = 15
    extrusion_style: int = 1  # 1 = back box, 2 = connected
    stroke_width: int = 2
    corner_radius: int = 0
    
    # Progress Bar
    bar_height: int = 12
    filled_char: str = '█'
    empty_char: str = '░'
    
    # Theme
    theme: str = 'light'
    
    @property
    def colors(self) -> Dict[str, str]:
        """Get colors for current theme"""
        if self.theme == 'dark':
            return ThemeColors.dark().to_dict()
        return ThemeColors.light().to_dict()
    
    @classmethod
    def default_light(cls) -> 'RenderConfig':
        """Get default light theme configuration"""
        return cls(theme='light')
    
    @classmethod
    def default_dark(cls) -> 'RenderConfig':
        """Get default dark theme configuration"""
        return cls(theme='dark')
    
    @classmethod
    def custom(cls, **kwargs) -> 'RenderConfig':
        """Create custom configuration"""
        return cls(**kwargs)

