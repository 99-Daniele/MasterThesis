import utils.DatabaseConnection as connect
import utils.Getters as getter

def refreshData(connection):
    events = getter.getEventsType(connection)
    courtHearingsEventsType = getter.getCourtHearingEventsType(connection)
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
    connect.updateTable(connection, 'eventitipo', eventsFiltered)
    connect.updateTable(connection, 'durataeventi', list(eventsDuration.values()))
    connect.updateTable(connection, 'duratafasi', phasesDuration)
    connect.updateTable(connection, 'duratastati', statesDuration)
    connect.updateTable(connection, 'durataprocessi', processDuration)
    connect.updateTable(connection, 'durataudienze', courtHearingsDuration)
    connect.updateTable(connection, 'processitipo', processSequence)

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

def groupCourtHearingByProcess(events, courtHearingsType):
    processes = {}
    for e in events:
        if e[1] in courtHearingsType:
            p = processes.get(e[4])
            if p == None:
                processes.update({e[4]: [e]})
            else:
                p.append(e)
    return processes

def addIDEvent(p, ID):
    flag = p[0][ID]
    process = [[flag, [p[0]]]]
    i = 1
    while i < len(p):
        if p[i][ID] != flag:
            process.append([p[i][ID], [p[i]]])
            flag = p[i][ID]
            if p[i][3] == 5:
                return process
        elif process[-1][1][-1][5] < p[i][5]:
            process[-1][1].append(p[i])
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
    return eventsDuration

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

def calcCourtHearingsDuration(processEvents):
    courtHearingDuration = []
    for p in processEvents.keys():
        events = processEvents.get(p)
        startDate = events[0][5]
        endDate = events[-1][5]
        courtHearingDuration.append((p, (endDate - startDate).days, startDate, endDate))
    return courtHearingDuration

def calcProcessesInfo(processEvents):
    processDuration = []
    processSequence = []
    for p in processEvents.keys():
        [startDate, endDate, processType, originalSequence, translatedSequence, finalSequence, phaseSequence] = getProcessInfo(processEvents.get(p))
        processDuration.append((p, (endDate - startDate).days, startDate, endDate))
        processSequence.append((p, processType, fromListToString(originalSequence), fromListToString(translatedSequence), fromListToString(finalSequence), fromListToString(phaseSequence)))
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
    phaseSequence = []
    for e in events:
        [endDate, processType, find, phase] = getSequences(e, endDate, processType, find, phase, originalSequence, translatedSequence, finalSequence, phaseSequence)
        if processType == -1:
            phaseSequence = [0]
    return [startDate, endDate, processType, originalSequence, translatedSequence, finalSequence, phaseSequence]

def getSequences(e, endDate, processType, find, phase, originalSequence, translatedSequence, finalSequence, phaseSequence):
    if not e[3].isdigit() and (len(finalSequence) == 0 or finalSequence[-1] != e[6] and not find):
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
    return [endDate, processType, find, phase]

def fromListToString(list):
    string = ",".join(str(l) for l in list)
    return string
