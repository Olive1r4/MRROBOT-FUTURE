#!/usr/bin/env python3
"""
Script para monitorar o status do bot em tempo real
"""
import asyncio
from supabase import create_client
from datetime import datetime, timezone

# CREDENCIAIS DA VPS (PRODUÇÃO)
SUPABASE_URL = "https://ogqjsysghltrpcnzroth.supabase.co"
SUPABASE_KEY = "sb_publishable_Vp62RRNKVAF6PkyCaArKPA_lYtJsarm"

async def monitor_bot():
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    print("=" * 70)
    print("📊 MONITOR DO BOT MRROBOT")
    print("=" * 70)

    try:
        # 1. Trades abertos
        trades_response = supabase.table('trades_mrrobot').select('*').eq('status', 'open').execute()
        trades = trades_response.data

        print(f"\n🔓 TRADES ABERTOS: {len(trades)}")
        if trades:
            for trade in trades:
                entry_time = datetime.fromisoformat(trade['entry_time'].replace('Z', '+00:00'))
                duration = (datetime.now(timezone.utc) - entry_time).total_seconds() / 60

                print(f"\n  • {trade['symbol']}")
                print(f"    ID: {trade['id']}")
                print(f"    Entrada: ${trade['entry_price']}")
                print(f"    Target: ${trade.get('target_price', 'N/A')}")
                print(f"    Stop Loss: ${trade.get('stop_loss_price', 'N/A')}")
                print(f"    Duração: {duration:.1f} minutos")

        # 2. Estatísticas do dia
        today = datetime.now(timezone.utc).date()
        stats_response = supabase.table('daily_stats_mrrobot').select('*').eq('trade_date', today.isoformat()).execute()

        print(f"\n📈 ESTATÍSTICAS DO DIA ({today}):")
        if stats_response.data:
            stats = stats_response.data[0]
            print(f"  • Total PnL: ${stats.get('total_pnl', 0):.2f}")
            print(f"  • Total Trades: {stats.get('total_trades', 0)}")
            print(f"  • Winning Trades: {stats.get('winning_trades', 0)}")
            print(f"  • Losing Trades: {stats.get('losing_trades', 0)}")
            print(f"  • Circuit Breaker: {'🔴 ATIVO' if stats.get('is_circuit_breaker_active') else '🟢 INATIVO'}")
        else:
            print("  • Nenhuma estatística registrada ainda")

        # 3. Últimos 5 trades fechados
        closed_trades = supabase.table('trades_mrrobot')\
            .select('*')\
            .eq('status', 'closed')\
            .order('exit_time', desc=True)\
            .limit(5)\
            .execute()

        print(f"\n📜 ÚLTIMOS 5 TRADES FECHADOS:")
        if closed_trades.data:
            for trade in closed_trades.data:
                pnl_emoji = "🟢" if trade.get('pnl', 0) > 0 else "🔴"
                print(f"  {pnl_emoji} {trade['symbol']}: ${trade.get('pnl', 0):.2f} ({trade.get('pnl_percentage', 0):.2f}%) - {trade.get('exit_reason', 'N/A')}")
        else:
            print("  • Nenhum trade fechado ainda")

        # 4. Últimos erros críticos
        errors = supabase.table('logs_mrrobot')\
            .select('*')\
            .eq('level', 'ERROR')\
            .order('created_at', desc=True)\
            .limit(3)\
            .execute()

        print(f"\n⚠️  ÚLTIMOS ERROS CRÍTICOS:")
        if errors.data:
            for error in errors.data:
                timestamp = error.get('created_at', 'N/A')
                print(f"  • [{timestamp}] {error.get('message', 'N/A')}")
        else:
            print("  • Nenhum erro registrado ✅")

    except Exception as e:
        print(f"\n❌ Erro ao buscar dados: {e}")

    print("\n" + "=" * 70)
    print(f"🕐 Atualizado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(monitor_bot())
