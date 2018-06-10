import pandas as pd
import numpy as np
from sklearn import preprocessing

def read_file():
    df = pd.read_excel("./data.xlsx")
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
    df = df.groupby('country').agg('mean')
    return df


def clean_data(df):
    replace_na(df)
    standardization(df)
    return df

df = read_file()
df = clean_data(df)
df = data_grouping(df)
print(df)
