#This website is a good resource to start with:
# https://realpython.com/beautiful-soup-web-scraper-python/

# Installation of Modules
# Run the following line in the terminal
# python -m pip install requests
# python -m pip install beautifulsoup4
# python -m pip install pandas
# I'd recommend using conda instead of pip 
# if you are using anaconda distribution 

import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_country(country,site):
    # Country is the string of the country being queried. URL is the string of the site being scraped. MUST be worldometer OR XXXX
    
    if site.lower() == 'worldometer':
        URL = "https://www.worldometers.info/coronavirus/#main_table"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        
        table = soup.find('table', id = 'main_table_countries_today')
        data = {'Country':[], 'Total Deaths':[],
                'New Deaths':[], 'Deaths/1M pop':[],
                'New Deaths/1M pop':[]}
        for row in table.tbody.find_all('tr'):
            # Find all data for each column
            columns = row.find_all('td')
            if columns != [] and columns[1].text.strip() != '':
                data['Country'].append(columns[1].text.strip())
                data['Total Deaths'].append(columns[4].text.strip())
                data['New Deaths'].append(columns[5].text.strip())
                data['Deaths/1M pop'].append(columns[11].text.strip())
                data['New Deaths/1M pop'].append(columns[20].text.strip())
        df = pd.DataFrame.from_dict(data)
    
        # Input country names below to get info about that country
        return df[df['Country']==country]
    elif site.lower() == '':
        URL = ""
        # WIll be different method for second site we choose
    else:
        return None
    
countryData = scrape_country('USA','WorldOMeter')
print(countryData)