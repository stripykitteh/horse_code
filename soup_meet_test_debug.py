from bs4 import BeautifulSoup

with open("/Users/phillipmonk/research_paper/html/meets/racing_com_form_2022-10-22_the-valley.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

print(soup.head.title)

#details = soup.find_all('div', {'class': 'number-circle'})
details = soup.find_all('div', {'class': 'race-numbers'})

last_race = 0

for detail in details:
    for race_str in detail.text.splitlines():
        if race_str.isdigit():
            print(race_str)
            this_race = int(race_str)
            if this_race > last_race:
                last_race = this_race
            
print("last_race=>" + str(last_race))

#classes = []
#for element in soup.find_all(class_=True):
#    classes.extend(element["class"])

#print(classes)
