# -*- coding: utf-8 -*-
"""
Main dashboard script
"""

from ScrapeWebsite import scrape_country

country = input("Input a country to search for:\n")
site = input("Choose a website to search on: WorldOMeter, WHO:\n")

print("Retrieving Data...")

data = scrape_country(country,site)
print(data)


input("Press any key...")