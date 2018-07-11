from bokeh.plotting import output_file, figure, show
from math import pi
import pandas as pd


class CandlestickChart:

    def __init__(self, gridAlpha=0.6, orientation=pi/4):
        self.gridAlpha = gridAlpha
        self.orientation = orientation

    def plot(self, df, granularity, MA=False, Bollinger=False):
        df['date'] = pd.to_datetime(df['TS'], unit='s')

        mids = (df.open + df.close) / 2
        spans = abs(df['close'] - df['open'])
        inc = df['close'] > df['open']
        dec = df['open'] > df['close']

        w = (4 / 5) * granularity * 1000

        output_file('tmp.html')

        p = figure(x_axis_type='datetime', toolbar_location='left')

        p.segment(df['date'], df['high'], df['date'], df['low'], color='black')
        p.rect(df['date'][inc], mids[inc], w, spans[inc], fill_color='#20E208', line_color='black')
        p.rect(df['date'][dec], mids[dec], w, spans[dec], fill_color='#F04500', line_color='black')

        if MA:
            for i in MA:
                p.line(df['date'], df[i], line_color='purple')
        if Bollinger:
            p.line(df['date'], df[Bollinger+'Up'])
            p.line(df['date'], df[Bollinger+'Down'])

        p.xaxis.major_label_orientation = self.orientation
        p.grid.grid_line_alpha = self.gridAlpha

        show(p)

    def plotEx(self, df, field, num=1, range=20):
        targetCol = df[field]
        gran = df.iloc[1]['TS'] - df.iloc[0]['TS']
        i = 0
        j = 0
        while j < num and i < len(targetCol):
            if targetCol.iloc[i]:
                self.plot(df.iloc[int(max(0, i-(range/2))): int(min(i + (range/2), len(df)))], granularity=gran)
                j += 1
            i += 1