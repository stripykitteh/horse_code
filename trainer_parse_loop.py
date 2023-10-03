#
# trainer_parse_loop.py
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
import sys
from datetime import datetime
from decimal import Decimal
from re import sub
import csv

def only_numerics(seq):
    return ''.join(c for c in seq if (c.isdigit() or c =='.'))

# trainer fields
fields = ['trainer_name', 'career_wins', 'group_1_wins', 'prize_money', 'win_pct', 'place_pct', 'recent_win_pct', 'group_1_win_pct', 'group_1_place_pct', 'group_2_win_pct', 'group_2_place_pct', 'group_3_win_pct', 'group_3_place_pct', 'listed_win_pct', 'listed_place_pct', 'other_win_pct', 'other_place_pct']
print("fields=>", fields)

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/trainer_data.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # write the data rows
    #for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/trainers_test/*stats.html")):
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/trainers_final/*stats.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")

            # Trainer parent
            parent = []

            # Name
            trainer_name = soup.find("span", {"itemprop": "name"}).text.strip()
            print("trainer_name=>", trainer_name)
            parent.append(trainer_name)

            deets = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

            # Career Wins
            if ord(deets[0].text.strip()[0]) == 8211: # en-dash means no career wins
                career_wins = '0'
            else:
                career_wins = deets[0].text.strip()
            print("career_wins=>", career_wins)
            parent.append(career_wins)
            
            # Group 1 Wins
            if ord(deets[1].text.strip()[0]) == 8211: # en-dash means no group 1 wins
                group_1_wins = '0'
            else:
                group_1_wins = deets[1].text.strip()
            print("group_1_wins=>", group_1_wins)
            parent.append(group_1_wins)
            
            # Prize Money
            prize_money = only_numerics(deets[2].text.strip())
            print("prize_money=>" + prize_money)
            parent.append(prize_money)

            # Win %
            win_pct = only_numerics(deets[3].text.strip())
            print("win_pct=>", win_pct)
            parent.append(win_pct)
            
            # Place %
            place_pct = only_numerics(deets[4].text.strip())
            print("place_pct=>", place_pct)
            parent.append(place_pct)            

            # Recent win %
            recent_win_pct = only_numerics(deets[5].text.strip())
            print("recent_win_percentage=>", recent_win_pct)
            parent.append(recent_win_pct)

            class_stats = soup.find("div", {"ng-show": "result.Class.length"}).find("table", {"class": "generalstats"})

            for row in class_stats.tbody.find_all('tr'):
                # Find all data for each column
                columns = row.find_all('td')

                if (len(columns) == 9):

                    # win_pct
                    win_pct = only_numerics(columns[5].text.strip())
                    print("win_pct=>", win_pct)
                    parent.append(win_pct)

                    # place_pct
                    place_pct = only_numerics(columns[6].text.strip())
                    print("place_pct=>", place_pct)
                    parent.append(place_pct)

            print("parent=>", parent)
            csvwriter.writerow(parent)

        fp.close()

exit(0)
