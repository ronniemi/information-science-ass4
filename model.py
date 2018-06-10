import pandas as pd
import numpy as np
from sklearn import preprocessing
import os.path
from sklearn.cluster import KMeans
from random import randint
import matplotlib.pyplot as plt

directory_path = ""

data_after_pre_procsess = pd.DataFrame()

def read_file(path):
    df = pd.read_excel(path)
    if len(df) < 1:
        raise ValueError('empty file')
    df.drop(['year'], inplace=True, axis=1)
    return df

# complete missing values
def replace_na(df):
    for column in df:
        if df[column].dtype == 'float64':
            df[column].fillna((df[column].mean()), inplace=True)

#Standardization
def standardization(df):
    for column in df:
        if df[column].dtype == 'float64':
            preprocessing.scale(df[column], axis=0, with_mean=True, with_std=True, copy=False)

def data_grouping(df):
    return df.groupby('country', as_index=False).agg('mean')


def clean_data(df):
    replace_na(df)
    standardization(df)
    df = data_grouping(df)
    return df

def pre_process(path):
    global directory_path
    global data_after_pre_procsess

    df = read_file(path)
    df = clean_data(df)

    directory_path = os.path.abspath(os.path.join(path, os.pardir))
    data_after_pre_procsess = df

    #pre_processed_file_path = directory_path + '/pre_processed_data.csv'
    #df.to_csv(pre_processed_file_path, index=False)

def generate_colors(list_size):
    colors = []
    for i in range(list_size):
        colors.append('%06X' % randint(0, 0xFFFFFF))
    return colors

def k_means(num_of_clusters, num_of_runs):
    try:
        data_after_pre_procsess.index = data_after_pre_procsess['country']
        data_after_pre_procsess.drop(['country'], inplace=True, axis=1)

        k_means_model = KMeans(n_clusters=num_of_clusters, init='random', n_init=num_of_runs)
        k_means_model.fit(data_after_pre_procsess)

        data_after_pre_procsess['prediction'] = k_means_model.labels_
    except:
        raise ValueError('pre processed file not exist')

def plot_scatter():
    x = data_after_pre_procsess['Social support']
    y = data_after_pre_procsess['Generosity']
    plt.scatter(x, y ,c=data_after_pre_procsess['prediction'], alpha=0.5)
    plt.title('K Means Clustering')
    plt.xlabel('Social support')
    plt.ylabel('Generosity')
    plt.show()
