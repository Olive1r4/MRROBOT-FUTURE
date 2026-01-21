
import os
import asyncio
from datetime import datetime, timezone
# from dotenv import load_dotenv
from supabase import create_client

# load_dotenv()

# CREDENCIAIS DA VPS (PRODUÇÃO)
SUPABASE_URL = "https://ogqjsysghltrpcnzroth.supabase.co"
SUPABASE_KEY = "sb_publishable_Vp62RRNKVAF6PkyCaArKPA_lYtJsarm"

async def reset_circuit_breaker():
    print(f"Connecting to Supabase {SUPABASE_URL}...")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        print(f"Error creating client: {e}")
        return

    today = datetime.now(timezone.utc).date()
    # today = "2026-01-21" # Caso precise forçar
    print(f"Resetting circuit breaker for date: {today}")

    try:
        data = {
            'is_circuit_breaker_active': False
        }

        response = supabase.table('daily_stats_mrrobot')\
            .update(data)\
            .eq('trade_date', today.isoformat())\
            .execute()

        print(f"Update Result Data: {response.data}")
        print("✅ Circuit Breaker RESET com sucesso!")

    except Exception as e:
        print(f"❌ Error resetting circuit breaker: {e}")

if __name__ == "__main__":
    asyncio.run(reset_circuit_breaker())
