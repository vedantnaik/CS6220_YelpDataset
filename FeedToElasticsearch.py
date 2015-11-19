__author__ = 'Vedant Naik, Dixit_Patel, Akshay_Raje'

import json
from elasticsearch import Elasticsearch
import util
es = Elasticsearch()
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
'''
def insert_business_json(name=""):
    num_lines = sum(1 for line in open('C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_'+name+'.json'))
    print "Records of ", name, " : ", num_lines
    count = 0
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_"+name+".json") as xFile:
        for line in xFile:

            business_json = json.loads(line)
            business_id = business_json.get('business_id')

            business_json['location'] = {'lat': business_json.get('latitude'), 'lon': business_json.get('longitude')}
            del business_json['latitude']
            del business_json['longitude']

            business_json = util.clean_json(business_json)
            count += 1
            print business_json
            print business_id, " ", business_json.get("type"), " -> ", business_json.get('business_id')

            reviews = read_review_in_style('review', business_id)
            business_json['review'] = []
            business_json['review'].extend(reviews)

            es.index(index=indexName,
                     doc_type=business_json.get("type"),
                     id=business_json.get('business_id'),
                     body=business_json, timeout=30)

    xFile.close()
    print "Records inserted ", count

'''
generic JSON inserting for other types
such as tip and others
'''
def insert_generic_json(name="", special_id=""):
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_"+name+".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)

            print "Inserting ", line_json.get("type"), " -> ", line_json.get('special_id')
            if special_id == '':
                es.index(index=indexName, doc_type=line_json.get("type"), body=line_json, timeout=30)
            else:
                es.index(index=indexName, doc_type=line_json.get("type"), id=line_json.get(special_id), body=line_json, timeout=30)

    xFile.close()

'''
update business by making a datatype of review inside business
'''
def update_with_review_json(name='', business_id=''):

    reviews = read_review_in_style(name, business_id)
    business_search_result = es.get(index='yelp', doc_type='business', id=business_id)

    business_search_result['_source']['review'] = []
    business_search_result['_source']['review'].extend(reviews)

    es.index(index=indexName, doc_type=business_search_result.get('_type'), id=business_search_result.get('_id'), body=business_search_result, timeout=30)


'''
yelp dataset follows a particular style of having all
reviews for a particular business_id grouped together.
after a particular group of business_id is found and appended
into same_business_id_reviews it breaks with the help of a flag
'''
def read_review_in_style(name='', business_id=''):
    first_found = False
    same_business_id_reviews = []
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_"+name+".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)
            if(line_json.get('business_id') == business_id):
                del line_json['type']
                same_business_id_reviews.append(line_json)
                first_found = True
            elif(first_found):
                break
    xFile.close()
    return same_business_id_reviews

def start_insertion():
    # starts with inserting mappings for es
    insert_mappings()

    # looks like business needs more attention
    insert_business_json("business")

    # insert tip for now
    # insert_generic_json("tip")

    # insert review now, called inside business now
    # insert_review_json("review")
    # update_with_review_json("review_t", "vcNAWiLM4dR7D2nwwJ7nCA")

if __name__ == '__main__':
    start_insertion()
