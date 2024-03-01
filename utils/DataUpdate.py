import utils.DatabaseConnection as dbc

from alive_progress import alive_bar
from operator import itemgetter

def refreshData(connection):
    events = updateEventsType(connection)
    processEvents = groupEventsByProcess(events)
    processPhaseEvents = groupEventsByProcessPhase(processEvents)
    processStateEvents = groupEventsByProcessState(processEvents)
    eventsDuration = calcEventsDuration(processEvents)
    phasesDuration = calcPhasesDuration(processPhaseEvents, eventsDuration)
    statesDuration = calcStatesDuration(processStateEvents, eventsDuration)
    [processDuration, processSequence] = calcProcessesInfo(processEvents)

def updateEventsType(connection):
    #updateQuery = "SELECT numEvento, en.etichetta, s.stato, s.fase, e.numProcesso, e.data, s.etichetta FROM eventi AS e, eventinome AS en, statinome AS s WHERE e.codice = en.codice AND e.statofinale = s.stato ORDER BY data"
    updateQuery = "SELECT numEvento, en.etichetta, s.stato, s.fase, e.numProcesso, e.data, s.etichetta FROM eventi AS e, eventinome AS en, statinome AS s WHERE e.codice = en.codice AND e.statofinale = s.stato AND( numProcesso = 109848 OR numProcesso = 109850 OR numProcesso = 109855 OR numProcesso = 109959) ORDER BY data"
    eventsType = dbc.getDataFromDatabase(connection, updateQuery)
    eventsTypeFiltered = [e[0:4] for e in eventsType]
    #dbc.updateTable(connection, "eventitipo", eventsTypeFiltered)
    return eventsType

def groupEventsByProcess(events):
    processes = {}
    for e in events:
        p = processes.get(e[4])
        if p == None:
            processes.update({e[4]: [e]})
        else:
           p.append(e)
    return processes

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

def addIDEvent(p, ID):
    flag = p[0][ID]
    process = [[flag, [p[0]]]]
    i = 1
    while i < len(p):
        if p[i][ID] != flag:
            process.append([p[i][ID], [p[i]]])
            flag = p[i][ID]
        else:
            process[-1][1].append(p[i])
        i = i + 1
    return process

def calcEventsDuration(processEvents):
    eventsDuration = {}
    for p in processEvents.keys():
        i = 0
        events = processEvents.get(p)
        while i < len(events) - 1:
            if events[i][0] > events[i + 1][0]:
                eventsDuration.update({events[i][0]: (events[i][0], 0, events[i][5], events[i][5])})
            else:
                eventsDuration.update({events[i][0]: (events[i][0], (events[i + 1][5] - events[i][5]).days, events[i][5], events[i + 1][5])})
            i = i + 1
        eventsDuration.update({events[i][0]: (events[i][0], 0, events[i][5], events[i][5])})
    return eventsDuration

def calcPhasesDuration(processEvents, eventDuration):
    phasesDuration = []
    for p in processEvents.keys():
        for process in processEvents.get(p):
            startDate = eventDuration.get(process[1][0][0])[2]
            endDate = eventDuration.get(process[1][-1][0])[3]
            phasesDuration.append((p, process[0], (endDate - startDate).days, startDate, endDate))
    return phasesDuration

def calcStatesDuration(processEvents, eventDuration):
    statesDuration = []
    for p in processEvents.keys():
        for process in processEvents.get(p):
            startDate = eventDuration.get(process[1][0][0])[2]
            endDate = eventDuration.get(process[1][-1][0])[3]
            tag = process[1][0][6]
            statesDuration.append((p, tag, process[0], (endDate - startDate).days, startDate, endDate))
    return statesDuration

def calcProcessesInfo(processEvents):
    processDuration = []
    processSequence = []
    for p in processEvents.keys():
        [startDate, endDate, processType, originalSequence, translatedSequence, finalSequence] = getProcessInfo(processEvents.get(p))
        processDuration.append((p, (endDate - startDate).days, startDate, endDate))
        processSequence.append((p, processType, fromListToString(originalSequence), fromListToString(translatedSequence), fromListToString(finalSequence)))
    return [processDuration, processSequence]

def getProcessInfo(events):
    startDate = events[0][5]
    endDate = events[-1][5]
    find = False
    phase = 0
    processType = -1
    originalSequence = []
    translatedSequence = []
    finalSequence = []
    for e in events:
        [endDate, processType, find, phase] = getSequences(e, endDate, processType, find, phase, originalSequence, translatedSequence, finalSequence)
    return [startDate, endDate, processType, originalSequence, translatedSequence, finalSequence]

def getSequences(e, endDate, processType, find, phase, originalSequence, translatedSequence, finalSequence):
    if not e[3].isdigit() and finalSequence[-1] != e[6] and not find:
        finalSequence.append(e[6])
    if e[3].isdigit() and not find:
        if int(e[3]) != 0:
            processType = 0
        if int(e[3]) < phase and "RESTART" not in finalSequence:
            finalSequence.append("RESTART")
        if int(e[3]) == phase and e[6] not in finalSequence:
            finalSequence.append(e[6])
        if int(e[3]) > phase:
            finalSequence.append(e[6])
            phase = int(e[3])
        if int(e[3]) == 5:
            endDate = e[5]
            if e[6] == "FINE":
                processType = 1
            else:
                processType = 2
            find = True
    originalSequence.append(e[2])
    translatedSequence.append(e[6])
    return [endDate, processType, find, phase]

def fromListToString(list):
    string = ",".join(str(l) for l in list)
    return string

