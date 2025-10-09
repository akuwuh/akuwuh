"""
Application service layer
"""

from typing import Optional
from ..domain import StatsCollection
from ..infrastructure import GitHubClient
from ..rendering.svg import SVGRenderer
from ..rendering.text import TextRenderer
from .config import RenderConfig


class LanguageStatsService:
    """
    Application service for generating language statistics.
    
    Coordinates between infrastructure, domain, and presentation layers.
    """
    
    def __init__(self, github_token: Optional[str] = None, username: Optional[str] = None):
        """
        Initialize service.
        
        Args:
            github_token: GitHub API token
            username: Default GitHub username
        """
        self.github_client = GitHubClient(token=github_token, username=username)
    
    def generate_svg(self, username: Optional[str] = None,
                    config: Optional[RenderConfig] = None) -> str:
        """
        Generate SVG visualization of language statistics.
        
        Args:
            username: GitHub username (uses default if not provided)
            config: Render configuration (uses default if not provided)
            
        Returns:
            SVG string
        """
        if config is None:
            config = RenderConfig.default_light()
        
        stats = self.github_client.fetch_language_stats(username)
        renderer = SVGRenderer(config)
        return renderer.render(stats)
    
    def generate_text(self, username: Optional[str] = None) -> list[str]:
        """
        Generate text-based visualization.
        
        Args:
            username: GitHub username
            
        Returns:
            List of formatted text lines
        """
        stats = self.github_client.fetch_language_stats(username)
        renderer = TextRenderer()
        return renderer.render(stats)
    
    def get_stats(self, username: Optional[str] = None) -> StatsCollection:
        """
        Get raw statistics collection.
        
        Args:
            username: GitHub username
            
        Returns:
            StatsCollection
        """
        return self.github_client.fetch_language_stats(username)
    
    def close(self):
        """Close resources"""
        self.github_client.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

