import mysql.connector as cnx

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