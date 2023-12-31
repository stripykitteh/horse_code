#
# horse_parse_test.py
# ------------------
# Loop through all of the horses and extract the prizemoney and all other
# pieces of data.
#
# Name
# Foaled
# Colour
# Sire/Dam
# Dam
# Trainer
# Age
# Sex
# Rating
# Group 1 Wins
# Starts
# Firsts
# Seconds
# Thirds
# Prize Money
# Season
# Group & Listed
# 1st Up
# 2nd Up
# 3rd Up
# Firm
# Good
# Soft
# Heavy
# Jumps
# Synth
# For each race:
# * Position
# * Runners
# * Track
# * Date
# * Dist/Cond
# * Prize/Class
# * Weight
# * 800M/400M
# * Margin
# * Rating
# * Odds

import glob
import re
import pathlib
from bs4 import BeautifulSoup
import sys
from datetime import datetime
from decimal import Decimal
from re import sub
import csv
import numpy as np
import statistics

def only_numerics(seq):
    return ''.join(c for c in seq if (c.isdigit() or c =='.'))

# horse fields
fields = ['horse_name', 'foaled', 'colour', 'sire', 'dam', 'sex',  'prize_money', 'season', 'grp_listed', 'first_up', 'second_up', 'third_up', 'firm', 'good', 'soft', 'heavy', 'jumps', 'synth', 'position', 'num_runners', 'trainer', 'prize_pool', '_class', 'jockey', 'race_course', 'race_no', 'date', 'group_1_wins', 'starts', 'firsts', 'seconds', 'thirds', 'dist', 'cond', 'weight', '800m', '400m', 'margin', 'rating', 'odds', 'odds_source', 'horse_t0_prestige_max', 'horse_t0_prestige_median', 'horse_t0_prestige_mean', 'horse_t0_position_median', 'horse_t0_position_mean', 'horse_t0_top3', 'horse_t0_top2', 'horse_t0_percent_top3', 'horse_t0_percent_top2', 'horse_t0_percent_top1', 'horse_t3_prestige_max', 'horse_t3_prestige_median', 'horse_t3_prestige_mean', 'horse_t3_position_median', 'horse_t3_position_mean', 'horse_t3_top3', 'horse_t3_top2', 'horse_t3_top1']
print("fields=>", fields)

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/horse_data.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # write the data rows
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/horses_final/*.html")):
    #for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/horses_final_test/*.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")
    
            # Horse Parent
            parent = []
            
            # Horse Name
            horse_name = soup.find("div", {"class": "name-container"}).find("h1").text
            parent.append(horse_name)

            deets = soup.find("ul", {"class": "vlist deets desk"}).find_all("span", {"class": "dc"})

            # Foaled, change format to YYYY-MM-DD
            parent.append(deets[0].text.strip()[6:10] + "-" + deets[0].text.strip()[3:5] + "-" + deets[0].text.strip()[0:2])

            # Colour
            parent.append(deets[1].text.strip())

            # Sire
            parent.append(deets[2].text.split("/")[0].strip())

            # Dam
            parent.append(deets[2].text.split("/")[1].strip())

            # Trainer is redundant, we can use the trainer data for individual races
            # parent.append(deets[3].text.strip())

            quick_stats = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

            # Current age is redundant, we can derive it for individual races
            # parent.append(quick_stats[0].text.strip())

            # Sex
            parent.append(quick_stats[1].text.strip())

            # Current rating is redundant, use the historic one
            # parent.append(quick_stats[2].text.strip())

            # Prize Money ($)
            parent.append(only_numerics(quick_stats[5].text.strip()))

            table_data = soup.find('ul', {'class': 'hlist block-list border'}).find_all('li')

            # Season
            parent.append(table_data[2].text.strip().split("\n")[1])

            # Group & Listed
            parent.append(table_data[3].text.strip().split("\n")[1])

            # 1st Up
            parent.append(table_data[4].text.strip().split("\n")[1])

            # 2nd Up
            parent.append(table_data[5].text.strip().split("\n")[1])

            # 3rd Up
            parent.append(table_data[6].text.strip().split("\n")[1])

            # Firm
            parent.append(table_data[7].text.strip().split("\n")[1])

            # Good
            parent.append(table_data[8].text.strip().split("\n")[1])

            # Soft
            parent.append(table_data[9].text.strip().split("\n")[1])

            # Heavy
            parent.append(table_data[10].text.strip().split("\n")[1])

            # Jumps
            parent.append(table_data[11].text.strip().split("\n")[1])

            # Synth
            parent.append(table_data[12].text.strip().split("\n")[1])

            # For each race
            past_races = soup.find("table", {"class": "form"}) #.find_all('li')

            # tracking career progress
            group_1_wins = 0
            starts = 0
            firsts = 0
            seconds = 0
            thirds = 0
            horse_t0_prestige_max = 0
            horse_t0_prestige_list = []
            horse_t0_position_list = []
            horse_t0_top3 = 0
            horse_t0_top2 = 0
            horse_t0_percent_top3 = 0
            horse_t0_percent_top2 = 0
            horse_t0_percent_top1 = 0
            horse_t3_prestige = np.zeros(3, dtype=float)
            horse_t3_position = np.zeros(3, dtype=int)
            
            # Easier to process the past races in reverse (chronological) order
            for row in reversed(past_races.tbody.find_all('tr')):

                child = []

                # Find all data for each column
                columns = row.find_all('td')

                if(len(columns) != 21):
                    continue

                # * Position
                if columns[0].text.strip() in ['SCR', 'LSCR', 'FF', 'DQ', 'LR', 'LP', 'F', 'BD', 'NP']:
                    continue
                position = int(columns[0].text.strip().split(chr(8211))[0])
                child.append(position)

                # * Num Runners
                num_runners = int(columns[0].text.strip().split(chr(8211))[1].strip('-'))
                child.append(num_runners)
                
                # * Horse
                #horse = columns[4].text.strip().split('\n')[1]
                #child.append(horse)

                # * Trainer
                people = columns[5].find_all("a", href=True)
                trainer = people[0].get("href").split("/")[-1]
                #trainer = columns[5].text.strip().split('\n')[0].split('\xa0')[1]
                child.append(trainer)

                # * Prize
                prize_pool_str = columns[11].text.strip().split('\n')[0]
                if prize_pool_str == chr(8211): # ignore trials
                    continue
                else:
                    # check if the prize money was in k (,000) or m (,000,000)
                    if prize_pool_str[-1] == 'k':
                        prize_pool = float(only_numerics(prize_pool_str)) * 1000
                    elif prize_pool_str[-1] == 'm':
                        prize_pool = float(only_numerics(prize_pool_str)) * 1000000
                    else:
                        prize_pool = float(only_numerics(prize_pool_str))

                    child.append(prize_pool)
                    
                # * Class
                class_s = columns[11].text.strip().split('\n')[-2]
                if class_s[0:2] == 'LR':
                    _class = 4
                elif class_s[0:2] == 'G3':
                    _class = 3
                elif class_s[0:2] == 'G2':
                    _class = 2
                elif class_s[0:2] == 'G1':
                    _class = 1
                else:
                    _class = 5
                
                child.append(_class)

                # * Jockey
                if prize_pool_str[0] == "$":
                    jockey = people[1].get("href").split("/")[-1]
                else:
                    jockey = ""
                child.append(jockey)
        
                # * Race Course/Race Number/Date
                race_course = columns[8].text.strip()
                # Lookup tracks in scope
                if race_course == 'CAUL':
                    child.append('Caulfield')
                elif race_course == 'FLEM':
                    child.append('Flemington')
                elif race_course == 'RHIL':
                    child.append('Rosehill Gardens')
                elif race_course == 'RAND':
                    child.append('Royal Randwick')
                else:
                    child.append(race_course)

                # Race Number
                # Access the list from the end to avoid course names like 'M V'
                race_no = only_numerics(columns[7].text.strip().split()[-4])
                child.append(race_no)
                    
                # change date format to YYYY-MM-DD
                date = "20" + columns[6].text.strip()[6:8] + "-" + columns[6].text.strip()[3:5] + "-" + columns[6].text.strip()[0:2]
                child.append(date)

                # Group 1 Wins
                if (_class == 1) and (position == 1):
                    group_1_wins += 1
                child.append(group_1_wins)
               
                # Starts
                starts += 1
                child.append(starts)

                # Firsts
                if position == 1:
                    firsts += 1
                child.append(firsts)

                # Seconds
                if position == 2:
                    seconds += 1
                child.append(seconds)

                # Thirds
                if position == 3:
                    thirds += 1
                child.append(thirds)
                
                # * Dist
                dist = columns[9].text.strip().split('\n')[0][:-1]
                child.append(dist)

                # * Cond
                cond = only_numerics(columns[9].text.strip().split('\n')[2])
                child.append(cond)

                # * Weight        
                weight = only_numerics(columns[12].text.strip().split('\n')[0])
                child.append(weight)

                # * 800M
                if prize_pool_str[0] == "$":
                    _800m = columns[13].text.strip().split('\n')[0]
                else:
                    _800m = ""
                child.append(only_numerics(_800m))
            
                # * 400M
                if prize_pool_str[0] == "$":
                    _400m = columns[13].text.strip().split('\n')[-1]
                else:
                    _400m = ""
                child.append(only_numerics(_400m))

                # * Margin
                # rarely, the margin is not recorded
                if columns[14].text == "":
                    child.append("")
                else:
                    # winner gets a margin of 0
                    if position == 1:
                        margin = 0
                    else:
                        margin = only_numerics(columns[14].text)
                    child.append(str(margin))

                # * Rating
                rating = columns[15].text.strip()
                child.append(rating)
        
                # com = columns[9].text.strip()

                # * Odds
                if prize_pool_str[0] == "$":
                    odds = only_numerics(columns[17].text.strip().split('\n')[0])
                else:
                    odds = 0
                child.append(str(odds))

                # * Odds Source
                if prize_pool_str[0] == "$":
                    if len(columns[17].text.strip().split('\n')) == 2:
                        odds_source = columns[17].text.strip().split('\n')[1]
                    else:
                        odds_source = ""
                child.append(odds_source)

                # horse_t0_prestige_max
                if horse_t0_prestige_max < prize_pool:
                    horse_t0_prestige_max = prize_pool
                child.append(horse_t0_prestige_max)

                horse_t0_prestige_list.append(prize_pool)
                
                # horse_t0_prestige_median
                child.append(statistics.median(horse_t0_prestige_list))

                # horse_t0_prestige_mean
                child.append(statistics.mean(horse_t0_prestige_list))                          

                horse_t0_position_list.append(position)
                
                # horse_t0_position_median
                child.append(statistics.median(horse_t0_position_list))

                # horse_t0_position_mean
                child.append(statistics.mean(horse_t0_position_list))
                             
                # horse_t0_top3
                child.append(firsts + seconds + thirds)
                             
                # horse_t0_top2
                child.append(firsts + seconds)                             

                # horse_t0_percent_top3
                child.append((firsts + seconds + thirds)/starts)
                             
                # horse_t0_percent_top2
                child.append((firsts + seconds)/starts)
                             
                # horse_t0_percent_top1
                child.append(firsts/starts)

                horse_t3_prestige[starts % 3] = prize_pool                             

                # horse_t3_prestige_max
                child.append(max(horse_t3_prestige))

                # horse_t3_prestige_median
                child.append(statistics.median(horse_t3_prestige))
                             
                # horse_t3_prestige_mean
                child.append(statistics.mean(horse_t3_prestige))

                horse_t3_position[starts % 3] = position
                
                # horse_t3_position_median
                child.append(max(horse_t3_position))
                             
                # horse_t3_position_mean
                child.append(statistics.mean(horse_t3_position))

                # horse_t3_top3
                child.append(len(horse_t3_position[np.where((horse_t3_position <= 3) & (horse_t3_position > 0))]))
                             
                # horse_t3_top2
                child.append(len(horse_t3_position[np.where((horse_t3_position <= 2) & (horse_t3_position > 0))]))
                             
                # horse_t3_top1
                child.append(len(horse_t3_position[np.where((horse_t3_position <= 1) & (horse_t3_position > 0))]))

                print("parent=>", parent)
                print("child=>", child)
                csvwriter.writerow(parent + child)
        
        fp.close()

    csvfile.close()

exit(0)
