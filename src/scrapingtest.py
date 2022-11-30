#This website is a good resource to start with:
# https://realpython.com/beautiful-soup-web-scraper-python/


import requests
#Run the following line in the terminal
#python -m pip install beautifulsoup4
from bs4 import BeautifulSoup
#python -m pip install requests

URL = "https://www.worldometers.info/coronavirus/country/us/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

results = soup.find_all(id = "maincounter-wrap")
print(results)
for element in results:
    title = element.find("h1")
    amount = element.find("span")
    if title is not None and amount is not None:
        print(title.text.strip(), amount.text.strip())
