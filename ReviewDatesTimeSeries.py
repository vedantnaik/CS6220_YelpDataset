__author__ = 'Vedant Naik, Dixit_Patel, Akshay_Raje'

import json
import cPickle

iDict = dict() # {bid : review}

with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json") as reviewFile:
    for line in reviewFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        reviewId = lineJson.get("review_id")
        date = lineJson.get("date")

        if(iDict.keys().__contains__(businessId)):
            iDict[businessId] += "," + date
        else:
            print businessId
            iDict.update({businessId:date})

    reviewFile.close()

with open(".\iDict",'wb') as f:
    print "making file"
    cPickle.dump(iDict, f)

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

