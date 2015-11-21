from datetime import date
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


def makeFile(cityToConsider):
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

    with open(".\ireviewDateDict_"+cityToConsider,'wb') as f:
        print "making file"
        cPickle.dump(reviewDateDict, f)
        f.close()


def initYear(yyyy):
    dict = {}
    dict.update({yyyy:{}})
    for i in range(53):
        dict[yyyy].update({i+1:0})
    return dict

def workOnFile(cityToConsider):
    with open(".\ireviewDateDict_"+cityToConsider,'rb') as f:
        print "reading from file"
        reviewDateDict = cPickle.load(f)
        count = 0

        """
        weekCount will be of the format-
            {bid : {year : {weekNum : count}}}
        """
        weekCount = {}

        for bid in [x for x in reviewDateDict.keys() if len(reviewDateDict[x]) > 100 and x == "4bEjOyTaDG24SY5TxsaUNQ"]:
            count += 1
            weekCount.update({bid: {}})

            for dt in sorted(reviewDateDict[bid], key=lambda d: map(int, d.split('-'))):
                yyyy, mm, dd = dt.split("-")
                if not weekCount[bid].keys().__contains__(yyyy):
                    happyNewYear = initYear(yyyy)
                    weekCount[bid].update(happyNewYear)

                dateObj = date(int (yyyy), int (mm),int (dd))
                weekNum = dateObj.isocalendar()[1]
                c = weekCount[bid][yyyy][weekNum]
                weekCount[bid][yyyy][weekNum] = c+1

        for yyyy in weekCount["4bEjOyTaDG24SY5TxsaUNQ"]:
            print yyyy + " - " + weekCount["4bEjOyTaDG24SY5TxsaUNQ"][yyyy].__str__()

        print count
        f.close()


if __name__ == '__main__':
    cityToConsider = "Las Vegas"
    # makeFile(cityToConsider)
    workOnFile(cityToConsider)