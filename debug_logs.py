
import os
import asyncio
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime
import json

# Load env variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials not found in .env")
    exit(1)

async def check_logs():
    print(f"Connecting to Supabase at {SUPABASE_URL}...")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        # 1. Fetch recent logs
        print("\n--- Recent Logs (Last 50) ---")
        try:
            response = supabase.table('bot_logs')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(50)\
                .execute()

            logs = response.data
            if not logs:
                print("No logs found.")
            else:
                for log in logs:
                    timestamp = log.get('created_at', 'N/A')
                    level = log.get('level', 'INFO')
                    message = log.get('message', '')
                    symbol = log.get('symbol', 'Global')
                    print(f"[{timestamp}] [{level}] [{symbol}] {message}")
        except Exception as e:
            print(f"Error fetching logs: {e}")

        # 2. Fetch active coins
        print("\n--- Active Coins Configuration ---")
        try:
            response = supabase.table('coins_config')\
                .select('*')\
                .eq('is_active', True)\
                .execute()

            coins = response.data
            if not coins:
                print("No active coins found.")
            else:
                print(f"Found {len(coins)} active coins:")
                for coin in coins:
                    print(f"- {coin.get('symbol')}: Leverage={coin.get('leverage')}x, Allocation={coin.get('allocation_percentage')}%")
        except Exception as e:
            print(f"Error fetching coins config: {e}")

        # 3. Fetch recent trades
        print("\n--- Recent Trades (Last 10) ---")
        try:
            response = supabase.table('trades_history')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(10)\
                .execute()

            trades = response.data
            if not trades:
                print("No recent trades found.")
            else:
                for trade in trades:
                    print(f"[{trade.get('created_at')}] {trade.get('symbol')} {trade.get('side')} - Status: {trade.get('status')} - PnL: {trade.get('pnl')}")
        except Exception as e:
            print(f"Error fetching trades: {e}")

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(check_logs())
