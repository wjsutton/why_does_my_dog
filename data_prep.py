# import python libraries for data prep
import pandas as pd
import numpy as np
from numpy.core.defchararray import find

# load datasets
dogs_df = pd.read_csv('data/dog_breeds.csv')
suggestions_df = pd.read_csv('data/dog_suggestions.csv')
names_df = pd.read_csv('data/dog_names.csv')
term_lookup_df = pd.read_csv('data/search_term_lookup.csv')

# join datasets together
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

# remove terms like puppy and dog, in cases like Why Does My German Shepard Puppy... 
df['search_end'] = df.search_end.str.replace(r'puppy', '', regex=True)
df['search_end'] = df.search_end.str.replace(r'dog', '', regex=True)

# remove any whitespace
df['search_start'] = df.search_start.str.strip()
df['search_end'] = df.search_end.str.strip()

# locate any queries that weren't identified from the lookup
# rejected queries are not about dogs, i.e. "why does my boxers ride up"
rejected_df = pd.merge(df,term_lookup_df, how = 'left', left_on ='search_end',right_on='search_term')

# re rank question order after dropping dups
term_lookup_df = pd.merge(df['search_end'].drop_duplicates(),term_lookup_df, how = 'inner', left_on ='search_end',right_on='search_term')
term_lookup_df["question_order"] = term_lookup_df["question_order"].rank(method="dense", ascending=True)
term_lookup_df["question_order"] = term_lookup_df["question_order"].astype(int)

# join datasets
df = pd.merge(df,term_lookup_df, how = 'inner', left_on ='search_end',right_on='search_term')

# remove any queries that returned nothing or are to be excluded
df = df.loc[df['search_start'] == 'why does my']
df = df.loc[df['term_category'] != 'exclude']

# write rejected queries for review
rejected_df.to_csv('data/rejected_queries.csv', encoding='utf-8-sig', index=False)

# write queries to use for dashboard
df.to_csv('dahboard_data/why_does_my_dog.csv', encoding='utf-8-sig', index=False)
