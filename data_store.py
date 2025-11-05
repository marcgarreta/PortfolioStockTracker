"""Data storage module for persisting portfolio data."""

import json
import os
from pathlib import Path
from typing import Optional
from portfolio import Portfolio


class DataStore:
    """Handles saving and loading portfolio data to/from local storage."""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize DataStore.
        
        Args:
            data_dir: Directory to store data files
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.portfolio_file = self.data_dir / "portfolio.json"
    
    def save_portfolio(self, portfolio: Portfolio) -> None:
        """
        Save portfolio to local storage.
        
        Args:
            portfolio: Portfolio to save
        """
        data = portfolio.to_dict()
        with open(self.portfolio_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_portfolio(self) -> Optional[Portfolio]:
        """
        Load portfolio from local storage.
        
        Returns:
            Portfolio if exists, None otherwise
        """
        if not self.portfolio_file.exists():
            return None
        
        try:
            with open(self.portfolio_file, 'r') as f:
                data = json.load(f)
            return Portfolio.from_dict(data)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error loading portfolio: {e}")
            return None
    
    def portfolio_exists(self) -> bool:
        """
        Check if portfolio data exists.
        
        Returns:
            True if portfolio file exists, False otherwise
        """
        return self.portfolio_file.exists()
    
    def clear_portfolio(self) -> None:
        """Delete the portfolio data file."""
        if self.portfolio_file.exists():
            self.portfolio_file.unlink()
