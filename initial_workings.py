import pandas as pd
#from pandas_profiling import ProfileReport
import numpy as np

# ProfileReport will build a report of your dataset and write it as a html file
#profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

# We can dive into the data created by investigating the keys (column names)
#profset = profile.description_set
#print(profset.keys())

# for example we can the correlations data we can select this from profset
#attributes = profset["correlations"]
#print(attributes.keys())

# and then select the auto correlations and write that data to csv
#auto_correlations = attributes["auto"]
#auto_correlations['metric'] = auto_correlations.index
#auto_correlations.to_csv('data/correlations.csv', index = False)
#auto_pivot = auto_correlations.pivot(index='metric',columns=(auto_correlations.columns != 'metric'),values='correlation') 
#print(auto_pivot)

df = pd.read_csv('data/dataset_2.csv')
df_pivot = pd.read_csv('data/dataset_2_pivot.csv')
corr_df = pd.read_csv('data/correlations.csv')
corr_df_pivot = pd.read_csv('data/correlations_pivot.csv')
types_df = pd.read_csv('data/metric_types.csv')

cross_join = df_pivot[['country','metric','value']]

world_df = df_pivot.merge(cross_join, how = 'inner', on='country')
world_df.columns = ['country', 'iso_country_code_2018','metric','value','target_metric','target_value']

world_df = world_df.merge(corr_df_pivot, how = 'inner', on=['metric','target_metric'])
world_df['correlation_absolute'] = world_df['correlation'].abs()

world_df = world_df.merge(types_df, how = 'inner', on='metric')

types_df.columns = ['target_metric','target_metric_type','target_latest','target_metric_no_year','target_ranking']
world_df = world_df.merge(types_df, how = 'inner', on='target_metric')

world_df["metric_rank_high"] = world_df.groupby(["metric","target_metric"])["value"].rank(method="min", ascending=False)
world_df["metric_rank_low"] = world_df.groupby(["metric","target_metric"])["value"].rank(method="min", ascending=True)
world_df["metric_rank"] = np.where(world_df['ranking'] == 'high',world_df["metric_rank_high"],world_df["metric_rank_low"])

world_df["target_metric_rank_high"] = world_df.groupby(["target_metric","metric"])["target_value"].rank(method="min", ascending=False)
world_df["target_metric_rank_low"] = world_df.groupby(["target_metric","metric"])["target_value"].rank(method="min", ascending=True)
world_df["target_metric_rank"] = np.where(world_df['target_ranking'] == 'high',world_df["target_metric_rank_high"],world_df["target_metric_rank_low"])

world_df = world_df.drop(columns=['metric_rank_high', 'metric_rank_low','target_metric_rank_high', 'target_metric_rank_low'])

world_df = world_df.loc[world_df['metric_no_year'] != world_df['target_metric_no_year']]
world_df = world_df.loc[world_df['metric_type'] != world_df['target_metric_type']]

world_df = world_df.drop_duplicates()

latest_metric_df = world_df.loc[world_df['latest'] == 1]
latest_metric_df = latest_metric_df[["country","metric_type","metric_no_year","metric_rank"]]
latest_metric_df.columns = ["country","metric_type","metric_no_year","latest_rank"]
world_df = world_df.merge(latest_metric_df, how = 'inner', on=["country","metric_type","metric_no_year"])

print(latest_metric_df)

world_df["country_strengths_order"] = world_df.groupby(["country","metric_type"])["latest_rank"].rank(method="dense", ascending=True)
world_df["country_weaknesses_order"] = world_df.groupby(["country","metric_type"])["latest_rank"].rank(method="dense", ascending=False)

print(world_df)
world_df = world_df.drop_duplicates()
world_df.to_csv('data/world_df.csv', index = False)