import asyncio
import ccxt.async_support as ccxt
from src.database import Database
from src.config import Config
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)

async def sync_trades():
    print("🚀 Starting Trades Synchronization...")

    # 1. Connect DB
    db = Database()
    client = db.get_client()

    # 2. Connect Binance
    exchange_config = {
        'apiKey': Config.BINANCE_API_KEY,
        'secret': Config.BINANCE_SECRET_KEY,
        'options': {'defaultType': 'future'}
    }
    binance = ccxt.binance(exchange_config)

    # 3. Fetch DB Trades
    res = client.table('trades').select('*').eq('status', 'OPEN').eq('mode', Config.TRADING_MODE).execute()
    db_trades = res.data
    print(f"📂 Found {len(db_trades)} OPEN trades in DB.")

    # 4. Fetch Binance Positions
    print("📡 Fetching REAL positions from Binance...")
    balance_info = await binance.fetch_balance()
    positions = balance_info['info']['positions']

    # Create simple map: Symbol -> Amount
    real_positions = {}
    for pos in positions:
        amt = float(pos['positionAmt'])
        if amt != 0:
            # Binance uses symbols like 'BTCUSDT', DB uses 'BTC/USDT'
            # Convert DB format (Slash) to Binance format (No Slash) for matching
            symbol_raw = pos['symbol'] # e.g. BTCUSDT
            real_positions[symbol_raw] = amt
            print(f"   ✅ Active on Binance: {symbol_raw} = {amt}")

    # 5. Compare and Fix
    for trade in db_trades:
        db_symbol = trade['symbol'] # BTC/USDT
        binance_symbol = db_symbol.replace('/', '') # BTCUSDT

        trade_id = trade['id']

        if binance_symbol not in real_positions:
            print(f"   ❌ GHOST TRADE DETECTED: {db_symbol} (ID: {trade_id})")
            print(f"      Action: Closing in DB (Sync Fix)...")

            # Close in DB
            client.table('trades').update({
                'status': 'CLOSED',
                'exit_reason': 'Sync Fix (Ghost Position)',
                'close_time': '2026-02-01T12:00:00',
                'pnl': 0
            }).eq('id', trade_id).execute()
        else:
            print(f"   MATCH: {db_symbol} exists on Binance.")
            # Optional: We could check if MULTIPLE db trades map to a SINGLE binance position
            # This is complex, for now let's just kill ghosts.

    await binance.close()
    print("✨ Sync Complete!")

if __name__ == "__main__":
    asyncio.run(sync_trades())
