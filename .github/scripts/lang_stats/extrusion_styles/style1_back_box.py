"""
Style 1: Back box extrusion (no diagonal connections)
"""

from typing import List
from .base import ExtrusionStyle


class BackBoxExtrusion(ExtrusionStyle):
    """
    Style 1: Back box extrusion.
    
    Creates the appearance of a box behind the main box without
    diagonal connection lines. This gives a clean, layered look.
    """
    
    def render_front_face(self, x: float, y: float, width: float, height: float, color: str) -> str:
        """Render the front face rectangle."""
        return f'''<rect x="{x}" y="{y}" width="{width}" height="{height}" 
        fill="none" stroke="{color}" stroke-width="{self.stroke_width}" 
        rx="{self.corner_radius}" />'''
    
    def render_extrusion(self, x: float, y: float, width: float, height: float,
                        extrude_x: float, extrude_y: float, color: str) -> List[str]:
        """
        Render the back box.
        
        Simply draws another rectangle offset by the extrusion depth,
        creating the illusion of a box behind the front box.
        """
        back_box = f'''<rect x="{x + extrude_x}" y="{y + extrude_y}" width="{width}" height="{height}" 
            fill="none" stroke="{color}" stroke-width="{self.stroke_width}" 
            rx="{self.corner_radius}" />'''
        return [back_box]

