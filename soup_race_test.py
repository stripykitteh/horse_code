#
# soup_race_test.py
# -----------------
# Look at a given race html file and try to pull out all the tags.
#
#


from bs4 import BeautifulSoup

with open("/Users/phillipmonk/research_paper/html/races_all/racing_com_form_2020-01-18_ascot_race_2.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

all_items = soup.find_all("span", {"class": "hover-red"})

for item in all_items:
    lines = item.text.splitlines()
    print(lines[2])
    for line in lines:
        print(line)

exit()



