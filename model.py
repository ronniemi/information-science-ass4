import pandas as pd
from sklearn import preprocessing
import os.path
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import plotly.plotly as py
import random

directory_path = ""
data_after_pre_procsess = pd.DataFrame()
countries = pd.DataFrame()

'''
read excel file and insert the data into dataFrame
@:param path path for data file
@:return dataFrame of data without the column year
'''
def read_file(path):
    df = pd.read_excel(path)
    if len(df) < 1:
        raise ValueError('empty file')
    df.drop(['year'], inplace=True, axis=1)
    return df

'''
complete missing values according to column mean value
@:param dataFrame with data
'''
def replace_na(df):
    for column in df:
        if df[column].dtype == 'float64':
            df[column].fillna((df[column].mean()), inplace=True)

'''
for each numeric column, change the value into the standard value
@:param dataFrame with data
'''
#Standardization
def standardization(df):
    for column in df:
        if df[column].dtype == 'float64':
            preprocessing.scale(df[column], axis=0, with_mean=True, with_std=True, copy=False)

'''
create new dataframe containing for each country the avg values of the country
@:param df dataFrame with data
@:return dataFrame after group by
'''
def data_grouping(df):
    return df.groupby('country', as_index=False).agg('mean')


'''
replace empty values, change values to standad values and group by
@:param df dataFrame with data
@:return dataFrame after cleaning the data
'''
def clean_data(df):
    replace_na(df)
    standardization(df)
    df = data_grouping(df)
    return df

'''
preform pre process on data
@:param path path for data file
'''
def pre_process(path):
    global directory_path
    global data_after_pre_procsess

    df = read_file(path)
    df = clean_data(df)

    directory_path = os.path.abspath(os.path.join(path, os.pardir))
    data_after_pre_procsess = df


'''
run k mean model on data according to user parameters
@:param num_of_clusters number of clusters according to user
@:param num_of_runs number of runs according to user
'''
def k_means(num_of_clusters, num_of_runs):
    global countries
    try:
        if len(countries) == 0:
            countries = data_after_pre_procsess['country']
            data_after_pre_procsess.index = data_after_pre_procsess['country']
            data_after_pre_procsess.drop(['country'], inplace=True, axis=1)

        k_means_model = KMeans(n_clusters=num_of_clusters, init='random', n_init=num_of_runs, random_state="RandomState")
        k_means_model.fit(data_after_pre_procsess)

        data_after_pre_procsess['prediction'] = k_means_model.labels_
    except:
        raise ValueError('data not in the right format')

'''
plot scatter graph of Generosity as a function of Social support.
save image of the graph in the chosen folder
@return path of the image
'''
def plot_scatter():
    x = data_after_pre_procsess['Social support']
    y = data_after_pre_procsess['Generosity']
    print(data_after_pre_procsess['prediction'].nunique())
    colors = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(data_after_pre_procsess['prediction'].nunique())]
    plt.scatter(x, y ,c=colors, alpha=1)
    plt.title('K Means Clustering')
    plt.xlabel('Social support')
    plt.ylabel('Generosity')
    path_to_img = directory_path + '/scatter_img.png'
    plt.savefig(path_to_img)
    return path_to_img

'''
plot choropleth graph according to records classification.
save image of the graph in the chosen folder
@return path of the image
'''
def plot_map():

    # Define the data to be visualised and some of the parameters of the visualisation
    data = [dict(
        type='choropleth',
        locations=countries,
        locationmode='country names',
        z=data_after_pre_procsess['prediction'].astype(str),
        text=countries.astype(str),
        colorscale= 'Rainbow',
        autocolorscale=False,
        reversescale=True,
        marker=dict(
            line=dict(
                color='rgb(180,180,180)',
                width=0.5
            )),
        colorbar=dict(
            autotick=False,
            title='prediction'),
    )]

    layout = dict(
        title='K Means Clustering',
        geo=dict(
            showframe=True,
            showcoastlines=True,
            projection=dict(
                type='Mercator'
            )
        )
    )

    # Plot
    fig = dict(data=data, layout=layout)
    py.sign_in(username='amitmag', api_key='UzC0vg747jN3LLGYMgJc')
    path_to_img = directory_path + '/map_img.png'
    py.image.save_as(fig ,filename= path_to_img)
    return path_to_img