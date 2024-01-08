import numpy as np 
import pandas as pd 
import seaborn as sns 
import matplotlib.pyplot as plt 
import bambi as bmb 
import hssm
import os
import arviz as az 
import pymc as pm 
from utils import *
hssm.set_floatX("float32")
random_seed = 10


files = os.listdir('data/')
comb_data = pd.concat([extract_data(fname) for fname in files]).reset_index(drop=True)

comb_data['bumps_'] = '0_noisy'
comb_data.loc[comb_data['bumps'] == 'single', 'bumps_'] = '1_single'
comb_data.loc[comb_data['bumps'] == 'center', 'bumps_'] = '2_center'
print('here')

# hssm_model = hssm.HSSM(data=comb_data[['participant', 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference']])
hssm_model = hssm.HSSM(data=comb_data[['participant', 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference']], 
            include=
            [{"name": "v",
              "formula": "v ~  C(bumps_)"},
              # {"name": "t", 
              #  "formula" : "t ~ (1|participant)"},
              {"name": "a",
               "formula": "a ~ difference"},
              {"name": "z",
              "formula": "z ~ C(direction) + C(diff_dir)"
              }
              ])

print('here')
sample = hssm_model.sample()
az.to_netcdf(sample, 'modeling_results/hssm_results/model_1')