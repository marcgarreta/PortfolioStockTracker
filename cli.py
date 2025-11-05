"""Command-line interface for the stock portfolio tracker."""

import sys
from datetime import datetime
from typing import Optional, Any
from stock import Stock
from transaction import Transaction, TransactionType
from portfolio import Portfolio
from data_store import DataStore


class PortfolioCLI:
    """Command-line interface for managing a stock portfolio."""
    
    def __init__(self):
        """Initialize the CLI."""
        self.data_store = DataStore()
        self.portfolio = self._load_or_create_portfolio()
    
    def _load_or_create_portfolio(self) -> Portfolio:
        """Load existing portfolio or create a new one."""
        portfolio = self.data_store.load_portfolio()
        if portfolio:
            print(f"Loaded portfolio: {portfolio.name}")
            return portfolio
        else:
            print("Creating new portfolio...")
            return Portfolio("My Portfolio")
    
    def _save_portfolio(self) -> None:
        """Save the current portfolio."""
        self.data_store.save_portfolio(self.portfolio)
        print("Portfolio saved.")
    
    def display_menu(self) -> None:
        """Display the main menu."""
        print("\n" + "="*60)
        print("STOCK PORTFOLIO TRACKER")
        print("="*60)
        print("1. Add Buy Transaction")
        print("2. Add Sell Transaction")
        print("3. Add Dividend Income")
        print("4. View Portfolio Summary")
        print("5. View Holdings")
        print("6. View All Transactions")
        print("7. View Transactions by Ticker")
        print("8. Exit")
        print("="*60)
    
    def get_user_input(self, prompt: str, input_type=str, allow_empty=False) -> Optional[Any]:
        """
        Get validated user input.
        
        Args:
            prompt: Prompt to display
            input_type: Expected type (str, float, int)
            allow_empty: Whether to allow empty input
        
        Returns:
            Validated input or None
        """
        while True:
            try:
                value = input(prompt).strip()
                if not value and allow_empty:
                    return None
                if not value:
                    print("Input cannot be empty. Please try again.")
                    continue
                
                if input_type == float:
                    return float(value)
                elif input_type == int:
                    return int(value)
                else:
                    return value
            except ValueError:
                print(f"Invalid input. Expected {input_type.__name__}. Please try again.")
    
    def add_buy_transaction(self) -> None:
        """Add a buy transaction."""
        print("\n--- Add Buy Transaction ---")
        ticker = self.get_user_input("Enter stock ticker (e.g., AAPL): ", str)
        quantity = self.get_user_input("Enter quantity: ", float)
        price = self.get_user_input("Enter price per share: ", float)
        
        if quantity <= 0 or price <= 0:
            print("Error: Quantity and price must be positive.")
            return
        
        # Optional: add stock name
        stock_name = self.get_user_input(
            "Enter company name (optional, press Enter to skip): ",
            str,
            allow_empty=True
        )
        
        # Add stock if new
        if ticker.upper() not in self.portfolio.stocks:
            stock = Stock(ticker, stock_name or ticker)
            self.portfolio.add_stock(stock)
        
        transaction = Transaction(ticker, TransactionType.BUY, quantity, price)
        self.portfolio.add_transaction(transaction)
        
        print(f"\n✓ Buy transaction added: {transaction}")
        self._save_portfolio()
    
    def add_sell_transaction(self) -> None:
        """Add a sell transaction."""
        print("\n--- Add Sell Transaction ---")
        ticker = self.get_user_input("Enter stock ticker: ", str)
        
        # Check if user has holdings
        holdings = self.portfolio.get_holdings()
        if ticker.upper() not in holdings:
            print(f"Error: You don't have any holdings of {ticker.upper()}.")
            return
        
        current_holding = holdings[ticker.upper()]
        print(f"Current holdings: {current_holding}")
        
        quantity = self.get_user_input("Enter quantity to sell: ", float)
        price = self.get_user_input("Enter sale price per share: ", float)
        
        if quantity <= 0 or price <= 0:
            print("Error: Quantity and price must be positive.")
            return
        
        if quantity > current_holding.quantity:
            print(f"Error: Cannot sell {quantity} shares. You only have {current_holding.quantity} shares.")
            return
        
        transaction = Transaction(ticker, TransactionType.SELL, quantity, price)
        self.portfolio.add_transaction(transaction)
        
        print(f"\n✓ Sell transaction added: {transaction}")
        self._save_portfolio()
    
    def add_dividend_income(self) -> None:
        """Add dividend income."""
        print("\n--- Add Dividend Income ---")
        ticker = self.get_user_input("Enter stock ticker: ", str)
        amount = self.get_user_input("Enter dividend amount (total): ", float)
        
        if amount <= 0:
            print("Error: Dividend amount must be positive.")
            return
        
        # For dividends, we use quantity=1 and price=amount for simplicity
        transaction = Transaction(ticker, TransactionType.DIVIDEND, 1, amount)
        self.portfolio.add_transaction(transaction)
        
        print(f"\n✓ Dividend income added: ${amount:.2f} from {ticker.upper()}")
        self._save_portfolio()
    
    def view_portfolio_summary(self) -> None:
        """Display portfolio summary."""
        print("\n" + "="*60)
        print("PORTFOLIO SUMMARY")
        print("="*60)
        
        summary = self.portfolio.get_portfolio_summary()
        holdings = self.portfolio.get_holdings()
        
        print(f"Portfolio Name: {summary['name']}")
        print(f"Total Holdings: {summary['total_holdings']} stocks")
        print(f"Total Transactions: {summary['total_transactions']}")
        print(f"\nTotal Cost Basis: ${summary['total_cost_basis']:.2f}")
        print(f"Realized Gains/Losses: ${summary['realized_gains']:.2f}")
        print(f"Dividend Income: ${summary['dividend_income']:.2f}")
        
        # Calculate total return
        total_return = summary['realized_gains'] + summary['dividend_income']
        print(f"\nTotal Return: ${total_return:.2f}")
        
        if summary['total_cost_basis'] > 0:
            return_pct = (total_return / summary['total_cost_basis']) * 100
            print(f"Return %: {return_pct:.2f}%")
        
        print("="*60)
    
    def view_holdings(self) -> None:
        """Display current holdings."""
        print("\n" + "="*60)
        print("CURRENT HOLDINGS")
        print("="*60)
        
        holdings = self.portfolio.get_holdings()
        
        if not holdings:
            print("No current holdings.")
            return
        
        print(f"{'Ticker':<10} {'Shares':<12} {'Avg Cost':<12} {'Total Cost':<15}")
        print("-" * 60)
        
        for ticker, holding in sorted(holdings.items()):
            print(
                f"{holding.ticker:<10} "
                f"{holding.quantity:<12.4f} "
                f"${holding.average_cost:<11.2f} "
                f"${holding.total_cost:<14.2f}"
            )
        
        total_cost = sum(h.total_cost for h in holdings.values())
        print("-" * 60)
        print(f"{'TOTAL':<10} {'':<12} {'':<12} ${total_cost:<14.2f}")
        print("="*60)
    
    def view_all_transactions(self) -> None:
        """Display all transactions."""
        print("\n" + "="*60)
        print("ALL TRANSACTIONS")
        print("="*60)
        
        if not self.portfolio.transactions:
            print("No transactions recorded.")
            return
        
        for i, transaction in enumerate(self.portfolio.transactions, 1):
            print(f"{i}. {transaction}")
        
        print("="*60)
    
    def view_transactions_by_ticker(self) -> None:
        """Display transactions for a specific ticker."""
        ticker = self.get_user_input("\nEnter stock ticker: ", str)
        
        transactions = self.portfolio.get_transactions_by_ticker(ticker)
        
        print("\n" + "="*60)
        print(f"TRANSACTIONS FOR {ticker.upper()}")
        print("="*60)
        
        if not transactions:
            print(f"No transactions found for {ticker.upper()}.")
            return
        
        for i, transaction in enumerate(transactions, 1):
            print(f"{i}. {transaction}")
        
        print("="*60)
    
    def run(self) -> None:
        """Run the main CLI loop."""
        print("\nWelcome to Stock Portfolio Tracker!")
        
        while True:
            self.display_menu()
            choice = self.get_user_input("Enter your choice (1-8): ", str)
            
            if choice == '1':
                self.add_buy_transaction()
            elif choice == '2':
                self.add_sell_transaction()
            elif choice == '3':
                self.add_dividend_income()
            elif choice == '4':
                self.view_portfolio_summary()
            elif choice == '5':
                self.view_holdings()
            elif choice == '6':
                self.view_all_transactions()
            elif choice == '7':
                self.view_transactions_by_ticker()
            elif choice == '8':
                print("\nThank you for using Stock Portfolio Tracker!")
                self._save_portfolio()
                sys.exit(0)
            else:
                print("Invalid choice. Please enter a number between 1 and 8.")


def main():
    """Main entry point for the CLI."""
    try:
        cli = PortfolioCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nExiting... Portfolio saved.")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
