import requests
import string
import pandas as pd
import re
import time
import xml.etree.ElementTree as ET

dogs_df = pd.read_csv('dog_breeds_wide_final.csv')

dog_lookup = dogs_df['title'].unique()
dog_breeds = dogs_df['search_term'].unique()
dog_breeds = [re.sub(r'\([^()]*\)', '', dog).strip() for dog in dog_breeds]
dog_breeds = [re.sub(r' ', '+', dog).lower() for dog in dog_breeds]

dog_queries = ['why+does+my+' + dog for dog in dog_breeds]

dog_df = pd.DataFrame()
dog_df['title'] = dog_lookup
dog_df['breed_in_query'] = dog_breeds
dog_df['queries'] = dog_queries

unique_queries = list(set(dog_queries))

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


suggestions_df.to_csv('dog_suggestions.csv', encoding='utf-8-sig', index=False)
dog_df.to_csv('dog_names.csv', encoding='utf-8-sig', index=False)

