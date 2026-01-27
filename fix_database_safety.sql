-- 1. Adjust RLS policies for trades table
-- Allow anyone with the API key (anon) to insert and update trades
DROP POLICY IF EXISTS "Service Role Full Access" ON trades;
DROP POLICY IF EXISTS "Public Read Access" ON trades;

CREATE POLICY "Allow all access for anon" ON trades FOR ALL USING (true) WITH CHECK (true);

-- 2. Adjust constraints for the side column
-- Drop existing constraint if it exists
ALTER TABLE trades DROP CONSTRAINT IF EXISTS trades_side_check;

-- Add new constraint allowing LONG and SHORT
ALTER TABLE trades ADD CONSTRAINT trades_side_check CHECK (side IN ('BUY', 'SELL', 'LONG', 'SHORT'));

-- 3. Ensure system_logs also allows inserts (just in case)
ALTER TABLE system_logs ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow anonymous insert" ON system_logs;
CREATE POLICY "Allow anonymous insert" ON system_logs FOR INSERT WITH CHECK (true);
