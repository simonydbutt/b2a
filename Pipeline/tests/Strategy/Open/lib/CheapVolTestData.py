import pandas as pd

enterData = pd.DataFrame(
    data=[
        [10, 10], [10, 10], [10, 10], [10, 10], [0.4, 20]
    ], columns=['close', 'volume']
)

volSmallData = pd.DataFrame(
    data=[
        [10, 20], [10, 30], [10, 10], [10, 10], [0.4, 20]
    ], columns=['close', 'volume']
)

closeLargeData = pd.DataFrame(
    data=[
        [10, 10], [10, 10], [10, 10], [10, 10], [20, 20]
    ], columns=['close', 'volume']
)
