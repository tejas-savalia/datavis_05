# Model 0
hssm_model = hssm.HSSM(data=comb_data[['participant', 'rt', 'response', 'means', 'direction', 'bumps_', 'diff_dir', 'difference']], 
            include=
            [{"name": "v",
              "formula": "v ~ C(direction) + C(bumps_) + C(diff_dir)"},
              {"name": "t", 
               "formula" : "t ~ (1|participant)"},
              {"name": "a",
               "formula": "a ~ difference"},
              {"name": "z",
              "formula": "z ~ C(direction)"
              }

              ])


