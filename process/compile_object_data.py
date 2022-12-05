import pandas as pd
import numpy.matlib as np
from scipy.stats import mannwhitneyu, ttest_ind
from math import comb
import statsmodels.formula.api as smf
import pathlib

from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap

def compile_object_data(data_path, pm, drop_columns):

    # data_path = '/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-22_soma_objects_soma.csv'
    # drop_columns = pd.read_csv('/fsx/processed-data/220811 96w 9 Gene KO /2022-08-22_soma_objects/2022-08-30_soma_objects_soma_column_drop_list.csv', header=None, dtype=str)
    morphology_file = 'FileName_morphology'

    # Load processed cellprofiler soma data from csv
    soma_data = pd.read_csv(data_path)
    soma_data.index = soma_data['ImageNumber']
    path_parts = list(data_path.parts)
    path_parts[-1] = path_parts[-1].replace('_soma.csv', '_Image.csv')
    data_path = pathlib.Path(*path_parts)
    image_data = pd.read_csv(data_path)
    image_data.index = image_data['ImageNumber']

    # Convert from per-soma measuremnt to per-image measurements
    data = pd.DataFrame(data = 0, index=image_data.index, columns=soma_data.columns)
    # print(image_data.index) 
    for i in image_data.index:
        data.loc[i] = soma_data.loc[i].mean(axis=0)

    # Set index to well name
    data.index = image_data[morphology_file]

    # Remove unwanted columns
    drop_columns = np.array(drop_columns).astype(str).flatten()
    for col in drop_columns:
        data = data.drop(data.columns[data.columns.str.contains(col)], axis=1)
    # print(data.head())
    # print(pm.head())
    # Reindex data by platemap filenames to make sure row order is correct
    pm.index = pm['filename']
    data = data.reindex(pm.index)

    # Set conditions to index
    data.index = pm['condition']
    pm.index = pm['condition']
    # Also add as column to data (for stats model)
    data['condition'] = data.index

    # Remove 'no_dye' condition
    if 'no_dye' in data.index:
        data = data.drop('no_dye', axis=0)
        pm = pm.drop('no_dye', axis=0)

    data = data - data.mean(axis=0)
    data = data / data.std(axis=0)

    # print(data.columns.tolist())

    # Remove a column (feature) if any values in that col are NA
    data = data.drop(columns=data.columns[data.isna().any()].tolist())
    pca = PCA(n_components=20, random_state=2)
    latent_data = pca.fit_transform(data) # Excluding the no dye controls
    reducer = TSNE(n_components=2, learning_rate='auto', init='pca', perplexity=3, random_state=2)
    # reducer = umap.UMAP(n_neighbors=5, random_state=4)
    embedded_data = reducer.fit_transform(latent_data)
    embedded_data = pd.DataFrame(embedded_data, 
                                index = data.index,
                                columns = ['tSNE 1', 'tSNE 2'])
    embedded_data['condition'] = pm['condition']

    return embedded_data

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