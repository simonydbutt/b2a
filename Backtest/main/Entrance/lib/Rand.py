import numpy as np


class Rand:

    def __init__(self, df, params):
        self.sampSize = params['sampSize'] if 'sampSize' in params.keys() else 100
        self.df = df

    def run(self):
        return [self.df.iloc[int(len(self.df)*val)]['TS'] for val in np.random.sample(self.sampSize)]
