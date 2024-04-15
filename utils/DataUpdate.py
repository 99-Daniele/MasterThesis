from collections import OrderedDict

import utils.DatabaseConnection as connect
import utils.FileOperation as file
import utils.Getters as getter

def refreshData(connection):
    verifyDatabase(connection)
    events = getter.getTestEvents()
    courtHearingsEventsType = str(tuple(file.getDataFromTextFile('utils/Preferences/courtHearingsEvents.txt')))
    eventsFiltered = filterEvents(events)
    processEvents = groupEventsByProcess(events)
    processPhaseEvents = groupEventsByProcessPhase(processEvents)
    processStateEvents = groupEventsByProcessState(processEvents)
    processCourtHearingEvents = groupCourtHearingByProcess(events, courtHearingsEventsType)
    eventsDuration = calcEventsDuration(processEvents)
    phasesDuration = calcPhasesDuration(processPhaseEvents, eventsDuration)
    statesDuration = calcStatesDuration(processStateEvents, eventsDuration)
    courtHearingsDuration = calcCourtHearingsDuration(processCourtHearingEvents)
    [processDuration, processSequence] = calcProcessesInfo(processEvents)
    eventsFilteredInfo = compareData(eventsFiltered, connection, "SELECT * FROM eventitipo ORDER BY numEvento")
    eventsDurationInfo = compareData(list(eventsDuration.values()), connection, "SELECT * FROM durataeventi ORDER BY numEvento")
    phasesDurationInfo = compareDataOrder(phasesDuration, connection, "SELECT * FROM duratafasi ORDER BY numProcesso, ordine", 2)
    statesDurationInfo = compareDataOrder(statesDuration, connection, "SELECT * FROM duratastati ORDER BY numProcesso, ordine", 3)
    processDurationInfo = compareData(processDuration, connection, "SELECT * FROM durataprocessi ORDER BY numProcesso")
    courtHearingsDurationInfo = compareData(courtHearingsDuration, connection, "SELECT * FROM durataudienze ORDER BY numProcesso")
    processSequenceInfo = compareData(processSequence, connection, "SELECT * FROM processitipo ORDER BY numProcesso")
    connect.updateTable(connection, 'eventitipo', eventsFilteredInfo, 'numEvento')
    connect.updateTable(connection, 'durataeventi', eventsDurationInfo, 'numEvento')
    connect.updateTableOrder(connection, 'duratafasi', phasesDurationInfo, 'numProcesso')
    connect.updateTableOrder(connection, 'duratastati', statesDurationInfo, 'numProcesso')
    connect.updateTable(connection, 'durataprocessi', processDurationInfo, 'numProcesso')
    connect.updateTable(connection, 'durataudienze', courtHearingsDurationInfo, 'numProcesso')
    connect.updateTable(connection, 'processitipo', processSequenceInfo, 'numProcesso')

def filterEvents(events):
    eventsFiltered = []
    for e in events:
        eventsFiltered.append((e[0], e[1], e[6], e[3]))
    return eventsFiltered

def groupEventsByProcess(events):
    processes = {}
    for e in events:
        p = processes.get(e[4])
        if p == None:
            processes.update({e[4]: [e]})
        else:
            p.append(e)
    processesOrdered = OrderedDict(sorted(processes.items()))
    return processesOrdered

def groupEventsByProcessPhase(processEvents):
    processPhaseEvents = {}
    for p in processEvents.keys():
        process = addIDEvent(processEvents.get(p), 3)
        processPhaseEvents.update({p: process})
    return processPhaseEvents

def groupEventsByProcessState(processEvents):
    processStateEvents = {}
    for p in processEvents.keys():
        process = addIDEvent(processEvents.get(p), 2)
        processStateEvents.update({p: process})
    return processStateEvents

def groupCourtHearingByProcess(events, courtHearingsType):
    processes = {}
    for e in events:
        if e[1] in courtHearingsType:
            p = processes.get(e[4])
            if p == None:
                processes.update({e[4]: [e]})
            else:
                p.append(e)
    processesOrdered = OrderedDict(sorted(processes.items()))
    return processesOrdered

def getNrOfOrder(events, ID):
    count = 1
    flag = events[0][ID]
    for e in events:
        if e[ID] != flag:
            flag = e[ID]
            count = count + 1
            if e[3] == '5':
                return [count, True]
    return [count, False]

