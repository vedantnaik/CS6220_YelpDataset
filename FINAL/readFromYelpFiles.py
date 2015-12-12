import csv
import os
import shutil
import subprocess

__author__ = 'Vedant'
from datetime import date
from string import find
import cPickle
from datetime import datetime, timedelta, date
import json
from collections import OrderedDict

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
        dict[yyyy].update({i+1:1})
    return dict

def initYearDays(yyyy):
    dict = {}
    dict.update({yyyy:{}})
    for i in range(366):
        dict[yyyy].update({i+1:(0,0)})
    return dict

def initYearMonths(yyyy):
    """
    GIVES:
    {yyyy : {mm : count}}
    """
    dict = {}
    dict.update({yyyy:{}})
    for i in range(12):
        dict[yyyy].update({i+1:1})
    return dict

def getTimeSeriesCartridge(STARTYEAR=2004,ENDYEAR=2016):
    cartridge = {}
    for y in range(STARTYEAR,ENDYEAR):
        cartridge.update(initYearMonths(y))
    return cartridge

def getWeeklyTimeSeriesCartridge(STARTYEAR=2004,ENDYEAR=2016):
    cartridge = {}
    for y in range(STARTYEAR,ENDYEAR):
        cartridge.update(initYearWeeks(y))
    return cartridge


def tofirstdayinisoweek(year, week):
    ret = datetime.strptime('%04d-%02d-1' % (year, week), '%Y-%W-%w')
    if date(year, 1, 4).isoweekday() > 4:
        ret -= timedelta(days=7)
    return ret

def getConfidence(ts):
    avgArray = {}
    for yyyy in ts.keys():
        avg = 0
        for mm in ts[yyyy]:
            avg+=ts[yyyy][mm]
        avgArray.update({yyyy:avg/12})

    print avgArray

    # TODO
    # check upward trend
    # check downward trend



def getBusinessTSCartridge(cityToConsider, bidToConsider):
    with open("myDataFiles\iReviewDateDict_"+cityToConsider,'rb') as f:
        print "reading from file"
        reviewDateDict = cPickle.load(f)

        # timeseries dict {yyyy : {mm : count}} from start year to end year
        return_ts=getTimeSeriesCartridge(STARTYEAR=2004,ENDYEAR=2016)

        # list of review dates for that bID
        dates=sorted(reviewDateDict[bidToConsider], key=lambda d: map(int, d.split('-')))
        return_startYear=min(2013,int(dates[0].split("-")[0])+1)

        for d in dates:
            yyyy, mm, dd = [int(x) for x in d.split("-")]
            return_ts[yyyy][mm] += 1

        # return_startYear, return_confidence = getConfidence(return_ts)

        maxRC = 0
        for x in return_ts.keys():
            print x, return_ts[x]
            maxOfYear = max(return_ts[x].values())
            if maxRC < maxOfYear:
                maxRC = maxOfYear

        maxRC *= 1.2

        return return_ts, return_startYear, maxRC


def writeCartridge(cartridge, bid):
    with open('resources/businesses/'+bid+'/'+bid+'_cartridge.csv', 'w+') as f_cart:
        f_cart.write('date,review_count')
        f_cart.write('\n')
        for y in cartridge.keys():
            for m in cartridge[y].keys():
                f_cart.write(y.__str__() + "/" + m.__str__() + "," + cartridge[y][m].__str__())
                f_cart.write("\n")
        f_cart.close()


def makeResourceFiles(bidsToConsider):

    if os.path.exists("./resources/seasonalplots/"): shutil.rmtree("./resources/seasonalplots/")
    os.makedirs("./resources/seasonalplots/")
    if os.path.exists("./resources/holtwintersplots/"): shutil.rmtree("./resources/holtwintersplots/")
    os.makedirs("./resources/holtwintersplots/")
    if os.path.exists("./resources/autoarimaplots/"): shutil.rmtree("./resources/autoarimaplots/")
    os.makedirs("./resources/autoarimaplots/")

    for bid in bidsToConsider:
        dir = "./resources/businesses/"+bid
        if os.path.exists(dir): shutil.rmtree(dir)
        os.makedirs(dir)

    with open('resources/start_years.csv', 'w+') as f:
            f.write('bid,startyear,maxRC')
            f.write('\n')
            for bid in bidsToConsider:
                cartridge, startYear, maxRC = getBusinessTSCartridge(cityToConsider, bid)
                writeCartridge(cartridge, bid)
                f.write(bid.__str__()+","+startYear.__str__()+","+maxRC.__str__())
                f.write('\n')
            f.close()


def getStartYearMaxRC():
    retDict = {}    # {bid:(startYear,maxRC)}
    with open('resources/start_years.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            bid, startyear, maxRC = row
            retDict.update({bid:(startyear,maxRC)})
        f.close()
    return retDict


def getBidsFromGist():
    retList = []    # [bid]
    with open('resources/top_10_percent_businesses_Restaurants_Las_Vegas.csv', 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            bid, maxRC = row
            retList.append(bid)
        f.close()
    return retList


if __name__ == '__main__':
    cityToConsider = "Las Vegas"
    #makeFile(cityToConsider)

    # trial list
    # bidsToConsider=["4bEjOyTaDG24SY5TxsaUNQ","2e2e7WgqU1BnpxmQL5jbfw", "zt1TpTuJ6y9n551sw9TaEg",
    #                 "sIyHTizqAiGu12XMLX3N3g", "Xhg93cMdemu5pAMkDoEdtQ", "YNQgak-ZLtYJQxlDwN-qIg",
    #                 "tFU2Js_nbIZOrnKfYJYBBg", "CZjcFdvJhksq9dy58NVEzw", "aGbjLWzcrnEx2ZmMCFm3EA",
    #                 "AtjsjFzalWqJ7S9DUFQ4bw"]

    # debug list
    #bidsToConsider = ["OwBPjUz2o0J5K3DzcHkBtg"]

    bidsToConsider = getBidsFromGist()

    makeResourceFiles(bidsToConsider)
    syRCdict=getStartYearMaxRC()

    for bid in bidsToConsider:
        startyear=syRCdict[bid][0]
        maxRC=syRCdict[bid][1]

        subprocess.call("Rscript seasonal-decomposition.R "+bid, shell=True)
        subprocess.call("Rscript all-models.R "+bid+" "+startyear+" "+maxRC, shell=True)

        # copy graphs to folders to help make visual comparisons
        shutil.copy("./resources/businesses/"+bid+"/"+bid+"_holtwinters_plot.jpg",
                    "./resources/holtwintersplots/"+bid+"_holtwinters_plot.jpg")
        shutil.copy("./resources/businesses/"+bid+"/"+bid+"_autoarima_plot.jpg",
                    "./resources/autoarimaplots/"+bid+"_autoarima_plot.jpg")
        shutil.copy("./resources/businesses/"+bid+"/"+bid+"_seasonal_plot.jpg",
                    "./resources/seasonalplots/"+bid+"_seasonal_plot.jpg")
