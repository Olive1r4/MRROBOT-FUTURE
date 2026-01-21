#!/usr/bin/env python3
"""
Script para fechar trades manualmente no banco
"""
import asyncio
from supabase import create_client
from datetime import datetime, timezone

# CREDENCIAIS DA VPS (PRODUÇÃO)
SUPABASE_URL = "https://ogqjsysghltrpcnzroth.supabase.co"
SUPABASE_KEY = "sb_publishable_Vp62RRNKVAF6PkyCaArKPA_lYtJsarm"

async def close_stuck_trades():
    print("🔧 Fechando trades travados...")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    try:
        # Buscar trades abertos
        response = supabase.table('trades_mrrobot').select('*').eq('status', 'open').execute()
        trades = response.data

        if not trades:
            print("✅ Nenhum trade aberto encontrado")
            return

        print(f"\n📊 Encontrados {len(trades)} trade(s) aberto(s):\n")

        for trade in trades:
            trade_id = trade['id']
            symbol = trade['symbol']
            entry_price = float(trade['entry_price'])

            print(f"Trade ID: {trade_id} | {symbol} | Entry: ${entry_price}")

            # Fechar com preço de entrada (PnL = 0)
            update_data = {
                'exit_price': entry_price,
                'exit_time': datetime.now(timezone.utc).isoformat(),
                'pnl': 0.0,
                'pnl_percentage': 0.0,
                'status': 'closed',
                'exit_reason': 'MANUAL_CLOSE_STUCK'
            }

            supabase.table('trades_mrrobot').update(update_data).eq('id', trade_id).execute()
            print(f"   ✅ Fechado manualmente\n")

        print("✅ Todos os trades foram fechados!")

    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    asyncio.run(close_stuck_trades())
