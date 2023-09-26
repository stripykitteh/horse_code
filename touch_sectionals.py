#
# touch_sectionals.py
# -------------------
#
# Create/touch the sectionals text files.
# This is a quick hack to save us a bit of time creating them manually.
#

import os

races_final = open("/Users/phillipmonk/research_paper/horse_code/data/races_final.csv", "r")

races = races_final.readlines()

for race in races:
    touch_str = "touch /Users/phillipmonk/research_paper/html/sectionals_txt/racing_com_form_" + race.split(",")[0] + "_" + race.split(",")[1] + "_" + race.split(",")[2][:-1] + "_sectionals.txt"
    print(touch_str)
    os.system(touch_str)

exit(0)
