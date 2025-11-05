#!/usr/bin/env python3
"""Test script to verify portfolio functionality."""

from datetime import datetime
from stock import Stock
from transaction import Transaction, TransactionType
from portfolio import Portfolio
from data_store import DataStore
import os
import shutil


def test_stock():
    """Test Stock class."""
    print("Testing Stock class...")
    stock = Stock("AAPL", "Apple Inc.")
    assert stock.ticker == "AAPL"
    assert stock.name == "Apple Inc."
    
    # Test serialization
    stock_dict = stock.to_dict()
    stock2 = Stock.from_dict(stock_dict)
    assert stock == stock2
    print("✓ Stock class tests passed")


def test_transaction():
    """Test Transaction class."""
    print("\nTesting Transaction class...")
    
    # Test buy transaction
    buy = Transaction("AAPL", TransactionType.BUY, 10, 150.50)
    assert buy.ticker == "AAPL"
    assert buy.quantity == 10
    assert buy.price == 150.50
    assert buy.total_value == 1505.0
    
    # Test sell transaction
    sell = Transaction("AAPL", TransactionType.SELL, 5, 160.00)
    assert sell.total_value == 800.0
    
    # Test serialization
    trans_dict = buy.to_dict()
    buy2 = Transaction.from_dict(trans_dict)
    assert buy2.ticker == buy.ticker
    assert buy2.quantity == buy.quantity
    
    print("✓ Transaction class tests passed")


def test_portfolio():
    """Test Portfolio class."""
    print("\nTesting Portfolio class...")
    
    portfolio = Portfolio("Test Portfolio")
    
    # Add buy transactions
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 10, 150.00))
    portfolio.add_transaction(Transaction("GOOGL", TransactionType.BUY, 5, 2800.00))
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 5, 155.00))
    
    # Check holdings
    holdings = portfolio.get_holdings()
    assert "AAPL" in holdings
    assert "GOOGL" in holdings
    assert holdings["AAPL"].quantity == 15
    assert holdings["GOOGL"].quantity == 5
    
    # Test average cost calculation
    aapl_holding = holdings["AAPL"]
    expected_avg = (10 * 150.00 + 5 * 155.00) / 15
    assert abs(aapl_holding.average_cost - expected_avg) < 0.01
    
    # Add sell transaction
    portfolio.add_transaction(Transaction("AAPL", TransactionType.SELL, 5, 160.00))
    holdings = portfolio.get_holdings()
    assert holdings["AAPL"].quantity == 10
    
    # Test realized gains
    realized_gains = portfolio.get_realized_gains()
    # Sold 5 shares at 160, avg cost was ~152.33
    assert realized_gains > 0
    
    # Add dividend
    portfolio.add_transaction(Transaction("AAPL", TransactionType.DIVIDEND, 1, 50.00))
    dividend_income = portfolio.get_dividend_income()
    assert dividend_income == 50.00
    
    # Test summary
    summary = portfolio.get_portfolio_summary()
    assert summary['total_holdings'] == 2
    assert summary['dividend_income'] == 50.00
    
    print("✓ Portfolio class tests passed")


def test_data_store():
    """Test DataStore class."""
    print("\nTesting DataStore class...")
    
    # Use a test directory
    test_dir = "/tmp/test_portfolio_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    store = DataStore(test_dir)
    
    # Create and save portfolio
    portfolio = Portfolio("Test Portfolio")
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 10, 150.00))
    portfolio.add_stock(Stock("AAPL", "Apple Inc."))
    
    store.save_portfolio(portfolio)
    assert store.portfolio_exists()
    
    # Load portfolio
    loaded_portfolio = store.load_portfolio()
    assert loaded_portfolio is not None
    assert loaded_portfolio.name == "Test Portfolio"
    assert len(loaded_portfolio.transactions) == 1
    assert loaded_portfolio.transactions[0].ticker == "AAPL"
    
    # Test serialization integrity
    holdings = loaded_portfolio.get_holdings()
    assert "AAPL" in holdings
    assert holdings["AAPL"].quantity == 10
    
    # Cleanup
    shutil.rmtree(test_dir)
    
    print("✓ DataStore class tests passed")


def test_integration():
    """Test full integration scenario."""
    print("\nTesting full integration scenario...")
    
    test_dir = "/tmp/test_portfolio_integration"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    
    store = DataStore(test_dir)
    portfolio = Portfolio("Integration Test")
    
    # Simulate real trading scenario
    # Day 1: Buy AAPL
    portfolio.add_stock(Stock("AAPL", "Apple Inc."))
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 100, 150.00))
    
    # Day 2: Buy more AAPL at different price
    portfolio.add_transaction(Transaction("AAPL", TransactionType.BUY, 50, 155.00))
    
    # Day 3: Buy MSFT
    portfolio.add_stock(Stock("MSFT", "Microsoft"))
    portfolio.add_transaction(Transaction("MSFT", TransactionType.BUY, 30, 350.00))
    
    # Day 4: Receive dividend
    portfolio.add_transaction(Transaction("AAPL", TransactionType.DIVIDEND, 1, 75.00))
    
    # Day 5: Sell some AAPL
    portfolio.add_transaction(Transaction("AAPL", TransactionType.SELL, 50, 160.00))
    
    # Save and reload
    store.save_portfolio(portfolio)
    loaded = store.load_portfolio()
    
    # Verify results
    holdings = loaded.get_holdings()
    assert len(holdings) == 2
    assert holdings["AAPL"].quantity == 100  # 100 + 50 - 50
    assert holdings["MSFT"].quantity == 30
    
    summary = loaded.get_portfolio_summary()
    assert summary['total_holdings'] == 2
    assert summary['dividend_income'] == 75.00
    assert summary['realized_gains'] > 0  # We sold at profit
    
    # Cleanup
    shutil.rmtree(test_dir)
    
    print("✓ Integration tests passed")


def main():
    """Run all tests."""
    print("="*60)
    print("STOCK PORTFOLIO TRACKER - TEST SUITE")
    print("="*60)
    
    try:
        test_stock()
        test_transaction()
        test_portfolio()
        test_data_store()
        test_integration()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        return 0
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(main())
