-- Enable Row Level Security
alter default privileges in schema public grant all on tables to postgres, service_role;

-- 1. Trades Table
CREATE TABLE IF NOT EXISTS trades (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    symbol VARCHAR(20) NOT NULL,
    side VARCHAR(10) NOT NULL CHECK (side IN ('BUY', 'SELL')),
    entry_price NUMERIC NOT NULL,
    close_price NUMERIC,
    amount NUMERIC NOT NULL,
    pnl NUMERIC,
    pnl_percentage NUMERIC,
    status VARCHAR(20) CHECK (status IN ('OPEN', 'CLOSED')),
    mode VARCHAR(10) DEFAULT 'PAPER' CHECK (mode IN ('PAPER', 'LIVE')),
    entry_reason VARCHAR(50),
    exit_reason VARCHAR(50),
    entry_time TIMESTAMPTZ DEFAULT NOW(),
    close_time TIMESTAMPTZ,
    strategy_data JSONB -- Store indicator values at entry for analysis
);

-- 2. Wallet History Table (Balance Tracking)
CREATE TABLE IF NOT EXISTS wallet_history (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT NOW(),
    total_balance NUMERIC NOT NULL,
    available_balance NUMERIC NOT NULL,
    mode VARCHAR(10) DEFAULT 'PAPER' CHECK (mode IN ('PAPER', 'LIVE'))
);

-- RLS Policies
ALTER TABLE trades ENABLE ROW LEVEL SECURITY;
ALTER TABLE wallet_history ENABLE ROW LEVEL SECURITY;

-- Allow public read access (for dashboards if needed) and Service Role full access
CREATE POLICY "Public Read Access" ON trades FOR SELECT USING (true);
CREATE POLICY "Service Role Full Access" ON trades USING (auth.role() = 'service_role');

CREATE POLICY "Public Read Access" ON wallet_history FOR SELECT USING (true);
CREATE POLICY "Service Role Full Access" ON wallet_history USING (auth.role() = 'service_role');
