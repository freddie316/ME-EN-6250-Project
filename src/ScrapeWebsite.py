#This website is a good resource to start with:
# https://realpython.com/beautiful-soup-web-scraper-python/

# Installation of Modules
# Run the following line in the terminal
# python -m pip install requests
# python -m pip install beautifulsoup4
# python -m pip install pandas
# I'd recommend using conda instead of pip 
# if you are using anaconda distribution 

# ScrapeWebsiteV2.2.0

import os
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from datetime import date, timedelta

def scrape_country(country,site):
    # Country is the string of the country being queried. URL is the string of the site being scraped. MUST be worldometer OR XXXX
    
    # Set up data dictionary
    data = {country:[], 'Total Deaths':[],
            'New Deaths':[], 'Deaths/1M pop':[],
            'New Deaths/1M pop':[]}
    
    if site.lower() == 'worldometer' or site.lower() == 'wom': # site input specifies worldometer
        URL = "https://www.worldometers.info/coronavirus/#main_table"
        page = requests.get(URL) # pull HTML from worldometer
        soup = BeautifulSoup(page.content, "html.parser") # parse HTML with soup
        
        # Scrape the table for the relevant data
        for day in ['today','yesterday','yesterday2']: # loop thru availabe days
            tableId = 'main_table_countries_' + day
            table = soup.find('table', id = tableId) # search the correct table
            if day == 'today':
                today = date.today().strftime("%m/%d/%y")
                data[country].append(today) # append days to dict
            elif day == 'yesterday':
                yesterday = date.today() - timedelta(days = 1)
                data[country].append(yesterday.strftime("%m/%d/%y"))
            else:
                yesterday2 = date.today() - timedelta(days = 2)
                data[country].append(yesterday2.strftime("%m/%d/%y"))
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
        
        # Prepare export path for JSON
        output = Path(os.getcwd())
        output = output.parent.absolute()
        filename = country + '-WOM.json'
        output = os.path.join(output, 'output\\' + filename)
        
        try:
            dfPrev = pd.read_json(output) # check if JSON already exists
            for i in reversed(range(0,len(df))):
                dataAlready = False
                for j in dfPrev[country]:
                    if df[country][i] == j:
                        dataAlready = True
                if dataAlready == False:
                    dfPrev = pd.concat([df.loc[i].to_frame().T,dfPrev],ignore_index=True)
            dfPrev.to_json(output)
            return dfPrev # Return the dataframe
        except:
            df.to_json(output)
            return df # Return the dataframe
        
       

    elif site.lower() == 'world health organization' or site.lower() == 'who':
        URL = "https://covid19.who.int/table"
        # choose chrome as the browser to look up the website,
        # installs chrome driver if not already installed
        browser = webdriver.Chrome(ChromeDriverManager().install())
        browser.get(URL) # open web page
        time.sleep(1) # wait for a bit to give browser time to fully load
        
        # Do a whole bunch of clicking to get the table to be how we want it
        button = browser.find_element_by_xpath("//button[@title='Active Columns']")
        button.click()
        
        cases = browser.find_element_by_xpath("//span[text()='Cases']")
        cases.click()
        cases1 =  browser.find_element_by_xpath("//div[text()='Cases - cumulative total']")
        cases1.click()
        cases2 = browser.find_element_by_xpath("//div[text()='Cases - newly reported in last 7 days']")
        cases2.click()
        cases.click()
        
        deaths = browser.find_element_by_xpath("//span[text()='Deaths']")
        deaths.click()
        deaths1 = browser.find_element_by_xpath("//div[text()='Deaths - cumulative total per 100,000 population']")
        deaths1.click()
        deaths2 = browser.find_element_by_xpath("//div[text()='Deaths - newly reported in last 7 days']")
        deaths2.click()
        deaths3 = browser.find_element_by_xpath("//div[text()='Deaths - newly reported in last 24 hours']")
        deaths3.click()
        deaths.click()
        
        vaccine = browser.find_element_by_xpath("//span[text()='Vaccine']")
        vaccine.click()
        vaccine1 = browser.find_element_by_xpath("//div[text()='Total vaccine doses administered per 100 population']")
        vaccine1.click()
        vaccine2 = browser.find_element_by_xpath("//div[text()='Persons fully vaccinated with last dose of primary series per 100 population']")
        vaccine2.click()
        vaccine3 = browser.find_element_by_xpath("//div[text()='Persons Boosted per 100 population']")
        vaccine3.click()
        #vaccine.click()
        
        sort = browser.find_element_by_xpath("//div[text()='Deaths']")
        sort.click()
        
        # transfer new HTML data from selenium to beautifulsoup
        page = browser.page_source # pull html from World Health Organization
        soup = BeautifulSoup(page, "html.parser") # parse HTML
        
        # Close browser and disconnect
        browser.quit()
        
        # Scrape table for relevant data
        table = soup.find('div', role = 'rowgroup')
        rows = table.find_all('div', role = 'row')
        today = date.today().strftime("%m/%d/%y")
        data[country].append(today) # append days to dict
        for row in rows:
            cells = row.find_all('div',role = 'cell')
            if cells[0].text.strip() != [] and cells[0].text.strip() == country:
                data['Total Deaths'].append(cells[1].text.strip())
                data['New Deaths'].append(cells[3].text.strip())
                data['Deaths/1M pop'].append(float(cells[2].text.strip())*10)
        data['New Deaths/1M pop'] = None
        
        # Convert dict to dataframe
        df = pd.DataFrame.from_dict(data)
        
        # Prepare export path for JSON
        output = Path(os.getcwd())
        output = output.parent.absolute()
        filename = country + '-WHO.json'
        output = os.path.join(output, 'output\\' + filename)
        try:
            dfPrev = pd.read_json(output)
            dataAlready = False
            for i in dfPrev[country]:
                if date.today().strftime("%m/%d/%y") == i:
                    dataAlready = True
            if dataAlready == False:
                df = pd.concat([df,dfPrev], ignore_index=True)
        except:
            df.to_json(output)
        return df
    else:
        return None
    
USAData = scrape_country('USA','WorldOMeter')
print(USAData)
# =============================================================================
# UKData = scrape_country('UK','WorldOMeter')
# print(UKData)
# ChinaData = scrape_country('China','WorldOMeter')
# print(ChinaData)
# =============================================================================
USADataWHO = scrape_country('United States of America','WHO')
print(USADataWHO)