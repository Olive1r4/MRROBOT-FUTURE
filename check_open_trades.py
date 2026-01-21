import os
import asyncio
from supabase import create_client

# CREDENCIAIS DA VPS (PRODUÇÃO)
SUPABASE_URL = "https://ogqjsysghltrpcnzroth.supabase.co"
SUPABASE_KEY = "sb_publishable_Vp62RRNKVAF6PkyCaArKPA_lYtJsarm"

async def check_open_trades():
    print(f"Connecting to Supabase {SUPABASE_URL}...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    try:
        response = supabase.table('trades_mrrobot')\
            .select('*')\
            .eq('status', 'open')\
            .execute()

        trades = response.data
        print(f"\n📊 Trades Abertos: {len(trades)}\n")

        for trade in trades:
            print(f"ID: {trade['id']}")
            print(f"Symbol: {trade['symbol']}")
            print(f"Entry Price: ${trade['entry_price']}")
            print(f"Target Price: ${trade.get('target_price', 'N/A')}")
            print(f"Stop Loss: ${trade.get('stop_loss_price', 'N/A')}")
            print(f"Entry Time: {trade.get('entry_time', 'N/A')}")
            print(f"---")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(check_open_trades())
