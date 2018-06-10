import pandas as pd
import numpy as np
from sklearn import preprocessing
import os.path

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
    df = read_file(path)
    df = clean_data(df)
    parent_path = os.path.abspath(os.path.join(path, os.pardir))
    df.to_csv(parent_path + '/pre_processed_data.csv', index=False)
