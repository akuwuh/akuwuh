"""
Style 2: Connected extrusion with visible 3D faces
"""

from typing import List
from .base import ExtrusionStyle


class ConnectedExtrusion(ExtrusionStyle):
    """
    Style 2: Connected extrusion with diagonal lines.
    
    Shows the right and bottom faces connecting the front to back,
    with diagonal lines creating a true 3D perspective effect.
    """
    
    def render_front_face(self, x: float, y: float, width: float, height: float, color: str) -> str:
        """Render the front face rectangle."""
        return f'''<rect x="{x}" y="{y}" width="{width}" height="{height}" 
        fill="none" stroke="{color}" stroke-width="{self.stroke_width}" 
        rx="{self.corner_radius}" />'''
    
    def render_extrusion(self, x: float, y: float, width: float, height: float,
                        extrude_x: float, extrude_y: float, color: str) -> List[str]:
        """
        Render the connected extrusion with visible faces and diagonal lines.
        
        Creates:
        - Right face (side panel)
        - Bottom face (bottom panel)
        - Three diagonal connection lines
        """
        elements = []
        
        # Right face (extrusion) - closed path
        right_face = f'''<path d="M {x + width} {y} 
            L {x + width + extrude_x} {y + extrude_y}
            L {x + width + extrude_x} {y + height + extrude_y}
            L {x + width} {y + height} Z"
            fill="none" stroke="{color}" stroke-width="{self.stroke_width}" />'''
        elements.append(right_face)
        
        # Bottom face (extrusion) - closed path
        bottom_face = f'''<path d="M {x} {y + height}
            L {x + extrude_x} {y + height + extrude_y}
            L {x + width + extrude_x} {y + height + extrude_y}
            L {x + width} {y + height} Z"
            fill="none" stroke="{color}" stroke-width="{self.stroke_width}" />'''
        elements.append(bottom_face)
        
        # Diagonal connecting lines
        elements.extend(self._render_diagonal_connections(x, y, width, height, extrude_x, extrude_y, color))
        
        return elements
    
    def _render_diagonal_connections(self, x: float, y: float, width: float, height: float,
                                    extrude_x: float, extrude_y: float, color: str) -> List[str]:
        """
        Render the three diagonal lines connecting front to back.
        
        Returns:
            List of line elements
        """
        diagonals = []
        
        # Top-right corner to back
        top_right = f'''<line x1="{x + width}" y1="{y}" 
            x2="{x + width + extrude_x}" y2="{y + extrude_y}"
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        diagonals.append(top_right)
        
        # Bottom-left corner to back
        bottom_left = f'''<line x1="{x}" y1="{y + height}" 
            x2="{x + extrude_x}" y2="{y + height + extrude_y}"
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        diagonals.append(bottom_left)
        
        # Bottom-right corner to back (completes the connection)
        bottom_right = f'''<line x1="{x + width}" y1="{y + height}" 
            x2="{x + width + extrude_x}" y2="{y + height + extrude_y}"
            stroke="{color}" stroke-width="{self.stroke_width}" />'''
        diagonals.append(bottom_right)
        
        return diagonals

