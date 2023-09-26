#
# meet_parse_loop.py
# ------------------
# Loop through all of the meets and extract the races from racenet
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

# Open a file for writing
with open('/Users/phillipmonk/research_paper/horse_code/data/racenet_race_data.csv', 'w') as csvfile:
    # create a new writer object
    csvwriter = csv.writer(csvfile)

    # write the data rows
    for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/meets_final/*.html")):
    #for file in sorted(glob.glob("/Users/phillipmonk/research_paper/html/meets_final_test/*.html")):
        with open(file) as fp:
            print("file=>", file)
            soup = BeautifulSoup(fp, "html.parser")
    


            paras = soup.find_all("div", {"class": "meeting-event-number__container"})
            for para in paras:
                child = []
                my_ref = para.find('a', href=True)
                if my_ref.text:
                    print("href=>", my_ref['href'])                    
                    child.append(my_ref['href'])
                    csvwriter.writerow(child)
        
        fp.close()

    csvfile.close()

exit(0)
