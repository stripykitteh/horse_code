#
# glob_races.py
# -------------
# Loop through all of the races and extract the horses.
#
#

import glob
import re
import pathlib
from bs4 import BeautifulSoup

horse_file = open("/Users/phillipmonk/research_paper/data/horses.csv", "w")

for file in glob.glob("/Users/phillipmonk/research_paper/html/races_all/*.html"):
    with open(file) as fp:
        soup = BeautifulSoup(fp, "html.parser")

    all_items = soup.find_all("span", {"class": "hover-red"})
    path = pathlib.Path(file)
    
    position = 0
    for item in all_items:
        position += 1
        lines = item.text.splitlines()
        horse_file.write(path.name + "," + str(position) + "," + lines[2] + "\n")
    
    fp.close()

horse_file.close()

exit(0)
