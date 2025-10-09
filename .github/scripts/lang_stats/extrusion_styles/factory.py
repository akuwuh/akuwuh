"""
Factory for creating extrusion style instances
"""

from typing import Dict, Type
from .base import ExtrusionStyle
from .style1_back_box import BackBoxExtrusion
from .style2_connected import ConnectedExtrusion


class ExtrusionStyleFactory:
    """
    Factory for creating extrusion style instances.
    
    Provides a centralized way to instantiate extrusion styles by number,
    making it easy to add new styles without modifying existing code.
    """
    
    # Registry of available styles
    _styles: Dict[int, Type[ExtrusionStyle]] = {
        1: BackBoxExtrusion,
        2: ConnectedExtrusion
    }
    
    @classmethod
    def create(cls, style_number: int, stroke_width: float, corner_radius: float = 0) -> ExtrusionStyle:
        """
        Create an extrusion style instance.
        
        Args:
            style_number: Style identifier (1, 2, etc.)
            stroke_width: Width of border lines
            corner_radius: Radius for rounded corners
            
        Returns:
            ExtrusionStyle instance
            
        Raises:
            ValueError: If style_number is not registered
        """
        if style_number not in cls._styles:
            available = ', '.join(str(k) for k in sorted(cls._styles.keys()))
            raise ValueError(f"Unknown extrusion style: {style_number}. Available styles: {available}")
        
        style_class = cls._styles[style_number]
        return style_class(stroke_width, corner_radius)
    
    @classmethod
    def register_style(cls, style_number: int, style_class: Type[ExtrusionStyle]) -> None:
        """
        Register a new extrusion style.
        
        Args:
            style_number: Style identifier
            style_class: ExtrusionStyle subclass
        """
        cls._styles[style_number] = style_class
    
    @classmethod
    def available_styles(cls) -> list:
        """Get list of available style numbers."""
        return sorted(cls._styles.keys())

