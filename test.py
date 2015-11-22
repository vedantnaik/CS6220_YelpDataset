from __future__ import print_function
__author__ = 'Dixit_Patel'

import json
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
# from elasticsearch import Elasticsearch
from scipy import stats
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot


def test():
    def recursive(hash_thing):
        if isinstance(hash_thing, dict):
            hash_thing = {k: v for k, v in hash_thing.items() if v is not None}
            for k,v in hash_thing.items():
                if isinstance(v, dict):
                    hash_thing[k] = recursive(hash_thing[k])
                    print(" sa ", recursive(hash_thing[k]))
            return hash_thing
        else:
            return hash_thing

    line = '{"business_id": "7VaXyrIw57IFNXzhYFn16g", "full_address": "8320 W Hayden Rd Scottsdale, AZ 85258", "hours": {"Monday": {"close": "18:00", "open": "06:30"}, "Tuesday": {"close": "18:00", "open": "06:30"}, "Friday": {"close": "18:00", "open": "06:30"}, "Wednesday": {"close": "18:00", "open": "06:30"}, "Thursday": {"close": "18:00", "open": "06:30"}, "Sunday": {"close": "18:00", "open": "07:00"}, "Saturday": {"close": "18:00", "open": "07:00"}}, "open": false, "categories": ["Food", "Juice Bars & Smoothies", "Pets", "Pet Stores"], "city": "Scottsdale", "review_count": 3, "name": "In The Raw", "neighborhoods": [], "longitude": -111.89871309999999, "state": "AZ", "stars": 2.5, "latitude": 33.557718100000002, "attributes": {"Parking": {"garage": false, "street": false, "validated": false, "lot": false, "valet": false}, "Accepts Credit Cards": {}, "Price Range": 2}, "type": "business"}'
    line = recursive(json.loads(line))

    print(line, "-")
def small_date():
    ar = []
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_"+'review_t'+".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)
            del line_json['text']
            ar.append(line_json)

    ar = sorted(ar, key=lambda k: k['date'], reverse=False)
    print('ar',  len(ar),  ar)
    # print('ar',  len(as),  as)

def moving_averages_test():
    print ("ts")
    df = pd.read_csv('resources/review_business_count_4bEjOyTaDG24SY5TxsaUNQ.csv')

    df = pd.read_csv('resources/year_2009_10_review_count.csv', index_col='Date', parse_dates=True)

    # print df.head()
    # print df.tail()


    close_px = df['review_count']

    close_px = close_px.sort_index(ascending=True)
    # close_px = close_px.tail(500)
    mavg = pd.rolling_mean(close_px, 8)

    close_px.plot(label='review_count')
    mavg.plot(label='mavg')
    plt.legend()
    plt.show()

def search1():
    es = Elasticsearch(timeout=60)
    indexName = 'yelp'
    reviews_dates = {}
    review_search_result = es.search(index=indexName, doc_type='review', size= 5000,
                                     body={"query": {"match": {"business_id": '4bEjOyTaDG24SY5TxsaUNQ'}}})
    for doc in review_search_result['hits']['hits']:
        strin = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').year)
        if strin in reviews_dates:
            reviews_dates[strin] = reviews_dates[strin] + 1
        else:
            reviews_dates[strin] = 1

    for k,v in reviews_dates.iteritems():
        print (k , ',' ,v)


def auto_regression_moving_averagess():
    print(sm.datasets.sunspots.NOTE)

    dta = sm.datasets.sunspots.load_pandas().data
    print(dta)
    print(pd.Index(sm.tsa.datetools.dates_from_range('2005', '2015')))
    dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2005', '2015'))
    del dta["YEAR"]
    dta.plot(figsize=(12,8))

    fig = plt.figure(figsize=(12,8))
    ax1 = fig.add_subplot(211)
    fig = sm.graphics.tsa.plot_acf(dta.values.squeeze(), lags=1, ax=ax1)
    ax2 = fig.add_subplot(212)
    fig = sm.graphics.tsa.plot_pacf(dta, lags=40, ax=ax2)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    # print "Date, review_count"
    # moving_averages_test()
    auto_regression_moving_averagess()
    # search1()