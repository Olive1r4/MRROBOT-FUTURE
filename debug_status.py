
import os
import asyncio
from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime

# Load env variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

async def check_status():
    print(f"Connecting to Supabase at {SUPABASE_URL}...")
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

        # Check bot_status
        print("\n--- Bot Status ---")
        try:
            response = supabase.table('bot_status')\
                .select('*')\
                .execute()

            statuses = response.data
            if not statuses:
                print("No bot status found.")
            else:
                for status in statuses:
                    print(f"ID: {status.get('id')} | Status: {status.get('status')} | Last Seen: {status.get('last_seen')}")
        except Exception as e:
            print(f"Error fetching bot status: {e}")

    except Exception as e:
        print(f"Critical error: {e}")

if __name__ == "__main__":
    asyncio.run(check_status())
