from __future__ import print_function
import datetime

dt = dict()
with open("kaggle/1.csv", 'r') as f1:
    for line in f1:
        if line != "" and ("Date" not in line):
            date, count = line.split(',')
            mm, dd, yyyy = date.split("/")
            isoyear, weeknumber, weekday = datetime.date(int(yyyy), int(mm), int(dd)).isocalendar()
            if dt.has_key(int(yyyy)):
                if dt[int(yyyy)].has_key(weeknumber):
                    dt[int(yyyy)][weeknumber] += int(count)
                else:
                    dt[int(yyyy)].update({weeknumber: int(count)})
            else:
                dt.update({int(yyyy): {weeknumber : int(count)}})

with open("kaggle/1_weekly.csv", 'w') as f2:
    for yyyy in dt.keys():
        for weeknumber in dt[yyyy].keys():
            print(",".join([str(yyyy), str(weeknumber), str(dt[yyyy][weeknumber])]),file=f2)
