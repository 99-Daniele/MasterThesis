from utils.DatabaseConnection import getDataFromDatabase

def getAllEvents(connection):
    query = "SELECT numProcesso, data, fase FROM eventi WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    return getDataFromDatabase(connection, query)

def getImportantEvents(connection):
    query = "SELECT numProcesso, data, fase FROM eventiimportanti WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    return getDataFromDatabase(connection, query)

def getCourtHearingsEvents(connection):
    query = "SELECT numProcesso, data, fase FROM udienze WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    return getDataFromDatabase(connection, query)

def getAllProcesses(connection):
    query = "SELECT * FROM processicondurata"
    return getDataFromDatabase(connection, query)

def getFinishedProcesses(connection):
    query = "SELECT * FROM processicondurata WHERE processofinito = 1"
    return getDataFromDatabase(connection, query)

def getUnfinishedProcesses(connection):
    query = "SELECT * FROM processicondurata WHERE processofinito = 0"
    return getDataFromDatabase(connection, query)

def getStoppedProcesses(connection):
    query = "SELECT * FROM processicondurata WHERE processofinito = 2"
    return getDataFromDatabase(connection, query)

def getStuckedProcesses(connection):
    query = "SELECT * FROM processicondurata WHERE processofinito = -1"
    return getDataFromDatabase(connection, query)