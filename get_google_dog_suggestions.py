# import python libraries for api call and parsing XML
import requests
import string
import pandas as pd
import re
import time
import xml.etree.ElementTree as ET

# load datasets of dog names and search terms for Google
dogs_df = pd.read_csv('data/dog_breeds.csv')

# clean up search queries
dog_lookup = dogs_df['title'].unique()
dog_breeds = dogs_df['search_term'].unique()
dog_breeds = [re.sub(r'\([^()]*\)', '', dog).strip() for dog in dog_breeds]
dog_breeds = [re.sub(r' ', '+', dog).lower() for dog in dog_breeds]

# append why+does+my+ to front of dog breed, note Google API views + as a blank space
dog_queries = ['why+does+my+' + dog for dog in dog_breeds]

# create lookup dataset from dog name in dog_breeds.csv
# to Google search queries for future joining in data_prep.py
dog_df = pd.DataFrame()
dog_df['title'] = dog_lookup
dog_df['breed_in_query'] = dog_breeds
dog_df['queries'] = dog_queries

# form list of queries for API calls
unique_queries = list(set(dog_queries))

# loop queries through API to return the top 10 suggested autocompletes
for idx, x in enumerate(unique_queries):
    time.sleep(5)
    apiurl = 'https://suggestqueries.google.com/complete/search?output=toolbar&hl=en&q=' + x
    r = requests.get(apiurl)
    tree = ET.fromstring(r.text)

    suggestions = []
    query = []
    print(idx)
    print(x)

    for child in tree.iter('suggestion'):
        suggestions = suggestions + [child.attrib['data']]
        query = query + [x]

    df = pd.DataFrame()
    df['term'] = query
    df['suggestion'] = suggestions

    if idx == 0:
        suggestions_df = df
    
    if idx > 0:
        suggestions_df = pd.concat([suggestions_df,df])

# output datasets to csv files
suggestions_df.to_csv('data/dog_suggestions.csv', encoding='utf-8-sig', index=False)
dog_df.to_csv('data/dog_names.csv', encoding='utf-8-sig', index=False)
