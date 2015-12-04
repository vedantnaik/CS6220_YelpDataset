from datetime import date
from string import find
import cPickle
from datetime import datetime
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
                businessIdDict[city].append((lineJson.get("business_id"), lineJson.get("categories")))
            else:
                businessIdDict.update({city:[(lineJson.get("business_id"), lineJson.get("categories"))]})

    for k in [k1 for k1 in businessIdDict.keys() if len(businessIdDict[k1]) > 100]:
        print k, " has ", len(businessIdDict[k]), " businesses."

    """
    Here we make a file for a give city which has a dict like so:
        {bid: [categories]}

    we also make a list of bids in our city
    """
    bidsInOurCity = []
    bidCategoryDict = {}    # {bid: category list}
    for id, categories in businessIdDict[cityToConsider]:
        bidsInOurCity.append(id)
        bidCategoryDict.update({id:categories})

    with open("myDataFiles\iBusinessCategoryDict_"+cityToConsider,'wb') as f:
        print "making file"
        cPickle.dump(bidCategoryDict, f)
        f.close()
    print "business file compelte"

    count = 0
    reviewDateDict = {}
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
                # add the date of this review to a dict against bid
                if reviewDateDict.keys().__contains__(bid):
                    reviewDateDict[bid].append(rDate)
                else:
                    reviewDateDict.update({bid:[rDate]})

    print count

    with open("myDataFiles\iReviewDateDict_"+cityToConsider,'wb') as f:
        print "making file"
        cPickle.dump(reviewDateDict, f)
        f.close()

def initYearWeeks(yyyy):
    dict = {}
    dict.update({yyyy:{}})
    for i in range(53):
        dict[yyyy].update({i+1:0})
    return dict

def initYearDays(yyyy):
    dict = {}
    dict.update({yyyy:{}})
    for i in range(366):
        dict[yyyy].update({i+1:(0,0)})
    return dict

def workOnFile(cityToConsider):
    with open("myDataFiles\iReviewDateDict_"+cityToConsider,'rb') as f:
        print "reading from file"
        reviewDateDict = cPickle.load(f)
#        catBidDict, bidsInTopCats = businessIdsClubbing(cityToConsider)

        count = 0

        """
        weekCount will be of the format-
            {bid : {year : {weekNum : count}}}
        """
        weekCount = {}
        yearDayCount = {}

        for bid in [x for x in reviewDateDict.keys() if len(reviewDateDict[x]) > 100 and x == "4bEjOyTaDG24SY5TxsaUNQ"]:
            # count += 1
            weekCount.update({bid: {}})
            yearDayCount.update({bid: {}})

            for dt in sorted(reviewDateDict[bid], key=lambda d: map(int, d.split('-'))):
                # count += 1
                yyyy, mm, dd = dt.split("-")


                if not weekCount[bid].keys().__contains__(yyyy):
                    happyNewYear = initYearWeeks(yyyy)
                    weekCount[bid].update(happyNewYear)
                    yearDayCount[bid].update(initYearDays(yyyy))


                dateObj = datetime(int (yyyy), int (mm),int (dd))
                y, weekNum, weekDay = dateObj.isocalendar()
                c = weekCount[bid][yyyy][weekNum]
                weekCount[bid][yyyy][weekNum] = c+1

                yearDay = dateObj.timetuple().tm_yday
                dtO, c = yearDayCount[bid][yyyy][yearDay]
                yearDayCount[bid][yyyy][yearDay] = (dt, c+1)


        # for yyyy in yearDayCount["4bEjOyTaDG24SY5TxsaUNQ"]:
        #     for xDate, xCount in [x for x in yearDayCount["4bEjOyTaDG24SY5TxsaUNQ"][yyyy].values() if not x is (0,0)]:
        #         count += 1
        #         # print xDate, ", ", xCount
        #     print yyyy + " - " + yearDayCount["4bEjOyTaDG24SY5TxsaUNQ"][yyyy].__str__()

        for y in yearDayCount["4bEjOyTaDG24SY5TxsaUNQ"].keys():
            print "==============================================="
            for k in yearDayCount["4bEjOyTaDG24SY5TxsaUNQ"][y].keys():
                xDate, xCount = yearDayCount["4bEjOyTaDG24SY5TxsaUNQ"][y][k]
                if xCount > 0:
                    print xDate, ", ", xCount

        print count
        f.close()


def businessIdsClubbing(cityToConsider):
    with open("myDataFiles\iBusinessCategoryDict_"+cityToConsider,'rb') as f:
        print "reading from file"
        businessDict = cPickle.load(f)
        # {bid: category list}

        catBidDict = {}
        for bid in businessDict:
            for cat in businessDict[bid]:
                if cat not in catBidDict.keys():
                    catBidDict.update({cat: [bid]})
                else:
                    catBidDict[cat].append(bid)

        topCats = set()
        for c in [x for x in catBidDict.keys() if len(catBidDict[x]) > 500]:
            print c, len(catBidDict[c]), " - ", catBidDict[c]

            topCats.add(c)
        f.close()

    return catBidDict, bidsInTopCats

if __name__ == '__main__':
    cityToConsider = "Las Vegas"
    # makeFile(cityToConsider)
    workOnFile(cityToConsider)
    # businessIdsClubbing(cityToConsider)
