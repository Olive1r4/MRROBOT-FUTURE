import pandas as pd
import pandas_ta as ta

class Strategy:
    def __init__(self):
        # Trend Following Setup
        self.ema_short_len = 50
        self.ema_long_len = 200
        self.adx_len = 14
        self.adx_threshold = 20
        self.atr_len = 14

    def parse_data(self, ohlcv):
        """Convert CCXT ohlcv to Pandas DataFrame."""
        if not ohlcv or len(ohlcv) == 0:
            return pd.DataFrame()

        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        return df

    def calculate_indicators(self, df):
        """Calculate EMAs, ADX and ATR."""
        if df.empty or len(df) < self.ema_long_len:
            return df

        # EMAs
        df['ema_50'] = ta.ema(df['close'], length=self.ema_short_len)
        df['ema_200'] = ta.ema(df['close'], length=self.ema_long_len)

        # ADX (Returns DataFrame: ADX_14, DMP_14, DMN_14)
        adx = ta.adx(df['high'], df['low'], df['close'], length=self.adx_len)
        if adx is not None:
            df = pd.concat([df, adx], axis=1)
            # Normalize column name
            df['adx'] = df[f'ADX_{self.adx_len}']

        # ATR (For volatility-based stops)
        df['atr'] = ta.atr(df['high'], df['low'], df['close'], length=self.atr_len)

        return df

    def check_signal(self, df):
        """
        Check for ENTRY signals (LONG or SHORT) based on Trend Following.
        """
        if df.empty or len(df) < self.ema_long_len:
            return None, None

        curr = df.iloc[-2] # Last closed candle
        prev = df.iloc[-3]

        # Trend Indicators
        ema_short = curr['ema_50']
        ema_long = curr['ema_200']

        strong_trend = curr['adx'] > self.adx_threshold

        signal_side = None
        reason = ""

        if strong_trend:
            # --- LONG LOGIC ---
            if ema_short > ema_long: # Bullish Trend
                # Price Cross over EMA 50 (Trend Continuation)
                if (curr['close'] > ema_short) and (prev['close'] <= prev['ema_50']):
                    signal_side = "LONG"
                    reason = "Trend Continuation UP (EMA 50 Breakout)"
                # Golden Cross (Rare but Strong)
                elif (curr['ema_50'] > curr['ema_200']) and (prev['ema_50'] <= prev['ema_200']):
                    signal_side = "LONG"
                    reason = "Golden Cross (50/200)"

            # --- SHORT LOGIC ---
            elif ema_short < ema_long: # Bearish Trend
                # Price Cross under EMA 50 (Trend Continuation Down)
                if (curr['close'] < ema_short) and (prev['close'] >= prev['ema_50']):
                    signal_side = "SHORT"
                    reason = "Trend Continuation DOWN (EMA 50 Breakdown)"
                # Death Cross (Rare but Strong)
                elif (curr['ema_50'] < curr['ema_200']) and (prev['ema_50'] >= prev['ema_200']):
                    signal_side = "SHORT"
                    reason = "Death Cross (50/200)"

        if signal_side:
            return signal_side, {
                "ema_50": float(curr['ema_50']),
                "ema_200": float(curr['ema_200']),
                "adx": float(curr['adx']),
                "atr": float(curr['atr']),
                "price": float(curr['close']),
                "signal_reason": reason
            }

        return None, None

    def check_exit(self, df, position_side):
        """
        Check for EXIT signals based on Trend Reversal.
        """
        if df.empty:
            return False, "No Data"

        curr = df.iloc[-1] # Current candle

        # LONG Exit: Close < EMA 50 (Lost short-term momentum) OR Close < EMA 200 (Trend Dead)
        # To be purely trend following on 15m, losing the EMA 50 is a good tactical exit.
        if position_side == "LONG":
            if curr['close'] < curr['ema_50']:
                return True, "Trend Weakness (Close < EMA 50)"

        # SHORT Exit: Close > EMA 50 (Gained short-term momentum)
        if position_side == "SHORT":
            if curr['close'] > curr['ema_50']:
                return True, "Trend Weakness (Close > EMA 50)"

        return False, None
