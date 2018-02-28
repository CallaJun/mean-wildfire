import sqlite3
from sqlite3 import Error
from random import randint
import collections
from cmath import sqrt
from math import pow
import math
import matplotlib.pyplot as plt
import pandas as pd

class Fire():
    def __init__(self, fire_size, stat_cause_code, discovery_date, cont_date, fire_year):
        self.fire_size = fire_size
        self.stat_cause_code = stat_cause_code
        self.fire_year = fire_year
        epoch = pd.to_datetime(0, unit='s').to_julian_date()
        self.fire_length = (pd.to_datetime(cont_date - epoch, unit='D') 
            - pd.to_datetime(discovery_date - epoch, unit='D')).days

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

def select_data(connection, year):
    cur = connection.cursor()
    cur.execute("SELECT FIRE_SIZE,STAT_CAUSE_CODE,DISCOVERY_DATE,CONT_DATE,FIRE_YEAR FROM Fires")
    data = cur.fetchall()
    relevant_data = []
    fire_objects = []
    epoch = pd.to_datetime(0, unit='s').to_julian_date()
    for row in data:
        if row[0] is None or row[1] is None or row[2] is None or row[3] is None:
            continue
        if row[4] != year:
            continue
        discovery = pd.to_datetime(row[2] - epoch, unit='D')
        contained = pd.to_datetime(row[3] - epoch, unit='D')
        fire_length = (contained - discovery).days
        relevant_data.append([row[0], fire_length])
        fire_objects.append(Fire(row[0], row[1], row[2], row[3], row[4]))
    return fire_objects
    #return relevant_data

def euclidean_distance(centroid, fire2):
    point1 = centroid
    point2 = [fire2.fire_size, fire2.fire_length]
    return math.sqrt(((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2))

def k_means(dataset, k):
    dataset_size = len(dataset) - 1
    print(dataset_size)
    centroids = []
    # Set initial centroid size randomly from the dataset
    for i in range(k):
        random_fire = dataset[int(randint(1, dataset_size))]
        centroids.append([random_fire.fire_size, random_fire.fire_length])

    num_iterations = 0
    while True:
        # Create clusters and distances lists, and set initial values
        clusters = []
        distances = []
        for i in range(dataset_size):
            clusters.append(0)
            distances.append(float("inf"))

        # Set points to nearest centroids
        for centroid in centroids:
            for i in range(dataset_size):
                # Find the distance between centroid and point, update if needed
                euclidean_dist = euclidean_distance(centroid, dataset[i])
                if euclidean_dist < distances[i]:
                    clusters[i] = centroids.index(centroid)
                    distances[i] = euclidean_dist
        cluster_points = [[] for i in range(k)]
        for i in range(dataset_size):
            cluster_points[clusters[i]].append(dataset[i])

        old_centroids = []
        for centroid in centroids:
            old_centroids.append(list(centroid))
        old_centroids_list = cluster_points[:]

        # Reset centroid value
        for centroid in centroids:
            for i in range(len(centroid)):
                centroid[i] = 0

        # Update centroid, sum data
        for i in range(len(cluster_points)):
            # Store current cluster
            current = i
            for data in cluster_points[i]:
                # Iterate through cluster
                centroids[current][0] += data.fire_size 
                centroids[current][1] += data.fire_length

        # Finish updating centroid, divide for mean
        for i in range(len(centroids)):
            # Check for empty cluster
            if len(cluster_points[i]) == 0:
                random_fire = dataset[int(randint(1, dataset_size))]
                centroids.append([random_fire.fire_size, random_fire.fire_length])
            else:
                centroids[i][0] /= len(cluster_points[i])
                centroids[i][1] /= len(cluster_points[i])

        num_iterations += 1
        # Test whether centroids are in their ideal location
        if old_centroids == centroids:
            colors = ['ro', 'go', 'bo', 'co', 'mo', 'yo', 'ko', 'wo']
            x1 = []
            y1 = []
            for i in range(len(old_centroids_list)):
                print(len(old_centroids_list)) # LIST OF CLUSTERS
                x2 = []
                y2 = []
                for data_list in old_centroids_list[i]:
                    x2.append(data_list.fire_size)
                    y2.append(data_list.fire_length)
                x1.append(list(x2))
                y1.append(list(y2))

            # Plot data, taking color into account
            for i in range(len(x1)):
                plt.plot(x1[i], y1[i], colors[i])

            # Add x and y axis
            plt.xlabel("X-Axis (fire size)")
            plt.ylabel("Y-Axis (fire length)")

            # Plot centroids
            print("Number of iterations: " + str(num_iterations))
            for i in range(len(centroids)):
                plt.plot([int(centroids[i][0])], [int(centroids[i][1])], 'kd')

            # Show the plot
            plt.show()
            break

def main():
    database = "wildfires.sqlite"
 
    # Create a database connection
    connection = create_connection(database)
    with connection:
        k_means(select_data(connection, 2004), 3)

if __name__ == '__main__':
    main()
