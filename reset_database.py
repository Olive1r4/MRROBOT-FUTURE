#!/usr/bin/env python3
"""
Script para resetar o banco de dados do MRROBOT
ATENÇÃO: Este script apaga TODOS os dados de trades, logs, cooldowns e estatísticas!
"""
import os
import asyncio
from supabase import create_client
from datetime import datetime

# CREDENCIAIS DA VPS (PRODUÇÃO)
SUPABASE_URL = "https://ogqjsysghltrpcnzroth.supabase.co"
SUPABASE_KEY = "sb_publishable_Vp62RRNKVAF6PkyCaArKPA_lYtJsarm"

async def reset_database():
    print("=" * 60)
    print("🗑️  RESET DO BANCO DE DADOS - MRROBOT")
    print("=" * 60)
    print(f"\n⚠️  ATENÇÃO: Este script irá APAGAR todos os dados!")
    print("\nTabelas que serão limpas:")
    print("  1. trades_mrrobot (histórico de trades)")
    print("  2. logs_mrrobot (logs do sistema)")
    print("  3. cooldown_mrrobot (cooldowns de moedas)")
    print("  4. daily_stats_mrrobot (estatísticas diárias)")
    print("\nNOTA: A view 'performance_by_symbol_mrrobot' será")
    print("      automaticamente limpa ao limpar 'trades_mrrobot'")

    print(f"\n🔌 Conectando ao Supabase {SUPABASE_URL}...")

    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Conectado ao Supabase\n")

        # 1. Limpar trades_mrrobot
        print("🗑️  Limpando trades_mrrobot...")
        try:
            # Primeiro, contar quantos registros existem
            count_response = supabase.table('trades_mrrobot').select('id', count='exact').execute()
            count = len(count_response.data) if count_response.data else 0

            if count > 0:
                # Deletar todos os registros
                delete_response = supabase.table('trades_mrrobot').delete().neq('id', 0).execute()
                print(f"   ✅ {count} trade(s) removido(s)")
            else:
                print(f"   ℹ️  Tabela já estava vazia")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")

        # 2. Limpar logs_mrrobot
        print("\n🗑️  Limpando logs_mrrobot...")
        try:
            count_response = supabase.table('logs_mrrobot').select('id', count='exact').execute()
            count = len(count_response.data) if count_response.data else 0

            if count > 0:
                delete_response = supabase.table('logs_mrrobot').delete().neq('id', 0).execute()
                print(f"   ✅ {count} log(s) removido(s)")
            else:
                print(f"   ℹ️  Tabela já estava vazia")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")

        # 3. Limpar cooldown_mrrobot
        print("\n🗑️  Limpando cooldown_mrrobot...")
        try:
            count_response = supabase.table('cooldown_mrrobot').select('symbol', count='exact').execute()
            count = len(count_response.data) if count_response.data else 0

            if count > 0:
                delete_response = supabase.table('cooldown_mrrobot').delete().neq('symbol', '').execute()
                print(f"   ✅ {count} cooldown(s) removido(s)")
            else:
                print(f"   ℹ️  Tabela já estava vazia")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")

        # 4. Limpar daily_stats_mrrobot
        print("\n🗑️  Limpando daily_stats_mrrobot...")
        try:
            count_response = supabase.table('daily_stats_mrrobot').select('trade_date', count='exact').execute()
            count = len(count_response.data) if count_response.data else 0

            if count > 0:
                delete_response = supabase.table('daily_stats_mrrobot').delete().neq('trade_date', '').execute()
                print(f"   ✅ {count} estatística(s) diária(s) removida(s)")
            else:
                print(f"   ℹ️  Tabela já estava vazia")
        except Exception as e:
            print(f"   ⚠️  Erro: {e}")

        print("\n" + "=" * 60)
        print("✅ RESET CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print(f"\n📊 Banco de dados limpo e pronto para nova rodada de testes")
        print(f"🕐 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")
        return False

    return True

if __name__ == "__main__":
    print("\n⚠️  CONFIRMAÇÃO NECESSÁRIA")
    print("Este script irá APAGAR PERMANENTEMENTE todos os dados do banco!")
    confirm = input("\nDigite 'CONFIRMO' para prosseguir: ")

    if confirm == "CONFIRMO":
        asyncio.run(reset_database())
    else:
        print("\n❌ Operação cancelada pelo usuário")
