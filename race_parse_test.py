#
# race_parse_test.py
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

def only_numerics(seq):
    return ''.join(c for c in seq if (c.isdigit() or c =='.'))

if len(sys.argv) != 2:
    print("# arguments should be 2, exiting")
    exit(-1)

with open(sys.argv[1]) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Race Header

# Combine date and time
race_header = soup.find_all("div", {"class": "X9ezXxrYROFcJlULNUEJWQ=="})
race_datetime = datetime.strptime(race_header[1].text + " " + race_header[2].text, "%A, %d %B %Y %I:%M%p")
print("race_datetime=>", race_datetime)

# Format distance
print("race_distance=>", race_header[3].text[:-1])
print("race_class=>", race_header[4].text)

track_cond = soup.find_all("div", {"class": "flex justify-center items-center mt-2"})

# Track Condition
print("track_cond=>", track_cond[-1].text.split(" ")[1].split("\xa0")[0])

# Track Rail
track_rail_all = soup.find("div", {"class": "flex flex-col justify-center"})

track_rail = track_rail_all.find("div", {"class": "index_rdc-basic-text__AyDZW rdc-two-lines leading-tight header__trackrail__detail"})
print("track_rail=>", track_rail.text)

# Race Details
# <div class="index_rdc-basic-text__AyDZW rdc-one-line">
#race_details = soup.find_all("div", {"class": "index_rdc-basic-text__AyDZW rdc-one-line"})
#print("race_details=> " + race_details[5].text)

# Race Time
race_time_list = soup.find_all("div", {"class": "mr-6 flex"})
race_time = race_time_list[0].find_all("div", {"class": "index_rdc-basic-text__AyDZW"})
race_time_secs = sum(float(x) * 60 ** i for i, x in enumerate(reversed(race_time[1].text.split("\xa0")[0].split(':'))))
print("race_time=> ", round(race_time_secs,2))

# Prize Money
prize_money_list = soup.find_all("div", {"class": "rdc-form-parent flex"})
for element in prize_money_list:
    element_text = element.get_text()
    if "Prize Money:" in element_text:
        # need to split on &nbsp
        prize_money = Decimal(sub(r'[^\d.]', '',element_text.split("\xa0")[1]))
        print("prize_money=>", prize_money)

        
# For each horse
table_rows = soup.find_all("div", {"class": "index_rdc-table-row__XoMhX"})

for row in table_rows:
    # Finishing Position
    finishing_pos = row.find("div", {"class": "index_rdc-basic-text__AyDZW font-circular font-bold"})
    if finishing_pos is None:
        finishing_pos = row.find("div", {"class": "index_rdc-basic-text__AyDZW font-circular"})
    if finishing_pos is not None:
        if finishing_pos.text == 'SCR':
            continue
        else:
            position = int(only_numerics(finishing_pos.text))
            print("position=>", position)

    # Horse Name
    horse_data = row.find_all(True, {"class": ["index_rdc-link--label__GFZdj",
                                               "index_rdc-basic-text__AyDZW text-base text-grey-66 font-normal flex"]})
    horse_data_length = len(horse_data)
    
    if horse_data_length > 0:
        # Horse Name & Barrier
        if horse_data[0] is not None:
            print("horse_name=>", re.search(' (.*) ', horse_data[0].text).group().strip())
            print("barrier=>", only_numerics(horse_data[0].text.split(" ")[-1]))

            
        # Trainer
        if horse_data[1] is not None:        
            print("trainer=>", horse_data[1].text)

        # Jockey
        if horse_data[-1] is not None:        
            print("jockey=>", horse_data[-1].text)
    
        # Weight
        runner_details = row.find_all("div", {"class": ["index_rdc-basic-text__AyDZW",
                                                        "index_rdc-table-cell__XouUW index_rdc-table-cell__center__1nsfz"]})
        runner_details_length = len(runner_details)

        print("weight=>", only_numerics(runner_details[6].text))

        # Prize ($)
        if ord(runner_details[7].text[0]) == 8211: # en-dash means no prize money
            prize = 0
        else:
            prize = Decimal(sub(r'[^\d.]', '',runner_details[7].text))
        print("prize=>", prize)

        # 800m/400m
        print("800m=>", only_numerics(runner_details[8].text.split('/')[0]))
        print("400m=>", only_numerics(runner_details[8].text.split('/')[1]))

        # Margin
        if position == 1:
            margin = 0
        else:
            margin = only_numerics(runner_details[9].text)
        print("margin=>", margin)

        # Comments
        #print("comments=>", runner_details[10].text)

        # SP
        sp = only_numerics(runner_details[11].text)
        if sp == '':
            sp = 0
        print("sp=>", sp)

        # S-TAB win
        if runner_details_length > 12:
            s_tab_win = only_numerics(runner_details[12].text)
            if s_tab_win == '':
                s_tab_win = 0
            print("s_tab_win=>", s_tab_win)

            # S-TAB place
            s_tab_place = only_numerics(runner_details[13].text)
            if s_tab_place == '':
                s_tab_place = 0
            print("s_tab_place=>", s_tab_place)
        
fp.close()

exit(0)
