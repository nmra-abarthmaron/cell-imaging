import pandas as pd
import numpy.matlib as np
from scipy.stats import mannwhitneyu, ttest_ind
from math import comb
import statsmodels.formula.api as smf

def cp_object_data():

    data_path = '/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-22_soma_objects_soma.csv'
    drop_columns = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-30_soma_objects_soma_column_drop_list.csv', header=None, dtype=str)
    morphology_file = 'FileName_TMRM'

    # Load platemap / well conditions
    pm = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/soma_outlines/220811_well_conditions.csv', index_col='filename')# Add condition labels to well dataframe

    # Load processed cellprofiler data from csv
    data = pd.read_csv(data_path)

    # Set index to well name
    data.index = data[morphology_file]

    # Create soma 'platemap' (condition list)
    pm_soma = pd.DataFrame()
    pm_soma['condition'] = pm.loc[data[morphology_file]]['condition']
    data['filename'] = pm_soma.index

    # Remove unwanted columns
    drop_columns = np.array(drop_columns).astype(str).flatten()
    for col in drop_columns:
        data = data.drop(data.columns[data.columns.str.contains(col)], axis=1)
    pm = pm_soma

    # Set conditions to index
    data.index = pm['condition']
    pm.index = pm['condition']
    # Also add as column to data (for stats model)
    data['condition'] = data.index

    # Remove 'no_dye' condition
    data = data.drop('no_dye', axis=0)
    pm = pm.drop('no_dye', axis=0)

    return data, pm

def object_stats(data, measurement, conditions, ctrl_cond):

    # Get 'comparison' conditions (all but control)
    comp_conditions = list(set(conditions) - set(ctrl_cond))
    # comp_conditions = conditions[1:]

    p_vals = pd.DataFrame(np.zeros((len(comp_conditions),1)), index=comp_conditions)
    for cond in comp_conditions:
        sub = data.loc[[ctrl_cond[0], cond]]
        x_data = data[measurement].loc[ctrl_cond]
        y_data = data[measurement].loc[cond]
        # res = mannwhitneyu(y=y_data, x=x_data)
        # res = ttest_ind(y_data, x_data)
        # p_vals.loc[cond] = res.pvalue
        md = smf.mixedlm(measurement + ' ~ condition', data=sub, groups=sub['filename'])
        mdf = md.fit(method=["lbfgs"])
        p_vals.loc[cond] = mdf.pvalues[1]

    # adj_p_vals = p_vals * comb(len(conditions), 2)
    # p = 0.05 / comb(len(conditions), 2)
    p_adj = 0.05 / len(comp_conditions)
    h = p_vals < p_adj

    return p_vals, p_adj, h