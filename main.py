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
    def __init__(self, fire_year, state, latitude, longitude):
        self.fire_year = fire_year
        self.state = state

        # What is actually used
        self.x_value = latitude
        self.y_value = longitude

def create_connection(db_file):
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

def select_data(connection, year):
    print("Year: ", year)
    cur = connection.cursor()
    cur.execute("SELECT FIRE_YEAR,STATE,LATITUDE,LONGITUDE FROM Fires")
    data = cur.fetchall()
    relevant_data = []
    fire_objects = []
    epoch = pd.to_datetime(0, unit='s').to_julian_date()
    for row in data:
        if row[2] is None or row[3] is None:
            continue
        if row[0] != year:
            continue
        relevant_data.append([row[2], row[3]])
        fire_objects.append(Fire(row[0], row[1], row[2], row[3]))
    return fire_objects

def euclidean_distance(centroid, fire2):
    point1 = centroid
    point2 = [fire2.x_value, fire2.y_value]
    return math.sqrt(((point1[0] - point2[0])**2) + ((point1[1] - point2[1])**2))

# List of lists of Fire objects
def evaluate_fires(cluster_list):
    for cluster in cluster_list:
        print(str(len(cluster_list)) + " fires in this cluster")
        causes = {}
        for fire in cluster:
            if fire.state not in causes:
                causes[fire.state] = 1
            else:
                causes[fire.state] += 1
        print(causes)

    print(len(cluster_list))

def k_means(dataset, k):
    dataset_size = len(dataset) - 1
    print("Dataset size: ", dataset_size)
    centroids = []
    # Set initial centroid size randomly from the dataset
    for i in range(k):
        random_fire = dataset[int(randint(1, dataset_size))]
        centroids.append([random_fire.x_value, random_fire.y_value])

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
                centroids[current][0] += data.x_value 
                centroids[current][1] += data.y_value

        # Finish updating centroid, divide for mean
        for i in range(len(centroids)):
            # Check for empty cluster
            if len(cluster_points[i]) == 0:
                random_fire = dataset[int(randint(1, dataset_size))]
                centroids.append([random_fire.x_value, random_fire.y_value])
            else:
                centroids[i][0] /= len(cluster_points[i])
                centroids[i][1] /= len(cluster_points[i])

        num_iterations += 1
        # Test whether centroids are in their ideal location
        if old_centroids == centroids:
            colors = ['ro', 'go', 'bo', 'co', 'mo', 'yo', 'ko', 'wo']
            x1 = []
            y1 = []
            evaluate_fires(old_centroids_list)
            for i in range(len(old_centroids_list)):
                x2 = []
                y2 = []
                for data_list in old_centroids_list[i]:
                    x2.append(data_list.x_value)
                    y2.append(data_list.y_value)
                x1.append(list(x2))
                y1.append(list(y2))

            # Plot data, taking color into account
            for i in range(len(x1)):
                plt.plot(x1[i], y1[i], colors[i])

            # Add x and y axis
            plt.xlabel("X-Axis (latitude)")
            plt.ylabel("Y-Axis (longitude)")

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
    connection = connect(database)
    with connection:
        k_means(select_data(connection, 2000), 2)

if __name__ == '__main__':
    main()
