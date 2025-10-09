"""
Base class for extrusion styles
"""

from abc import ABC, abstractmethod
from typing import List


class ExtrusionStyle(ABC):
    """
    Abstract base class for 3D box extrusion styles.
    
    Each style defines how the 3D effect is rendered by providing
    SVG elements for the front face and extrusion effect.
    """
    
    def __init__(self, stroke_width: float, corner_radius: float = 0):
        """
        Initialize extrusion style with common parameters.
        
        Args:
            stroke_width: Width of border lines
            corner_radius: Radius for rounded corners
        """
        self.stroke_width = stroke_width
        self.corner_radius = corner_radius
    
    @abstractmethod
    def render_front_face(self, x: float, y: float, width: float, height: float, color: str) -> str:
        """
        Render the front face of the box.
        
        Args:
            x, y: Top-left corner position
            width, height: Box dimensions
            color: Border color
            
        Returns:
            SVG element string for the front face
        """
        pass
    
    @abstractmethod
    def render_extrusion(self, x: float, y: float, width: float, height: float, 
                        extrude_x: float, extrude_y: float, color: str) -> List[str]:
        """
        Render the extrusion effect.
        
        Args:
            x, y: Top-left corner of front face
            width, height: Dimensions of front face
            extrude_x, extrude_y: Extrusion depth
            color: Border color
            
        Returns:
            List of SVG element strings for the extrusion
        """
        pass
    
    def render(self, x: float, y: float, width: float, height: float,
               extrude_x: float, extrude_y: float, color: str) -> List[str]:
        """
        Render complete 3D box with front face and extrusion.
        
        Args:
            x, y: Top-left corner of front face
            width, height: Dimensions of front face
            extrude_x, extrude_y: Extrusion depth
            color: Border color
            
        Returns:
            List of all SVG element strings
        """
        elements = []
        elements.append(self.render_front_face(x, y, width, height, color))
        elements.extend(self.render_extrusion(x, y, width, height, extrude_x, extrude_y, color))
        return elements

