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


import glob
import re
import pathlib
from bs4 import BeautifulSoup

file = "/Users/phillipmonk/research_paper/html/races/racing_com_form_2023-08-09_warwick-farm_race_4.html"


with open(file) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Race Header
race_header = soup.find_all("div", {"class": "X9ezXxrYROFcJlULNUEJWQ=="})

print("race_date=> " + race_header[1].text)
print("race_tod=> " + race_header[2].text)
print("race_distance=> " + race_header[3].text)
print("race_class=> " + race_header[4].text)

track_cond = soup.find_all("div", {"class": "flex justify-center items-center mt-2"})

# Track Condition
print("track_cond=> " + track_cond[1].text.split("\xa0")[0])

# Track Rail
track_rail_all = soup.find("div", {"class": "flex flex-col justify-center"})

track_rail = track_rail_all.find("div", {"class": "index_rdc-basic-text__AyDZW rdc-two-lines leading-tight header__trackrail__detail"})

print("track_rail=> " + track_rail.text)

# Race Details
# <div class="index_rdc-basic-text__AyDZW rdc-one-line">

race_details = soup.find_all("div", {"class": "index_rdc-basic-text__AyDZW rdc-one-line"})

print("race_details=> " + race_details[5].text)

# Race Time

race_time_list = soup.find_all("div", {"class": "mr-6 flex"})
race_time = race_time_list[0].find_all("div", {"class": "index_rdc-basic-text__AyDZW"})

print("race_time=> " + race_time[1].text.split("\xa0")[0])

# Prize Money

prize_money_list = soup.find_all("div", {"class": "rdc-form-parent flex"})
for element in prize_money_list:
    element_text = element.get_text()
    if "Prize Money:" in element_text:
        # need to split on &nbsp
        prize_money = element_text.split("\xa0")[1]
        print("prize_money=>" + prize_money)

# For each horse

table_rows = soup.find_all("div", {"class": "index_rdc-table-row__XoMhX"})

for row in table_rows:
    print(row.get_text())
    # Finishing Position
    finishing_pos = row.find("div", {"class": "index_rdc-basic-text__AyDZW font-circular font-bold"})
    if finishing_pos is None:
        finishing_pos = row.find("div", {"class": "index_rdc-basic-text__AyDZW font-circular"})
    if finishing_pos is not None:
        print("finishing_pos=> " + finishing_pos.text)

    # Horse Name
    horse_data = row.find_all("span", {"class": "index_rdc-link--label__GFZdj"})
    horse_data_length = len(horse_data)

    if horse_data_length > 0:
        # Horse Name
        if horse_data[0] is not None:
            print("horse_name=> " + horse_data[0].text)

        # Trainer
        if horse_data[1] is not None:        
            print("trainer=>" + horse_data[1].text)

        # Jockey
        if horse_data[2] is not None:        
            print("jockey=>" + horse_data[2].text)
    
        # Weight
        runner_details = row.find_all("div", {"class": "index_rdc-basic-text__AyDZW"})
        runner_details_length = len(runner_details)

        print("runner_details_length=>" + str(runner_details_length))
        print("weight=>" + runner_details[5].text)

        # Prize ($)
        print("prize=>" + runner_details[6].text)

        # 800m/400m
        print("800m_400m=>" + runner_details[7].text)

        # Margin
        print("margin=>" + runner_details[8].text)

        # Comments
        print("comments=>" + runner_details[9].text)

        # SP
        print("sp=>" + runner_details[10].text)

        # S-TAB win
        if runner_details_length > 11:
            print("s_tab_win=>" + runner_details[11].text)

            # S-TAB place
            print("s_tab_place=>" + runner_details[12].text)
        
fp.close()

exit(0)
