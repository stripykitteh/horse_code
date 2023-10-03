#
# sectionals_parse_loop.py
# ------------------------
# Loop through all of the races and extract the sectional data
#

import glob
import re
import pathlib
from bs4 import BeautifulSoup
import sys
from datetime import datetime
from decimal import Decimal
from re import sub
import csv

def only_numerics(seq):
    return ''.join(c for c in seq if (c.isdigit() or c =='.'))

# race fields
fields = ['race_course', 'race_no', 'date', 'horse_name', 'r1_l8', 'r2_l8', 'r3_l8', 'r4_l8', 'r5_l8', 'r1_l6', 'r2_l6', 'r3_l6', 'r4_l6', 'r5_l6', 'r1_l4', 'r2_l4', 'r3_l4', 'r4_l4', 'r5_l4', 'r1_l2', 'r2_l2', 'r3_l2', 'r4_l2', 'r5_l2']
print("fields=>", fields)

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/sectional_data.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # write the data rows
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/sectionals_test/*.html")):
    #for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/sectionals/*.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")

            # Race Parent
            parent = []

            # Course
            race_course = file.split("_")[8].split("-")[0]            
            if race_course in ("royal", "rosehill"):
                race_course += "-" + file.split("_")[8].split("-")[1]
            parent.append(race_course)      

            # Race No
            race_no = file.split("_")[9].split("-")[-1]
            parent.append(race_no)

            # Date
            date = file.split("_")[8].split("-")[-1]           
            parent.append(date[0:4] + "-" + date[4:6] + "-" + date[6:8])


            sectionals_blocks = soup.find_all("div", {"analytics-tag": "Sectionals"})

            for sectional_block in sectionals_blocks:

                # Race child
                child = []
                
                horse_name_str = sectional_block.find("strong", {"data-analytics": "Form Guide : Sectionals : Horse Profile"})

                # Horse Name
                horse_name = horse_name_str.text.strip().split(" ", 1)[-1]
                print("horse_name=>", horse_name)
                child.append(horse_name)
                
                sectional_rows = sectional_block.find_all("table", {"class": "generic-table__table"})

                for sectional_row in sectional_rows:
                    
                    _800_times = sectional_row.find_all("td", {"class": "generic-table__col--runnerTimeDifferenceL800"})
                    for _800_time in _800_times:
                        print("_800_time=>", _800_time.text)
                        if _800_time.text == "-":
                            child.append(0)
                        else:
                            child.append(_800_time.text)

                    # pad values if there are less than 5
                    if len(_800_times) > 0:
                        for i in range(len(_800_times), 5):
                            child.append(0)
                
                    _600_times = sectional_row.find_all("td", {"class": "generic-table__col--runnerTimeDifferenceL600"})
                    for _600_time in _600_times:
                        print("_600_time=>", _600_time.text)              
                        if _600_time.text == "-":
                            child.append(0)
                        else:
                            child.append(_600_time.text)

                    # pad values if there are less than 5
                    if len(_600_times) > 0:
                        for i in range(len(_600_times), 5):
                            child.append(0)
                        
                    _400_times = sectional_row.find_all("td", {"class": "generic-table__col--runnerTimeDifferenceL400"})
                    for _400_time in _400_times:
                        print("_400_time=>", _400_time.text)
                        if _400_time.text == "-":
                            child.append(0)
                        else:
                            child.append(_400_time.text)

                    # pad values if there are less than 5
                    if len(_400_times) > 0:
                        for i in range(len(_400_times), 5):
                            child.append(0)
                        
                    _200_times = sectional_row.find_all("td", {"class": "generic-table__col--runnerTimeDifferenceL200"})
                    for _200_time in _200_times:
                        print("_200_time=>", _200_time.text)
                        if _200_time.text == "-":
                            child.append(0)
                        else:
                            child.append(_200_time.text)

                    # pad values if there are less than 5
                    if len(_200_times) > 0:
                        for i in range(len(_400_times), 5):
                            child.append(0)
                        
                print("parent=>", parent)            
                print("child=>", child)
                # only write the row to disk if there is some sectional data
                if (len(child) > 1):
                    csvwriter.writerow(parent + child)
    
        fp.close()

    csvfile.close()

exit(0)
