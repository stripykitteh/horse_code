#
# jockey_from_horse.py
# --------------------
# Loop through all of the horses and extract the jockey href mappings.
#
# Write the results out to the data directory.
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

# jockey mapping fields
fields = ['jockey_page', 'jockey_name']
print("fields=>", fields)

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/jockey_pages.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # writing the fields
    csvwriter.writerow(fields)

    # write the data rows
    #for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/horses_final/*.html")):
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/horses_final_test/*.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")
    
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

                # * Prize
                prize = columns[11].text.strip().split('\n')[0]

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
                
                people = columns[5].find_all("a", href=True)
                trainer = people[0].get("href").split("/")[-1]
                jockey = people[1].get("href").split("/")[-1]
                print("trainer=>", trainer)
                print("jockey=>", jockey)                
                for persons in columns[5].find_all("a", href=True):
                    print("persons=>", persons.get("href").split("/")[-1])

                print("child=>", child)
                csvwriter.writerow(child)
        
        fp.close()

    csvfile.close()

exit(0)
