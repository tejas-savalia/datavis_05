import numpy as np
import pandas as pd
import os

def extract_data(fname):
    # Drop rows with missing data in column: 'means'
    if fname.endswith('csv'):
        data = pd.read_csv('data/'+fname)
        if len(data) != 587:
            # print(len(data))
            return None
    else: 
        return None

    try:
        data = data.dropna(subset=['means'])
        # Filter rows based on column: 'difference'
        data = data[data['difference'].notna()]
        # Select columns: 'means', 'direction' and 8 other columns
        if data['participant'].unique()[0]%3 == 0:
            data['key_resp'] = data['slider_resp_recorded_keyresp.keys']
            data['rt'] = data['slider_resp_recorded_keyresp.rt']
            data['cond'] = 'chart'
        elif data['participant'].unique()[0]%3 == 1:
            data['key_resp'] = data['numerical_choice_resp.keys']
            data['rt'] = data['numerical_choice_resp.rt']
            data['cond'] = 'slider'
        else:
            data['key_resp'] = data['slider_resp_recorded_keyresp_2.keys']
            data['rt'] = data['slider_resp_recorded_keyresp_2.rt']
            data['cond'] = 'numerical'

        data = data.loc[:, ['participant', 'means', 'direction', 'bumps', 'diff_dir', 'trials.thisN', 'difference', 'incorrect choice', 'key_resp', 'rt', 'cond']]
        data['accuracy'] = (data['incorrect choice'].values != data['key_resp'].values)
        data['response'] = -1
        data.loc[data['accuracy'], 'response'] = 1
    except:
        return None
    return data.reset_index(drop=True)

# data_clean = extract_data(data.copy())
# data_clean.head()