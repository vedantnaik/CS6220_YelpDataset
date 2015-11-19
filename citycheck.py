__author__ = 'Dixit_Patel'
import json


# line = '{"business_id": "2EKGrbf2_81MrtjKZeOTng", "full_address": "Kaiserstr. 93\n76133 Karlsruhe", "hours": {}, "open": false, "categories": ["Food", "Coffee & Tea"], "city": "Karlsruhe", "review_count": 5, "name": "coffee fellows", "neighborhoods": [], "longitude": 8.4091588999999995, "state": "BW", "stars": 2.5, "latitude": 49.009267600000001, "attributes": {}, "type": "business"}'
# line = line.replace("\n","")
# lineJson = json.loads(line)
# businessId = lineJson.get("business_id")
# type = lineJson.get("type")
#
# print "=====>", businessId, type


businessIdDict = {}     #   {cityName : list of business ids}
with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json") as businessFile:
    for line in [y for y in businessFile.read().split("\n") if not len(y)<1]:
        line = line.__str__()
        line = line.replace("\\n","").replace("\\t","").replace("\\r","")
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        type = lineJson.get("type")

        city = lineJson.get("city")

        if businessIdDict.keys().__contains__(city):
            businessIdDict[city].append(lineJson.get("business_id"))
        else:
            businessIdDict.update({city:[lineJson.get("business_id")]})

"""SELECT CITY YOU WANT TO WORK ON"""
cityToConsider = "Chandler"

for k in [k1 for k1 in businessIdDict.keys() if len(businessIdDict[k1]) >= 1000]:
    print k, "-", len(businessIdDict[k])

reviewDateDict = {}
bidsInOurCity = businessIdDict[cityToConsider]

with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json") as reviewFile:
    for line in reviewFile.read().split("\n"):
        line = line.__str__()
        line = line.replace("\\n","").replace("\\t","").replace("\\r","")
        lineJson = json.loads(line)
        bid = lineJson.get("business_id")
        rDate = lineJson.get("date")
        if bidsInOurCity.__contains__(bid):
            print bid
            # add the date of this review to a dict agaisnt bid
            if reviewDateDict.keys().__contains__(bid):
                reviewDateDict[bid].append(rDate)
            else:
                reviewDateDict.update({bid:[rDate]})

for review in reviewDateDict:
    print review
