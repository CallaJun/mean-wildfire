import sqlite3
from sqlite3 import Error

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

    cur.execute("SELECT FIRE_SIZE,LATITUDE,LONGITUDE FROM Fires")
    data = cur.fetchall()
    for row in data:
        print("size: ", row[0],
            " lati: ", row[1],
            " long: ", row[2])
    #for row in rows:
    #    print(row)

def euclidean_distance(point1, point2):
    sum = 0
    from math import pow
    from cmath import sqrt
    for i in xrange(len(point1)):
        sum += pow(float(point1[i]) - float(point2[i]), 2)
    return abs(sqrt(sum))

def main():
    database = "wildfires.sqlite"
 
    # create a database connection
    connection = create_connection(database)
    with connection:
        print("Query all Fires")
        select_data(connection)

if __name__ == '__main__':
    main()