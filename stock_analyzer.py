import os
from dotenv import load_dotenv
from openai import OpenAI
import json
from typing import Dict, Any, Optional
from alpha_vantage.fundamentaldata import FundamentalData
import warnings

# Suppress SSL warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

class StockAnalyzer:
    """
    Class for analyzing stock financial data using OpenAI and Alpha Vantage APIs
    """
    def __init__(self):
        """Initialize the stock analyzer with API clients"""
        load_dotenv()
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.alpha_vantage_client = FundamentalData(
            key=os.getenv('ALPHAVANTAGE_API_KEY'), 
            output_format='pandas'
        )
        
    @staticmethod
    def _to_float(value: str) -> float:
        """
        Convert string to float safely
        Args:
            value: String value to convert
        Returns:
            float: Converted value or 0.0 if conversion fails
        """
        try:
            return float(value)
        except (ValueError, TypeError):
            return 0.0

    def get_balance_sheet(self, stock_symbol: str) -> Optional[Dict[str, Any]]:
        """
        Get balance sheet data for a stock symbol
        Args:
            stock_symbol: Stock symbol to query
        Returns:
            Dict containing balance sheet data or None if not found
        """
        try:
            data, _ = self.alpha_vantage_client.get_balance_sheet_quarterly(symbol=stock_symbol)
            if data is None or data.empty:
                return None
                
            first_row = data.iloc[0]
            balance_sheet = {
                'report_date': first_row['fiscalDateEnding'],
                'total_assets': self._to_float(first_row['totalAssets']),
                'current_assets': self._to_float(first_row['totalCurrentAssets']),
                'total_liabilities': self._to_float(first_row['totalLiabilities']),
                'current_liabilities': self._to_float(first_row['totalCurrentLiabilities']),
                'total_shareholder_equity': self._to_float(first_row['totalShareholderEquity']),
                'retained_earnings': self._to_float(first_row['retainedEarnings'])
            }

            # Add additional financial metrics if available
            additional_metrics = ['totalRevenue', 'grossProfit', 'operatingIncome', 'netIncome']
            for metric in additional_metrics:
                if metric in first_row:
                    balance_sheet[metric] = self._to_float(first_row[metric])

            return balance_sheet
            
        except Exception as e:
            print(f"Error getting balance sheet data: {str(e)}")
            return None

    def analyze_financial_health(self, balance_sheet: Dict[str, Any]) -> str:
        """
        Analyze financial health using OpenAI
        Args:
            balance_sheet: Dictionary containing balance sheet data
        Returns:
            str: Analysis from OpenAI
        """
        try:
            prompt = (
                "Eres un experto en análisis financiero. Analiza la salud financiera de la empresa "
                "con los siguientes datos: {data}. Calcula los ratios de liquidez (current ratio, "
                "cash ratio) y solvencia (debt-equity ratio). Proporciona una interpretación "
                "de los valores y una conclusión general sobre la salud financiera."
            ).format(data=json.dumps(balance_sheet, indent=2))

            completion = self.openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "Eres un experto en análisis financiero"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.2,
                top_p=0.2,
                n=1,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None,
            )

            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error getting financial analysis: {str(e)}")
            return "No se pudo obtener el análisis financiero"

def format_balance_sheet(balance_sheet: Dict[str, Any]) -> str:
    """
    Format balance sheet data for display
    Args:
        balance_sheet: Dictionary containing balance sheet data
    Returns:
        str: Formatted string representation
    """
    if not balance_sheet:
        return "No data available"

    additional_metrics = ['totalRevenue', 'grossProfit', 'operatingIncome', 'netIncome']
    
    formatted = [
        f"\nMost Recent Balance Sheet Data (as of {balance_sheet['report_date']}):",
        f"Total Assets: ${balance_sheet['total_assets']:,.2f}",
        f"Current Assets: ${balance_sheet['current_assets']:,.2f}",
        f"Total Liabilities: ${balance_sheet['total_liabilities']:,.2f}",
        f"Current Liabilities: ${balance_sheet['current_liabilities']:,.2f}",
        f"Total Shareholder Equity: ${balance_sheet['total_shareholder_equity']:,.2f}",
        f"Retained Earnings: ${balance_sheet['retained_earnings']:,.2f}"
    ]

    # Add additional metrics if available
    for metric in additional_metrics:
        if metric in balance_sheet:
            formatted.append(f"{metric.replace('_', ' ').title()}: ${balance_sheet[metric]:,.2f}")

    return "\n".join(formatted)

def main():
    """Main function to run the stock analyzer"""
    print("Stock Analyzer using OpenAI")
    print("==========================")

    # Get stock symbol from user
    stock_symbol = input("Enter the stock symbol (e.g., AAPL, MSFT): ").upper()

    # Initialize analyzer
    analyzer = StockAnalyzer()
    
    # Get balance sheet data
    balance_sheet = analyzer.get_balance_sheet(stock_symbol)
    
    # Display results
    print("\nStock Information:")
    print("-----------------")
    
    if balance_sheet:
        # Print JSON data
        print("\nBalance Sheet JSON:")
        print(json.dumps(balance_sheet, indent=4))
        
        # Print formatted data
        print("\nFormatted Data:")
        print(format_balance_sheet(balance_sheet))
        
        # Get and print financial analysis
        analysis = analyzer.analyze_financial_health(balance_sheet)
        print("\nFinancial Analysis:")
        print("-" * 20)
        print(analysis)
    else:
        print("No data available for this stock symbol")

if __name__ == "__main__":
    main()
