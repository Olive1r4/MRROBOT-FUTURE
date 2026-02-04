
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

    symbols = ['SOL/USDT', 'XRP/USDT', 'DOGE/USDT']

    print("Checking leverage settings on Binance for each symbol:")
    for symbol in symbols:
        try:
            positions = await exchange.fetch_positions([symbol])
            for p in positions:
                if float(p['contracts']) != 0:  # Only show active positions
                    print(f"{symbol}: Leverage={p['leverage']}x | Contracts={p['contracts']}")

            # Also check market info
            market = exchange.market(symbol)
            print(f"  Max Leverage: {market['limits']['leverage']['max']}x")

        except Exception as e:
            print(f"Error checking {symbol}: {e}")

    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
