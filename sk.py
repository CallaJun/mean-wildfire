import sqlite3
import pandas as pd
from sklearn.cluster import KMeans
from sklearn import metrics
import matplotlib.pyplot as plt 
def main():
    # Create a database connection
    connection = sqlite3.connect("wildfires.sqlite")
    df = pd.read_sql_query("SELECT LATITUDE,LONGITUDE FROM 'Fires'", connection)
    attributes = ['LATITUDE','LONGITUDE']

    #df = df.drop(['LATITUDE','LONGITUDE'], axis=1)
    #df['LATITUDE'] = df['LATITUDE'].fillna(df['LATITUDE'].median())
    #df['LONGITUDE'] = df['LONGITUDE'].fillna(df['LONGITUDE'].median())

    data_attributes = df[attributes]
    kmeans_model = KMeans(n_clusters=2, random_state=1)
    distances = kmeans_model.fit_transform(data_attributes)
    labels = kmeans_model.labels_
    plt.scatter(distances[:,0],distances[:,1],c=labels)
    plt.title('K-means')
    plt.show()

if __name__ == '__main__':
    main()
