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

def only_numerics(seq):
    return ''.join(c for c in seq if (c.isdigit() or c =='.'))

# horse fields
fields = ['horse_name', 'foaled', 'colour', 'sire', 'dam', 'trainer', 'age', 'sex', 'rating', 'group_1_wins', 'starts', 'firsts', 'seconds', 'thirds', 'prize_money', 'season', 'grp_listed', 'first_up', 'second_up', 'third_up', 'firm', 'good', 'soft', 'heavy', 'jumps', 'synth', 'position', 'num_runners', 'trainer', 'prize', '_class', 'jockey', 'track_date', 'dist', 'cond', 'weight', '800m', '400m', 'margin', 'rating', 'odds', 'odds_source'] 
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

            # Foaled
            parent.append(deets[0].text.strip())

            # Colour
            parent.append(deets[1].text.strip())

            # Sire
            parent.append(deets[2].text.split("/")[0].strip())

            # Dam
            parent.append(deets[2].text.split("/")[1].strip())

            # Trainer
            parent.append(deets[3].text.strip())

            quick_stats = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

            # Age
            parent.append(quick_stats[0].text.strip())

            # Sex
            parent.append(quick_stats[1].text.strip())

            # Rating
            parent.append(quick_stats[2].text.strip())

            # Group 1 Wins
            if ord(quick_stats[3].text.strip()) == 8211: # en-dash means no group 1 wins
                group_1_wins = '0'
            else:
                group_1_wins = quick_stats[3].text.strip()
            parent.append(group_1_wins)

            # Starts
            starts = quick_stats[4].find("span", {"once-text": "result.Stats[0].Starts + '-'"})
            parent.append(starts.text.strip("-"))

            # Firsts
            firsts = quick_stats[4].find("span", {"once-text": "result.Stats[0].Firsts + '-'"})
            parent.append(firsts.text.strip("-"))

            # Seconds
            seconds = quick_stats[4].find("span", {"once-text": "result.Stats[0].Seconds + '-'"})
            parent.append(seconds.text.strip("-"))

            # Thirds
            thirds = quick_stats[4].find("span", {"once-text": "result.Stats[0].Thirds"})
            parent.append(thirds.text.strip("-"))

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

            for row in past_races.tbody.find_all('tr'):

                child = []

                # Find all data for each column
                columns = row.find_all('td')

                if(len(columns) != 21):
                    continue

                # * Position
                if columns[0].text.strip() in ['SCR', 'LSCR', 'FF', 'DQ', 'LR', 'LP', 'F', 'BD', 'NP']:
                    continue
                position = columns[0].text.strip().split(chr(8211))[0]
                child.append(position)

                # * Num Runners
                num_runners = columns[0].text.strip().split(chr(8211))[1].strip('-')
                child.append(num_runners)
                
                # * Horse
                #horse = columns[4].text.strip().split('\n')[1]
                #child.append(horse)

                # * Trainer
                trainer = columns[5].text.strip().split('\n')[0].split('\xa0')[1]
                child.append(trainer)

                # * Prize
                prize = columns[11].text.strip().split('\n')[0]
                if prize == chr(8211): # ignore trials
                    continue
                else:
                    # check if the prize money was in k (,000) or m (,000,000)
                    if prize[-1] == 'k':
                        child.append(float(only_numerics(prize)) * 1000)
                    elif prize[-1] == 'm':
                        child.append(float(only_numerics(prize)) * 1000000)
                    else:
                        child.append(float(only_numerics(prize)))

                # * Class
                _class = columns[11].text.strip().split('\n')[-1]
                child.append(_class)

                    # * Jockey
                if prize[0] == "$":
                    # rarely the jockey is not recorded
                    if len(columns[5].text.strip().split('\n')[1].split('\xa0')) == 2:
                        jockey = columns[5].text.strip().split('\n')[1].split('\xa0')[1]
                    else:
                        jockey = ""
                else:
                    jockey = ""
                child.append(jockey)
        
                # * Track/Date
                race_date = columns[6].text.strip()
                child.append(race_date)
        
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
                if prize[0] == "$":
                    _800m = columns[13].text.strip().split('\n')[0]
                else:
                    _800m = ""
                child.append(only_numerics(_800m))
            
                # * 400M
                if prize[0] == "$":
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
                if prize[0] == "$":
                    odds = only_numerics(columns[17].text.strip().split('\n')[0])
                else:
                    odds = 0
                child.append(str(odds))

                # * Odds Source
                if prize[0] == "$":
                    if len(columns[17].text.strip().split('\n')) == 2:
                        odds_source = columns[17].text.strip().split('\n')[1]
                    else:
                        odds_source = ""
                child.append(odds_source)

                print("parent=>", parent)
                print("child=>", child)
                csvwriter.writerow(parent + child)
        
        fp.close()

    csvfile.close()

exit(0)
