from alive_progress import alive_bar
import mysql.connector as cnx
import os

import utils.FileOperation as file

def getDatabaseConnection():
    if os.path.isfile('utils/databaseCredentials.json'):
        credentials = file.getDataFromJsonFile('utils/databaseCredentials.json')
        host = credentials['host']
        user = credentials['user']
        password = credentials['password']
        database = credentials['database']
        return connectToDatabase(host, user, password, database)
    else:
        while True:
            host = input("Insert host: ")
            user = input("Insert user: ")
            password = input("Insert password: ")
            database = input("Insert database name: ")
            try:
                connection = connectToDatabase(host, user, password, database)
                credentials = {'host': host, 'user': user, 'password': password, 'database': database}
                file.writeOnJsonFile('utils/databaseCredentials.json', credentials)
                return connection
            except:
                print("\nWrong credentials!! Please give right credentials")

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

def executeQuery(connection, query):
    cursor = connection.cursor(buffered = True)
    cursor.execute(query)
    connection.commit()  

def executeQueryWithValues(connection, query, values):
    cursor = connection.cursor(buffered = True)
    cursor.execute(query, values)
    connection.commit()  

def doesATableExist(connection, table):
    query = "SELECT COUNT(*) > 0 FROM information_schema.tables WHERE table_name = '" + table + "' AND table_type = 'BASE TABLE' LIMIT 1"
    r = getDataFromDatabase(connection, query)
    return r[0][0] == 1

def doesATableHaveColumns(connection, table, columns):
    for column in columns:
        query = "SELECT COUNT(*) > 0 FROM information_schema.columns WHERE table_name = '" + table + "' AND column_name = '" + column + "'"
        r = getDataFromDatabase(connection, query)
        if r[0][0] == 0:
            return False
    return True

def doesAViewExist(connection, table):
    query = "SELECT COUNT(*) > 0 FROM information_schema.tables WHERE table_name = '" + table + "' AND table_type = 'VIEW' LIMIT 1"
    r = getDataFromDatabase(connection, query)
    return r[0][0] == 1

def createTable(connection, tableName, columnNames, columnTypes, primaryKeys, notNullables): 
    if doesATableExist(connection, tableName):
        dropTable(connection, tableName)
    query = "CREATE TABLE " + tableName + "("
    i = 0
    while i < len(columnNames):
        query = query + columnNames[i] + " " + columnTypes[i]
        if i in notNullables:
            query = query + " NOT NULL"
        query = query + ", "
        i = i + 1
    query = query + "PRIMARY KEY ("
    j = 0
    while j < len(primaryKeys):
        key = primaryKeys[j]
        query = query + columnNames[key]
        if j < len(primaryKeys) - 1:
            query = query + ", "
        j = j + 1
    query = query + "));"
    executeQuery(connection, query)

def createStrangeTable(connection, table, query):
    if doesATableExist(connection, table):
        dropTable(connection, table)
    executeQuery(connection, query)

def createView(connection, view, query):
    if doesAViewExist(connection, view):
        dropTable(connection, view)
    executeQuery(connection, query)
    return

def dropTable(connection, table):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't drop this table since it doesn't exist!!")
    query = "DROP TABLE " + table
    executeQuery(connection, query)

def dropView(connection, view):
    if not doesAViewExist(connection, view):
        raise Exception("\nYou can't drop this view since it doesn't exist!!")
    query = "DROP VIEW " + view
    executeQuery(connection, query)

def updateTable(connection, table, dataInfo, condition):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't update this table since it doesn't exist!! Please use function 'createTable()' in order to create it.")
    removeFromDatabase(connection, table, dataInfo[1], condition)
    connection.commit()
    insertIntoDatabase(connection, table, dataInfo[0])
    connection.commit()

def updateTableMultiple(connection, table, dataInfo, condition):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't update this table since it doesn't exist!! Please use function 'createTable()' in order to create it.")
    removeFromDatabaseMultiple(connection, table, dataInfo[1], condition)
    connection.commit()
    insertIntoDatabase(connection, table, dataInfo[0])
    connection.commit()

def clearTable(connection, table):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't clear this table since it doesn't exist!! Please use function 'createTable()' in order to create it.")
    query = "DELETE FROM {}".format(table)
    executeQuery(connection, query)

def insertIntoDatabase(connection, table, tuples):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't insert into this table since it doesn't exist!! Please use function 'createTable()' in order to create it.")
    if len(tuples) > 0:
        with alive_bar(int(len(tuples))) as bar:
            length = len(tuples[0])
            filler = createFiller(length)
            for t in tuples:
                query = ("INSERT INTO {} VALUES" + filler).format(table)
                executeQueryWithValues(connection, query, t)
                bar()

def removeFromDatabase(connection, table, ids, condition):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't delete from this table since it doesn't exist!! Please use function 'createTable()' in order to create it.")
    with alive_bar(int(len(ids))) as bar:
        for id in ids:
            query = ("DELETE FROM {} WHERE " + condition + " = " + str(id)).format(table)
            executeQuery(connection, query)
            bar()

def removeFromDatabaseMultiple(connection, table, conditions, condition):
    if not doesATableExist(connection, table):
        raise Exception("\nYou can't delete from this table since it doesn't exist!! Please use function 'createTable()' in order to create it.")
    with alive_bar(int(len(conditions))) as bar:
        for c in conditions:
            query = ("DELETE FROM {} WHERE " + condition + " = " + str(c[0]) + " AND ordine = " + str(c[1])).format(table)
            executeQuery(connection, query)
            bar()

def createFiller(length):
    filler = "("
    for i in range(length - 1):
        filler = filler + "%s, "
    filler = filler + "%s)"
    return filler