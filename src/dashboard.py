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
    country = input("Input a country to search for:\t")
    site = input("Choose a website to search on: WorldOMeter, WHO:\t")
    if site.lower() == 'worldometer' or site.lower() == 'who' or site.lower() == 'world health organization':
        return country, site
    elif n > 1:
        print("Invalid Website Selection, valid selections are 'WorldOMeter', 'WHO', or 'World Health Organization'")
        print(f"{n-1} attempts remaining")
        return get_user_input(n - 1)
    else:
        raise MyException('Maximum attempts reached!')


cont = 1
df = pd.DataFrame()
while cont != '0':
    country, site = get_user_input()
    print("Retrieving Data...")
    df = pd.DataFrame(scrape_country(country, site))
    print(tabulate(df, headers='keys', tablefmt='fancy_grid'))

    cont = input("Input 0 to exit or any other key to continue:\n")
