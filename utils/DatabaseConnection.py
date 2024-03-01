import mysql.connector as cnx

import utils.DataUpdate as du

from alive_progress import alive_bar

def connectToDatabase(h, usr, psw, db):
    connection = cnx.connect(
        host = h,
        user = usr,
        password = psw,
        database = db,
        auth_plugin = 'mysql_native_password'
    )
    return connection

def getDataFromDatabase(connection, query):
    cursor = connection.cursor(buffered = True)
    cursor.execute(query)
    return cursor.fetchall()

def dropTable(connection, table):
    query = "DROP TABLE IF EXISTS " + table
    cursor = connection.cursor(buffered = True)
    cursor.execute(query)
    connection.commit()  

def updateTable(connection, table, tuples):
    clearTable(connection, table)
    with alive_bar(int(len(tuples))) as bar:
        for t in tuples:
            t = du.translateTuple(t)
            insertIntoDatabase(connection, table, t)
            bar()
    connection.commit()  

def clearTable(connection, table):
    query = "DELETE FROM {}".format(table)
    cursor = connection.cursor(buffered = True)
    cursor.execute(query)
    connection.commit()  

def insertIntoDatabase(connection, table, process):
    query = "INSERT INTO {} VALUES (%s, %s, %s, %s, %s)".format(table)
    values = (process[0], process[1], process[2], process[3], process[4])
    cursor = connection.cursor(buffered = True)
    cursor.execute(query, values) 

