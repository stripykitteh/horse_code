#
# trainer_parse_test.py
# ------------------
# Loop through all of the trainers and extract the prizemoney and all other
# pieces of data.
#
# the variables we are interested in for trainers include:
#
# trainers's entire career
# -------------------------
# trainer_t0_win_sum
# trainer_t0_position_median
# trainer_t0_position_mean
# trainer_t0_percent_in_top3
# trainer_t0_percent_in_top2
# trainer_t0_percent_in_top1
# trainer_t0_num_appearancea
#

import glob
import re
import pathlib
from bs4 import BeautifulSoup

file = "/Users/phillipmonk/research_paper/html/trainers/racing_com_trainers_chris-waller_stats.html"

with open(file) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Name
trainer_name = soup.find("span", {"itemprop": "name"}).text.strip()
print("trainer_name=>" + str(trainer_name))

deets = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

# Career Wins
print("career_wins=>" + deets[0].text.strip())

# Group 1 Wins
print("group_1_wins=>" + deets[1].text.strip())

# Prize Money
print("prize_money=>" + deets[2].text.strip())

# Win %
print("win_percentage=>" + deets[3].text.strip())

# Place %
print("place_percentage=>" + deets[4].text.strip())

# Recent win %
print("recent_win_percentage=>" + deets[5].text.strip())

class_stats = soup.find("div", {"ng-show": "result.Class.length"}).find("table", {"class": "generalstats"})

for row in class_stats.tbody.find_all('tr'):
    # Find all data for each column
    columns = row.find_all('td')

    if (len(columns) == 9):

        # Class
        print("class=>" + columns[0].text.strip())
    
        # Starts
        print("starts=>" + columns[1].text.strip())

        # 1st
        print("1st=>" + columns[2].text.strip())

        # 2nd
        print("2nd=>" + columns[3].text.strip())

        # 3rd
        print("3rd=>" + columns[4].text.strip())

        # win_pct
        print("win_pct=>" + columns[5].text.strip())

        # place_pct
        print("place_pct=>" + columns[6].text.strip())

        # prize_money
        print("prize_money=>" + columns[7].text.strip())

        # P.O.T.
        print("pot=>" + columns[8].text.strip())

jockey_stats = soup.find("div", {"ng-show": "result.Jockeys.length"}).find("table", {"class": "profile"})

for row in jockey_stats.tbody.find_all('tr'):
    # Find all data for each column
    columns = row.find_all('td')

    if (len(columns) == 9):

        # Jockey
        print("jockey=>" + columns[0].text.strip())
    
        # Starts
        print("starts=>" + columns[1].text.strip())

        # 1st
        print("1st=>" + columns[2].text.strip())

        # 2nd
        print("2nd=>" + columns[3].text.strip())

        # 3rd
        print("3rd=>" + columns[4].text.strip())

        # win_pct
        print("win_pct=>" + columns[5].text.strip())

        # place_pct
        print("place_pct=>" + columns[6].text.strip())

        # prize_money
        print("prize_money=>" + columns[7].text.strip())

        # P.O.T.
        print("pot=>" + columns[8].text.strip())

prize_money_stats = soup.find("div", {"ng-show": "result.PrizeMoney.length"}).find("table", {"class": "generalstats"})

for row in prize_money_stats.tbody.find_all('tr'):
    # Find all data for each column
    columns = row.find_all('td')

    if (len(columns) == 9):

        # Trainer
        print("prize_money=>" + columns[0].text.strip())
    
        # Starts
        print("starts=>" + columns[1].text.strip())

        # 1st
        print("1st=>" + columns[2].text.strip())

        # 2nd
        print("2nd=>" + columns[3].text.strip())

        # 3rd
        print("3rd=>" + columns[4].text.strip())

        # win_pct
        print("win_pct=>" + columns[5].text.strip())

        # place_pct
        print("place_pct=>" + columns[6].text.strip())

        # prize_money
        print("prize_money=>" + columns[7].text.strip())

        # P.O.T.
        print("pot=>" + columns[8].text.strip()) 


fp.close()

exit(0)
