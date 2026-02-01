import asyncio
from src.database import Database
from src.config import Config

async def check_open_trades():
    db = Database()
    client = db.get_client()

    print(f"Checking DB: {Config.SUPABASE_URL}")
    print(f"Mode: {Config.TRADING_MODE}")

    # 1. Check ALL OPEN trades regardless of mode
    res = client.table('trades').select('*').eq('status', 'OPEN').execute()
    print(f"\n--- ALL OPEN TRADES IN DB ({len(res.data)}) ---")
    for t in res.data:
        print(f"ID: {t['id']} | Symbol: {t['symbol']} | Side: {t['side']} | Mode: {t['mode']} | Entry: {t['entry_time']}")

    # 2. Check specifically for LIVE OPEN trades (what the bot sees)
    res_live = client.table('trades').select('*').eq('status', 'OPEN').eq('mode', Config.TRADING_MODE).execute()
    print(f"\n--- TRADES VISIBLE TO BOT (Mode={Config.TRADING_MODE}) ({len(res_live.data)}) ---")
    for t in res_live.data:
        print(f"ID: {t['id']} | Symbol: {t['symbol']}")

if __name__ == "__main__":
    asyncio.run(check_open_trades())
