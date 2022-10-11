import pandas as pd
import numpy as np
from numpy.core.defchararray import find

dogs_df = pd.read_csv('dog_breeds_wide_cleaned.csv')
suggestions_df = pd.read_csv('dog_suggestions.csv')
names_df = pd.read_csv('dog_names.csv')

# joindatasets together
df = pd.merge(dogs_df,names_df, how = 'inner', on ='title')
df = pd.merge(df,suggestions_df, how = 'inner', left_on ='queries',right_on='term')

# find search term position in output
a = df.suggestion.str.replace(" ", "+")
a = a.values.astype(str)
b = df.search_term.values.astype(str)
df = df.assign(str_position=find(a, b))

# part strings by before and after dog breed
df['search_start'] = df.apply(lambda x: x['suggestion'][:x['str_position']],axis = 1)
df['search_end'] = df.apply(lambda x: x['suggestion'][x['str_position']+len(x['search_term']):],axis = 1)

df['search_end'] = df.search_end.str.replace(r'puppy', '', regex=True)
df['search_end'] = df.search_end.str.replace(r'dog', '', regex=True)
#df['search_end'] = df.search_end.str.replace("^puppy", "")
#df['search_end'] = df.search_end.str.replace("^dog", "")

df['search_start'] = df.search_start.str.strip()
df['search_end'] = df.search_end.str.strip()


df['search_category'] = np.select(
[
    df['search_end'].str.contains("bark"), 
    df['search_end'].str.contains("howl"),
    df['search_end'].str.contains("whine"),
    df['search_end'].str.contains("whining"),
    df['search_end'].str.contains("cry"),
    df['search_end'].str.contains("smell"),
    df['search_end'].str.contains("stink"),
    df['search_end'].str.contains("sleep"),
    df['search_end'].str.contains("eat"),
    df['search_end'].str.contains("paw"),
    df['search_end'].str.contains("follow")
], 
[ 'noise','noise','noise','noise','noise','odeur','odeur','laziness','eating habits','behaviour','behaviour'], 
default=0 )

#filter_df = df.loc[df['search_category'] == '0']

#print(filter_df['search_end'].unique())
df.to_csv('why_does_my_dog.csv', encoding='utf-8-sig', index=False)