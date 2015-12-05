from __future__ import print_function
import datetime
with open("./resources/year_all_review_count_zt1TpTuJ6y9n551sw9TaEg_smooth.csv", 'r') as f1, \
        open("./resources/zt1TpTuJ6y9n551sw9TaEg_smoothed_data.csv", 'w') as f2:
    print("Year,Week_Num,Review_Count", file=f2)
    for line in f1:
        if (not line.__contains__("Date")) and line != "":
            full_date, count = line.replace("\n", "").split(',')
            year, month, day = full_date.split('-')
            iso_year, week_number, weekday = datetime.date(int(year), int(month), int(day)).isocalendar()
            print(",".join([str(iso_year), str(week_number), count]), file=f2)
