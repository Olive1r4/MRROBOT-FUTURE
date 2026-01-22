import asyncio
import logging
from src.config import Config
from src.exchange import Exchange
from src.database import Database
from src.strategy import Strategy

# Configure Logging
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=getattr(logging, Config.LOG_LEVEL)
)

class MrRobotTrade:
    def __init__(self):
        self.exchange = Exchange()
        self.db = Database()
        self.strategy = Strategy()
        self.running = True
        self.current_trade = None

        # Load any existing OPEN trade from DB
        self._load_open_trade()

    def _load_open_trade(self):
        """Recover state from DB."""
        try:
            client = self.db.get_client()
            response = client.table('trades')\
                .select('*')\
                .eq('status', 'OPEN')\
                .eq('mode', Config.TRADING_MODE)\
                .eq('symbol', Config.SYMBOL)\
                .limit(1)\
                .execute()

            if response.data and len(response.data) > 0:
                self.current_trade = response.data[0]
                logging.info(f"Resumed OPEN trade: {self.current_trade['id']} - Entry: {self.current_trade['entry_price']}")
        except Exception as e:
            logging.error(f"Error loading open trades: {e}")

    async def run(self):
        logging.info(f"Starting MrRobot Trade [{Config.TRADING_MODE}] on {Config.SYMBOL}")

        while self.running:
            try:
                # 1. Fetch Data
                candles = await self.exchange.get_candles()
                if not candles:
                    await asyncio.sleep(60)
                    continue

                df = self.strategy.parse_data(candles)
                df = self.strategy.calculate_indicators(df)

                current_price = await self.exchange.get_current_price()

                # 2. Manage Position
                if self.current_trade:
                    await self.manage_trade(df, current_price)
                else:
                    await self.look_for_entry(df, current_price)

                # Wait before next cycle
                # 4H candles don't change often, but we check price for SL/TP frequently
                await asyncio.sleep(60)

            except Exception as e:
                logging.error(f"Main Loop Error: {e}")
                await asyncio.sleep(60)

    async def look_for_entry(self, df, current_price):
        signal, data = self.strategy.check_signal(df)

        if signal == "LONG":
            logging.info(f"SIGNAL DETECTED: {signal} at {current_price}")

            # 1. Calculate Size
            balance_info = await self.exchange.get_balance()
            # For Paper Mode, we use 'free' which holds the tracked balance
            # For Live Mode, we also use 'free' USDT
            available_balance = float(balance_info['free'])

            if available_balance < 10: # Minimum check
                logging.warning(f"Insufficient balance: {available_balance}")
                return

            amount = self.exchange.calculate_position_size(available_balance, current_price)

            # 2. Execute Order
            order = await self.exchange.create_order(signal, amount)

            if order:
                # 3. Log to DB
                trade_record = {
                    'symbol': Config.SYMBOL,
                    'side': signal,
                    'entry_price': float(order['average']),
                    'amount': float(order['amount']),
                    'status': 'OPEN',
                    'mode': Config.TRADING_MODE,
                    'entry_reason': 'EMA Cross + SuperTrend',
                    'strategy_data': data
                }

                res = self.db.log_trade(trade_record)
                if res and res.data:
                    self.current_trade = res.data[0]
                    logging.info(f"Trade OPENED: {self.current_trade['id']}")

    async def manage_trade(self, df, current_price):
        # 1. Check Technical Exit
        should_exit, reason = self.strategy.check_exit(df, self.current_trade['side'])

        # 2. Check Stop Loss (Fixed 5%)
        entry_price = float(self.current_trade['entry_price'])
        # Long PnL % = (Current - Entry) / Entry
        pnl_pct = (current_price - entry_price) / entry_price

        # SL condition for LONG
        if pnl_pct <= -0.05:
            should_exit = True
            reason = "Stop Loss (-5%)"

        if should_exit:
            await self.close_trade(reason, current_price)

    async def close_trade(self, reason, current_price):
        logging.info(f"Closing trade. Reason: {reason} | Price: {current_price}")

        # 1. Execute Close Order
        # Sell the same amount we bought
        amount = float(self.current_trade['amount'])
        # If LONG, we SELL to close
        side = 'SELL' if self.current_trade['side'] == 'LONG' else 'BUY'

        order = await self.exchange.create_order(side, amount)

        if order:
            # 2. Calculate Realized PnL
            # (Exit - Entry) * Amount
            entry_price = float(self.current_trade['entry_price'])
            exit_price = float(order['average'])

            # Raw PnL
            pnl = (exit_price - entry_price) * amount
            # Leveraged PnL is technically tracking the Margin change,
            # but PnL calculation above is effectively the profit in USDT.

            # 3. Update DB
            update_data = {
                'status': 'CLOSED',
                'close_price': exit_price,
                'close_time': datetime.now().isoformat(),
                'exit_reason': reason,
                'pnl': pnl,
                'pnl_percentage': (exit_price - entry_price) / entry_price * 100
            }

            self.db.update_trade(self.current_trade['id'], update_data)

            # 4. Update Paper Balance if needed
            if Config.TRADING_MODE == 'PAPER':
                await self.exchange.update_paper_balance(pnl)

            logging.info(f"Trade CLOSED. PnL: {pnl:.2f} USDT")
            self.current_trade = None

if __name__ == "__main__":
    bot = MrRobotTrade()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(bot.run())
    except KeyboardInterrupt:
        logging.info("Stopping Bot...")
    finally:
        loop.run_until_complete(bot.exchange.close())
