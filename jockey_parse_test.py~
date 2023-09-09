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

file = "/Users/phillipmonk/research_paper/html/horses/racing_com_horses_cabaca.html"

with open(file) as fp:
    soup = BeautifulSoup(fp, "html.parser")

# Name
horse_name = soup.find("div", {"class": "name-container"}).find("h1").text
print("horse_name=>" + str(horse_name))

deets = soup.find("ul", {"class": "vlist deets desk"}).find_all("span", {"class": "dc"})

# Foaled
print("foaled=>" + deets[0].text.strip())
                   
# Colour
print("colour=>" + deets[1].text.strip())

# Sire
print("sire=>" + deets[2].text.split("/")[0].strip())

# Dam
print("dam=>" + deets[2].text.split("/")[1].strip())

# Trainer
print("trainer=>" + deets[3].text.strip())

quick_stats = soup.find("table", {"class": "quick-stats-table desk"}).find_all("span", {"class": "stat"})

# Age
print("age=>" + quick_stats[0].text.strip())

# Sex
print("sex=>" + quick_stats[1].text.strip())

# Rating
print("rating=>" + quick_stats[2].text.strip())

# Group 1 Wins
print("group_1_wins=>" + quick_stats[3].text.strip())

# Starts
starts = quick_stats[4].find("span", {"once-text": "result.Stats[0].Starts + '-'"})
print("starts=>" + starts.text.strip("-"))

# Firsts
firsts = quick_stats[4].find("span", {"once-text": "result.Stats[0].Firsts + '-'"})
print("firsts=>" + firsts.text.strip("-"))

# Seconds
seconds = quick_stats[4].find("span", {"once-text": "result.Stats[0].Seconds + '-'"})
print("seconds=>" + seconds.text.strip("-"))

# Thirds
thirds = quick_stats[4].find("span", {"once-text": "result.Stats[0].Seconds + '-'"})
print("thirds=>" + thirds.text.strip("-"))

# Prize Money
print("prize_money=>" + quick_stats[5].text.strip())

table_data = soup.find('ul', {'class': 'hlist block-list border'}).find_all('li')

# Season
print("season=>" + table_data[2].text.strip().split("\n")[1])

# Group & Listed
print("grp_listed=>" + table_data[3].text.strip().split("\n")[1])

# 1st Up
print("first_up=>" + table_data[4].text.strip().split("\n")[1])

# 2nd Up
print("second_up=>" + table_data[5].text.strip().split("\n")[1])

# 3rd Up
print("third_up=>" + table_data[6].text.strip().split("\n")[1])

# Firm
print("firm=>" + table_data[7].text.strip().split("\n")[1])

# Good
print("good=>" + table_data[8].text.strip().split("\n")[1])

# Soft
print("soft=>" + table_data[9].text.strip().split("\n")[1])

# Heavy
print("heavy=>" + table_data[10].text.strip().split("\n")[1])

# Jumps
print("jumps=>" + table_data[11].text.strip().split("\n")[1])

# Synth
print("synth=>" + table_data[12].text.strip().split("\n")[1])

past_races = soup.find("table", {"class": "form"}) #.find_all('li')

for row in past_races.tbody.find_all('tr'):    
    # Find all data for each column
    columns = row.find_all('td')

    if(len(columns) == 21):

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

exit(0)
