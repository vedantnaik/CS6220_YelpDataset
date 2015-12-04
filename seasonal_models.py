__author__ = 'Dixit_Patel'

import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm


'''
this fun does seasonal decomposition
for a file in csv format containing
year, review_count
TODO: later extending to take in a dict
'''
def seasonal_decomposition(file_name):
    df = ['Index', 'Date', 'review_count']
    df = pd.read_csv(file_name, delimiter=',').dropna()
    df['review_count_lambda_smooth'] = df['review_count'].apply(lambda x: x+1)

    df.index = pd.DatetimeIndex(df['Date'])
    df = df.resample('M',how='mean')
    df = df.fillna(1)

    # fig,ax = plt.subplots(1,1, figsize=(6,4))
    flow = df['review_count_lambda_smooth']
    res = sm.tsa.seasonal_decompose(flow)

    res.plot()

    plt.legend()
    plt.show()

if __name__ == '__main__':
    seasonal_decomposition('resources/year_all_review_count.csv')
