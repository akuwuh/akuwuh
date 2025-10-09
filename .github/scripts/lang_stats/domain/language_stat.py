"""
Domain model for a single language statistic
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class LanguageStat:
    """
    Immutable domain entity representing a language statistic.
    
    Attributes:
        name: Programming language name
        percentage: Usage percentage (0-100)
        bytes: Number of bytes in this language
    """
    name: str
    percentage: float
    bytes: int = 0
    
    def __post_init__(self):
        """Validate domain invariants"""
        if not 0 <= self.percentage <= 100:
            raise ValueError(f"Percentage must be between 0 and 100, got {self.percentage}")
        if self.bytes < 0:
            raise ValueError(f"Bytes must be non-negative, got {self.bytes}")
        if not self.name:
            raise ValueError("Language name cannot be empty")
    
    @property
    def display_name(self) -> str:
        """Get formatted display name"""
        return self.name.strip()
    
    def __str__(self) -> str:
        return f"{self.display_name}: {self.percentage:.1f}%"

