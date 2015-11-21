__author__ = 'Vedant Naik, Dixit_Patel, Akshay_Raje'

import json
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time
import util
from operator import itemgetter

es = Elasticsearch(timeout=60)
indexName = 'yelp'

'''
put mappings and index creation for
the specific type of yelp data
'''


def insert_mappings():
    with open(r'mappings\createIndex.json') as createIndex:
        data = json.load(createIndex)
    es.indices.create(index=indexName, body=data, ignore=400)


'''
just inserts business json, needs special treatment
for handling geo-location point in elasticsearch.
Involves data cleaning for JSON's as well
Now involves appending review JSON too!
**Make sure review JSON in inside previous to business json
'''


def insert_business_json(name=""):
    # num_lines = sum(1 for line in
    # open('C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_'+name+'.json'))
    # print "Records of ", name, " : ", num_lines
    count = 0
    bulk_json = []
    bulk_json_id = []
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_" + name + ".json") as xFile:
        for line in xFile:
            # if count >= 10000:
            #     break
            business_json = json.loads(line)
            business_id = business_json.get('business_id')

            business_json['location'] = {'lat': business_json.get('latitude'), 'lon': business_json.get('longitude')}
            del business_json['latitude']
            del business_json['longitude']

            business_json = util.clean_json(business_json)
            count += 1
            # print business_json
            bulk_json_id.append(business_json.get('business_id'))

            reviews = get_review_json_array('review', business_id)

            # assume the first date of review as start of business, sort!
            reviews = sorted(reviews, key=lambda k: k['date'], reverse=False)
            business_json['review'] = []
            business_json['review'].extend(reviews)
            if reviews is not None and len(reviews) > 0:
                business_json['date'] = reviews[0]['date']

            business_json['_id'] = business_json['business_id']
            business_json['_type'] = business_json['type']
            business_json['_index'] = indexName
            bulk_json.append(business_json)
            if len(bulk_json) > 10000:
                print(business_json.get("type"), " -> ", bulk_json_id)
                helpers.bulk(es, bulk_json)
                bulk_json = []
                bulk_json_id = []
                # es.index(index=indexName, doc_type=business_json.get("type"),
                # id=business_json.get('business_id'), body=business_json, timeout=30)
        print(name, " -> ", bulk_json_id)
        helpers.bulk(es, bulk_json)
    xFile.close()
    print("Records inserted ", count)


'''
generic JSON inserting for other types
such as tip and others
'''


def insert_generic_json(name="", special_id=""):
    count = 0
    print("starting ", name)
    bulk_json = []
    bulk_json_id = []
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_" + name + ".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)
            count += 1
            if special_id != '':
                # print
                # line_json['_id'] = line_json['business_id']
                # else:
                # es.index(index=indexName, doc_type=line_json.get("type"),
                # id=line_json.get(special_id), body=line_json, timeout=30)
                line_json['_id'] = line_json.get(special_id)
            bulk_json_id.append(line_json.get(special_id))
            # if count >= 100000:
            #     break
            line_json['_type'] = line_json.get("type")
            line_json['_index'] = indexName
            bulk_json.append(line_json)
            if len(bulk_json) > 10000:
                print("Inserting ", line_json.get("type"), " -> ", bulk_json_id)
                # es.index(index=indexName, doc_type=line_json.get("type"), body=line_json, timeout=30)
                helpers.bulk(es, bulk_json)
                bulk_json = []
                bulk_json_id = []

        print("Inserting ", name, " -> ", bulk_json_id)
        helpers.bulk(es, bulk_json)
    print("Records inserted ", count)
    xFile.close()


'''
update business by making a datatype of review inside business
'''


def update_with_review_json(name='', business_id=''):
    reviews = read_review_in_style(name, business_id)
    business_search_result = es.get(index=indexName, doc_type='business', id=business_id)

    business_search_result['_source']['review'] = []
    business_search_result['_source']['review'].extend(reviews)

    es.index(index=indexName, doc_type=business_search_result.get('_type'), id=business_search_result.get('_id'),
             body=business_search_result, timeout=30)


'''
get review json array given a particular business_id
'''


def get_review_json_array(name='', business_id=''):
    reviews = []
    review_search_result = es.search(index=indexName, doc_type=name, size= 5000,
                                     body={"query": {"match": {"business_id": business_id}}})
    for doc in review_search_result['hits']['hits']:
        reviews.append(doc['_source'])
    print('returning ', len(reviews), ' number of reviews for ', business_id)
    return reviews  # .sort(key= itemgetter('date'), reverse=True)


'''
yelp dataset follows a particular style of having all
reviews for a particular business_id grouped together.
after a particular group of business_id is found and appended
into same_business_id_reviews it breaks with the help of a flag
'''


def read_review_in_style(name='', business_id=''):
    first_found = False
    same_business_id_reviews = []
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_" + name + ".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)
            if line_json.get('business_id') == business_id:
                del line_json['type']
                same_business_id_reviews.append(line_json)
                first_found = True
            elif first_found:
                break
    xFile.close()
    return same_business_id_reviews


'''
function to call flush and optimize
'''


def index_flush_translog():
    # es.indices.flush_synced
    es.indices.refresh

    es.indices.flush(force=True, index=indexName, wait_if_ongoing=True)
    print('refresh')
    # index_optimize


'''
function to optimize all indices
'''


def index_optimize():
    es.indices.optimize


'''
start inserting json
'''


def start_insertion():
    start = time.clock()

    # starts with inserting mappings for es
    insert_mappings()

    # insert review before!
    insert_generic_json("review")
    # get_review_json_array('review','vcNAWiLM4dR7D2nwwJ7nCA')

    print('timetaken review', time.clock() - start, 's')

    # force a tranlog flush because we need the review data
    # to populate inside business
    index_flush_translog()

    print('timetaken flush_translog ', time.clock() - start, 's')

    # looks like business needs more attention
    insert_business_json("business")

    print('timetaken business', time.clock() - start, 's')
    # insert tip for now
    # insert_generic_json("tip")

    # insert review now, called inside business now
    # update_with_review_json("review_t", "vcNAWiLM4dR7D2nwwJ7nCA")


if __name__ == '__main__':
    start_insertion()
    