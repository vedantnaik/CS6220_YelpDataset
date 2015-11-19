__author__ = 'Dixit_Patel, Akshay_Raje, Vedant Naik'
import json

'''
This function assumes and removes k-v from JSON which is
empty( "{}" ) or having false/0 values, returns the same
'''
def json_cleaner_recursive(json_str):
    if isinstance(json_str, dict):
        json_str = {k: v for k, v in json_str.items() if v is not None and bool(v)}
        for k,v in json_str.items():
            if isinstance(v, dict):
                json_str[k] = json_cleaner_recursive(json_str[k])
                # print " -> ", json_cleaner_recursive(json_str[k])
        return json_str
    else:
        return json_str

'''
The recursive holder for cleaning a JSON
'''
def clean_json(json_str):
    return json_cleaner_recursive(json_str)

if __name__ == '__main__':
    line = '{"business_id": "2jXXBLPA6Qk1j6vOUXV9sQ", "full_address": "365 Convention Center DrEastsideLas Vegas, NV 89109", "hours": {}, "open": false, "categories": ["Nightlife"], "city": "Las Vegas", "review_count": 7, "name": "The Beach", "neighborhoods": ["Eastside"], "longitude": -115.155494, "state": "NV", "stars": 3.5, "latitude": 36.131763900000003, "attributes": {"Accepts Credit Cards": {}, "Music": {"dj": true, "background_music": false, "jukebox": false, "live": true, "video": false, "karaoke": false}, "Alcohol": "full_bar"}, "type": "business"}'
    line = clean_json(json.loads(line))

    print line, "-"
    # test()
