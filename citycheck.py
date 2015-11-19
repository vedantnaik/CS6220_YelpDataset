__author__ = 'Dixit_Patel'
import json


line = '{"business_id": "2EKGrbf2_81MrtjKZeOTng", "full_address": "Kaiserstr. 93\n76133 Karlsruhe", "hours": {}, "open": false, "categories": ["Food", "Coffee & Tea"], "city": "Karlsruhe", "review_count": 5, "name": "coffee fellows", "neighborhoods": [], "longitude": 8.4091588999999995, "state": "BW", "stars": 2.5, "latitude": 49.009267600000001, "attributes": {}, "type": "business"}'
line = line.replace("\n","")
lineJson = json.loads(line)
businessId = lineJson.get("business_id")
type = lineJson.get("type")

print "=====>", businessId, type


businessIdList = []
with open(r"C:\\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_business.json") as businessFile:
    for line in businessFile.read().split("\n") if len(line) > 0:
        line = line.__str__()
        line = line.replace("\\n","").replace("\\t","").replace("\\r","")
        print line, "-"
        lineJson = json.loads(line)
        businessId = lineJson.get("business_id")
        type = lineJson.get("type")
        if lineJson.get("city") == "New York":
            businessIdList.append(lineJson.get("business_id"))
print "businesslist", len(businessIdList)
reviews = []
with open(r"C:\\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json") as businessFile:
    for line in businessFile.read().split("\n"):
        line = line.__str__()
        lineJson = json.loads(line)
        if businessIdList.__contains__(lineJson.get("")):
            reviews.append(lineJson)

for review in reviews:
    print review
