from investing_companion.indicators import bollinger
from investing_companion import strategy
import pandas as pd
import numpy as np
from enum import enum, auto

class Bollinger_Strategy(strategy.BaseStrategy):
    
    class Method(Enum):
        BAND_CROSSOVER_SIMPLE = auto()
        DOUBLE_BAND_CROSSOVER = auto()

    def __init__(self, symbol, start=None, end=None, period='max',
                 bollinger_obj=bollinger.BollingerBands(), 
                 method=Method.BAND_CROSSOVER_SIMPLE,
                 buffer=1):
        super().__init__(symbol, start, end, period)
        self.bol_band = bollinger_obj
        self.method = method
        self.buffer = buffer
        self.data = pd.concat([self.data, self.bol_band.build_df(self.data)], axis=1)
    
    def backtest_strategy(self, start=None):
        if start is None:
            start = self.macd_object.window_size
        
        if self.method == Method.BAND_CROSSOVER_SIMPLE:
            buy_sig = (self.data['Close'] < self.data[self.bol_band.lower_band_name])\
                      .rolling(self.buffer).apply(self.buffer_all).fillna(0).astype(bool)
            
            cross_buy_sig = (self.data['Close'].shift(self.buffer) >= 
                             self.data[self.bol_band.lower_band_name].shift(self.buffer-1))
            
            sell_sig = (self.data['Close'] > self.data[self.bol_band.upper_band_name])\
                      .rolling(self.buffer).apply(self.buffer_all).fillna(0).astype(bool)
            
            cross_sell_sig = (self.data['Close'].shift(self.buffer) <= 
                             self.data[self.bol_band.upper_band_name].shift(self.buffer-1))
        
        if self.method == Method.DOUBLE_BAND_CROSSOVER:
            return
        
        buy_cond = buy_sig & cross_buy_sig
        sell_cond = sell_sig & cross_sell_sig

    def optimize_strat_params(self):
        pass