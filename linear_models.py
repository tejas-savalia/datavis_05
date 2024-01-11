if __name__ == '__main__':
    import numpy as np 
    import pandas as pd 
    import seaborn as sns 
    import matplotlib.pyplot as plt 
    import bambi as bmb 
    # import hssm
    import os
    import arviz as az 
    import pymc as pm
    # hssm.set_floatX("float32")
    random_seed = 10
    from utils import *


    files = os.listdir('data/')
    comb_data = pd.concat([extract_data(fname) for fname in files]).reset_index(drop=True)
    comb_data = comb_data.loc[comb_data['rt'] < 10].reset_index(drop = True)
    comb_data = comb_data.loc[comb_data['rt'] > 0.1].reset_index(drop = True)

    comb_data['bumps_'] = '0_noisy'
    comb_data.loc[comb_data['bumps'] == 'single', 'bumps_'] = '1_single'
    comb_data.loc[comb_data['bumps'] == 'center', 'bumps_'] = '1_center'
    comb_data['participant_id'] = comb_data['participant']


    single_param_models = ['diff_dir', 'means', 'direction', 'bumps', 'difference', 'cond']
    def single_param_model_fits(single_param_models, dv = 'accuracy', family = 'bernoulli', data = comb_data):
        model_single_param_samples = {}
        for param in single_param_models:
            print('Fittting param: ', param)
            models_oneparam_nh = bmb.Model(f'{dv}~{param}', data = comb_data, family= family)
            models_oneparam_nh.build()
            model_single_param_samples[param] = models_oneparam_nh.fit(idata_kwargs={"log_likelihood": True})

        return model_single_param_samples

    def additive_model_fit(dv = 'accuracy', family = 'bernoulli', data = comb_data):
        allparam_nh = bmb.Model(f'{dv}~ C(diff_dir) + means + C(direction) + C(bumps) + difference + cond', 
        data = comb_data, family=family)
        allparam_nh.build()
        # allparam_nh.graph()
        allparam_nh_samples = allparam_nh.fit(idata_kwargs={"log_likelihood": True})
        return allparam_nh_samples

    def models_with_interaction_fits(dv = 'accuracy', family = 'bernoulli', data = comb_data, formula_rhs = 'C(diff_dir) + means + C(direction) + difference + C(bumps_)*C(cond)'):
        allparam_interaction_nh = bmb.Model(f'{dv} ~ {formula_rhs}', 
        data = data, family=family)
        allparam_interaction_nh.build()
        # allparam_interaction_nh.graph()
        allparam_interaction_nh_samples = allparam_interaction_nh.fit(idata_kwargs={"log_likelihood": True})
        return allparam_interaction_nh_samples


    model_comp_dict = {}
    model_comp_dict['model_allparam_bumps_cond_interaction'] = models_with_interaction_fits()
    for key in model_comp_dict.keys():
        model_comp_dict[key].to_netcdf(f'modeling_results/linear_modeling_results/'key)