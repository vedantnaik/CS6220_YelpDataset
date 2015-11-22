__author__ = 'Dixit_Patel'

from elasticsearch import Elasticsearch
from datetime import datetime

'''
search for review count occuring for
a particular year, month, date or week
with           Y    M      D       W
default = Date(D)
'''

def search_review_count(argument='M'):
    es = Elasticsearch(timeout=60)
    indexName = 'yelp'
    reviews_dates = {}
    review_search_result = es.search(index=indexName, doc_type='review', size= 5000,
                                     body={"query": {"match": {"business_id": '4bEjOyTaDG24SY5TxsaUNQ'}}})
    for doc in review_search_result['hits']['hits']:
        if argument == 'M':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').month)
        elif argument == 'Y':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').year)
        elif argument == 'D':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d'))
        elif argument == 'W':
            argument_day = str(datetime.strptime(doc['_source']['date'],'%Y-%m-%d').weekday())

        if argument_day in reviews_dates:
            reviews_dates[argument_day] = reviews_dates[argument_day] + 1
        else:
            reviews_dates[argument_day] = 1

    for k,v in reviews_dates.iteritems():
        print (str(k)+','+str(v))

    return reviews_dates

if __name__ == '__main__':
    search_review_count('W')