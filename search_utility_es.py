__author__ = 'Dixit_Patel'

from elasticsearch import Elasticsearch
from datetime import datetime
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
        if argument == 'M':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').month)
        elif argument == 'Y':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').year)
        elif argument == 'D':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').date())
        elif argument == 'W':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').weekday())

        if argument_day in reviews_dates:
            reviews_dates[argument_day] = reviews_dates[argument_day] + 1
        else:
            reviews_dates[argument_day] = 1
    #ordering
    reviews_dates = OrderedDict(sorted(reviews_dates.items(), key=lambda t: t[0]))


    with open('resources/year_all_review_count_'+business_id+'.csv', 'w+') as f:
        f.write('Date,review_count')
        f.write('\n')
        for k,v in reviews_dates.iteritems():
            print (str(k)+','+str(v))
            f.write(str(k)+','+str(v))
            f.write('\n')

    return reviews_dates

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
    search_review_count('D', '4bEjOyTaDG24SY5TxsaUNQ')
    # sample_plot()
