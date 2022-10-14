import pandas as pd
import numpy.matlib as np
from scipy.stats import mannwhitneyu, ttest_ind
from math import comb

def cp_image_data(data_path, pm, drop_columns):


    # Load processed cellprofiler data from csv
    data = pd.read_csv(data_path)
    # Set index to well name
    morphology_file = 'FileName_TMRM'
    data.index = data[morphology_file]
    pm.index = pm['filename']
    
    # Remove unwanted columns
    drop_columns = np.array(drop_columns).astype(str).flatten()
    for col in drop_columns:
        data = data.drop(data.columns[data.columns.str.contains(col)], axis=1)

    # Reindex data by platemap filenames to make sure row order is correct
    data = data.reindex(pm.index)

    # Set conditions to index
    data.index = pm['condition']
    pm.index = pm['condition']

    # Remove 'no_dye' condition
    if 'no_dye' in data.index:
        data = data.drop('no_dye', axis=0)
        pm = pm.drop('no_dye', axis=0)

    return data, pm

def image_stats(data, measurement, conditions, ctrl_cond):    

    # Get 'comparison' conditions (all but control)
    comp_conditions = list(set(conditions) - set(ctrl_cond))
    # comp_conditions = conditions[1:]

    p_vals = pd.DataFrame(np.zeros((len(comp_conditions),1)), index=comp_conditions)
    for cond in comp_conditions:
        sub = data.loc[[ctrl_cond[0], cond]]
        x_data = data[measurement].loc[ctrl_cond]
        y_data = data[measurement].loc[cond]
        res = mannwhitneyu(y=y_data, x=x_data)
        # res = ttest_ind(y_data, x_data)
        p_vals.loc[cond] = res.pvalue

    # adj_p_vals = p_vals * comb(len(conditions), 2)
    # p = 0.05 / comb(len(conditions), 2)
    p_adj = 0.05 / len(comp_conditions)
    h = p_vals < p_adj

    return p_vals, p_adj, h