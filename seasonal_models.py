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
    fig = sm.graphics.tsa.plot_pacf(flow, lags=10, ax=ax)

    ax = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_acf(flow, lags=10, ax=ax)

    # arma_mod20 = sm.tsa.ARMA(flow, (2, 0)).fit()
    # print('=')
    # print(arma_mod20.params)
    # print('=')
    arma_mod30 = sm.tsa.ARMA(flow, (3, 1)).fit()

    # print('==')
    # print(arma_mod20.aic, arma_mod20.bic, arma_mod20.hqic)
    # print('==')

    print('===')
    print(arma_mod30.params)
    print(arma_mod30.aic, arma_mod30.bic, arma_mod30.hqic)
    print('===')

    resid = arma_mod30.resid
    sm.graphics.qqplot(resid, line='q', fit=True)

    fig = plt.figure(figsize=(12, 8))
    ax1 = fig.add_subplot(411)
    fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
    ax2 = fig.add_subplot(412)
    fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

    r, q, p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
    print '==>', p, q, r
    data = np.c_[range(1, 41), r[1:], q, p]
    table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
    print(table.set_index('lag'))

    predict_reviews = arma_mod30.predict('2012', '2015', dynamic=True)
    print(predict_reviews)

    fig, ax = plt.subplots(figsize=(12, 8))
    ax = df.ix['2008':].plot(ax=ax)
    fig = arma_mod30.plot_predict('2014', '2015', dynamic=True, ax=ax, plot_insample=False)

    plt.legend()
    plt.show()

def print_auto_regression_moving_averages(file_name, p, r):
    df = ['Index', 'Date', 'review_count']
    df = pd.read_csv(file_name, delimiter=',').dropna()
    df['review_count_lambda_smooth'] = df['review_count'].apply(lambda x: x+1)

    df.index = pd.DatetimeIndex(df['Date'])
    df = df.resample('M', how='mean')
    df = df.fillna(1)

    flow = df['review_count_lambda_smooth']

    arma_mod30 = sm.tsa.ARMA(flow, (p, r)).fit()
    print('===', 'p', p, 'r', r)
    print(arma_mod30.params)
    print('aic ', arma_mod30.aic, 'bic ', arma_mod30.bic, ' hqic ',  arma_mod30.hqic)
    print('===')


if __name__ == '__main__':
    # seasonal_decomposition('resources/year_all_review_count.csv')
<<<<<<< HEAD
    print_auto_regression_moving_averages('resources/year_all_review_count_'+ '4bEjOyTaDG24SY5TxsaUNQ' +'.csv', 1, 0)
    print_auto_regression_moving_averages('resources/year_all_review_count_'+ '4bEjOyTaDG24SY5TxsaUNQ' +'.csv', 2, 0)

    print_auto_regression_moving_averages('resources/year_all_review_count_'+ '4bEjOyTaDG24SY5TxsaUNQ' +'.csv', 0, 1)
    print_auto_regression_moving_averages('resources/year_all_review_count_'+ '4bEjOyTaDG24SY5TxsaUNQ' +'.csv', 0, 2)

    print_auto_regression_moving_averages('resources/year_all_review_count_'+ '4bEjOyTaDG24SY5TxsaUNQ' +'.csv', 1, 1)
    print_auto_regression_moving_averages('resources/year_all_review_count_'+ '4bEjOyTaDG24SY5TxsaUNQ' +'.csv', 1, 0)

=======
    bidToConsider = '4bEjOyTaDG24SY5TxsaUNQ'

    auto_regression_moving_averages('resources/year_all_review_count_'+bidToConsider+'_smooth.csv')
>>>>>>> 4d0726607b8a6aa186c14c1ca34e76b92b62e7dc
