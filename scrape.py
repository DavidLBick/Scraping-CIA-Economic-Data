import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import pdb
import pandas as pd

url = "https://www.cia.gov/library/publications/the-world-factbook/fields/214.html#UK" 
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")
table = soup.find('table', id = 'fieldListing')
rows = table.findAll("tr")
rows = rows[1:] #first entry is garbage

countries = []; agriculture = []; industry = []; services = []

for row in rows:
    td_tags = row.findAll("td")
    # first td tag holds country name in an a tag
    country = td_tags[0].findAll("a")[0].text
    # get the second td because the 2nd holds the numbers, the first holds the country name
    row_data = td_tags[1] 
    # span tags hold the numbers
    spans = row_data.findAll("span", {'class': 'subfield-number'})
    data = [x.text for x in spans]
    data = list(map(lambda x: float(x[:-1]) if x != [] else x, data))
    if len(data) < 3: continue # requires a valid entry for each field
    countries.append(country); agriculture.append(data[0])
    industry.append(data[1]); services.append(data[2])

data = pd.DataFrame(list(zip(countries, agriculture, industry, services)), 
                    columns = ['Country', 'Agriculture', "Industry", "Services"]) 

