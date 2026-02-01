import asyncio
from src.exchange import Exchange
from src.config import Config

async def main():
    ex = Exchange()
    try:
        await ex.client.load_markets()
        positions = await ex.client.fetch_positions(symbols=['ETH/USDT'])
        for p in positions:
            if float(p['contracts']) != 0:
                print(f"Symbol: {p['symbol']}, Size: {p['contracts']}, Side: {p['side']}, Leverage: {p['leverage']}")

        balance = await ex.get_balance()
        print(f"Balance: {balance}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        await ex.client.close()

if __name__ == "__main__":
    asyncio.run(main())
