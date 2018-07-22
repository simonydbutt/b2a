from bokeh.plotting import output_file, figure, show
from bokeh.models import LinearAxis, Range1d
from math import pi
import pandas as pd


class CandlestickChart:

    def __init__(self, gridAlpha=0.6, orientation=pi/4):
        self.gridAlpha = gridAlpha
        self.orientation = orientation

    def plot(self, df, granularity, MA=False, Bollinger=False, Vol=False):
        df['date'] = pd.to_datetime(df['TS'], unit='s')

        mids = (df.open + df.close) / 2
        spans = abs(df['close'] - df['open'])
        inc = df['close'] > df['open']
        dec = df['open'] > df['close']

        w = granularity * 1000

        output_file('tmp.html')
        if Vol:
            coef = 1.5 if Bollinger else 2
            priceRange = max(df.high) - min(df.low)
            p = figure(x_axis_type='datetime', toolbar_location='left',
                       y_range=(min(df.low) - priceRange/coef, max(df.high) + 0.1*priceRange))
        else:
            p = figure(x_axis_type='datetime', toolbar_location='left')

        p.segment(df['date'], df['high'], df['date'], df['low'], color='black')
        p.rect(df['date'][inc], mids[inc], (4/5)*w, spans[inc], fill_color='#20E208', line_color='black')
        p.rect(df['date'][dec], mids[dec], (4/5)*w, spans[dec], fill_color='#F04500', line_color='black')
        p.yaxis.axis_label = 'Asset Price'
        p.xaxis.axis_label = 'Datetime'

        if MA:
            for i in MA:
                p.line(df['date'], df[i], line_color='purple')
        if Bollinger:
            p.line(df['date'], df['bollingerUp'])
            p.line(df['date'], df['bollingerDown'])
        if Vol:
            p.add_layout(LinearAxis(y_range_name='Vol', axis_label='Volume'), 'right')
            p.extra_y_ranges = {'Vol': Range1d(
                start=0, end=float(max(df['takerBaseAssetVol']) * 4))}
            p.rect(df['date'], df['takerBaseAssetVol'] / 2, w, df['takerBaseAssetVol'],
                   fill_color='darkgrey', color='black', y_range_name='Vol')

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
                self.plot(df.iloc[int(max(0, i-(range/2))): int(min(i + (range/2), len(df)))],
                          granularity=gran, Vol=True)
                j += 1
            i += 1

    def plotStrat(self, df, timeStart, timeEnd, vol=False):
        df_ = df[(df['TS'] >= timeStart) & (df['TS'] < timeEnd)]
        gran = df.iloc[1]['TS'] - df.iloc[0]['TS']
        if 'ma' in df_.keys() and 'bollinger' in df_.keys():
            self.plot(df=df_, granularity=gran, MA=['ma'], Bollinger='bollinger', Vol=vol)
        else:
            self.plot(df=df_, granularity=gran, Vol=vol)