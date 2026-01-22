-- Migration: Add market_settings table
CREATE TABLE IF NOT EXISTS market_settings (
    symbol VARCHAR(20) PRIMARY KEY, -- Ex: 'BTC/USDT'
    is_active BOOLEAN DEFAULT true, -- Liga/Desliga a moeda
    leverage INTEGER DEFAULT 5,     -- Alavancagem específica (ex: 5)
    stop_loss_percent DECIMAL DEFAULT 0.05, -- Stop Loss personalizado (5%)
    created_at TIMESTAMP WITH TIME ZONE DEFAULT timezone('utc'::text, now())
);

-- Habilitar RLS (Segurança)
ALTER TABLE market_settings ENABLE ROW LEVEL SECURITY;

-- Política: O bot (e você) podem ler e editar livremente
CREATE POLICY "Enable read access for all users" ON market_settings FOR SELECT USING (true);
CREATE POLICY "Enable insert/update for service_role" ON market_settings FOR ALL USING (true);

-- Inserir as moedas iniciais (Seed Data)
INSERT INTO market_settings (symbol, is_active, leverage) VALUES
('BTC/USDT', true, 5),
('ETH/USDT', true, 5),
('SOL/USDT', true, 5)
ON CONFLICT (symbol) DO NOTHING;
