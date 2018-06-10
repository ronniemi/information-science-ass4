import pandas as pd
import numpy as np
from sklearn import preprocessing

def read_file():
    df = pd.read_excel("./data.xlsx")
    return df

# complete missing values
def replace_na(df):
    for column in df:
        if df[column].dtype == 'float64':
            df[column].fillna((df[column].mean()), inplace=True)

#Standardization
def standardization(df):
    preprocessing.scale(df, axis=0, with_mean=True, with_std=True, copy=False)


#def data_grouping(df):

def clean_data(df):
    replace_na(df)
    standardization(df)




df = read_file()
clean_data(df)
print(df)
