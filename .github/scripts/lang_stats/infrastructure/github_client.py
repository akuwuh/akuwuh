"""
GitHub API client for fetching language statistics
"""

import requests
from typing import Dict, List, Optional
from ..domain import LanguageStat, StatsCollection


class GitHubAPIError(Exception):
    """Raised when GitHub API request fails"""
    pass


class GitHubClient:
    """
    Client for interacting with GitHub API.
    
    Handles authentication, rate limiting, and data fetching.
    """
    
    API_BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        """
        Initialize GitHub client.
        
        Args:
            token: GitHub personal access token (optional but recommended)
            username: GitHub username for fetching user repos
        """
        self.token = token
        self.username = username
        self._session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Create configured requests session"""
        session = requests.Session()
        session.headers.update({
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'Lang-Stats-Generator'
        })
        if self.token:
            session.headers['Authorization'] = f'token {self.token}'
        return session
    
    def fetch_language_stats(self, username: Optional[str] = None) -> StatsCollection:
        """
        Fetch language statistics for a GitHub user.
        
        Args:
            username: GitHub username (uses self.username if not provided)
            
        Returns:
            StatsCollection with language statistics
            
        Raises:
            GitHubAPIError: If API request fails
            ValueError: If no username provided
        """
        username = username or self.username
        if not username:
            raise ValueError("Username must be provided")
        
        repos = self._fetch_user_repos(username)
        language_bytes = self._aggregate_language_bytes(repos)
        stats = self._calculate_percentages(language_bytes)
        
        return StatsCollection(stats)
    
    def _fetch_user_repos(self, username: str) -> List[Dict]:
        """
        Fetch all repositories for a user.
        
        Args:
            username: GitHub username
            
        Returns:
            List of repository data dictionaries
            
        Raises:
            GitHubAPIError: If request fails
        """
        url = f"{self.API_BASE_URL}/users/{username}/repos"
        params = {'per_page': 100, 'type': 'owner'}
        
        try:
            response = self._session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise GitHubAPIError(f"Failed to fetch repos for {username}: {e}")
    
    def _aggregate_language_bytes(self, repos: List[Dict]) -> Dict[str, int]:
        """
        Aggregate language bytes across all repositories.
        
        Args:
            repos: List of repository data
            
        Returns:
            Dictionary mapping language names to total bytes
        """
        language_totals = {}
        
        for repo in repos:
            if repo.get('fork'):
                continue  # Skip forked repos
            
            languages_url = repo.get('languages_url')
            if not languages_url:
                continue
            
            try:
                response = self._session.get(languages_url)
                response.raise_for_status()
                languages = response.json()
                
                for lang, bytes_count in languages.items():
                    language_totals[lang] = language_totals.get(lang, 0) + bytes_count
            except requests.RequestException:
                continue  # Skip repos with errors
        
        return language_totals
    
    def _calculate_percentages(self, language_bytes: Dict[str, int]) -> List[LanguageStat]:
        """
        Calculate percentages from byte counts.
        
        Args:
            language_bytes: Dictionary of language bytes
            
        Returns:
            List of LanguageStat objects
            
        Raises:
            ValueError: If no languages found
        """
        if not language_bytes:
            raise ValueError("No language data found")
        
        total_bytes = sum(language_bytes.values())
        stats = []
        
        for lang, bytes_count in language_bytes.items():
            percentage = (bytes_count / total_bytes) * 100
            stats.append(LanguageStat(name=lang, percentage=percentage, bytes=bytes_count))
        
        return stats
    
    def close(self):
        """Close the session"""
        self._session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

