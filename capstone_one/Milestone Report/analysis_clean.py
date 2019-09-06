## Third in the series of cleaning files

import pandas as pd
import numpy as np
df = pd.read_pickle('kickstarter_clean.pkl')

## Updating date fields
date_fields = ['created_at', 'deadline', 'launched_at', 'state_changed_at']
for fields in date_fields:
    df[fields] = pd.to_datetime(df[fields], unit = 's')


## List of columns to drop
drop_list = ['backers_count', 'category', 'converted_pledged_amount',
            'created_at_date', 'created_at_time', 'creator', 'currency_trailing_code',
            'current_currency', 'deadline_date', 'deadline_time', 'fx_rate', 'goal', 'id',
            'launched_at_date', 'launched_at_time', 'location',
            'name', 'pledged', 'profile', 'state_changed_at_date', 'state_changed_at_time', 'urls',
            'usd_type', 'profile_id', 'location_localized_name',
            'profile_project_id', 'profile_state', 'urls_web', 'rewards', 'category_slug',
            'state_changed_at', 'static_usd_rate']


df_analysis = df.drop(drop_list, axis = 1)

df_analysis.reset_index(drop = True, inplace = True)

## Medians of rewards
df_analysis['med_rewards'] = df_analysis.usd_rewards.apply(np.median)
## Len of Rewards
df_analysis['reward_len'] = df_analysis.usd_rewards.str.len()

df_analysis.to_pickle('kickstarter_analysis.pkl')
