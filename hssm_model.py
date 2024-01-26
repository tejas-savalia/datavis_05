if __name__ == '__main__':
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
    comb_data['participant_id'] = comb_data['participant']
    print('here')

    # hssm_model = hssm.HSSM(data=comb_data[['participant', 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference']])
    hssm_model = hssm.HSSM(data=comb_data[['participant_id', 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference', 'cond']], 
                include=
                [{"name": "v",
                  "formula": "v ~  difference*C(bumps_) + difference*C(cond) + C(bumps_)*C(cond)"},
                  {"name": "a",
                  "formula": "a ~ C(diff_dir)*C(direction)"},
                  {"name": "z",
                  "formula": "z ~ difference"
                  },
                  ],
                  hierarchical = False,
                  p_outlier = 0.05,
                  # lapse=bmb.Prior("Uniform", lower=0.0, upper=20.0),
                  loglik_kind = "analytical",
                  prior_settings="safe"
                  )

    print('here, nonhierarchical no interaction + direction on z with inferencedata')
    sample = hssm_model.sample(target_accept=0.95)
    az.to_netcdf(sample, 'modeling_results/hssm_results/model_2')