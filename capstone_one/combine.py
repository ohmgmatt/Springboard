import pandas as pd

from os import path
import glob
import numpy as np
import json
import matplotlib.pyplot as plt
import math
import time

## Accessing where data files are stored
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "data"))

files = glob.glob(filepath + "/*.csv")

## Combining all datasets
sets = []
for filename in files:
    f = pd.read_csv(filename, index_col = None, header = 0)
    sets.append(f)

df = pd.concat(sets, axis = 0, ignore_index = True)



## Clean Up
## Cleaning the time fields
def epoch_to_date(epoch):
    struct = time.gmtime(epoch)
    date_string = time.strftime("%Y-%m-%d", struct)
    return date_string

def epoch_to_time(epoch):
    struct = time.gmtime(epoch)
    time_string = time.strftime("%H:%M:%S", struct)
    return time_string

date_fields = ['created_at', 'deadline', 'launched_at', 'state_changed_at']

for field in date_fields:
    df[field+'_date'] = df[field].apply(epoch_to_date)
    df[field+'_time'] = df[field].apply(epoch_to_time)


## Cleaning up the categories
## Pulling the information from inside the json structure
## so they're in their own columns
def puller(value, category):
    try:
        return json.loads(value)[category]
    except:
        return 'N/A'

to_clean = {
    'category':['name', 'slug'],
    'location':['displayable_name', 'localized_name','country', 'state'],
    'profile':['id', 'project_id', 'state'],
    'urls':['web']
}

for key,value in to_clean.items():
    for v in value:
        df[key+'_'+v] = df[key].apply(puller, category = v)


## Dropping values that are not relevant to the analysis
## Values range from being specific to the account that pulled the datasets
## to redundant information such as currency_symble
## where it's redundant from curreny but provides less information
droplist = ['friends', 'is_backing', 'is_starred', 'permissions',
        'currency_symbol', #$ related to USD, CAD, AUS etc.
        'disable_communication', #? not necessary
        'is_starrable', #? not necessary
        'photo', #not necessary. no image analysis
        'source_url'] #only discover category url, not useful for analysis since we already have category
df.drop(droplist, axis = 1, inplace = True)


## Pulling the URLs from 'web' column for easier processing
def url_pull(x):
    return json.loads(x)['web']['project'].split('?')[0]

df['web_url'] = df['urls'].apply(url_pull)



df.to_pickle('kickstarter.pkl')
