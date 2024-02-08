from utils.DatabaseConnection import getDataFromDatabase

def getAllEvents(connection, startDate, endDate):
    query = ""
    if endDate == None and startDate == None:
        query = "SELECT numEvento, numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventi"
    elif endDate == None:
        query = "SELECT numEvento, e.numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventi AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataInizioProcesso >= '" + startDate + "'"
    elif startDate == None:    
        query = "SELECT numEvento, e.numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventi AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataFineProcesso <= '" + endDate + "'"
    else:
        query = "SELECT numEvento, e.numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventi AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getImportantEvents(connection, startDate, endDate):
    query = ""
    if endDate == None and startDate == None:
        query = "SELECT numEvento, numProcesso, codice, data, fase, statoiniziale, statofinale  FROM eventiimportanti"
    elif endDate == None:
        query = "SELECT numEvento, e.numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventiimportanti AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataInizioProcesso >= '" + startDate + "'"
    elif startDate == None:    
        query = "SELECT numEvento, e.numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventiimportanti AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataFineProcesso <= '" + endDate + "'"
    else:
        query = "SELECT numEvento, e.numProcesso, codice, data, fase, statoiniziale, statofinale FROM eventiimportanti AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getCourtHearingsEvents(connection, startDate, endDate):
    query = ""
    if endDate == None and startDate == None:
        query = "SELECT numEvento, numProcesso, evento, data, fase, stato FROM udienze"
    elif endDate == None:
        query = "SELECT numEvento, e.numProcesso, evento, data, fase, stato FROM udienze AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataInizioProcesso >= '" + startDate + "'"
    elif startDate == None:    
        query = "SELECT numEvento, e.numProcesso, evento, data, fase, stato FROM udienze AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataFineProcesso <= '" + endDate + "'"
    else:
        query = "SELECT numEvento, e.numProcesso, evento, data, fase, stato FROM udienze AS e, processicondurata AS p WHERE e.numProcesso = p.numProcesso AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getAllProcesses(connection, startDate, endDate):
    query = ""
    if startDate == None and endDate == None:
        query = "SELECT * FROM processicondurata"
    elif startDate == None:
        query = "SELECT * FROM processicondurata WHERE dataFineProcesso <= '" + endDate + "'"
    elif endDate == None:
        query = "SELECT * FROM processicondurata WHERE dataInizioProcesso >= '" + startDate + "'"
    else:
        query = "SELECT * FROM processicondurata WHERE dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getFinishedProcesses(connection, startDate, endDate):
    query = ""
    if startDate == None and endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 1"
    elif startDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 1 AND dataFineProcesso <= '" + endDate + "'"
    elif endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 1 AND dataInizioProcesso >= '" + startDate + "'"
    else:
        query = "SELECT * FROM processicondurata WHERE processofinito = 1 AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getUnfinishedProcesses(connection, startDate, endDate):
    query = ""
    if startDate == None and endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 0"
    elif startDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 0 AND dataFineProcesso <= '" + endDate + "'"
    elif endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 0 AND dataInizioProcesso >= '" + startDate + "'"
    else:
        query = "SELECT * FROM processicondurata WHERE processofinito = 0 AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getStoppedProcesses(connection, startDate, endDate):
    query = ""
    if startDate == None and endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 2"
    elif startDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 2 AND dataFineProcesso <= '" + endDate + "'"
    elif endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = 2 AND dataInizioProcesso >= '" + startDate + "'"
    else:
        query = "SELECT * FROM processicondurata WHERE processofinito = 2 AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)

def getStuckedProcesses(connection, startDate, endDate):
    query = ""
    if startDate == None and endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = -1"
    elif startDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = -1 AND dataFineProcesso <= '" + endDate + "'"
    elif endDate == None:
        query = "SELECT * FROM processicondurata WHERE processofinito = -1 AND dataInizioProcesso >= '" + startDate + "'"
    else:
        query = "SELECT * FROM processicondurata WHERE processofinito = -1 AND dataInizioProcesso >= '" + startDate + "' AND dataFineProcesso <= '" + endDate + "'"
    return getDataFromDatabase(connection, query)