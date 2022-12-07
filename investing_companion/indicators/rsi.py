from investing_companion import indicators
import pandas as pd

class RelativeStrengthIndex(indicators.IndicatorBase):
    '''
    The Class used to calculate the RSI indicator. Inherits from IndicatorBase.

    :param: base_df: The Dataframe which contains the data needed for RSI calculation
    :param: window_size: the window size for the RSI. Default=14
    :param tag: dentifier name for the instance. Not to be confused with the column names

    Methods:
    rsi()
    set_column_names()
    build_df()
    '''
    def __init__(self, window_size=14, tag='RSI'):
        super().__init__(tag)
        self.window_size = window_size
        self.set_column_names()


    def set_column_names(self):
        self.rsi_name = f'RSI({self.window_size})'


    def build_df(self, base_df):
        df = pd.DataFrame(index=base_df.index)
        df['diff'] = base_df.diff(1)
        df['upward'] = df['diff'].clip(lower=0).round(2)
        df['downward'] = df['diff'].clip(upper=0).abs().round(2)
        
    

        df['average_upward'] = df['upward'].rolling(self.window_size,
                                                    min_periods=self.window_size)\
                                                    .mean()[:self.window_size+1]

        df['average_downward'] = df['downward'].rolling(self.window_size,
                                                        min_periods=self.window_size)\
                                                        .mean()[:self.window_size+1]

        #Calculating Wilder's Smoothing Mean (WSM)
        #Average gains
        for i, row in enumerate(df['average_upward'].iloc[self.window_size+1:]):
            df['average_upward'].iloc[i+self.window_size+1] =\
                (df['average_upward'].iloc[i+self.window_size]*
                (self.window_size-1) +
                df['upward'].iloc[i+self.window_size+1])\
                    /self.window_size
        #Average Losses
        for i, row in enumerate(df['average_downward'].iloc[self.window_size+1:]):
            df['average_downward'].iloc[i+self.window_size+1] =\
                (df['average_downward'].iloc[i+self.window_size]*
                (self.window_size-1) +
                df['downward'].iloc[i+self.window_size+1])\
                    /self.window_size

        df['rs'] = df['average_upward']/df['average_downward']
        

        df[self.rsi_name] = 100 - (100/(1.0+df['rs'])) 
        df = df[[self.rsi_name]]

        return df
