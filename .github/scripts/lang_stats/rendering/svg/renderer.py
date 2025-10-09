"""
Main SVG renderer orchestrator
"""

from typing import List
from ...domain import StatsCollection
from ...core.config import RenderConfig
from ...extrusion_styles import ExtrusionStyleFactory
from ...utils import escape_xml
from .patterns import CheckeredPatternGenerator
from ..progress_bar import ProgressBarRenderer


class SVGRenderer:
    """
    Main SVG rendering orchestrator.
    
    Coordinates the rendering of language statistics as SVG.
    """
    
    def __init__(self, config: RenderConfig):
        """
        Initialize SVG renderer.
        
        Args:
            config: Render configuration
        """
        self.config = config
        self.pattern_gen = CheckeredPatternGenerator(
            bar_height=config.bar_height,
            num_squares=6
        )
        self.progress_renderer = ProgressBarRenderer()
    
    def render(self, stats: StatsCollection) -> str:
        """
        Render complete SVG from statistics.
        
        Args:
            stats: Language statistics collection
            
        Returns:
            Complete SVG string
        """
        # Calculate dimensions
        dimensions = self._calculate_dimensions(stats)
        
        # Build SVG parts
        svg_parts = []
        svg_parts.append(self._render_svg_header(dimensions))
        svg_parts.append(self._render_defs())
        svg_parts.append(self._render_box_borders(dimensions))
        svg_parts.append(self._render_content(dimensions))
        svg_parts.append('</svg>')
        
        return '\n'.join(svg_parts)
    
    def _calculate_dimensions(self, stats: StatsCollection) -> dict:
        """Calculate SVG dimensions"""
        max_text_width = 0
        content_data = []
        
        for stat in stats:
            line_text = self._format_line(stat.name, stat.percentage)
            text_width = len(line_text) * self.config.char_width
            max_text_width = max(max_text_width, text_width)
            
            content_data.append({
                'lang_name': stat.name,
                'percentage': stat.percentage,
                'filled_blocks': round((stat.percentage / 100) * self.config.progress_bar_blocks)
            })
        
        box_width = max_text_width + (self.config.box_padding_x * 2)
        box_height = len(stats) * (self.config.char_height + self.config.line_spacing) + (self.config.box_padding_y * 2)
        
        svg_width = box_width + self.config.extrusion_depth_x + 40
        svg_height = box_height + self.config.extrusion_depth_y + 40
        
        return {
            'svg_width': svg_width,
            'svg_height': svg_height,
            'box_width': box_width,
            'box_height': box_height,
            'box_x': 20,
            'box_y': 20,
            'content_data': content_data
        }
    
    def _format_line(self, lang_name: str, percentage: float) -> str:
        """Format a single language line"""
        lang_display = lang_name.ljust(self.config.lang_name_width)
        percent_str = f'{percentage:5.1f} %'
        return f'{lang_display}  {" " * self.config.progress_bar_blocks}  {percent_str}'
    
    def _render_svg_header(self, dims: dict) -> str:
        """Render SVG opening tag"""
        return f'<svg width="{dims["svg_width"]}" height="{dims["svg_height"]}" xmlns="http://www.w3.org/2000/svg">'
    
    def _render_defs(self) -> str:
        """Render SVG definitions (patterns, styles)"""
        parts = ['  <defs>']
        parts.append('    <!-- Checkered pattern for empty bar (░ effect) -->')
        
        pattern_id = f'checkered-pattern-{self.config.theme}'
        pattern = self.pattern_gen.generate(pattern_id, self.config.colors['text'])
        parts.append(f'    {pattern}')
        
        parts.append('    <style>')
        parts.append(f'      .lang-text {{ font-family: {self.config.font_family}; font-size: {self.config.font_size}px; fill: {self.config.colors["text"]}; }}')
        parts.append(f'      .bar-filled {{ fill: {self.config.colors["filled_bar"]}; }}')
        parts.append(f'      .bar-empty {{ fill: url(#{pattern_id}); }}')
        parts.append('    </style>')
        parts.append('  </defs>')
        parts.append('')
        
        return '\n'.join(parts)
    
    def _render_box_borders(self, dims: dict) -> str:
        """Render 3D box borders"""
        parts = ['  <!-- 3D Box Borders -->', '  <g id="box-borders">']
        
        extrusion_style = ExtrusionStyleFactory.create(
            self.config.extrusion_style,
            self.config.stroke_width,
            self.config.corner_radius
        )
        
        border_elements = extrusion_style.render(
            dims['box_x'], dims['box_y'],
            dims['box_width'], dims['box_height'],
            self.config.extrusion_depth_x, self.config.extrusion_depth_y,
            self.config.colors['border']
        )
        
        for element in border_elements:
            parts.append(f'    {element}')
        
        parts.append('  </g>')
        parts.append('')
        
        return '\n'.join(parts)
    
    def _render_content(self, dims: dict) -> str:
        """Render statistics content"""
        parts = ['  <!-- Language Statistics -->', '  <g id="content">']
        
        y_pos = dims['box_y'] + self.config.box_padding_y + self.config.char_height
        bar_x_offset = self.config.box_padding_x + (self.config.lang_name_width + 2) * self.config.char_width
        
        for data in dims['content_data']:
            # Language name
            lang_text = data['lang_name'].ljust(self.config.lang_name_width)
            parts.append(f'    <text x="{dims["box_x"] + self.config.box_padding_x}" y="{y_pos}" class="lang-text">{escape_xml(lang_text)}</text>')
            
            # Progress bar
            bar_y = y_pos - self.config.char_height + 6
            bar_width = self.config.progress_bar_blocks * self.config.char_width * 0.95
            
            filled_width = data['filled_blocks'] * self.config.char_width * 0.95
            empty_width = bar_width - filled_width
            
            if filled_width > 0:
                parts.append(f'    <rect x="{dims["box_x"] + bar_x_offset}" y="{bar_y}" width="{filled_width}" height="{self.config.bar_height}" class="bar-filled" />')
            
            if empty_width > 0:
                parts.append(f'    <rect x="{dims["box_x"] + bar_x_offset + filled_width}" y="{bar_y}" width="{empty_width}" height="{self.config.bar_height}" class="bar-empty" />')
            
            # Percentage
            percent_str = f'{data["percentage"]:5.1f} %'
            percent_x = dims["box_x"] + bar_x_offset + bar_width + (2 * self.config.char_width)
            parts.append(f'    <text x="{percent_x}" y="{y_pos}" class="lang-text">{percent_str}</text>')
            
            y_pos += self.config.char_height + self.config.line_spacing
        
        parts.append('  </g>')
        
        return '\n'.join(parts)

