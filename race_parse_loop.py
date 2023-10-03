#
# race_parse_loop.py
# ------------------
# Loop through all of the races and extract the prizemoney and all other
# pieces of data.
#
# Date
# Time
# Distance
# Class
# Track Rating
# Track Rail
# Race Details
# Race Time
# Prize Money
# For each horse:
# * Finishing Position
# * Horse Name
# * Barrier
# * Trainer
# * Jockey
# * Weight
# * Prize ($)
# * 800m/400m position
# * Margin
# * Comments
# * SP
# * S-TAB (Win and place)
#
# Miscellania
# -----------
# * Add ability to take filename from command line
# * Write output as one line per horse in csv format
# * Fix dates and other fields that use commas
# * Convert times to seconds, i.e., 1:13.26 should be 73.26
# * Convert currency to a decimal number, i.e., $130,000 should be 130000
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
import statistics
import math

def only_numerics(seq):
    return ''.join(c for c in seq if (c.isdigit() or c =='.'))

# race fields
fields = ['race_course', 'race_no', 'datetime', 'distance', 'class', 'track_cond', 'track_rail', 'race_time', 'prize_money', 'position', 'horse_name', 'barrier', 'trainer', 'jockey', 'weight', 'prize', '800m', '400m', 'margin', 'horse_adjusted_t1_speed', 'sp', 's_tab_win', 's_tab_place']
print("fields=>", fields)

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/race_data.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # write the data rows
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/races_final/*.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")

            # Race Parent
            parent = []

            # Course
            race_course = soup.find("div", {"class": "_0bTO7kg5XVVoXUyVBR5Rzg=="}).text
            parent.append(race_course)      

            # Race No
            race_no = file.split("_")[-1].split(".")[0]
            parent.append(race_no)

            # Combine date and time
            race_header = soup.find_all("div", {"class": "X9ezXxrYROFcJlULNUEJWQ=="})
            datetime = datetime.strptime(race_header[1].text + " " + race_header[2].text, "%A, %d %B %Y %I:%M%p")
            parent.append(str(datetime))
        
            # Format distance and class
            distance = int(race_header[3].text[:-1])
            parent.append(distance)
            parent.append(race_header[4].text)

            # Track Condition
            track_cond_str = soup.find_all("div", {"class": "flex justify-center items-center mt-2"})
            track_cond = int(track_cond_str[-1].text.split(" ")[1].split("\xa0")[0])
            parent.append(track_cond)

            # Track Rail
            track_rail_all = soup.find("div", {"class": "flex flex-col justify-center"})

            track_rail = track_rail_all.find("div", {"class": "index_rdc-basic-text__AyDZW rdc-two-lines leading-tight header__trackrail__detail"})
            parent.append(track_rail.text)

            # Race Details
            # <div class="index_rdc-basic-text__AyDZW rdc-one-line">
            #race_details = soup.find_all("div", {"class": "index_rdc-basic-text__AyDZW rdc-one-line"})
            #print("race_details=> " + race_details[5].text)

            # Race Time
            race_time_list = soup.find_all("div", {"class": "mr-6 flex"})
            race_time = race_time_list[0].find_all("div", {"class": "index_rdc-basic-text__AyDZW"})
            race_time_secs = sum(float(x) * 60 ** i for i, x in enumerate(reversed(race_time[1].text.split("\xa0")[0].split(':'))))
            parent.append(str(round(race_time_secs,2)))

            # Prize Money
            prize_money_list = soup.find_all("div", {"class": "rdc-form-parent flex"})
            for element in prize_money_list:
                element_text = element.get_text()
                if "Prize Money:" in element_text:
                    # need to split on &nbsp
                    prize_money = Decimal(sub(r'[^\d.]', '',element_text.split("\xa0")[1]))
                    parent.append(str(prize_money))
        
            # For each horse
            table_rows = soup.find_all("div", {"class": "index_rdc-table-row__XoMhX"})

            for row in table_rows:

                child = []
    
                # Finishing Position
                finishing_pos = row.find("div", {"class": "index_rdc-basic-text__AyDZW font-circular font-bold"})
                if finishing_pos is None:
                    finishing_pos = row.find("div", {"class": "index_rdc-basic-text__AyDZW font-circular"})
                if finishing_pos is not None:
                    # ignore scratchings, late scratchings, failed-to-finishes, disqualifieds and lost riders etc
                    if finishing_pos.text in ['SCR', 'LSCR', 'FF', 'DQ', 'LR', 'LP', 'F', 'BD']: 
                        continue
                    else:
                        position = int(only_numerics(finishing_pos.text))
                        child.append(str(position))

                # Horse Name
                horse_data = row.find_all(True, {"class": ["index_rdc-link--label__GFZdj",
                                                           "index_rdc-basic-text__AyDZW text-base text-grey-66 font-normal flex"]})
                horse_data_length = len(horse_data)
    
                if horse_data_length > 0:
                    # Horse Name & Barrier
                    if horse_data[0] is not None:
                        child.append(re.search(' (.*) ', horse_data[0].text).group().strip())
                        child.append(only_numerics(horse_data[0].text.split(" ")[-1]))
                else:
                    continue

                # Trainer
                if horse_data[1] is not None:        
                    child.append(horse_data[1].text)

                # Jockey
                if horse_data[-1] is not None:        
                    child.append(horse_data[-1].text)
    
                # Weight
                runner_details = row.find_all("div", {"class": ["index_rdc-basic-text__AyDZW",
                                                                "index_rdc-table-cell__XouUW index_rdc-table-cell__center__1nsfz"]})
                runner_details_length = len(runner_details)

                child.append(only_numerics(runner_details[6].text))

                # Prize ($)
                if ord(runner_details[7].text[0]) == 8211: # en-dash means no prize money
                    prize = 0
                else:
                    prize = Decimal(sub(r'[^\d.]', '',runner_details[7].text))
                child.append(str(prize))

                # 800m/400m
                if ord(runner_details[8].text[0]) == 8211: # en-dash means splits weren't recorded
                    child.append("")
                    child.append("")
                else:
                    child.append(only_numerics(runner_details[8].text.split('/')[0]))
                    child.append(only_numerics(runner_details[8].text.split('/')[1]))

                # Margin
                # rarely, the margin is not recorded, use a dummy value of 5
                if runner_details[9].text == "":
                    margin = 5
                else:
                    # winner gets a margin of 0
                    if position == 1:
                        margin = 0
                    else:
                        margin = float(only_numerics(runner_details[9].text))
                child.append(margin)

                # horse_t1_speed
                # convert the margin to a distance then calculate the speed
                # 1 length ~= 2.4 metres
                horse_t1_distance = distance - (margin * 2.4)
                horse_t1_speed = (horse_t1_distance/race_time_secs) * 3.6

                # Adjust the speed
                # ----------------
                
                # We use a formula to standardise the speeds of horses over
                # different distances, basically calling a 60 sec 1000 metre
                # sprint and a 210 sec 3200 metre race the same speed and using
                # a log curve in between as appropriate.
                
                adj_distance = ((horse_t1_distance/1000)**(math.log(3.5)/math.log(3.2))*1000)/horse_t1_distance                
                # We also add a factor for the track condition.
                # Track rating 1-3 means no adjustment
                # For every point above 3, we increase the speed by 0.5%, so
                # e.g. a track rating of 7 attracts a multiplier of 1.02 (2%).

                if track_cond < 3:
                    adj_track = 1
                else:
                    adj_track = 1 + (track_cond - 3)*0.005

                horse_adjusted_t1_speed = horse_t1_speed * adj_distance * adj_track
                child.append(horse_adjusted_t1_speed)
                                
                # Comments
                #print("comments=>", runner_details[10].text)

                # SP
                sp = only_numerics(runner_details[11].text)
                if sp == '':
                    sp = 0
                child.append(str(sp))

                # S-TAB win
                if runner_details_length > 12:
                    s_tab_win = only_numerics(runner_details[12].text)
                    if s_tab_win == '':
                        s_tab_win = 0
                    child.append(str(s_tab_win))

                    # S-TAB place
                    s_tab_place = only_numerics(runner_details[13].text)
                    if s_tab_place in ('', '..'): # runner did not place or No Third Dividend (N.T.D)
                        s_tab_place = 0
                    child.append(str(s_tab_place))

                print("parent=>", parent)            
                print("child=>", child)
                csvwriter.writerow(parent + child)
    
        fp.close()

    csvfile.close()

exit(0)
