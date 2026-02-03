import asyncio
import ccxt.async_support as ccxt
from dotenv import load_dotenv
import os

load_dotenv()

async def cancel_all_orders():
    exchange = ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_SECRET_KEY'),
        'enableRateLimit': True,
        'options': {'defaultType': 'future'}
    })

    try:
        # Get all open orders
        orders = await exchange.fetch_open_orders()
        print(f"Found {len(orders)} open orders")

        # Cancel each one
        for order in orders:
            symbol = order['symbol']
            order_id = order['id']
            try:
                await exchange.cancel_order(order_id, symbol)
                print(f"✅ Cancelled {symbol} order {order_id}")
            except Exception as e:
                print(f"❌ Error cancelling {symbol}: {e}")

        print(f"\n✅ Cancelled {len(orders)} orders total")

    finally:
        await exchange.close()

if __name__ == "__main__":
    asyncio.run(cancel_all_orders())
