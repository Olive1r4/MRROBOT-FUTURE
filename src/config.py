import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # System
    TRADING_MODE = os.getenv('TRADING_MODE', 'PAPER').upper()
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    # Binance
    BINANCE_API_KEY = os.getenv('BINANCE_API_KEY')
    BINANCE_SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

    # Supabase
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')

    # Strategy
    SYMBOL = os.getenv('SYMBOL', 'BTC/USDT')
    TIMEFRAME = os.getenv('TIMEFRAME', '4h')
    LEVERAGE = int(os.getenv('LEVERAGE', 5))
    INITIAL_PAPER_BALANCE = float(os.getenv('INITIAL_PAPER_BALANCE', 90.0))

    @staticmethod
    def validate():
        if Config.TRADING_MODE == 'LIVE':
            if not Config.BINANCE_API_KEY or not Config.BINANCE_SECRET_KEY:
                raise ValueError("Binance API credentials are required for LIVE mode.")

        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            raise ValueError("Supabase credentials are required.")

Config.validate()
