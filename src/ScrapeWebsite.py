#This website is a good resource to start with:
# https://realpython.com/beautiful-soup-web-scraper-python/

# Installation of Modules
# Run the following line in the terminal
# python -m pip install requests
# python -m pip install beautifulsoup4
# python -m pip install pandas
# I'd recommend using conda instead of pip 
# if you are using anaconda distribution 

# ScrapeWebsiteV1.1.0

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path

def scrape_country(country,site):
    # Country is the string of the country being queried. URL is the string of the site being scraped. MUST be worldometer OR XXXX
    
    # Set up data dictionary
    data = {country:[], 'Total Deaths':[],
            'New Deaths':[], 'Deaths/1M pop':[],
            'New Deaths/1M pop':[]}
    
    if site.lower() == 'worldometer': # site input specifies worldometer
        URL = "https://www.worldometers.info/coronavirus/#main_table"
        page = requests.get(URL) # pull HTML from worldometer
        soup = BeautifulSoup(page.content, "html.parser") # parse HTML with soup
        
        # Scrape the table for the relevant data
        for day in ['today','yesterday','yesterday2']: # loop thru availabe days
            tableId = 'main_table_countries_' + day
            table = soup.find('table', id = tableId) # search the correct table
            if day != 'yesterday2':
                data[country].append(day.capitalize()) # append days to dict
            else:
                data[country].append("Two Days Ago")
            for row in table.tbody.find_all('tr'): # find all rows
                # Find all data for each column
                columns = row.find_all('td') # find all data entries
                if columns != [] and columns[1].text.strip() == country:
                    # look for only relevant country, and append data to dict
                    data['Total Deaths'].append(columns[4].text.strip())
                    data['New Deaths'].append(columns[5].text.strip())
                    data['Deaths/1M pop'].append(columns[11].text.strip())
                    data['New Deaths/1M pop'].append(columns[20].text.strip())

        # Convert dictionary into a dataframe
        df = pd.DataFrame.from_dict(data)
        df.style.set_caption(country)
        
        # Export dataframe to JSON
        output = Path(os.getcwd())
        output = output.parent.absolute()
        filename = country + '.json'
        output = os.path.join(output, 'output\\' + filename)
        df.to_json(output)
    
        # Return the dataframe
        return df
    elif site.lower() == 'world health organization' or site.lower() == 'who':
        URL = "https://covid19.who.int/table"
        # WIll be different method for second site we choose
        page = requests.get(URL) # pull html from World Health Organization
        soup = BeautifulSoup(page.content, "html.parser") # parse HTML
        
        # Scrape table for relevant data 
        
        
    else:
        return None
    
USAData = scrape_country('USA','WorldOMeter')
print(USAData)
UKData = scrape_country('UK','WorldOMeter')
print(UKData)
ChinaData = scrape_country('China','WorldOMeter')
print(ChinaData)
