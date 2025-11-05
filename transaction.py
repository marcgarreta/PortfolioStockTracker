"""Transaction class to represent buy/sell trades."""

from datetime import datetime
from enum import Enum
from typing import Optional


class TransactionType(Enum):
    """Enumeration for transaction types."""
    BUY = "BUY"
    SELL = "SELL"
    DIVIDEND = "DIVIDEND"


class Transaction:
    """Represents a single transaction (buy, sell, or dividend)."""
    
    def __init__(
        self,
        ticker: str,
        transaction_type: TransactionType,
        quantity: float,
        price: float,
        date: Optional[datetime] = None,
        transaction_id: Optional[str] = None
    ):
        """
        Initialize a Transaction.
        
        Args:
            ticker: Stock ticker symbol
            transaction_type: Type of transaction (BUY, SELL, DIVIDEND)
            quantity: Number of shares
            price: Price per share
            date: Transaction date (defaults to now)
            transaction_id: Unique transaction ID (auto-generated if not provided)
        """
        self.ticker = ticker.upper()
        self.transaction_type = transaction_type
        self.quantity = float(quantity)
        self.price = float(price)
        self.date = date or datetime.now()
        self.transaction_id = transaction_id or self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate a unique transaction ID."""
        return f"{self.ticker}_{self.date.strftime('%Y%m%d%H%M%S%f')}"
    
    @property
    def total_value(self) -> float:
        """Calculate total value of transaction."""
        return self.quantity * self.price
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary for serialization."""
        return {
            'transaction_id': self.transaction_id,
            'ticker': self.ticker,
            'transaction_type': self.transaction_type.value,
            'quantity': self.quantity,
            'price': self.price,
            'date': self.date.isoformat(),
            'total_value': self.total_value
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Transaction':
        """Create Transaction from dictionary."""
        return cls(
            ticker=data['ticker'],
            transaction_type=TransactionType(data['transaction_type']),
            quantity=data['quantity'],
            price=data['price'],
            date=datetime.fromisoformat(data['date']),
            transaction_id=data.get('transaction_id')
        )
    
    def __str__(self) -> str:
        return (
            f"{self.transaction_type.value} {self.quantity} shares of {self.ticker} "
            f"@ ${self.price:.2f} on {self.date.strftime('%Y-%m-%d')} "
            f"(Total: ${self.total_value:.2f})"
        )
    
    def __repr__(self) -> str:
        return (
            f"Transaction(ticker='{self.ticker}', "
            f"type={self.transaction_type.value}, "
            f"quantity={self.quantity}, price={self.price})"
        )
