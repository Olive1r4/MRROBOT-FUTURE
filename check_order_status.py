
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

    # Orders to check from debug_trades.py
    orders_to_check = [
        ('SOL/USDT', '194912320306'),
        ('SOL/USDT', '194849536265'),
        ('SOL/USDT', '194912321272')
    ]

    print("Checking specific orders on Binance...")
    for symbol, order_id in orders_to_check:
        try:
            order = await exchange.fetch_order(order_id, symbol)
            print(f"Order {order_id} ({symbol}): Status={order['status']}, Price={order['price']}, OrgPrice={order.get('price')}, Side={order['side']}")
        except Exception as e:
            print(f"Error checking {order_id}: {e}")

    await exchange.close()

if __name__ == "__main__":
    asyncio.run(main())
