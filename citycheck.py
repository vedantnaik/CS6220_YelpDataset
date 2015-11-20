from string import find
import cPickle

__author__ = 'Dixit_Patel'
import json

"""
input: "abcdnsdkfjd "text": "sdfnkjsdfkjbd", "type": "review" sdfnsdkjfnksdf"
output: "abcdnsdkfjd "text": "", "type": "review" sdfnsdkjfnksdf"
"""
def removeText(str):
    startIndex = find(str, "\"text\":")
    startIndex += 9
    return str[0:startIndex] + str[str.rfind("\", \"type\":"):len(str)]

# line = '{"business_id": "2EKGrbf2_81MrtjKZeOTng", "full_address": "Kaiserstr. 93\n76133 Karlsruhe", "hours": {}, "open": false, "categories": ["Food", "Coffee & Tea"], "city": "Karlsruhe", "review_count": 5, "name": "coffee fellows", "neighborhoods": [], "longitude": 8.4091588999999995, "state": "BW", "stars": 2.5, "latitude": 49.009267600000001, "attributes": {}, "type": "business"}'
# line = line.replace("\n","")
# lineJson = json.loads(line)
# businessId = lineJson.get("business_id")
# type = lineJson.get("type")
#
# print "=====>", businessId, type

def makeFile():
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
    count = 0

    with open(r".\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_review.json") as reviewFile:
        for line in [l for l in reviewFile.read().split("\n") if len(l) > 0]:
            line = line.__str__().decode("utf8")
            line = line.replace("\\n","").replace("\\t","").replace("\\r","").replace("\\u","").replace("\\","").replace("'","")

            line = removeText(line)
            try:
                lineJson = json.loads(line)
            except ValueError:
                print count
                print line
                print "exited with some problem"
                exit(0)

            bid = lineJson.get("business_id")
            rDate = lineJson.get("date")
            if bidsInOurCity.__contains__(bid):
                count += 1
                #print bid
                # add the date of this review to a dict agaisnt bid
                if reviewDateDict.keys().__contains__(bid):
                    reviewDateDict[bid].append(rDate)
                else:
                    reviewDateDict.update({bid:[rDate]})

    print count

    with open(".\ireviewDateDict",'wb') as f:
        print "making file"
        cPickle.dump(reviewDateDict, f)
        f.close()

def workOnFile():

    with open(".\ireviewDateDict",'rb') as f:
        print "reading from file"
        reviewDateDict = cPickle.load(f)
        count = 0
        for bid in [x for x in reviewDateDict.keys() if len(reviewDateDict[x]) > 200]:
            count += 1
            print "got this", sorted(reviewDateDict[bid], key=lambda d: map(int, d.split('-')))

        print count
        f.close()


if __name__ == '__main__':
    #makeFile()
    workOnFile()