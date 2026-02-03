from supabase import create_client, Client
from src.config import Config
import logging

class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            try:
                cls._instance.client: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
                logging.info("Connected to Supabase successfully.")
            except Exception as e:
                logging.error(f"Failed to connect to Supabase: {e}")
                raise e
        return cls._instance

    def get_client(self) -> Client:
        return self.client

    def log_trade(self, trade_data: dict):
        try:
            db = self.get_client()
            response = db.table('trades_mrrobot').insert(trade_data).execute()
            return response
        except Exception as e:
            logging.error(f"Error logging trade: {e}")
            return None

    def update_trade(self, trade_id: str, update_data: dict):
        try:
            db = self.get_client()
            response = db.table('trades_mrrobot').update(update_data).eq('id', trade_id).execute()
            return response
        except Exception as e:
            logging.error(f"Error updating trade: {e}")
            return None

    def update_trade_by_cycle(self, grid_cycle_id: str, update_data: dict):
        """Update trade using the grid_cycle_id stored in strategy_data jsonb column"""
        try:
            db = self.get_client()
            # We need to query first to find the ID, then update by ID
            # Or use Supabase JSON filtering if enabled.
            # Simpler approach: Select ID where strategy_data->>grid_cycle_id equals value

            response = db.table('trades_mrrobot')\
                .select('id')\
                .eq('strategy_data->>grid_cycle_id', grid_cycle_id)\
                .limit(1)\
                .execute()

            if response.data and len(response.data) > 0:
                trade_id = response.data[0]['id']
                return self.update_trade(trade_id, update_data)
            else:
                logging.warning(f"Trade with cycle_id {grid_cycle_id} not found for update, falling back to insert.")
                return None
        except Exception as e:
            logging.error(f"Error updating trade by cycle: {e}")
            return None

    def cancel_pending_trades(self, symbol: str):
        try:
            db = self.get_client()
            # Update all 'PENDING' trades for this symbol to 'CANCELLED'
            response = db.table('trades_mrrobot')\
                .update({'status': 'CANCELLED'})\
                .eq('symbol', symbol)\
                .eq('status', 'PENDING')\
                .execute()
            return response
        except Exception as e:
            logging.error(f"Error cancelling pending trades for {symbol}: {e}")
            return None

    def get_open_trades_count(self, symbol: str) -> int:
        """Count number of OPEN trades for a symbol."""
        try:
            db = self.get_client()
            response = db.table('trades_mrrobot')\
                .select('id', count='exact')\
                .eq('symbol', symbol)\
                .eq('status', 'OPEN')\
                .execute()

            # response.count returns the count if 'exact' is specified
            if response.count is not None:
                return response.count
            return len(response.data) if response.data else 0
        except Exception as e:
            logging.error(f"Error counting open trades for {symbol}: {e}")
            return 0

    def log_wallet(self, wallet_data: dict):
        try:
            db = self.get_client()
            # Only keep history, don't update existing rows usually for history
            response = db.table('wallet_logs_mrrobot').insert(wallet_data).execute()
            return response
        except Exception as e:
            logging.error(f"Error logging wallet history: {e}")
            return None

    def get_latest_paper_balance(self):
        try:
            db = self.get_client()
            # Get the most recent wallet history entry for PAPER mode
            response = db.table('wallet_logs_mrrobot')\
                .select('total_balance')\
                .eq('mode', 'PAPER')\
                .order('timestamp', desc=True)\
                .limit(1)\
                .execute()

            if response.data and len(response.data) > 0:
                return float(response.data[0]['total_balance'])
            return None
        except Exception as e:
            logging.error(f"Error fetching paper balance: {e}")
            return None

    def get_active_markets(self):
        """Fetch all active markets from settings."""
        try:
            db = self.get_client()
            response = db.table('market_settings')\
                .select('*')\
                .eq('is_active', True)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logging.error(f"Error fetching active markets: {e}")
            return []

    def log_system_error(self, log_data: dict):
        """Log system errors to the database."""
        try:
            db = self.get_client()
            db.table('logs_mrrobot').insert(log_data).execute()
        except:
            # We don't use logging.error here to avoid infinite loops if DB is down
            pass
