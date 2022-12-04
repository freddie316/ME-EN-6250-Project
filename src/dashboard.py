# -*- coding: utf-8 -*-
"""
Main dashboard script
"""

from ScrapeWebsite import scrape_country
from tabulate import tabulate
import pandas as pd
class MyException(Exception):
    pass


def get_user_input(n=5):    
    while n>0:
        site = input("Choose a website to search on: WorldOMeter, WHO:\t")
        if site.lower() == 'worldometer' or site.lower() == 'wom':
            with open('country-list-WOM.txt') as country_list:
                data = country_list.read()
                valid_countries = data.split('\n')
            break
        elif site.lower() == 'who' or site.lower() == 'world health organization':
            with open('country-list-WHO.txt') as country_list:
                data = country_list.read()
                valid_countries = data.split('\n')
            break
        else:
            print("Invalid Website Selection, valid selections are 'WorldOMeter', 'WOM', 'WHO', or 'World Health Organization'")
            n-=1
            print(f"{n} attempts remaining")
            continue
    
    n = 5
    while n>0:
        country = input("Input a country to search for:\t")
        if country not in valid_countries:
            print("Invalid Country Selection")
            print('Similar Valid Countries are:')
            for i in valid_countries:
                if country[0] == i[0]:
                    print(i)
            n-=1
            print(f"{n} attempts remaining")
            continue
        else:
            break

    return country, site    
    valid_countries.close()
    raise MyException('Maximum attempts reached!')


cont = 1
df = pd.DataFrame()
while cont != '0':
    country, site = get_user_input()
    print("Retrieving Data...")
    df = pd.DataFrame(scrape_country(country, site))
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

    cont = input("Input 0 to exit or any other key to continue:\n")