def addIDEvent(p, ID):
    maxOrder = getNrOfOrder(p, ID)[0]
    finished = getNrOfOrder(p, ID)[1]
    flag = p[0][ID]
    order = 2
    process = [[flag, 1, [p[0]]]]
    i = 1
    while i < len(p):
        if p[i][ID] != flag:
            if order == maxOrder and finished == False:
                return process
            process.append([p[i][ID], order, [p[i]]])
            flag = p[i][ID]
            order = order + 1
            if p[i][3] == 5:
                return process
        elif process[-1][2][-1][5] < p[i][5]:
            process[-1][2].append(p[i])
        i = i + 1
    return process

def calcEventsDuration(processEvents):
    eventsDuration = {}
    for p in processEvents.keys():
        i = 0
        events = processEvents.get(p)
        while i < len(events):
            e = events[i]
            if i == 0:
                nextEvent = getNextEvent(e, events[i + 1:], e[5]) 
            else:
                nextEvent = getNextEvent(e, events[i + 1:], events[i - 1][5])
            eventsDuration.update({e[0]: (e[0], (nextEvent[5] - e[5]).days, e[5], nextEvent[5])})
            i = i + 1
    eventsDurationOrderer = OrderedDict(sorted(eventsDuration.items()))
    return eventsDurationOrderer

def getNextEvent(event, events, prevDate):
    if event[3] == '5':
        return event
    i = 0
    while i < len(events) and ((events[i][5] - event[5]).days < 0 or (event[5] < prevDate and (events[i][5] - event[5]).days > 365)):
        i = i +  1
    if i == len(events):
        return event
    else:
        return events[i]

def getLastEvent(events):
    startDate = events[0][5]
    i = -1
    endDate = events[i][5]
    while endDate < startDate:
        i = i - 1
        endDate = events[i][5]
    return events[i]

def calcPhasesDuration(processEvents, eventDuration):
    phasesDuration = []
    for p in processEvents.keys():
        for process in processEvents.get(p):
            startDate = eventDuration.get(process[2][0][0])[2]
            startEventId = eventDuration.get(process[2][0][0])[0]
            endDate = eventDuration.get(process[2][-1][0])[3]
            endEventId = eventDuration.get(process[2][-1][0])[0]
            phasesDuration.append((p, process[0], process[1], (endDate - startDate).days, startDate, endDate, startEventId, endEventId))
    return phasesDuration

def calcStatesDuration(processEvents, eventDuration):
    statesDuration = []
    for p in processEvents.keys():
        for process in processEvents.get(p):
            startDate = eventDuration.get(process[2][0][0])[2]
            startEventId = eventDuration.get(process[2][0][0])[0]
            endDate = eventDuration.get(process[2][-1][0])[3]
            endEventId = eventDuration.get(process[2][-1][0])[0]
            tag = process[2][0][6]
            statesDuration.append((p, tag, process[0], process[1], (endDate - startDate).days, startDate, endDate, startEventId, endEventId))
    return statesDuration

def calcCourtHearingsDuration(processEvents):
    courtHearingDuration = []
    for p in processEvents.keys():
        events = processEvents.get(p)
        startDate = events[0][5]
        startEventId = events[0][0]
        lastEvent = getLastEvent(events)
        endDate = lastEvent[5]
        endEventId = lastEvent[0]
        courtHearingDuration.append((p, (endDate - startDate).days, startDate, endDate, startEventId, endEventId))
    return courtHearingDuration

def calcProcessesInfo(processEvents):
    processDuration = []
    processSequence = []
    for p in processEvents.keys():
        [startDate, endDate, startEventId, endEventId, processType, originalSequence, translatedSequence, finalSequence, phaseSequence] = getProcessInfo(processEvents.get(p))
        processDuration.append((p, (endDate - startDate).days, startDate, endDate, startEventId, endEventId))
        processSequence.append((p, processType, fromListToString(originalSequence), fromListToString(translatedSequence), fromListToString(finalSequence), fromListToString(phaseSequence)))
    return [processDuration, processSequence]

def getProcessInfo(events):
    startDate = events[0][5]
    startEventId = events[0][0]
    endDate = events[-1][5]
    endEventId = events[-1][0]
    find = False
    phase = 0
    processType = -1
    originalSequence = []
    translatedSequence = []
    finalSequence = []
    phaseSequence = []
    for e in events:
        [endDate, endEventId, processType, find, phase] = getSequences(e, endDate, endEventId, processType, find, phase, originalSequence, translatedSequence, finalSequence, phaseSequence)
        if processType == -1:
            phaseSequence = [0]
    return [startDate, endDate, startEventId, endEventId, processType, originalSequence, translatedSequence, finalSequence, phaseSequence]

