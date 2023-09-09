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

file = "/Users/phillipmonk/research_paper/html/jockeys/racing_com_jockeys_kerrin-mcevoy_form.html"

with open(file) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Name
jockey_name = soup.find("span", {"itemprop": "name"}).text.strip()
print("jockey_name=>" + str(jockey_name))

deets = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

# Age
print("age=>" + deets[0].text.strip())
                   
# Weight
print("weight=>" + deets[1].text.strip())

# Career Wins
print("career_wins=>" + deets[2].text.strip())

# Group 1 Wins
print("group_1_wins=>" + deets[3].text.strip())

# Prize Money
print("prize_money=>" + deets[4].text.strip())

# Win %
print("win_percentage=>" + deets[5].text.strip())

# Recent win %
print("jockey_t50_win_pct=>" + deets[6].text.strip())

past_races = soup.find("table", {"class": "form"})

for row in past_races.tbody.find_all('tr'):
    # Find all data for each column
    columns = row.find_all('td')

    if (len(columns) == 21):

        for i in range(len(columns)):
            print("column " + str(i) + ":" + columns[i].text.strip())

        # * Position
        pos = columns[0].text.strip()
        print("pos=>" + pos)

        # * Horse
        horse = columns[4].text.strip().split('\n')[1]
        print("horse=>" + horse)

        # * Trainer
        trainer = columns[5].text.strip().split('\n')[0].split('\xa0')[1]
        print("trainer=>" + trainer)

        # * Prize
        prize = columns[11].text.strip().split('\n')[0]
        print("prize=>" + prize)

        # * Class
        _class = columns[11].text.strip().split('\n')[-1]
        print("_class=>" + _class)

        # * Jockey
        if prize[0] == "$":
            jockey = columns[5].text.strip().split('\n')[1].split('\xa0')[1]
        else:
            jockey = ""
        print("jockey=>" + jockey)
        
        # * Track/Date
        race_date = columns[6].text.strip()
        print("track_date=>" + race_date)
        
        # * Dist
        dist = columns[9].text.strip().split('\n')[0]
        print("dist=>" + dist)

        # * Cond
        cond = columns[9].text.strip().split('\n')[2]
        print("cond=>" + cond)

        # * Weight        
        weight = columns[12].text.strip().split('\n')[0]
        print("weight=>" + weight)

        # * 800M
        if prize[0] == "$":
            _800m = columns[13].text.strip().split('\n')[0]
        else:
            _800m = ""
        print("_800m=>" + _800m)            
            
        # * 400M
        if prize[0] == "$":
            _400m = columns[13].text.strip().split('\n')[3]
        else:
            _400m = ""
        print("_400m=>" + _400m)

        # * Margin
        margin = columns[14].text
        print("margin=>" + margin)
        
        # * Rating
        rating = columns[15].text.strip()
        print("rating=>" + rating)
        
        # com = columns[9].text.strip()

        # * Odds
        if prize[0] == "$":
            odds = columns[17].text.strip().split('\n')[0]
        else:
            odds = ""
        print("odds=>" + odds)

        # * Odds Source
        if prize[0] == "$":
            odds_source = columns[17].text.strip().split('\n')[1]
        else:
            odds_source = ""
        print("odds_source=>" + odds_source)
        
fp.close()

file = "/Users/phillipmonk/research_paper/html/jockeys/racing_com_jockeys_kerrin-mcevoy_stats.html"

with open(file) as fp:
    soup = BeautifulSoup(fp, "html.parser")

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

trainer_stats = soup.find("div", {"class": "box-content nopadding trainers"}).find("table", {"class": "profile"})

for row in trainer_stats.tbody.find_all('tr'):
    # Find all data for each column
    columns = row.find_all('td')

    if (len(columns) == 9):

        # Trainer
        print("trainer=>" + columns[0].text.strip())
    
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
