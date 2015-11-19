__author__ = 'Vedant Naik, Dixit_Patel, Akshay_Raje'

import json
from elasticsearch import Elasticsearch

es = Elasticsearch()
indexName = 'yelp'

## put mappings and index creation

def insert_mappings():
    with open(r'mappings\createIndex.json') as createIndex:
        data = json.load(createIndex)
    es.indices.create(index=indexName, body=data, ignore=400)

def insert_business_json(name=""):
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_"+name+".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)
            business_id = line_json.get('business_id')

            line_json['location'] = {'lat': line_json.get('latitude'), 'lon': line_json.get('longitude')}
            del line_json['latitude']
            del line_json['longitude']

            line_json = {k: v for k, v in line_json.items() if v is not None}

            # print line_json
            print business_id, " ", line_json.get("type"), " -> ", line_json.get('business_id')

            es.index(index=indexName,
                     doc_type=line_json.get("type"),
                     id=line_json.get('business_id'),
                     body=line_json, timeout=30)

        xFile.close()

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

def start_insertion():
    # starts with inserting mappings for es
    insert_mappings()

    # looks like business needs more attention
    insert_business_json("business")

    # insert tip for now
    insert_generic_json("tip")


if __name__ == '__main__':
    start_insertion()
