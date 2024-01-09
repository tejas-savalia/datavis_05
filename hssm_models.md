# Model 1
## Need to rerun this one, accidentally overwrote.
Fully converged after removing the direction factor.

hssm_model = hssm.HSSM(data=comb_data[[ 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference', 'cond']], 
            include=
            [{"name": "v",
              "formula": "v ~  C(bumps_)"},
              {"name": "a",
              "formula": "a ~ C(cond)"},
              {"name": "z",
              "formula": "z ~ C(direction) + C(diff_dir)"
              }
              ],
              p_outlier = 0.05,
              lapse=bmb.Prior("Uniform", lower=0.0, upper=20.0),
              loglik_kind = "approx_differentiable",
              prior_settings="safe"
              )
              




# Model 2
This one did not converge.
hssm_model = hssm.HSSM(data=comb_data[[ 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference', 'cond']], 
            include=
            [{"name": "v",
              "formula": "v ~  C(bumps_) + C(cond)"},
              {"name": "a",
              "formula": "a ~ 0 + difference"},
              {"name": "z",
              "formula": "z ~ C(direction) + C(diff_dir)"
              }
              ],
              p_outlier = 0.05,
              lapse=bmb.Prior("Uniform", lower=0.0, upper=20.0),
              loglik_kind = "approx_differentiable",
              prior_settings="safe"
              )

