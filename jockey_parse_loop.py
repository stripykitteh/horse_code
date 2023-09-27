#
# jockey_parse_test.py
# ------------------
# Loop through all of the jockeys and extract the prizemoney and all other
# pieces of data.
#
# the variables we are interested in for jockeys include:
#
# jockey's entire career      jockey's last 5 races
# -------------------------   -------------------------
# jockey_t0_prestige_max      jockey_t5_prestige_max
# jockey_t0_prestige_median   jockey_t5_prestige_median
# jockey_t0_prestige_mean     jockey_t5_prestige_mean
# jockey_t0_win_max           jockey_t5_win_max
# jockey_t0_win_sum           jockey_t5_win_sum
# jockey_t0_win_mean          jockey_t5_win_mean
# -                           -
# -                           -
# jockey_t0_position_median   jockey_t5_position_mean
# jockey_t0_position_mean     -
# jockey_t0_percent_in_top3   jockey_t5_percent_in_top3
# jockey_t0_percent_in_top2   jockey_t5_percent_in_top2
# jockey_t0_percent_in_top1   jockey_t5_percent_in_top1
# -
# -
# -
# jockey_t0_no_of_appearances
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

# jockey fields
fields = ['jockey_name', 'career_wins', 'group_1_wins', 'prize_money', 'win_pct', 'recent_win_pct', 'group_1_win_pct', 'group_1_place_pct', 'group_2_win_pct', 'group_2_place_pct', 'group_3_win_pct', 'group_3_place_pct', 'listed_win_pct', 'listed_place_pct', 'other_win_pct', 'other_place_pct']
print("fields=>", fields)

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/jockey_data.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # write the data rows
    #for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/jockeys_test/*stats.html")):
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/jockeys_final/*stats.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")

            # Race parent
            parent = []

            # Name
            jockey_name = soup.find("span", {"itemprop": "name"}).text.strip()
            print("jockey_name=>", jockey_name)
            parent.append(jockey_name)

            deets = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

            # Career Wins
            career_wins = deets[2].text.strip()
            print("career_wins=>", career_wins)
            parent.append(career_wins)

            # Group 1 Wins
            group_1_wins = deets[3].text.strip()
            print("group_1_wins=>", group_1_wins)
            parent.append(group_1_wins)

            # Prize Money
            prize_money = only_numerics(deets[4].text.strip())
            print("prize_money=>", prize_money)
            parent.append(prize_money)
            
            # Win %
            win_pct = only_numerics(deets[5].text.strip())
            print("win_pct=>", win_pct)
            parent.append(win_pct)
            
            # Recent win %
            recent_win_pct = only_numerics(deets[6].text.strip())
            print("recent_win_pct=>", recent_win_pct)
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
