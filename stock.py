"""Stock class to represent individual stock information."""

from typing import Optional


class Stock:
    """Represents a stock with ticker and basic information."""
    
    def __init__(self, ticker: str, name: str = ""):
        """
        Initialize a Stock.
        
        Args:
            ticker: Stock ticker symbol (e.g., 'AAPL')
            name: Company name (optional)
        """
        self.ticker = ticker.upper()
        self.name = name or ticker
    
    def to_dict(self) -> dict:
        """Convert stock to dictionary for serialization."""
        return {
            'ticker': self.ticker,
            'name': self.name
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Stock':
        """Create Stock from dictionary."""
        return cls(
            ticker=data['ticker'],
            name=data.get('name', '')
        )
    
    def __str__(self) -> str:
        return f"{self.ticker} - {self.name}"
    
    def __repr__(self) -> str:
        return f"Stock(ticker='{self.ticker}', name='{self.name}')"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Stock):
            return False
        return self.ticker == other.ticker
    
    def __hash__(self) -> int:
        return hash(self.ticker)
