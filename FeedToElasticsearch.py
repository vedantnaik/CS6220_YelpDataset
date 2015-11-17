__author__ = 'Vedant'

import re
import os
import json
from pprint import pprint
from elasticsearch import Elasticsearch

es = Elasticsearch()
indexName = "TODO_ENTER_NAME"

with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json") as businessFile:
    for line in businessFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        type = lineJson.get("type")
        print businessId, " ", type

        es.index(index=indexName,
                 doc_type=type,
                 id= businessId,        # TODO: check if this is right for id
                 body={"doc_no" : businessId,
                       "text" : line})

    businessFile.close()

with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_checkin.json") as checkinFile:
    for line in checkinFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        type = lineJson.get("type")
        print businessId, " ", type

        es.index(index=indexName,
                 doc_type=type,
                 id= businessId,        # TODO: check if this is right for id
                 body={"doc_no" : businessId,
                       "text" : line})

    checkinFile.close()


with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json") as reviewFile:
    for line in reviewFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        reviewId = lineJson.get("review_id")
        userId = lineJson.get("user_id")
        stars = lineJson.get("stars")
        type = lineJson.get("type")
        print businessId, " ", type

        es.index(index=indexName,
                 doc_type=type,
                 id= businessId,        # TODO: check if this is right for id
                 body={"doc_no" : businessId,   # TODO: reviewID or businessID
                       "text" : line})

    reviewFile.close()

with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_tip.json") as tipFile:
    for line in tipFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        userId = lineJson.get("user_id")
        type = lineJson.get("type")
        print businessId, " ", type

        es.index(index=indexName,
                 doc_type=type,
                 id= businessId,        # TODO: check if this is right for id
                 body={"doc_no" : businessId,   # TODO: reviewID or businessID
                       "text" : line})

    tipFile.close()

with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_user.json") as userFile:
    for line in userFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        userId = lineJson.get("user_id")
        type = lineJson.get("type")
        print userId, " ", type

        es.index(index=indexName,
                 doc_type=type,
                 id= userId,        # TODO: check if this is right for id
                 body={"doc_no" : userId,   # TODO: reviewID or businessID
                       "text" : line})
    userFile.close()
