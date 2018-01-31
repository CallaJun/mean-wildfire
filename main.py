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

def select_all_tasks(connection):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = connection.cursor()
    cur.execute("SELECT * FROM Fires")
 
    rows = cur.fetchall()
    print(len(rows))
    #for row in rows:
    #    print(row)

def main():
    database = "FPA_FOD_20170508.sqlite"
 
    # create a database connection
    connection = create_connection(database)
    with connection:
        print("Query all Fires")
        select_all_tasks(connection)

if __name__ == '__main__':
    main()