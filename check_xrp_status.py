
import os
import asyncio
import ccxt.async_support as ccxt
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINANCE_API_KEY')
SECRET_KEY = os.getenv('BINANCE_SECRET_KEY')

async def main():
    exchange = ccxt.binance({
        'apiKey': API_KEY,
        'secret': SECRET_KEY,
        'options': {'defaultType': 'future'}
    })

    symbol = 'XRP/USDT'
    print(f"Checking open orders for {symbol}...")
    try:
        orders = await exchange.fetch_open_orders(symbol)
        print(f"Found {len(orders)} open orders:")
        for o in orders:
            print(f"ID: {o['id']} | Type: {o['type']} | Side: {o['side']} | Price: {o['price']} | Amount: {o['amount']}")

        print("\nChecking Position Risk:")
        positions = await exchange.fetch_positions([symbol])
        for p in positions:
            print(f"Entry: {p['entryPrice']} | Mark: {p['markPrice']} | Amount: {p['contracts']} | PNL: {p['unrealizedPnl']}")

    except Exception as e:
        print(f"Error: {e}")

    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
