__author__ = 'Vedant_Naik, Dixit_Patel, Akshay_Raje'
import json
from elasticsearch import Elasticsearch

es = Elasticsearch()
indexName = "yelp"

## put mappings and index creation
def insert_mappings():
    with open(r'mappings\createIndex.json') as createIndex:
        data = json.load(createIndex)
    es.indices.create(index='yelp', body=data, ignore=400)

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
#
# with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_checkin.json") as checkinFile:
#     for line in checkinFile.read().split("\n"):
#         line = line.__str__()
#         lineJson = json.loads(line)
#         businessId = lineJson.get("business_id")
#         type = lineJson.get("type")
#         print businessId, " ", type
#
#         es.index(index=indexName,
#                  doc_type=type,
#                  id= businessId,        # TODO: check if this is right for id
#                  body=lineJson, timeout=30)
#
#     checkinFile.close()
#
#
# with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json") as reviewFile:
#     for line in reviewFile.read().split("\n"):
#         line = line.__str__()
#         lineJson = json.loads(line)
#         businessId = lineJson.get("business_id")
#         reviewId = lineJson.get("review_id")
#         userId = lineJson.get("user_id")
#         stars = lineJson.get("stars")
#         type = lineJson.get("type")
#         print businessId, " ", type
#
#         es.index(index=indexName,
#                  doc_type=type,
#                  id= businessId,        # TODO: check if this is right for id
#                  body=lineJson, timeout=30) # TODO: reviewID or businessID
#
#     reviewFile.close()
#
# with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_tip.json") as tipFile:
#     for line in tipFile.read().split("\n"):
#         line = line.__str__()
#         lineJson = json.loads(line)
#         businessId = lineJson.get("business_id")
#         userId = lineJson.get("user_id")
#         type = lineJson.get("type")
#         print businessId, " ", type
#
#         es.index(index=indexName,
#                  doc_type=type,
#                  id= businessId,        # TODO: check if this is right for id
#                  body=lineJson, timeout=30) # TODO: reviewID or businessID
#
#
#     tipFile.close()
#
# with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_user.json") as userFile:
#     for line in userFile.read().split("\n"):
#         line = line.__str__()
#         lineJson = json.loads(line)
#         userId = lineJson.get("user_id")
#         type = lineJson.get("type")
#         print userId, " ", type
#
#         es.index(index=indexName,
#                  doc_type=type,
#                  id= userId,        # TODO: check if this is right for id
#                  body=lineJson, timeout=30)   # TODO: reviewID or businessID

    # userFile.close()
