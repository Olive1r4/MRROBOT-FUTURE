
import os
import asyncio
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime

# Load env variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("Error: Supabase credentials not found in .env")
    exit(1)

async def check_mrrobot_status():
    print(f"Connecting to Supabase at {SUPABASE_URL}...")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        # 1. Check Circuit Breaker Logs
        print("\n--- Circuit Breaker / Critical Logs (Last 20) ---")
        try:
            # Look for recent errors or circuit breaker mentions
            response = supabase.table('logs_mrrobot')\
                .select('*')\
                .order('created_at', desc=True)\
                .limit(20)\
                .execute()

            logs = response.data
            if not logs:
                print("No logs found.")
            else:
                for log in logs:
                    msg = log.get('message', '')
                    level = log.get('level', 'INFO')
                    # Highlight circuit breaker or critical
                    if 'circuit' in msg.lower() or 'breaker' in msg.lower() or level in ['CRITICAL', 'ERROR']:
                        print(f"⚠️  [{log.get('created_at')}] [{level}] {msg}")
                    else:
                        print(f"[{log.get('created_at')}] [{level}] {msg}")
        except Exception as e:
            print(f"Error fetching logs: {e}")

        # 2. Check Daily Stats for PnL
        print("\n--- Daily Stats (Today) ---")
        try:
            # Just get the most recent daily stat
            response = supabase.table('daily_stats_mrrobot')\
                .select('*')\
                .order('date', desc=True)\
                .limit(1)\
                .execute()

            stats = response.data
            if stats:
                stat = stats[0]
                print(f"Date: {stat.get('date')}")
                print(f"Total PnL: {stat.get('total_pnl')}")
                print(f"Trade Count: {stat.get('trade_count')}")
                print(f"Win Rate: {stat.get('win_rate')}%")
                print(f"Max Drawdown: {stat.get('max_drawdown')}")
                print(f"Status: {stat.get('status', 'Unknown')}")
            else:
                print("No daily stats found.")
        except Exception as e:
            print(f"Error fetching daily stats: {e}")

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(check_mrrobot_status())
