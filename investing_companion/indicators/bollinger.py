from investing_companion import indicators
import pandas as pd

class BollingerBands(indicators.IndicatorBase):
    '''
    Class for the Bollinger bands indicator. Inherits from IndicatorBase

    Methods:
    :set_column_names()
    :build_df()
    '''
    def __init__(self, window_size = 20, std_deviations=2, price_point='Close', tag='Boll_Bands'):
        '''
        Class constructor. Calls set_column_names after initializing attributes.

        :param window_size(int): the size of the window used in the SMA calculation. Default=20
        :param std_deviations(int): The amount of standard deviations used to determine the bands. Default=2
        :param tag(str): Identifier name for the instance. Not to be confused with the column names
        :param price_point(str): The price point (Open, Close, High, etc) from which to calculate the indicator
        '''
        super().__init__(price_point,tag)
        self.window_size = window_size
        self.std_deviations = std_deviations
        self.set_column_names()


    def __str__(self):
        return f'BB{(self.window_size,self.std_deviations)} (Evaluated on:{self.price_point})'


    def set_column_names(self):
        self.upper_band_name = f'BB_Upper{(self.window_size, self.std_deviations)}'
        self.lower_band_name = f'BB_Lower{(self.window_size,self.std_deviations)}'

    
    def build_df(self, base_df):
        sma = base_df[self.price_point].rolling(self.window_size, min_periods=self.window_size).mean()
        stdev = base_df[self.price_point].rolling(self.window_size, min_periods=self.window_size).std(ddof=0)
        upper_band = sma + stdev*self.std_deviations
        lower_band = sma - stdev*self.std_deviations

        df = pd.DataFrame({self.upper_band_name: upper_band,
                           self.lower_band_name: lower_band,})

        return df
