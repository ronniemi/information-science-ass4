import pandas as pd
import numpy as np
from sklearn import preprocessing
import os.path
from sklearn.cluster import KMeans

#pre_processed_file_path = ""
pre_processed_file_path = r"d:\documents\users\ronniemi\Downloads\Assignment4\pre_processed_data.csv"

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

# change country columns from string type to numeric lables
def lable_encoder(df):
    le = preprocessing.LabelEncoder()
    df['country'] = le.fit_transform(df['country'])
    return df

def k_means(num_of_clusters, num_of_runs):
    try:
        pre_processed_data = pd.read_csv(pre_processed_file_path)
        pre_processed_data = lable_encoder(pre_processed_data)
        k_means_model = KMeans(n_clusters=num_of_clusters, init='random', n_init=num_of_runs)
        countries_prediction = k_means_model.fit_predict(pre_processed_data)
        pre_processed_data['prediction'] = pd.Series(countries_prediction, index=pre_processed_data.index)
        pre_processed_data.to_csv(r"d:\documents\users\ronniemi\Downloads\Assignment4\final.csv", index=False)
    except:
        raise ValueError('pre processed file not exist')

def pre_process(path):
    df = read_file(path)
    df = clean_data(df)
    parent_path = os.path.abspath(os.path.join(path, os.pardir))
    pre_processed_file_path = parent_path + '/pre_processed_data.csv'
    df.to_csv(pre_processed_file_path, index=False)

k_means(3,3)