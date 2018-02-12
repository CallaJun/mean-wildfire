import sqlite3
from sqlite3 import Error
from random import randint
import collections
from cmath import sqrt
from math import pow
import matplotlib.pyplot as plt
import pandas as pd

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

def select_data(connection):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = connection.cursor()

    # Printing out each row from Fires
    #cur.execute("SELECT * FROM Fires")
    #rows = cur.fetchall()
    #print(len(rows))

    #cur.execute("SELECT FIRE_SIZE,STAT_CAUSE_CODE FROM Fires")
    cur.execute("SELECT FIRE_SIZE,STAT_CAUSE_CODE,DISCOVERY_DATE,CONT_DATE,FIRE_YEAR FROM Fires")
    data = cur.fetchall()
    relevant_data = []
    epoch = pd.to_datetime(0, unit='s').to_julian_date()
    for row in data:
        # if row[4] != year we want, continue (row 4 is the fire year
        if row[0] is None or row[1] is None or row[2] is None or row[3] is None:
            continue
        discovery = pd.to_datetime(row[2] - epoch, unit='D')
        contained = pd.to_datetime(row[3] - epoch, unit='D')
        fire_length = (contained - discovery).days
        relevant_data.append([row[0], fire_length])
    return relevant_data

def euclidean_distance(point1, point2):
    sum = 0
    from math import pow
    from cmath import sqrt
    for i in range(len(point1)):
        sum += pow(float(point1[i]) - float(point2[i]), 2)
    return abs(sqrt(sum))

def k_means(dataset, k):
    dataset_size = len(dataset)-1
    print(dataset_size)
    #dataset_size = 10000
    centroids = []
    # Set initial centroid size randomly from the dataset
    for i in range(k):
        centroids.append(list(dataset[int(randint(1, dataset_size))]))

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
            cluster_points[clusters[i]].append(list(dataset[i]))

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
                for i in range(len(data)):
                    centroids[current][i] += float(data[i])

        # Finish updating centroid, divide for mean
        for i in range(len(centroids)):
            for j in range(len(data)):
                # Check for empty cluster
                if len(cluster_points[i]) == 0:
                    centroids[i][j] = int(randint(1, dataset_size))
                else:
                    centroids[i][j] /= len(cluster_points[i])

        num_iterations += 1
        # Test whether centroids are in their ideal location
        if old_centroids == centroids:
            colors = ['ro', 'go', 'bo', 'co', 'mo', 'yo', 'ko', 'wo']
            x1 = []
            y1 = []
            for i in range(len(old_centroids_list)):
                x2 = []
                y2 = []
                for data_list in old_centroids_list[i]:
                    x2.append(data_list[0])
                    y2.append(data_list[1])
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
 
    # create a database connection
    connection = create_connection(database)
    with connection:
        print("Query all Fires")
        k_means(select_data(connection), 4)

if __name__ == '__main__':
    main()
