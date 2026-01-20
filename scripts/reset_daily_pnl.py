
import asyncio
import os
import sys
from datetime import datetime

# Adicionar o diretório raiz ao path para importar src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config import Config
from src.database import Database

async def reset():
    print("🔄 Inicializando reset de PnL Diário...")
    config = Config()
    db = Database(config)

    today = datetime.now().date().isoformat()

    try:
        # Verificar se existe registro para hoje
        data = await db.get_daily_pnl()
        if not data:
            print(f"ℹ️ Nenhum dado diário encontrado para {today}. Nada para resetar.")
            return

        print(f"📊 Dados atuais para {today}: PnL=${data.get('total_pnl')}, Trades={data.get('total_trades')}")

        # Resetar estatísticas diárias e liberar Circuit Breaker
        response = db.client.table('daily_stats_mrrobot').update({
            'total_pnl': 0,
            'total_trades': 0,
            'winning_trades': 0,
            'losing_trades': 0,
            'is_circuit_breaker_active': False,
            'circuit_breaker_activated_at': None
        }).eq('trade_date', today).execute()

        print("✅ Reset concluído com sucesso!")
        print("🚀 O bot agora está livre para operar novamente hoje.")

    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")

if __name__ == "__main__":
    asyncio.run(reset())