def getSequences(e, endDate, endEventId, processType, find, phase, originalSequence, translatedSequence, finalSequence, phaseSequence):
    if not e[3].isdigit() and (len(finalSequence) == 0 or finalSequence[-1] != e[7] and not find):
        finalSequence.append(e[7])
    if e[3].isdigit() and not find:
        if int(e[3]) != 0:
            processType = 0
        if int(e[3]) < phase and "RESTART" not in finalSequence:
            finalSequence.append("RESTART")
        if int(e[3]) == phase and e[7] not in finalSequence:
            finalSequence.append(e[7])
        if int(e[3]) > phase:
            finalSequence.append(e[7])
            phaseSequence.append(int(e[3]))
            phase = int(e[3])
        if int(e[3]) == 5:
            endDate = e[5]
            endEventId = e[0]
            if e[7] == "FINE":
                processType = 1
            else:
                processType = 2
            find = True
    if len(originalSequence) == 0:
        originalSequence.append(e[2])
        translatedSequence.append(e[6])
    elif e[2] != originalSequence[-1]:
        originalSequence.append(e[2])
        translatedSequence.append(e[6])
    return [endDate, endEventId, processType, find, phase]

def fromListToString(list):
    string = ",".join(str(l) for l in list)
    return string

def verifyDatabase(connection):
    if not connect.doesATableExist(connection, "eventi"):
        raise "\nEvents table is not present or is called differently than 'eventi'. Please change name or add such table because it's fundamental for the analysis"
    if not connect.doesATableHaveColumns(connection, "eventi", ['numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale']):
        raise "\nEvents table does not have all requested columns. The requested columns are: 'numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale'"
    if not connect.doesATableExist(connection, "processi"):
        raise "\Processes table is not present or is called differently than 'processi'. Please change name or add such table because it's fundamental for the analysis"
    if not connect.doesATableHaveColumns(connection, "processi", ['numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione']):
        raise "\Processes table does not have all requested columns. The requested columns are: 'numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione'"
    if not connect.doesATableExist(connection, "eventinome"):
        connect.createTable(connection, 'eventinome', ['codice', 'etichetta'], ['VARCHAR(10)', 'TEXT'], [0], [])
        eventsName = file.getDataFromTextFile('utils/Preferences/eventsName.txt')
        connect.insertIntoDatabase(connection, 'eventinome', eventsName)
    else:
        eventsName = file.getDataFromTextFile('utils/Preferences/eventsName.txt')
        eventsNameInfo = compareData(eventsName, connection, "SELECT * FROM eventinome ORDER BY codice")
        connect.updateTable(connection, 'eventinome', eventsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "materienome"):
        connect.createTable(connection, 'materienome', ['codice', 'etichetta'], ['VARCHAR(10)', 'TEXT'], [0], [])
        subjectsName = file.getDataFromTextFile('utils/Preferences/subjectsName.txt')
        connect.insertIntoDatabase(connection, 'materienome', subjectsName)
    else:
        subjectsName = file.getDataFromTextFile('utils/Preferences/subjectsName.txt')
        subjectsNameInfo = compareData(subjectsName, connection, "SELECT * FROM materienome ORDER BY codice")
        connect.updateTable(connection, 'materienome', subjectsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "statinome"):
        connect.createTable(connection, 'statinome', ['stato', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(5)', 'TEXT', 'VARCHAR(10)', 'VARCHAR(5)'], [0], [])
        statesName = file.getDataFromTextFile('utils/Preferences/statesName.txt')
        connect.insertIntoDatabase(connection, 'statinome', statesName)
    else:
        statesName = file.getDataFromTextFile('utils/Preferences/statesName.txt')
        statesNameInfo = compareData(statesName, connection, "SELECT * FROM statinome ORDER BY stato")
        connect.updateTable(connection, 'statinome', statesNameInfo, 'stato')
    if not connect.doesATableExist(connection, "eventitipo"):
        connect.createTable(connection, 'eventitipo', ['numEvento', 'evento', 'stato', 'fase'], ['BIGINT', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
    if not connect.doesATableExist(connection, "durataeventi"):
        connect.createTable(connection, 'durataeventi', ['numEvento', 'durata', 'dataInizio', 'dataFine'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME'], [0], [])
    if not connect.doesATableExist(connection, "duratafasi"):
        connect.createTable(connection, 'duratafasi', ['numProcesso', 'fase', 'ordine', 'durata', 'dataInizioFase', 'dataFineFase', 'numEventoInizioFase', 'numEventoFineFase'], ['BIGINT', 'VARCHAR(5)', 'INT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0, 2], [])
    if not connect.doesATableExist(connection, "duratastati"):
        connect.createTable(connection, 'duratastati', ['numProcesso', 'etichetta', 'stato', 'ordine', 'durata', 'dataInizioStato', 'dataFineStato', 'numEventoInizioStato', 'numEventoFineStato'], ['BIGINT', 'TEXT', 'VARCHAR(10)', 'INT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0, 3], [])
    if not connect.doesATableExist(connection, "durataprocessi"):
        connect.createTable(connection, 'durataprocessi', ['numProcesso', 'durata', 'dataInizioProcesso', 'dataFineProcesso', 'numEventoInizioProcesso', 'numEventoFineProcesso'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0], [])
    if not connect.doesATableExist(connection, "durataudienze"):
        connect.createTable(connection, 'durataudienze', ['numProcesso', 'durata', 'dataInizioUdienza', 'dataFineUdienza', 'numEventoInizioUdienza', 'numEventoFineUdienza'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0], [])
    if not connect.doesATableExist(connection, "processitipo"):
        connect.createTable(connection, 'processitipo', ['numProcesso', 'processofinito', 'sequenzaStati', 'sequenzaTradotta', 'sequenzaCorta', 'sequenzaFasi'], ['BIGINT', 'INT', 'TEXT', 'TEXT','TEXT','TEXT'], [0], [])
    if not connect.doesAViewExist(connection, "aliasgiudice"):
        query = "CREATE VIEW aliasgiudice AS SELECT giudice, CONCAT('giudice ', ROW_NUMBER() OVER ()) AS alias FROM (SELECT DISTINCT giudice FROM eventi WHERE giudice <> 'null' ORDER BY giudice) AS g"
        connect.createView(connection, 'aliasgiudice', query)
    if not connect.doesAViewExist(connection, "processicambiogiudice"):
        query = "CREATE VIEW processiCambioGiudice AS SELECT numProcesso, (CASE WHEN numProcesso IN (SELECT pc.numProcesso FROM ((SELECT numProcesso FROM eventi AS e WHERE (giudice <> 'null') GROUP BY numProcesso HAVING (COUNT(DISTINCT giudice) > 1)) AS e, processi AS pc) WHERE (e.numProcesso = pc.numProcesso)) THEN 1 ELSE 0 END) AS cambioGiudice FROM processi"
        connect.createView(connection, 'processiCambioGiudice', query)

def compareData(data, connection, query):
    databaseDate = connect.getDataFromDatabase(connection, query)
    i = 0
    j = 0
    dataInfo = [[], []]
    while i < len(data) and j < len(databaseDate):
        if data[i][0] == databaseDate[j][0]:
            if data[i] != databaseDate[j]:
                dataInfo[0].append(data[i])
                dataInfo[1].append(data[i][0])
            i = i + 1
            j = j + 1
        elif data[i][0] > databaseDate[j][0]:
            dataInfo[1].append(databaseDate[j][0])
            j = j + 1
        else:
            dataInfo[0].append(data[i])
            i = i + 1
    while i < len(data):
        dataInfo[0].append(data[i])
        i = i + 1
    while j < len(databaseDate):
        dataInfo[1].append(databaseDate[j][0])
        j = j + 1
    return dataInfo

def compareDataOrder(data, connection, query, order):
    databaseDate = connect.getDataFromDatabase(connection, query)
    i = 0
    j = 0
    dataInfo = [[], []]
    while i < len(data) and j < len(databaseDate):
        if data[i][0] == databaseDate[j][0] and data[i][order] == databaseDate[j][order]:
            if data[i] != databaseDate[j]:
                dataInfo[0].append(data[i])
                dataInfo[1].append([data[i][0], data[i][order]])
            i = i + 1
            j = j + 1
        elif data[i][0] > databaseDate[j][0] or (data[i][0] == databaseDate[j][0] and data[i][order] > databaseDate[j][order]):
            dataInfo[1].append([databaseDate[j][0], databaseDate[j][order]])
            j = j + 1
        else:
            dataInfo[0].append(data[i])
            i = i + 1
    while i < len(data):
        dataInfo[0].append(data[i])
        i = i + 1
    while j < len(databaseDate):
            dataInfo[1].append([databaseDate[j][0], databaseDate[j][order]])
            j = j + 1
    return dataInfo
