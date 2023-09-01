import sys
import requests
from bs4 import BeautifulSoup

race_no = sys.argv[1]

URL = "https://www.racing.com/form/2023-07-01/flemington/race/" + race_no + "#/results"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

f = open("demofile" + race_no + ".txt", "w")
f.write(page.text)
f.close()
