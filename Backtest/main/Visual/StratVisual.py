from bokeh.plotting import figure, output_file, show
from Backtest.main.Utils.AssetBrackets import AssetBrackets


class StratVisual:

    def __init__(self, resultsDict):
        self.resultsDict = resultsDict
        self.A = AssetBrackets()

    def periodReturns(self):
        brackets = self.A.getBrackets()
        rd = self.resultsDict
        p = figure(plot_width=1000, plot_height=700)
        for asset in [coin for coin in rd.keys() if coin != 'Total']:
            if asset in brackets['big']:
                color = 'green'
            elif asset in brackets['mid']:
                color = 'orange'
            elif asset in brackets['small']:
                color = 'red'
            else:
                color = 'purple'
            p.circle(rd[asset]['numPeriods'], rd[asset]['results'], size=5, color=color)
        output_file("tmp.html")
        show(p)

    def stratByAsset(self):
        pass

