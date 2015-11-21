__author__ = 'Dixit_Patel'
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def test():
    def recursive(hash_thing):
        if isinstance(hash_thing, dict):
            hash_thing = {k: v for k, v in hash_thing.items() if v is not None}
            for k,v in hash_thing.items():
                if isinstance(v, dict):
                    hash_thing[k] = recursive(hash_thing[k])
                    print(" sa ", recursive(hash_thing[k]))
            return hash_thing
        else:
            return hash_thing

    line = '{"business_id": "7VaXyrIw57IFNXzhYFn16g", "full_address": "8320 W Hayden Rd Scottsdale, AZ 85258", "hours": {"Monday": {"close": "18:00", "open": "06:30"}, "Tuesday": {"close": "18:00", "open": "06:30"}, "Friday": {"close": "18:00", "open": "06:30"}, "Wednesday": {"close": "18:00", "open": "06:30"}, "Thursday": {"close": "18:00", "open": "06:30"}, "Sunday": {"close": "18:00", "open": "07:00"}, "Saturday": {"close": "18:00", "open": "07:00"}}, "open": false, "categories": ["Food", "Juice Bars & Smoothies", "Pets", "Pet Stores"], "city": "Scottsdale", "review_count": 3, "name": "In The Raw", "neighborhoods": [], "longitude": -111.89871309999999, "state": "AZ", "stars": 2.5, "latitude": 33.557718100000002, "attributes": {"Parking": {"garage": false, "street": false, "validated": false, "lot": false, "valet": false}, "Accepts Credit Cards": {}, "Price Range": 2}, "type": "business"}'
    line = recursive(json.loads(line))

    print(line, "-")
def small_date():
    ar = []
    with open(r"C:\yelp_dataset_challenge_academic_dataset\yelp_academic_dataset_"+'review_t'+".json") as xFile:
        for line in xFile:
            line_json = json.loads(line)
            del line_json['text']
            ar.append(line_json)

    ar = sorted(ar, key=lambda k: k['date'], reverse=False)
    print('ar',  len(ar),  ar)
    # print('ar',  len(as),  as)

def tsPandas():
    print ("ts")
    df = pd.read_csv('resources/table.csv')

    df = pd.read_csv('resources/table.csv', index_col='Date', parse_dates=True)

    # print df.head()
    # print df.tail()


    close_px = df['Adj Close']

    close_px = close_px.sort_index(ascending=True)
    close_px = close_px.tail(500)
    mavg = pd.rolling_mean(close_px, 40)

    close_px.plot(label='Close')
    mavg.plot(label='mavg')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    print "start"
    tsPandas()