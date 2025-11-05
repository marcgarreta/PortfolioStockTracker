"""Portfolio class to manage holdings and calculations."""

from collections import defaultdict
from typing import Dict, List, Optional, Tuple
from transaction import Transaction, TransactionType
from stock import Stock


class Holding:
    """Represents current holdings of a stock."""
    
    def __init__(self, ticker: str, quantity: float, average_cost: float):
        """
        Initialize a Holding.
        
        Args:
            ticker: Stock ticker symbol
            quantity: Number of shares held
            average_cost: Average cost per share
        """
        self.ticker = ticker.upper()
        self.quantity = quantity
        self.average_cost = average_cost
    
    @property
    def total_cost(self) -> float:
        """Calculate total cost basis."""
        return self.quantity * self.average_cost
    
    def to_dict(self) -> dict:
        """Convert holding to dictionary."""
        return {
            'ticker': self.ticker,
            'quantity': self.quantity,
            'average_cost': self.average_cost,
            'total_cost': self.total_cost
        }
    
    def __str__(self) -> str:
        return (
            f"{self.ticker}: {self.quantity} shares @ ${self.average_cost:.2f} "
            f"(Total Cost: ${self.total_cost:.2f})"
        )


class Portfolio:
    """Manages a stock portfolio with transactions and holdings."""
    
    def __init__(self, name: str = "My Portfolio"):
        """
        Initialize a Portfolio.
        
        Args:
            name: Portfolio name
        """
        self.name = name
        self.transactions: List[Transaction] = []
        self.stocks: Dict[str, Stock] = {}
    
    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add a transaction to the portfolio.
        
        Args:
            transaction: Transaction to add
        """
        self.transactions.append(transaction)
        
        # Add stock if not already present
        if transaction.ticker not in self.stocks:
            self.stocks[transaction.ticker] = Stock(transaction.ticker)
    
    def add_stock(self, stock: Stock) -> None:
        """
        Add a stock to the portfolio.
        
        Args:
            stock: Stock to add
        """
        self.stocks[stock.ticker] = stock
    
    def get_holdings(self) -> Dict[str, Holding]:
        """
        Calculate current holdings from transactions.
        
        Returns:
            Dictionary mapping ticker to Holding object
        """
        holdings_data = defaultdict(lambda: {'quantity': 0.0, 'total_cost': 0.0})
        
        for transaction in self.transactions:
            if transaction.transaction_type == TransactionType.BUY:
                holdings_data[transaction.ticker]['quantity'] += transaction.quantity
                holdings_data[transaction.ticker]['total_cost'] += transaction.total_value
            elif transaction.transaction_type == TransactionType.SELL:
                # Calculate average cost before the sale
                current_qty = holdings_data[transaction.ticker]['quantity']
                if current_qty > 0:
                    avg_cost = holdings_data[transaction.ticker]['total_cost'] / current_qty
                    # Reduce cost basis proportionally
                    holdings_data[transaction.ticker]['total_cost'] -= (avg_cost * transaction.quantity)
                holdings_data[transaction.ticker]['quantity'] -= transaction.quantity
        
        # Convert to Holding objects
        holdings = {}
        for ticker, data in holdings_data.items():
            if data['quantity'] > 0:  # Only include if we have shares
                average_cost = data['total_cost'] / data['quantity'] if data['quantity'] > 0 else 0
                holdings[ticker] = Holding(ticker, data['quantity'], average_cost)
        
        return holdings
    
    def get_realized_gains(self) -> float:
        """
        Calculate realized gains/losses from sell transactions.
        
        Returns:
            Total realized gains (negative for losses)
        """
        realized_gains = 0.0
        holdings_tracker = defaultdict(lambda: {'quantity': 0.0, 'total_cost': 0.0})
        
        for transaction in self.transactions:
            ticker = transaction.ticker
            
            if transaction.transaction_type == TransactionType.BUY:
                holdings_tracker[ticker]['quantity'] += transaction.quantity
                holdings_tracker[ticker]['total_cost'] += transaction.total_value
            elif transaction.transaction_type == TransactionType.SELL:
                # Calculate average cost at time of sale
                if holdings_tracker[ticker]['quantity'] > 0:
                    avg_cost = holdings_tracker[ticker]['total_cost'] / holdings_tracker[ticker]['quantity']
                    cost_basis = avg_cost * transaction.quantity
                    sale_value = transaction.total_value
                    realized_gains += (sale_value - cost_basis)
                    
                    # Update holdings
                    holdings_tracker[ticker]['quantity'] -= transaction.quantity
                    holdings_tracker[ticker]['total_cost'] -= cost_basis
        
        return realized_gains
    
    def get_dividend_income(self) -> float:
        """
        Calculate total dividend income.
        
        Returns:
            Total dividend income
        """
        return sum(
            transaction.total_value
            for transaction in self.transactions
            if transaction.transaction_type == TransactionType.DIVIDEND
        )
    
    def get_transactions_by_ticker(self, ticker: str) -> List[Transaction]:
        """
        Get all transactions for a specific ticker.
        
        Args:
            ticker: Stock ticker symbol
        
        Returns:
            List of transactions for the ticker
        """
        return [t for t in self.transactions if t.ticker == ticker.upper()]
    
    def get_portfolio_summary(self) -> dict:
        """
        Generate a comprehensive portfolio summary.
        
        Returns:
            Dictionary with portfolio summary data
        """
        holdings = self.get_holdings()
        total_cost = sum(h.total_cost for h in holdings.values())
        realized_gains = self.get_realized_gains()
        dividend_income = self.get_dividend_income()
        
        return {
            'name': self.name,
            'total_holdings': len(holdings),
            'total_cost_basis': total_cost,
            'realized_gains': realized_gains,
            'dividend_income': dividend_income,
            'total_transactions': len(self.transactions),
            'holdings': {ticker: holding.to_dict() for ticker, holding in holdings.items()}
        }
    
    def to_dict(self) -> dict:
        """Convert portfolio to dictionary for serialization."""
        return {
            'name': self.name,
            'stocks': {ticker: stock.to_dict() for ticker, stock in self.stocks.items()},
            'transactions': [t.to_dict() for t in self.transactions]
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Portfolio':
        """Create Portfolio from dictionary."""
        portfolio = cls(name=data.get('name', 'My Portfolio'))
        
        # Load stocks
        for ticker, stock_data in data.get('stocks', {}).items():
            portfolio.stocks[ticker] = Stock.from_dict(stock_data)
        
        # Load transactions
        for transaction_data in data.get('transactions', []):
            portfolio.transactions.append(Transaction.from_dict(transaction_data))
        
        return portfolio
    
    def __str__(self) -> str:
        holdings = self.get_holdings()
        return f"Portfolio '{self.name}' with {len(holdings)} holdings and {len(self.transactions)} transactions"
