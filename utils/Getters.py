from utils.DatabaseConnection import getDataFromDatabase
import pandas as pd

def createEventsDataFrame(events):
    pIds = []
    dates = []
    phases = []
    tags = []
    for e in events:
            pIds.append(e[0])
            dates.append(e[1])
            phases.append(e[2])
            tags.append(e[3])
    return pd.DataFrame(data = {"data": dates, "numProcesso": pIds, "fase": phases, "etichetta": tags})

def createProcessesDataFrame(processes):
    durations = []
    dates = []
    judges = []
    sections = []
    subjects = []
    for p in processes:
        dates.append(p[0])
        durations.append(p[1])
        judges.append(p[2])
        sections.append(p[3])
        subjects.append(p[4])
    return pd.DataFrame(data = {"data": dates, "durata": durations, "giudice": judges, "sezione": sections, "materia": subjects})

def getAllEvents(connection):
    query = "SELECT numProcesso, data, fase, etichetta FROM eventi AS e, elencoeventiimportanti AS ei WHERE numProcesso IN (SELECT * FROM processifiniti) AND e.codice = ei.evento ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return createEventsDataFrame(events)

def getImportantEvents(connection):
    query = "SELECT numProcesso, data, fase, evento FROM eventiimportanti WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return createEventsDataFrame(events)

def getCourtHearingsEvents(connection):
    query = "SELECT numProcesso, data, fase, evento FROM udienze WHERE numProcesso IN (SELECT * FROM processifiniti) ORDER BY fase"
    events = getDataFromDatabase(connection, query)
    return createEventsDataFrame(events)

def getAllProcesses(connection):
    query = "SELECT dataInizioProcesso, durata, giudice, sezione, materia FROM processicondurata AS pd, processi AS p WHERE pd.numProcesso = p.numProcesso"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getFinishedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata, giudice, sezione, materia FROM processicondurata AS pd, processi AS p WHERE pd.numProcesso = p.numProcesso AND processofinito = 1"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getUnfinishedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata, giudice, sezione, materia FROM processicondurata AS pd, processi AS p WHERE pd.numProcesso = p.numProcesso AND processofinito = 0"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getStoppedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata, giudice, sezione, materia FROM processicondurata AS pd, processi AS p WHERE pd.numProcesso = p.numProcesso AND processofinito = 2"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getStuckedProcesses(connection):
    query = "SELECT dataInizioProcesso, durata, giudice, sezione, materia FROM processicondurata AS pd, processi AS p WHERE pd.numProcesso = p.numProcesso AND processofinito = -1"
    processes = getDataFromDatabase(connection, query)
    return createProcessesDataFrame(processes)

def getTop10Judges(connection):
    query = "SELECT * FROM top10giudici"
    judges = getDataFromDatabase(connection, query)
    j = []
    for judge in judges:
            j.append(judge[0])
    return j

def getTop10Subjects(connection):
    query = "SELECT * FROM top10materie"
    subjects = getDataFromDatabase(connection, query)
    s = []
    for subject in subjects:
            s.append(subject[0])
    return s