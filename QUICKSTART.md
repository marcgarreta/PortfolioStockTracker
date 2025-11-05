# Quick Start Guide

Get started with Stock Portfolio Tracker in 3 easy steps!

## 1. Installation

```bash
# Clone the repository
git clone https://github.com/marcgarreta/PortfolioStockTracker.git
cd PortfolioStockTracker

# No dependencies to install! Uses Python standard library only.
```

## 2. Run the Application

```bash
python main.py
```

## 3. Basic Usage

### Add Your First Stock Purchase

1. Select option `1` (Add Buy Transaction)
2. Enter ticker: `AAPL`
3. Enter quantity: `10`
4. Enter price: `150.00`
5. Enter company name (optional): `Apple Inc.`

### View Your Portfolio

- Option `4`: See portfolio summary with total cost and returns
- Option `5`: View all your current holdings
- Option `6`: See all transactions

### Record a Dividend

1. Select option `3` (Add Dividend Income)
2. Enter ticker: `AAPL`
3. Enter amount: `25.00`

### Sell Shares

1. Select option `2` (Add Sell Transaction)
2. Enter ticker: `AAPL`
3. Enter quantity to sell: `5`
4. Enter sale price: `160.00`

The system automatically calculates your realized gains!

## Example Session

```
============================================================
STOCK PORTFOLIO TRACKER
============================================================
1. Add Buy Transaction
2. Add Sell Transaction
3. Add Dividend Income
4. View Portfolio Summary
5. View Holdings
6. View All Transactions
7. View Transactions by Ticker
8. Exit
============================================================
Enter your choice (1-8): 1

--- Add Buy Transaction ---
Enter stock ticker (e.g., AAPL): AAPL
Enter quantity: 10
Enter price per share: 150.00
Enter company name (optional, press Enter to skip): Apple Inc.

✓ Buy transaction added: BUY 10.0 shares of AAPL @ $150.00
```

## Running Tests

```bash
# Run the comprehensive test suite
python test_portfolio.py

# Run the example script
python example.py
```

## Data Storage

- All portfolio data is saved in `data/portfolio.json`
- Data is automatically saved after each transaction
- Backup this file to preserve your portfolio history

## Tips

- Use descriptive company names for better tracking
- Record dividends when received to track total returns
- View portfolio summary regularly to monitor performance
- Transaction history is permanent - helps with tax reporting

## Need Help?

See the full [README.md](README.md) for detailed documentation.
