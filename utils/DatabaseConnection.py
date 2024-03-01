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
        length = len(tuples[0])
        filler = createFiller(length)
        for t in tuples:
            insertIntoDatabase(connection, table, filler, t)
            bar()
    connection.commit()  

def clearTable(connection, table):
    query = "DELETE FROM {}".format(table)
    cursor = connection.cursor(buffered = True)
    cursor.execute(query)
    connection.commit()  

def insertIntoDatabase(connection, table, filler, values):
    query = ("INSERT INTO {} VALUES" + filler).format(table)
    cursor = connection.cursor(buffered = True)
    cursor.execute(query, values)

def createFiller(length):
    filler = "("
    for i in range(length - 1):
        filler = filler + "%s, "
    filler = filler + "%s)"
    return filler

