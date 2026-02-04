
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

    print("Checking recent trades to identify leverage used:")
    for symbol in symbols:
        try:
            # Fetch recent trades
            trades = await exchange.fetch_my_trades(symbol, limit=3)
            if trades:
                print(f"\n{symbol} - Recent Trades:")
                for t in trades:
                    # Calculate implied leverage from cost/amount
                    cost = float(t.get('cost', 0))
                    price = float(t.get('price', 0))
                    amount = float(t.get('amount', 0))

                    print(f"  Price: {price} | Amount: {amount} | Cost: {cost}")
                    print(f"  Fee: {t.get('fee')}")

        except Exception as e:
            print(f"Error checking {symbol}: {e}")

    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
