import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

__author__ = 'Dixit_Patel'

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
    df = df.resample('M', how='mean')
    df = df.fillna(1)

    # fig,ax = plt.subplots(1,1, figsize=(6,4))
    flow = df['review_count_lambda_smooth']
    res = sm.tsa.seasonal_decompose(flow)

    res.plot()

    plt.legend()
    plt.show()

'''
applies acf, pacf and ARIMA prediction on the timeseries
given as csv format
'''


def auto_regression_moving_averages(file_name):

    df = ['Index', 'Date', 'review_count']
    df = pd.read_csv(file_name, delimiter=',').dropna()
    df['review_count_lambda_smooth'] = df['review_count'].apply(lambda x: x+1)

    df.index = pd.DatetimeIndex(df['Date'])
    df = df.resample('M', how='mean')
    df = df.fillna(1)

    flow = df['review_count_lambda_smooth']

    # clean data fram
    df = df.drop(['review_count'], axis=1)

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_pacf(flow, lags=40, ax=ax)

    ax = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_acf(flow, lags=40, ax=ax)

    arma_mod20 = sm.tsa.ARMA(flow, (2, 0)).fit()
    print('=')
    print(arma_mod20.params)
    print('=')
    arma_mod30 = sm.tsa.ARMA(flow, (3, 0)).fit()

    print('==')
    print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
    print('==')

    print('===')
    print(arma_mod30.params)
    print('===')

    resid = arma_mod30.resid
    sm.graphics.qqplot(resid, line='q', fit=True)

    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(411)
    fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
    ax2 = fig.add_subplot(412)
    fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

    r, q, p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
    data = np.c_[range(1, 41), r[1:], q, p]
    table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    print(table.set_index('lag'))

    predict_reviews = arma_mod30.predict('2012', '2015', dynamic=True)
    print(predict_reviews)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax = df.ix['2005':].plot(ax=ax)
    fig = arma_mod30.plot_predict('2012', '2015', dynamic=True, ax=ax, plot_insample=False)

    plt.legend()
    plt.show()

if __name__ == '__main__':
    # seasonal_decomposition('resources/year_all_review_count.csv')
    auto_regression_moving_averages('resources/year_all_review_count.csv')
