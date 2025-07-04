# Stock Analysis

A Python application that analyzes stock financial data using OpenAI and Alpha Vantage APIs. The application fetches balance sheet data, calculates financial ratios, and provides AI-powered financial analysis.

## Features

- **Balance Sheet Data Retrieval**: Fetches quarterly balance sheet data from Alpha Vantage
- **Financial Ratio Calculations**: Computes key financial ratios (current ratio, cash ratio, debt-to-equity ratio)
- **AI-Powered Analysis**: Uses OpenAI GPT-4 to provide comprehensive financial health analysis
- **Interactive Interface**: Command-line interface for easy stock symbol input
- **Multilingual Support**: Analysis provided in Spanish

## Code Structure

### StockAnalyzer Class
The main class that handles all stock analysis operations:

- **`__init__()`**: Initializes OpenAI and Alpha Vantage API clients
- **`get_balance_sheet(stock_symbol)`**: Retrieves and processes balance sheet data
- **`analyze_financial_health(balance_sheet, ratios)`**: Generates AI-powered financial analysis
- **`_to_float(value)`**: Safely converts string values to float

### Key Functions

- **`format_balance_sheet(balance_sheet)`**: Formats balance sheet data for display
- **`calculate_ratios(balance_sheet)`**: Calculates financial ratios:
  - Current Ratio (current assets / current liabilities)
  - Cash Ratio (cash equivalents / current liabilities)
  - Debt Index (total liabilities / shareholder equity)
  - Debt-to-Equity Ratio (debt / shareholder equity)
- **`main()`**: Main execution function with interactive interface

### Data Points Analyzed

The application extracts and analyzes:
- Total Assets and Current Assets
- Total Liabilities and Current Liabilities
- Shareholder Equity and Retained Earnings
- Cash and Cash Equivalents
- Short/Long-term Debt
- Revenue, Gross Profit, Operating Income, Net Income (when available)

## Setup

1. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_api_key_here
   ALPHAVANTAGE_API_KEY=your_api_key_here
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python stock_analyzer.py
   ```

## Usage

1. Run the application
2. Enter a stock symbol (e.g., AAPL, MSFT, GOOGL)
3. The application will:
   - Fetch the latest balance sheet data
   - Calculate financial ratios
   - Display raw and formatted financial data
   - Provide AI-powered financial analysis in Spanish

## Output

The application provides:
- JSON formatted balance sheet data
- Formatted financial statements
- Calculated financial ratios
- Comprehensive financial health analysis with insights on solvency and liquidity

## Dependencies

- `openai`: OpenAI API client for GPT-4 analysis
- `alpha_vantage`: Alpha Vantage API client for stock data
- `pandas`: Data manipulation and analysis
- `python-dotenv`: Environment variable management
- `httpx`: HTTP client for API requests
- `numpy`: Numerical computing support

## API References

- Alpha Vantage API: https://www.alphavantage.co/documentation/
- Balance Sheet Documentation: https://www.alphavantage.co/documentation/#balance-sheet
