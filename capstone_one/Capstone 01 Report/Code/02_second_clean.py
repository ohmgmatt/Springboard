import pandas as pd
import numpy as np

df = pd.read_pickle('kickstarter_desc.pkl')

## Rename parsed column
df.rename(columns = {"description":"parsed"}, inplace = True)

## Pull out the four columns
df[['description', 'img_count', 'vid_count', 'rewards']] = pd.DataFrame(df['parsed'].tolist(), index=df.index)

## drop parsed column
df.drop('parsed',axis = 1, inplace = True)

## Drop rows that don't have all information
df.dropna(subset=['img_count', 'vid_count', 'rewards'], inplace = True)

## Transforms "N/A" strings to NaNs, clean up empty vals
df.replace('N/A',np.NaN, inplace = True)

##Clean up empty / null values
df.description.replace('', None, inplace = True)

##Clean up categories
def cat_core(str):
    if "/" in str:
        split_list = str.split('/')
        core = split_list[0]
        return core
    else:
        return str

df['category_core'] = df['category_slug'].apply(cat_core)

## Clean up dates
df['created_at_date'] = pd.to_datetime(df['created_at_date'])
df['deadline_date'] = pd.to_datetime(df['deadline_date'])
df['launched_at_date'] = pd.to_datetime(df['launched_at_date'])
df['state_changed_at_date'] = pd.to_datetime(df['state_changed_at_date'])

## USD Goal
df['usd_goal'] = df['goal'] * df['static_usd_rate']

## Percent Reached
df['percent_goal'] = (df['pledged'] / df['goal']) * 100.00

## Video Usage
df['vid_usage'] = df['vid_count'] >= 1.0

## Reached Goal
df['reach_goal'] = df['percent_goal'] >= 100.00

## Drop Duplicates
df.drop_duplicates(subset = ['id', 'name'], inplace = True)

## Rewards Translated
def convert_tool(values, rate):
    new_rewards = []
    for v in values:
        new_rewards.append(round(v * rate, 2))
    return new_rewards
df['usd_rewards'] = df.apply(lambda x: convert_tool(x['rewards'], x['static_usd_rate']), axis = 1)

## Description, Blurb, Slug Len
df['description_len'] = df['description'].str.len()
df['blurb_len'] = df['blurb'].str.len()
df['slug_len'] = df['slug'].str.len()

##State of Project
df = df[(df['state']=='successful') | (df['state'] == 'failed')]
df.drop(df[(df['state'] == 'failed') & (df['reach_goal'] == True)].index, inplace = True)
df.drop(df[(df['state'] == 'successful') & (df['reach_goal'] == False)].index, inplace = True)

## Saving File
df.to_pickle('kickstarter_clean.pkl')
