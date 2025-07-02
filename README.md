# Stock Analysis

# Setup

1. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ALPHAVANTAGE_API_KEY=your_api_key_here
   ```

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python stock_analyzer.py
   ```

API : https://www.alphavantage.co/documentation/
https://www.alphavantage.co/documentation/#balance-sheet


# Activate your virtual environment first
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Uninstall and reinstall pandas and numpy
pip uninstall pandas numpy -y
pip install pandas numpy

# If you still have issues, try installing specific compatible versions
pip install numpy==1.24.3 pandas==2.0.3