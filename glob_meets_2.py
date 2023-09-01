#
# glob_meets_2.py
# ---------------
# Loop through the files in the html/meets_2 subdirectory and calculate and write
# to file how many races each meeting had.
#

import glob
import re
from bs4 import BeautifulSoup

race_file = open("/Users/phillipmonk/research_paper/data/races_2.csv", "w")

for file in glob.glob("/Users/phillipmonk/research_paper/html/meets_2/*.html"):
    meet_date = file[63:73]
    meet_track = file[74:-5]
    with open(file) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    details = soup.find_all('div', {'class': 'race-numbers'})

    last_race = 0

    for detail in details:
        for race_str in detail.text.splitlines():
            if race_str.isdigit():
                race_file.write(meet_date + "," + meet_track + "," + race_str + "\n")
                this_race = int(race_str)
                if this_race > last_race:
                    last_race = this_race
    
    fp.close()

race_file.close()

exit(0)
