#!/usr/bin/env python3
"""
Example script demonstrating the Stock Portfolio Tracker API.

This shows how to use the classes programmatically without the CLI.
"""

from stock import Stock
from transaction import Transaction, TransactionType
from portfolio import Portfolio
from data_store import DataStore


def example_usage():
    """Demonstrate how to use the portfolio tracker programmatically."""
    
    print("Stock Portfolio Tracker - Example Usage\n")
    print("="*60)
    
    # Create a new portfolio
    portfolio = Portfolio("Investment Portfolio")
    print(f"Created portfolio: {portfolio.name}\n")
    
    # Add stocks
    apple = Stock("AAPL", "Apple Inc.")
    microsoft = Stock("MSFT", "Microsoft Corporation")
    google = Stock("GOOGL", "Alphabet Inc.")
    
    portfolio.add_stock(apple)
    portfolio.add_stock(microsoft)
    portfolio.add_stock(google)
    print("Added stocks: AAPL, MSFT, GOOGL\n")
    
    # Add buy transactions
    print("Adding buy transactions...")
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 50, 150.00))
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 25, 155.00))
    portfolio.add_transaction(Transaction("MSFT", TransactionType.BUY, 30, 350.00))
    portfolio.add_transaction(Transaction("GOOGL", TransactionType.BUY, 10, 2800.00))
    print("✓ Added 4 buy transactions\n")
    
    # Add dividend income
    print("Adding dividend income...")
    portfolio.add_transaction(Transaction("AAPL", TransactionType.DIVIDEND, 1, 37.50))
    portfolio.add_transaction(Transaction("MSFT", TransactionType.DIVIDEND, 1, 21.00))
    print("✓ Added dividend transactions\n")
    
    # Add sell transaction
    print("Adding sell transaction...")
    portfolio.add_transaction(Transaction("AAPL", TransactionType.SELL, 25, 165.00))
    print("✓ Sold 25 shares of AAPL\n")
    
    # Display holdings
    print("="*60)
    print("CURRENT HOLDINGS")
    print("="*60)
    holdings = portfolio.get_holdings()
    for ticker, holding in sorted(holdings.items()):
        print(f"  {holding}")
    print()
    
    # Display portfolio summary
    print("="*60)
    print("PORTFOLIO SUMMARY")
    print("="*60)
    summary = portfolio.get_portfolio_summary()
    print(f"  Total Holdings: {summary['total_holdings']} stocks")
    print(f"  Total Transactions: {summary['total_transactions']}")
    print(f"  Total Cost Basis: ${summary['total_cost_basis']:,.2f}")
    print(f"  Realized Gains: ${summary['realized_gains']:,.2f}")
    print(f"  Dividend Income: ${summary['dividend_income']:,.2f}")
    
    total_return = summary['realized_gains'] + summary['dividend_income']
    print(f"  Total Return: ${total_return:,.2f}")
    
    if summary['total_cost_basis'] > 0:
        return_pct = (total_return / summary['total_cost_basis']) * 100
        print(f"  Return %: {return_pct:.2f}%")
    print()
    
    # Save portfolio to disk
    print("="*60)
    print("SAVING PORTFOLIO")
    print("="*60)
    store = DataStore("data")
    store.save_portfolio(portfolio)
    print("✓ Portfolio saved to data/portfolio.json\n")
    
    # Load portfolio from disk
    print("="*60)
    print("LOADING PORTFOLIO")
    print("="*60)
    loaded_portfolio = store.load_portfolio()
    if loaded_portfolio:
        print(f"✓ Loaded portfolio: {loaded_portfolio.name}")
        print(f"  Transactions: {len(loaded_portfolio.transactions)}")
        print(f"  Holdings: {len(loaded_portfolio.get_holdings())}")
    print()
    
    # Display transactions for specific ticker
    print("="*60)
    print("TRANSACTIONS FOR AAPL")
    print("="*60)
    aapl_transactions = portfolio.get_transactions_by_ticker("AAPL")
    for i, transaction in enumerate(aapl_transactions, 1):
        print(f"  {i}. {transaction}")
    print()
    
    print("="*60)
    print("EXAMPLE COMPLETE")
    print("="*60)


if __name__ == "__main__":
    example_usage()
