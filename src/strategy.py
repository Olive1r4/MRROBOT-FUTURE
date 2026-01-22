import pandas as pd
import pandas_ta as ta

class Strategy:
    def __init__(self):
        self.ema_fast_len = 9
        self.ema_slow_len = 21
        self.supertrend_len = 10
        self.supertrend_factor = 3

    def parse_data(self, ohlcv):
        """Convert CCXT ohlcv to Pandas DataFrame."""
        if not ohlcv or len(ohlcv) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_indicators(self, df):
        """Calculate EMAs and SuperTrend."""
        if df.empty or len(df) < 50:
            return df

        # EMAs
        df['ema_fast'] = ta.ema(df['close'], length=self.ema_fast_len)
        df['ema_slow'] = ta.ema(df['close'], length=self.ema_slow_len)

        # SuperTrend
        # returns DataFrame with columns: SUPERT_7_3.0, SUPERTd_7_3.0, SUPERTl_7_3.0, SUPERTs_7_3.0
        st = ta.supertrend(df['high'], df['low'], df['close'], length=self.supertrend_len, multiplier=self.supertrend_factor)

        if st is not None:
            df = pd.concat([df, st], axis=1)
            # Normalize column name for easier access (find the one starting with SUPERT_)
            st_col = [col for col in df.columns if col.startswith('SUPERT_')][0]
            df['supertrend'] = df[st_col] # The value line

            # Identify SuperTrend direction (True = UP/Green, False = DOWN/Red)
            # Pandas TA usually gives a direction column, typically 1 for up, -1 for down.
            # Let's inspect the specific implementation output or assume standar behavior.
            # Usually: Close > Supertrend = Bullish.

        return df

    def check_signal(self, df):
        """
        Check for ENTRY signals based on closed candles.
        We look at the last closed candle (iloc[-2]) because iloc[-1] is the open/current candle.
        """
        if df.empty or len(df) < 30:
            return None, None

        # Last closed candle
        curr = df.iloc[-2]
        prev = df.iloc[-3]

        # Conditions
        # 1. Golden Cross: EMA 9 crosses above EMA 21
        crossover = (curr['ema_fast'] > curr['ema_slow']) and (prev['ema_fast'] <= prev['ema_slow'])

        # 2. Price above SuperTrend
        trend_bullish = curr['close'] > curr['supertrend']

        # Entry Signal
        if crossover and trend_bullish:
            return "LONG", {
                "ema_fast": curr['ema_fast'],
                "ema_slow": curr['ema_slow'],
                "supertrend": curr['supertrend'],
                "price": curr['close']
            }

        return None, None

    def check_exit(self, df, position_side):
        """
        Check for EXIT signals based on closed candles.
        """
        if df.empty:
            return False, "No Data"

        curr = df.iloc[-2]
        prev = df.iloc[-3]

        if position_side == "LONG":
            # 1. Reverse Cross: EMA 9 crosses below EMA 21
            cross_under = (curr['ema_fast'] < curr['ema_slow']) and (prev['ema_fast'] >= prev['ema_slow'])

            if cross_under:
                return True, "EMA Cross Under"

        # Note: Stop Loss is usually handled by the Bot loop checking current price vs entry price,
        # but strategy can also define technical exits.

        return False, None
