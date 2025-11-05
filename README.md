# Stock Portfolio Tracker

A Python application to track your personal stock portfolio. Manage buy/sell transactions, track holdings, calculate gains/losses, and monitor dividend income - all stored locally.

## Features

- **Transaction Management**: Add buy/sell trades with ticker symbol, quantity, and price
- **Portfolio Summary**: View comprehensive portfolio statistics including cost basis, realized gains, and dividend income
- **Holdings View**: See current stock holdings with quantities, average costs, and total values
- **Gains/Losses Tracking**: Automatically calculate realized gains/losses from sell transactions
- **Dividend Income Tracking**: Record and track dividend payments
- **Local Storage**: All data stored locally in JSON format (no external database required)
- **Command-Line Interface**: Easy-to-use interactive CLI
- **Object-Oriented Design**: Clean code organization with classes for Stocks, Transactions, and Portfolio

## Installation

### Prerequisites

- Python 3.7 or higher

### Setup

1. Clone the repository:
```bash
git clone https://github.com/marcgarreta/PortfolioStockTracker.git
cd PortfolioStockTracker
```

2. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. No external dependencies required! The application uses only Python standard library.

## Usage

### Running the Application

Start the CLI application:
```bash
python main.py
```

Or run the CLI directly:
```bash
python cli.py
```

### Main Menu Options

When you start the application, you'll see the main menu:

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
```

### Adding Transactions

#### Buy Transaction (Option 1)
- Enter stock ticker (e.g., AAPL, GOOGL, MSFT)
- Enter quantity of shares
- Enter price per share
- Optionally enter company name

Example:
```
Enter stock ticker: AAPL
Enter quantity: 10
Enter price per share: 150.50
Enter company name (optional): Apple Inc.
```

#### Sell Transaction (Option 2)
- Enter stock ticker
- The system will show your current holdings
- Enter quantity to sell
- Enter sale price per share
- System validates you have sufficient shares

#### Dividend Income (Option 3)
- Enter stock ticker
- Enter total dividend amount received

### Viewing Portfolio Information

#### Portfolio Summary (Option 4)
Displays comprehensive portfolio statistics:
- Total number of holdings
- Total cost basis
- Realized gains/losses
- Total dividend income
- Overall return percentage

#### Holdings (Option 5)
Shows current stock holdings:
- Ticker symbol
- Number of shares
- Average cost per share
- Total cost basis

#### All Transactions (Option 6)
Lists all transactions chronologically with details

#### Transactions by Ticker (Option 7)
Filter and view transactions for a specific stock

## Code Architecture

The application is organized into several modules:

### Core Classes

- **`stock.py`**: `Stock` class representing individual stocks
- **`transaction.py`**: `Transaction` class for buy/sell/dividend transactions
- **`portfolio.py`**: `Portfolio` class managing holdings and calculations
- **`data_store.py`**: `DataStore` class handling local data persistence
- **`cli.py`**: `PortfolioCLI` class providing the command-line interface
- **`main.py`**: Entry point for the application

### Data Storage

- Portfolio data is stored in `data/portfolio.json`
- JSON format for easy readability and portability
- Automatic saving after each transaction

## Example Workflow

1. **Start the application**: `python main.py`
2. **Add a buy transaction**: Buy 10 shares of AAPL at $150
3. **Add more positions**: Buy shares of other stocks
4. **Record dividends**: Add dividend income when received
5. **Sell shares**: Sell some shares when desired
6. **View summary**: Check your portfolio performance
7. **View holdings**: See all current positions

## Data Format

Portfolio data is stored as JSON with the following structure:

```json
{
  "name": "My Portfolio",
  "stocks": {
    "AAPL": {
      "ticker": "AAPL",
      "name": "Apple Inc."
    }
  },
  "transactions": [
    {
      "transaction_id": "AAPL_20231105120000000000",
      "ticker": "AAPL",
      "transaction_type": "BUY",
      "quantity": 10.0,
      "price": 150.50,
      "date": "2023-11-05T12:00:00",
      "total_value": 1505.00
    }
  ]
}
```

## Features in Detail

### Automatic Calculations

- **Average Cost**: Automatically calculates average cost basis for holdings
- **Realized Gains**: Tracks profit/loss when you sell shares
- **Cost Basis Tracking**: Maintains accurate cost basis even after partial sells
- **Return Percentage**: Calculates overall portfolio return

### Transaction Types

- **BUY**: Purchase of shares
- **SELL**: Sale of shares (with gain/loss calculation)
- **DIVIDEND**: Dividend income received

### Input Validation

- Ensures positive quantities and prices
- Validates sufficient shares for sell transactions
- Prevents invalid transaction types
- Handles empty or malformed input gracefully

## Limitations & Future Enhancements

Current limitations:
- No real-time price fetching (manual price entry)
- No current market value calculation
- No unrealized gains (only realized from sells)
- Simple FIFO cost basis (not tax-lot specific)

Potential future enhancements:
- Integration with financial APIs for real-time prices
- Unrealized gains calculation based on current prices
- Advanced tax reporting features
- Import/export functionality (CSV)
- Web-based UI
- Multi-portfolio support
- Performance charts and visualizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

**Happy Investing! 📈💰**