"""
GitHub API data fetcher for language statistics
"""

import requests
from collections import defaultdict
from .config import MAX_LANGUAGES


def fetch_language_stats(username, token):
    """
    Fetch language statistics from GitHub API
    
    Args:
        username: GitHub username
        token: GitHub API token
        
    Returns:
        List of tuples: [(language_name, percentage), ...]
        Sorted by percentage descending
    """
    headers = {'Authorization': f'token {token}'}
    
    # Get all repos
    repos_url = f'https://api.github.com/users/{username}/repos?per_page=100'
    repos = requests.get(repos_url, headers=headers).json()
    
    # Aggregate language bytes across all repos
    lang_bytes = defaultdict(int)
    
    for repo in repos:
        if isinstance(repo, dict) and not repo.get('fork', False):
            lang_url = repo.get('languages_url')
            if lang_url:
                languages = requests.get(lang_url, headers=headers).json()
                if isinstance(languages, dict):
                    for lang, bytes_count in languages.items():
                        lang_bytes[lang] += bytes_count
    
    # Calculate percentages
    total_bytes = sum(lang_bytes.values())
    if total_bytes == 0:
        return []
    
    lang_stats = []
    for lang, bytes_count in lang_bytes.items():
        percentage = (bytes_count / total_bytes) * 100
        lang_stats.append((lang, percentage))
    
    # Sort by percentage descending
    lang_stats.sort(key=lambda x: x[1], reverse=True)
    
    return lang_stats[:MAX_LANGUAGES]
