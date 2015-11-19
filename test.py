__author__ = 'Dixit_Patel'
import json
def test():
    def recursive(hash_thing):
        if isinstance(hash_thing, dict):
            hash_thing = {k: v for k, v in hash_thing.items() if v is not None}
            for k,v in hash_thing.items():
                if isinstance(v, dict):
                    hash_thing[k] = recursive(hash_thing[k])
                    print " sa ", recursive(hash_thing[k])
            return hash_thing
        else:
            return hash_thing

    line = '{"business_id": "7VaXyrIw57IFNXzhYFn16g", "full_address": "8320 W Hayden Rd Scottsdale, AZ 85258", "hours": {"Monday": {"close": "18:00", "open": "06:30"}, "Tuesday": {"close": "18:00", "open": "06:30"}, "Friday": {"close": "18:00", "open": "06:30"}, "Wednesday": {"close": "18:00", "open": "06:30"}, "Thursday": {"close": "18:00", "open": "06:30"}, "Sunday": {"close": "18:00", "open": "07:00"}, "Saturday": {"close": "18:00", "open": "07:00"}}, "open": false, "categories": ["Food", "Juice Bars & Smoothies", "Pets", "Pet Stores"], "city": "Scottsdale", "review_count": 3, "name": "In The Raw", "neighborhoods": [], "longitude": -111.89871309999999, "state": "AZ", "stars": 2.5, "latitude": 33.557718100000002, "attributes": {"Parking": {"garage": false, "street": false, "validated": false, "lot": false, "valet": false}, "Accepts Credit Cards": {}, "Price Range": 2}, "type": "business"}'
    line = recursive(json.loads(line))

    print line, "-"

if __name__ == '__main__':
    test()