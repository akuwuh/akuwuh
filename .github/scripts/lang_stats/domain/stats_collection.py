"""
Domain model for a collection of language statistics
"""

from typing import List, Iterator
from .language_stat import LanguageStat


class StatsCollection:
    """
    Domain aggregate for managing a collection of language statistics.
    
    Enforces business rules and provides domain operations.
    """
    
    def __init__(self, stats: List[LanguageStat]):
        """
        Initialize with a list of language statistics.
        
        Args:
            stats: List of LanguageStat objects
            
        Raises:
            ValueError: If stats is empty or percentages don't sum to ~100
        """
        if not stats:
            raise ValueError("Stats collection cannot be empty")
        
        self._stats = sorted(stats, key=lambda s: s.percentage, reverse=True)
        self._validate_percentages()
    
    def _validate_percentages(self):
        """Validate that percentages sum to approximately 100%"""
        total = sum(stat.percentage for stat in self._stats)
        if not (99.0 <= total <= 101.0):  # Allow for rounding
            raise ValueError(f"Percentages must sum to ~100%, got {total:.2f}%")
    
    @property
    def stats(self) -> List[LanguageStat]:
        """Get immutable copy of statistics"""
        return list(self._stats)
    
    @property
    def top_language(self) -> LanguageStat:
        """Get the most used language"""
        return self._stats[0]
    
    @property
    def count(self) -> int:
        """Get number of languages"""
        return len(self._stats)
    
    def get_top_n(self, n: int) -> List[LanguageStat]:
        """
        Get top N languages by usage.
        
        Args:
            n: Number of languages to return
            
        Returns:
            List of top N LanguageStat objects
        """
        return self._stats[:n]
    
    def filter_by_threshold(self, min_percentage: float) -> 'StatsCollection':
        """
        Get new collection with languages above threshold.
        
        Args:
            min_percentage: Minimum percentage to include
            
        Returns:
            New StatsCollection with filtered stats
        """
        filtered = [s for s in self._stats if s.percentage >= min_percentage]
        if not filtered:
            raise ValueError(f"No languages above {min_percentage}% threshold")
        return StatsCollection(filtered)
    
    def to_tuples(self) -> List[tuple]:
        """
        Convert to list of (name, percentage) tuples for backward compatibility.
        
        Returns:
            List of (language_name, percentage) tuples
        """
        return [(stat.name, stat.percentage) for stat in self._stats]
    
    def __iter__(self) -> Iterator[LanguageStat]:
        """Make collection iterable"""
        return iter(self._stats)
    
    def __len__(self) -> int:
        """Get collection length"""
        return len(self._stats)
    
    def __getitem__(self, index: int) -> LanguageStat:
        """Get stat by index"""
        return self._stats[index]
    
    def __str__(self) -> str:
        return f"StatsCollection({self.count} languages)"
    
    def __repr__(self) -> str:
        return f"StatsCollection({self._stats})"

