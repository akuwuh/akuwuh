"""
Extrusion styles for 3D box rendering
"""

from .base import ExtrusionStyle
from .style1_back_box import BackBoxExtrusion
from .style2_connected import ConnectedExtrusion
from .factory import ExtrusionStyleFactory

__all__ = [
    'ExtrusionStyle',
    'BackBoxExtrusion',
    'ConnectedExtrusion',
    'ExtrusionStyleFactory'
]

