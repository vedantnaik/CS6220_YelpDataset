__author__ = 'Dixit_Patel'

from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import OrderedDict

'''
search for review count occuring for
a particular year, month, date or week
with           Y    M      D       W
default = Date(D)
'''

def search_review_count(argument='M', business_id='4bEjOyTaDG24SY5TxsaUNQ'):
    es = Elasticsearch(timeout=60)
    indexName = 'yelp'
    reviews_dates = {}
    review_search_result = es.search(index=indexName, doc_type='review', size= 5000,
                                     body={"query": {"match": {"business_id": business_id}}})
    for doc in review_search_result['hits']['hits']:
        popularity_score = (0.7 * doc['_source']['stars'] * doc['_source']['votes']['useful'] +
                            + 0.2 * doc['_source']['stars'] * doc['_source']['votes']['cool']
                            + 0.1 * doc['_source']['stars']
                            )/ doc['_source']['stars']
        temp_date_pop_index = (datetime.strptime(doc['_source']['date'], '%Y-%m-%d'), popularity_score)
        if argument == 'M':
            # argument_day = str('%02d' % temp_date.month) + "-" + str(temp_date.year)
            argument_day = temp_date_pop_index[0].date()
        elif argument == 'Y':
            argument_day = temp_date_pop_index[0].year
        elif argument == 'D':
            argument_day = temp_date_pop_index[0].date()
        elif argument == 'W':
            argument_day = (temp_date_pop_index[0] - timedelta(days=temp_date_pop_index[0].weekday())).date()

        if argument_day in reviews_dates:
            reviews_dates[argument_day] += temp_date_pop_index[1]
        else:
            reviews_dates[argument_day] = temp_date_pop_index[1]
    #ordering
    reviews_dates = OrderedDict(sorted(reviews_dates.items(), key=lambda t: t[0]))

    # looping again for getting monthly date
    if argument == 'M':
        months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        review_months = OrderedDict({})
        for yr in range(reviews_dates.keys()[0].year, reviews_dates.keys()[len(reviews_dates) - 1].year + 1):
            for k in months:
                month = str('%02d' % int(k)) + "-" + str(yr)
                review_months[month] = 0.1


        for k, v in reviews_dates.iteritems():
            month = str('%02d' % k.month) + "-" + str(k.year)
            review_months[month] = review_months[month] + v

        reviews_dates = review_months

    with open('resources/year_all_review_count_'+business_id+'.csv', 'w+') as f:
        f.write('Date,review_count')
        f.write('\n')
        for k, v in reviews_dates.iteritems():
            print (str(k)+','+str(v))
            f.write(str(k)+','+str(v))
            f.write('\n')


    return reviews_dates

'''
ref:
http://stackoverflow.com/questions/3424899/whats-the-simplest-way-to-subtract-a-month-from-a-date-in-python
'''
def monthdelta(date, delta):
    m, y = (date.month+delta) % 12, date.year + ((date.month)+delta-1) // 12
    if not m: m = 12
    d = min(date.day, [31, 29 if y % 4 == 0 and not y % 400 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m-1])
    return date.replace(day=d, month=m, year=y)

def sample_plot1():
    x = np.array([datetime(2013, 9, 28, i, 0) for i in range(24)])
    print x
    y = np.random.randint(100, size=x.shape)

    plt.plot(x,y)
    plt.show()

def sample_plot():
    x = []
    y = []

    with open(r"resources\sample_dates_2011.txt") as xfile:
        for line in xfile:
            line = line.split(',')
            x.append(datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S'))
            y.append(line[1])


    plt.plot(x,y)
    plt.show()

if __name__ == '__main__':
    search_review_count('M', 'zt1TpTuJ6y9n551sw9TaEg')
    # sample_plot()
