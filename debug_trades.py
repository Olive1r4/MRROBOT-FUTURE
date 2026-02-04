
import os
import asyncio
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

async def main():
    db = create_client(SUPABASE_URL, SUPABASE_KEY)

    response = db.table('trades_mrrobot').select('*').eq('status', 'OPEN').execute()
    trades = response.data

    print(f"Found {len(trades)} OPEN trades:")
    for t in trades:
        symbol = t.get('symbol')
        entry = float(t.get('entry_price'))
        current_pnl = t.get('pnl') # Likely None until closed
        strategy_data = t.get('strategy_data', {})
        print(f"Symbol: {symbol} | Entry: {entry} | ID: {t.get('id')}")
        print(f"  Strategy Data: {strategy_data}")

if __name__ == "__main__":
    asyncio.run(main())
