# this file handles the update of database data.

from alive_progress import alive_bar
import datetime as dt
import pandas as pd

import cache.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData(connection):
    import time
    verifyDatabase(connection)
    minDate = getter.getMinDate()
    maxDate = getter.getMaxDate()
    events = getter.getEvents()
    courtHearingsEventsType = str(tuple(file.getDataFromTextFile('preferences/courtHearingsEvents.txt')))
    numEventTag = 'numEvento'
    numProcessTag = 'numProcesso'
    eventTag = 'evento'
    durationTag = 'durata'
    judgeTag = 'giudice'
    dateTag = 'data'
    stateTag = 'stato'
    phaseTag = 'fase'
    subjectTag = 'materia'
    sectionTag = 'sezione'
    finishedTag = 'finito'
    nextDateTag = 'succData'
    nextIdTag = 'succId'
    endPhase = '4'
    start = time.time()
    #updateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    processEvents = getProcessEvents(events)
    #updateEventsDurationDataframe(processEvents, maxDate, endPhase, numEventTag, numProcessTag, eventTag, durationTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag, nextDateTag, nextIdTag)
    print(time.time() - start)
    exit()
    [eventsDuration, phasesDuration, statesDuration, processDuration, courtHearingsDuration, processSequence] = getDurations(events, courtHearingsEventsType, minDate, maxDate)
    eventsFiltered.sort(key = lambda x: x[0])
    eventsDuration.sort(key = lambda x: x[0])
    phasesDuration.sort(key = lambda x: [x[0], x[2]])
    statesDuration.sort(key = lambda x: [x[0], x[3]])
    processDuration.sort(key = lambda x: x[0])
    courtHearingsDuration.sort(key = lambda x: x[0])
    processSequence.sort(key = lambda x: x[0])
    cache.updateCache('importantEvents.json', importantEventsDataframe)
    cache.updateCache('stateEvents.json', stateEventsDataframe)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)
    cache.updateCache('courtHearingsEvents.json', courtHearingsEventsDataframe)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    cache.updateCache('statesDuration.json', stateDurationDataframe)
    cache.updateCache('phasesDuration.json', phaseDurationDataframe)
    eventDurationDataframe = frame.keepOnlyRelevant(eventDurationDataframe, 0.005, 'evento', 'conteggio')
    cache.updateCache('eventsDuration.json', eventDurationDataframe)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    return
    eventsFilteredInfo = compareData(eventsFiltered, connection, "SELECT * FROM eventitipo ORDER BY numEvento")
    eventsDurationInfo = compareData(eventsDuration, connection, "SELECT * FROM durataeventi ORDER BY numEvento")
    phasesDurationInfo = compareDataOrder(phasesDuration, connection, "SELECT * FROM duratafasi ORDER BY numProcesso, ordine", 2)
    statesDurationInfo = compareDataOrder(statesDuration, connection, "SELECT * FROM duratastati ORDER BY numProcesso, ordine", 3)
    processDurationInfo = compareData(processDuration, connection, "SELECT * FROM durataprocessi ORDER BY numProcesso")
    courtHearingsDurationInfo = compareData(courtHearingsDuration, connection, "SELECT * FROM durataudienze ORDER BY numProcesso")
    processSequenceInfo = compareData(processSequence, connection, "SELECT * FROM processitipo ORDER BY numProcesso")
    connect.updateTable(connection, 'eventitipo', eventsFilteredInfo, 'numEvento')
    connect.updateTable(connection, 'durataeventi', eventsDurationInfo, 'numEvento')
    connect.updateTableWithOrder(connection, 'duratafasi', phasesDurationInfo, 'numProcesso')
    connect.updateTableWithOrder(connection, 'duratastati', statesDurationInfo, 'numProcesso')
    connect.updateTable(connection, 'durataprocessi', processDurationInfo, 'numProcesso')
    connect.updateTable(connection, 'durataudienze', courtHearingsDurationInfo, 'numProcesso')
    connect.updateTable(connection, 'processitipo', processSequenceInfo, 'numProcesso')

# update events dataframe.
def updateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    updateAllEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updateImportantEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updateStateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    updatePhaseEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)

# update all events dataframe.
def updateAllEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    allEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    allEventsDataframe = allEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('allEvents.json', allEventsDataframe)

# update important events dataframe.
def updateImportantEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    importantEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    try:
        importantEvents = list(file.getDataFromTextFile('preferences/importantEvents.txt'))
        importantEventsDataframe = importantEventsDataframe[importantEventsDataframe[eventTag].isin(importantEvents)]
    except:
        pass
    importantEventsDataframe = importantEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('importantEvents.json', importantEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    stateEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, stateTag], as_index = False).first()
    try:
        importantStates = list(file.getDataFromTextFile('preferences/importantStates.txt'))
        stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[stateTag].isin(importantStates)]
    except:
        pass
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase):
    phaseEventsDataframe = frame.createEventsDataFrame(events, numEventTag, numProcessTag, eventTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, endPhase)
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# group events by process.
def getProcessEvents(events):
    allProcessEvents = []
    processId = events[0][1]
    processSubject = events[0][7]
    processSection = events[0][8]
    processEvents = [processId, processSubject, processSection, -1]
    end = False
    with alive_bar(int(len(events))) as bar:
        for i in range(int(len(events))):
            if events[i][1] != processId or end:
                allProcessEvents.append(processEvents)
                processEvents = [processId, processSubject, processSection, -1]
                processId = events[i][1]
                processSubject = events[i][7]
                processSection = events[i][8]
                end = False
            else:
                if events[i][6] != '0':
                    processEvents[3] = 0
                if events[i][6] == '4':
                    if events[i][5] == 'FINE':
                        processEvents[3] = 1
                    else:
                        processEvents[3] = 2
                    end = True
                processEvents.append(events[i])
            bar()
    return allProcessEvents

# update events duration dataframe.
def updateEventsDurationDataframe(processEvents, maxDate, endPhase, numEventTag, numProcessTag, eventTag, durationTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag, nextDateTag, nextIdTag):
    eventsDuration = calcEventsDuration(processEvents, maxDate, endPhase)
    eventsDurationDataframe = frame.createEventsDurationsDataFrame(eventsDuration, numEventTag, numProcessTag, eventTag, durationTag, judgeTag, dateTag, stateTag, phaseTag, subjectTag, sectionTag, finishedTag,  nextDateTag, nextIdTag)
    cache.updateCache('eventsDuration.json', eventsDurationDataframe)

# calc events durations.
def calcEventsDuration(processEvents, maxDate, endPhase):
    eventsDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            [processEventsDuration, filteredEvents] = getEventDuration(processEvents[i], maxDate, endPhase)
            eventsDuration.extend(processEventsDuration)
            bar()
    return eventsDuration

# return events duration.
# in case of unfinished events, uses as endDate given maxDate (which is the date of the last event in the database).
def getEventDuration(events, maxDate, endPhase):
    processId = events[0]
    subject = events[1]
    section = events[2]
    finished = events[3]
    if len(events) == 4:
        return [(), ()]
    events = events[4:]
    eventsDuration = []
    correctEvents = []
    end = False
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[6] == endPhase and not end:
            end = True
            correctEvents.append(curr)
        currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(next[4], '%Y-%m-%d %H:%M:%S')
        if end:
            duration = 0
            nextDate = curr[4]
            nextId = curr[0]
        else:
            duration = (nextDateDt - currDateDt).days
            nextDate = next[4]
            nextId = next[0]
            correctEvents.append(curr)
        eventsDuration.append([curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, nextDate, nextId])
    curr = events[-1]
    currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
    maxDateDt = dt.datetime.strptime(maxDate, '%Y-%m-%d %H:%M:%S')
    if curr[6] == endPhase and not end:
        end = True
        correctEvents.append(curr)
    if end:
        duration = 0
        nextDate = curr[4]
        nextId = curr[0]
    else:
        duration = (maxDateDt - currDateDt).days
        nextDate = maxDate
        nextId = None
        correctEvents.append(curr)  
    eventsDuration.append((curr[0], processId, curr[2], duration, curr[4], curr[3], curr[5], curr[6], subject, section, finished, nextDate, nextId))
    return [eventsDuration, correctEvents]

# return events, phases, process and court hearing durations based on events.
# in case of unfinished processes predicts final duration.
def getDurations(events, courtHearingsType, minDate, maxDate):
    processEvents = []
    processId = events[0][4]
    firstEventId = events[0][0]
    firstEventDate = events[0][5]
    processJudge = events[0][8]
    processSubject = events[0][9]
    processSection = events[0][10]
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    courtHearingsDuration = []
    processesSequences = []
    processesDuration = []
    originalSequenceDict = {}
    translatedSequenceDict = {}
    shortSequenceDict = {}
    phaseSequenceDict = {}
    eventSequenceDict = {}
    finishedProcesses = []
    unfinishedProcesses = []
    endPhase = '4'
    numProcessTag = 'numProcesso'
    durationTag = 'durata'
    judgeTag = 'giudice'
    subjectTag = 'materia'
    sectionTag = 'sezione'
    with alive_bar(int(len(events) / 10)) as bar:
        for i in range(int(len(events) / 10)):
            if events[i][4] != processId:
                [processEventsDuration, filteredEvents] = getEventsDuration(processEvents, maxDate, endPhase)
                if len(filteredEvents) > 0:
                    eventsDuration = eventsDuration + processEventsDuration
                    phasesDuration = phasesDuration + getPhasesDuration(filteredEvents, endPhase)
                    statesDuration = statesDuration + getStatesDuration(filteredEvents, endPhase)
                    [processSequence, originalSequence, translatedSequence, shortSequence, phaseSequence, eventSequence, finished] = getProcessesSequence(filteredEvents, endPhase)
                    courtHearingsDuration = courtHearingsDuration + getCourtHearingsDuration(filteredEvents, courtHearingsType, processSequence, '2')
                    processesSequences = processesSequences + processSequence
                    if finished:
                        processDuration = getProcessesDuration(filteredEvents)
                        processesDuration = processesDuration + processDuration
                        #finishedProcesses.append([processId, processDuration[0][1], firstEventDate, processJudge, processSubject, processSection, eventSequence])
                        #finishedProcesses.append([processId, processDuration[0][1], firstEventDate, processJudge, processSubject, processSection])
                        #addToDict(originalSequence, originalSequenceDict)
                        #addToDict(translatedSequence, translatedSequenceDict)
                        #addToDict(shortSequence, shortSequenceDict)
                        #addToDict(phaseSequence, phaseSequenceDict)
                        #addToDict(eventSequence, eventSequenceDict)
                    #else:
                    #    if int(processSequence[0][5][-1]) > 2:
                    #        unfinishedProcesses.append([processId, firstEventDate, firstEventId, processJudge, processSubject, processSection, eventSequence, originalSequence, translatedSequence, shortSequence, phaseSequence, eventSequence])
                processEvents = []
                processId = events[i][4]
                firstEventId = events[i][0]
                firstEventDate = events[i][5]
                processJudge = events[i][8]
                processSubject = events[i][9]
                processSection = events[i][10]
            else:
                processEvents.append(events[i])
            bar() 
    #trainModel(finishedProcesses, minDate, maxDate)
    #model = prediction.trainModel(finishedProcesses, numProcessTag, durationTag, 'dataInizioProcesso', judgeTag, subjectTag, sectionTag)
    with alive_bar(int(len(unfinishedProcesses))) as bar:
        for p in unfinishedProcesses:
            #prediction.predictDuration(model, p)
            #processDuration = getPredictedDuration(p, originalSequenceDict, translatedSequenceDict, shortSequenceDict, phaseSequenceDict, eventSequenceDict)
            #processesDuration = processesDuration + processDuration
            bar()
    return [eventsDuration, phasesDuration, statesDuration, processesDuration, courtHearingsDuration, processesSequences]

# add sequence to dictionary.
# if sequence already exists, update means values, otherwise add to dictonary.
def addToDict(sequence, dict):
    id = dict.get(utilities.fromListToString(sequence[2]))
    if id == None:
        dict.update({utilities.fromListToString(sequence[2]): [sequence[0], sequence[1], 1]})
    else:
        new_count = id[2] + 1
        new_mean = ((id[0] * id[2]) + sequence[0]) / new_count
        new_sequence = []
        for i in range(len(sequence[1])):
            s1 = id[1][i]
            s2 = sequence[1][i]
            new_sequence.append([s1[0], ((s1[1] * id[2]) + s2[1]) / new_count])
        dict.update({utilities.fromListToString(sequence[2]): [new_mean, new_sequence, new_count]})

# return events duration.
# in case of unfinished events, uses as endDate given maxDate (which is the date of the last event in the database).
def getEventDuration2(events, maxDate, endPhase):
    if len(events) == 0:
        return [[], []]
    curr = events[0]
    currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
    if len(events) == 1:
        eventsDuration = [[curr[0], 0, curr[4], curr[4], curr[0]]]
        correctEvents = [curr]
        return [eventsDuration, correctEvents]
    next = events[1]
    nextDateDt = dt.datetime.strptime(next[4], '%Y-%m-%d %H:%M:%S')
    first = [curr[0], (nextDateDt - currDateDt).days, curr[4], next[4], next[0]]
    eventsDuration = [first]
    correctEvents = [curr]
    i = 1
    end = False
    while i < len(events) - 1:
        curr = events[i]
        next = events[i + 1]
        prev = events[i - 1]
        if curr[6] == endPhase and not end:
            end = True
            correctEvents.append(curr)
        if curr[2] == prev[2] or curr[2] == next[2]:
            currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(next[4], '%Y-%m-%d %H:%M:%S')
            if end:
                duration = 0
                nextDate = curr[4]
                nextId = curr[0]
            else:
                duration = (nextDateDt - currDateDt).days
                nextDate = next[4]
                nextId = next[0]
                correctEvents.append(curr)
            eventsDuration.append([curr[0], duration, curr[4], nextDate, nextId])
        i = i + 1
    curr = events[i]
    prev = events[i - 1]
    if curr[6] == endPhase and not end:
        end = True
        correctEvents.append(curr)
    if curr[2] == prev[2]:
        currDateDt = dt.datetime.strptime(curr[4], '%Y-%m-%d %H:%M:%S')
        maxDateDt = dt.datetime.strptime(maxDate, '%Y-%m-%d %H:%M:%S')
        if end:
            duration = 0
            nextDate = curr[4]
            nextId = curr[0]
        else:
            duration = (maxDateDt - currDateDt).days
            nextDate = maxDate
            nextId = None
            correctEvents.append(curr)  
        eventsDuration.append([curr[0], duration, curr[4], nextDate, nextId])
    return [eventsDuration, correctEvents]

# return phases duration.
def getPhasesDuration(events, endPhase):
    phasesDuration = []
    firstEvent = events[0]
    order = 1
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if next[3] != curr[3]:
            duration = (curr[5] - firstEvent[5]).days
            phasesDuration.append((curr[4], curr[3], order, duration, firstEvent[5], curr[5], firstEvent[0], curr[0]))
            firstEvent = next
            order = order + 1
            if next[3] == endPhase:
                phasesDuration.append((next[4], endPhase, order, 0, next[5], next[5], next[0], next[0]))
                return phasesDuration
    return phasesDuration

# return states duration.
def getStatesDuration(events, endPhase):
    statesDuration = []
    firstEvent = events[0]
    order = 1
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if next[2] != curr[2]:
            duration = (curr[5] - firstEvent[5]).days
            statesDuration.append((curr[4], curr[6], curr[2], order, duration, firstEvent[5], curr[5], firstEvent[0], curr[0]))
            firstEvent = next
            order = order + 1
            if next[3] == endPhase:
                statesDuration.append((next[4], next[6], next[2], order, 0, next[5], next[5], next[0], next[0]))
                return statesDuration
    return statesDuration

# return court hearings duration.
def getCourtHearingsDuration(events, courtHearingsType, processSequence, minPhase):
    firstEvent = None
    lastEvent = None
    if processSequence[0][5][-1].isdigit and int(processSequence[0][5][-1]) > int(minPhase):
        return []
    for e in events:
        if e[1] in courtHearingsType:
            if firstEvent == None:
                firstEvent = e
            lastEvent = e
    if firstEvent == None:
        return []
    duration = (lastEvent[5] - firstEvent[5]).days
    return [(e[4], duration, firstEvent[5], lastEvent[5], firstEvent[0], lastEvent[0])]

# return processes sequence.
def getProcessesSequence(events, endPhase):
    processType = -1
    processId = events[0][4]
    firstEventDate = events[0][5]
    totDuration = (events[-1][5] - firstEventDate).days
    originalSequence = [events[0][2]]
    originalSequenceDuration = [totDuration, [[events[0][2], 0]], originalSequence]
    translatedSequence = [events[0][6]]
    translatedSequenceDuration = [totDuration, [[events[0][6], 0]], translatedSequence]
    shortSequence = [events[0][7]]
    shortSequenceDuration = [totDuration, [[events[0][7], 0]], shortSequence]
    if events[0][3] == '0':
        phasesSequence = [events[0][3]]
    else:
        phasesSequence = ['1']
    phasesSequenceOriginal = [events[0][3]]
    phasesSequenceOriginalDuration = [totDuration, [[events[0][3], 0]], phasesSequenceOriginal]
    eventsSequence = [events[0][1]]
    eventsSequenceDuration = [totDuration, [[events[0][1], 0]], eventsSequence]
    for e in events:
        duration = (e[5] - firstEventDate).days
        if e[3] != '0':
            processType = 0
        if e[2] != originalSequence[-1]:
            originalSequence.append(e[2])
            originalSequenceDuration[1].append([e[2], duration])
        if e[6] != translatedSequence[-1]:
            translatedSequence.append(e[6])
            translatedSequenceDuration[1].append([e[6], duration])
        if not e[3].isdigit() and e[7] != shortSequence[-1]:
            shortSequence.append(e[7])
            shortSequenceDuration[1].append([e[7], duration])
        if e[3].isdigit():
            if int(e[3]) >= int(phasesSequence[-1]) and e[7] not in shortSequence:
                shortSequence.append(e[7])
                shortSequenceDuration[1].append([e[7], duration])
            elif int(e[3]) < int(phasesSequence[-1]) and shortSequence[-1] != 'REST':
                shortSequence.append('REST')
                shortSequenceDuration[1].append(['REST', duration])
            if e[3] not in phasesSequence:
                phasesSequence.append(e[3])
                phasesSequence.sort()
            if e[3] != phasesSequenceOriginal[-1]:
                phasesSequenceOriginal.append(e[3])
                phasesSequenceOriginalDuration[1].append([e[3], duration])
        if e[1] != eventsSequence[-1]:
            eventsSequence.append(e[1])
            eventsSequenceDuration[1].append([e[1], duration])
        if phasesSequence[-1] == endPhase:
            if shortSequence[-1] == 'FINE':
                processType = 1
            else:
                processType = 2
    return [[(processId, processType, utilities.fromListToString(originalSequence), utilities.fromListToString(translatedSequence), utilities.fromListToString(shortSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence))], originalSequenceDuration, translatedSequenceDuration, shortSequenceDuration, phasesSequenceOriginalDuration, eventsSequenceDuration, processType != 0]

# return process duration of finished process.
def getProcessesDuration(events):
    duration = (events[-1][5] - events[0][5]).days
    return [(events[0][4], duration, events[0][5], events[-1][5], events[0][0], events[-1][0])]

# verify if user database has all needed tables and views with all needed columns.
def verifyDatabase(connection):
    if not connect.doesATableExist(connection, "eventi"):
        raise Exception("\n'eventi' table is not present or is called differently than 'eventi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "eventi", ['numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale'], ['BIGINT', 'BIGINT', 'VARCHAR(4)', 'TEXT', 'DATETIME', 'VARCHAR(5)', 'VARCHAR(5)']):
        raise Exception("\n'eventi' table does not have all requested columns. The requested columns are: 'numEvento'(BIGINT), 'numProcesso'(BIGINT), 'codice'(VARCHAR(4)), 'giudice'(TEXT), 'data'(DATETIME), 'statoiniziale'(VARCHAR(5)), 'statofinale'VARCHAR(5))")
    if not connect.doesATableExist(connection, "processi"):
        raise Exception("\n'processi' table is not present or is called differently than 'processi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "processi", ['numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione'], ['BIGINT', 'DATETIME', 'TEXT', 'VARCHAR(10)', 'VARCHAR(5)']):
        raise Exception("\n'processi' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'dataInizio'(DATETIME), 'giudice'(TEXT), 'materia'(VARCHAR(10)), 'sezione'(VARCHAR(5))")
    if not connect.doesATableExist(connection, "eventinome"):
        connect.createTable(connection, 'eventinome', ['codice', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(10)', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
        eventsName = file.getDataFromTextFile('utils/Utilities/eventsName.txt')
        connect.insertIntoDatabase(connection, 'eventinome', eventsName)
    else:
        if not connect.doesATableHaveColumns(connection, "eventinome", ['codice', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(10)', 'TEXT', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'eventinome' table does not have all requested columns. The requested columns are: 'codice'(VARCHAR(10)), 'etichetta'(TEXT), 'abbreviazione'(TEXT), 'fase'(VARCHAR(5))")
        eventsName = file.getDataFromTextFile('utils/Utilities/eventsName.txt')
        eventsNameInfo = compareData(eventsName, connection, "SELECT * FROM eventinome ORDER BY codice")
        connect.updateTable(connection, 'eventinome', eventsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "materienome"):
        connect.createTable(connection, 'materienome', ['codice', 'descrizione', 'rituale', 'etichetta'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(4)', 'TEXT'], [0], [])
        subjectsName = file.getDataFromTextFile('utils/Utilities/subjectsName.txt')
        connect.insertIntoDatabase(connection, 'materienome', subjectsName)
    else:
        if not connect.doesATableHaveColumns(connection, "materienome", ['codice', 'descrizione', 'rituale', 'etichetta'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(4)', 'TEXT']):
            raise Exception("\n'materienome' table does not have all requested columns. The requested columns are: 'codice'(VARCHAR(10)), 'descrizione'(TEXT), 'rituale'(VARCHAR(4)), 'etichetta'(TEXT)")
        subjectsName = file.getDataFromTextFile('utils/Utilities/subjectsName.txt')
        subjectsNameInfo = compareData(subjectsName, connection, "SELECT * FROM materienome ORDER BY codice")
        connect.updateTable(connection, 'materienome', subjectsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "statinome"):
        connect.createTable(connection, 'statinome', ['stato', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(5)', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
        statesName = file.getDataFromTextFile('utils/Utilities/statesName.txt')
        connect.insertIntoDatabase(connection, 'statinome', statesName)
    else:
        if not connect.doesATableHaveColumns(connection, "statinome", ['stato', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(5)', 'TEXT', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'statinome' table does not have all requested columns. The requested columns are: 'stato'(VARCHAR(5)), 'etichetta'(TEXT), 'abbreviazione'(TEXT), 'fase'(VARCHAR(5))")
        statesName = file.getDataFromTextFile('utils/Utilities/statesName.txt')
        statesNameInfo = compareData(statesName, connection, "SELECT * FROM statinome ORDER BY stato")
        connect.updateTable(connection, 'statinome', statesNameInfo, 'stato')

    if not connect.doesATableExist(connection, "eventitipo"):
        connect.createTable(connection, 'eventitipo', ['numEvento', 'evento', 'stato', 'fase'], ['BIGINT', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
    else:
        if not connect.doesATableHaveColumns(connection, "eventitipo", ['numEvento', 'evento', 'stato', 'fase'], ['BIGINT', 'TEXT', 'TEXT', 'VARCHAR(5)']):
            raise Exception("\n'eventitipo' table does not have all requested columns. The requested columns are: 'numEvento'(BIGINT), 'evento'(TEXT), 'stato'(TEXT), 'fase'(VARCHAR(5))")
    if not connect.doesATableExist(connection, "durataeventi"):
        connect.createTable(connection, 'durataeventi', ['numEvento', 'durata', 'dataInizio', 'dataFine', 'numEventoSuccessivo'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT'], [0], [])
    else:
        if not connect.doesATableHaveColumns(connection, "durataeventi", ['numEvento', 'durata', 'dataInizio', 'dataFine', 'numEventoSuccessivo'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT']):
            raise Exception("\n'durataeventi' table does not have all requested columns. The requested columns are: 'numEvento'(BIGINT), 'durata'(INT), 'dataInizio'(DATETIME), 'dataFine'(DATETIME), 'numEventoSuccessivo'(BIGINT)")
    if not connect.doesATableExist(connection, "duratafasi"):
        connect.createTable(connection, 'duratafasi', ['numProcesso', 'fase', 'ordine', 'durata', 'dataInizioFase', 'dataFineFase', 'numEventoInizioFase', 'numEventoFineFase'], ['BIGINT', 'VARCHAR(5)', 'INT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0, 2], [])
    else:
        if not connect.doesATableHaveColumns(connection, "duratafasi", ['numProcesso', 'fase', 'ordine', 'durata', 'dataInizioFase', 'dataFineFase', 'numEventoInizioFase', 'numEventoFineFase'], ['BIGINT', 'VARCHAR(5)', 'INT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT']):
            raise Exception("\'duratafasi' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'fase'(VARCHAR(5)), 'ordine'(INT), 'durata'(INT), 'dataInizioFase'(DATETIME), 'dataFineFase'(DATETIME), 'numEventoInizioFase'(BINGINT), 'numEventoFineFase'(BINGINT)")
    if not connect.doesATableExist(connection, "duratastati"):
        connect.createTable(connection, 'duratastati', ['numProcesso', 'etichetta', 'stato', 'ordine', 'durata', 'dataInizioStato', 'dataFineStato', 'numEventoInizioStato', 'numEventoFineStato'], ['BIGINT', 'TEXT', 'VARCHAR(10)', 'INT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0, 3], [])
    else:
        if not connect.doesATableHaveColumns(connection, "duratastati", ['numProcesso', 'etichetta', 'stato', 'ordine', 'durata', 'dataInizioStato', 'dataFineStato', 'numEventoInizioStato', 'numEventoFineStato'], ['BIGINT', 'TEXT', 'VARCHAR(10)', 'INT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT']):
            raise Exception("\n'duratastati' table does not have all requested columns. The requested columns are: 'numProcesso'(BINGINT), 'etichetta'(TEXT), 'stato'(VARCHAR(10)), 'ordine'(INT), 'durata'(INT), 'dataInizioStato'(DATETIME), 'dataFineStato'(DATETIME), 'numEventoInizioStato'(BIGINT), 'numEventoFineStato'(BIGINT)")
    if not connect.doesATableExist(connection, "durataprocessi"):
        connect.createTable(connection, 'durataprocessi', ['numProcesso', 'durata', 'dataInizioProcesso', 'dataFineProcesso', 'numEventoInizioProcesso', 'numEventoFineProcesso'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0], [])
    else:
        if not connect.doesATableHaveColumns(connection, "durataprocessi", ['numProcesso', 'durata', 'dataInizioProcesso', 'dataFineProcesso', 'numEventoInizioProcesso', 'numEventoFineProcesso'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT']):
            raise Exception("\n'durataprocessi' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'durata'(INT), 'dataInizioProcesso'(DATETIME), 'dataFineProcesso'(DATETIME), 'numEventoInizioProcesso'(BIGINT), 'numEventoFineProcesso'(BIGINT)")
    if not connect.doesATableExist(connection, "durataudienze"):
        connect.createTable(connection, 'durataudienze', ['numProcesso', 'durata', 'dataInizioUdienza', 'dataFineUdienza', 'numEventoInizioUdienza', 'numEventoFineUdienza'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT'], [0], [])
    else:
        if not connect.doesATableHaveColumns(connection, "durataudienze", ['numProcesso', 'durata', 'dataInizioUdienza', 'dataFineUdienza', 'numEventoInizioUdienza', 'numEventoFineUdienza'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT', 'BIGINT']):
            raise Exception("\n'durataudienze' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'durata'(INT), 'dataInizioUdienza'(DATETIME), 'dataFineUdienza'(DATETIME), 'numEventoInizioUdienza'(BIGINT), 'numEventoFineUdienza'(BIGINT)")
    if not connect.doesATableExist(connection, "processitipo"):
        connect.createTable(connection, 'processitipo', ['numProcesso', 'processofinito', 'sequenzaStati', 'sequenzaTradotta', 'sequenzaCorta', 'sequenzaFasi', 'sequenzaEventi'], ['BIGINT', 'INT', 'TEXT', 'TEXT','TEXT','TEXT', 'TEXT'], [0], [])
    else:
        if not connect.doesATableHaveColumns(connection, "processitipo", ['numProcesso', 'processofinito', 'sequenzaStati', 'sequenzaTradotta', 'sequenzaCorta', 'sequenzaFasi', 'sequenzaEventi'], ['BIGINT', 'INT', 'TEXT', 'TEXT','TEXT','TEXT', 'TEXT']):
            raise Exception("\n'processitipo' table does not have all requested columns. The requested columns are: 'numProcesso'(BIGINT), 'processofinito'(INT), 'sequenzaStati'(TEXT), 'sequenzaTradotta'(TEXT), 'sequenzaCorta'(TEXT), 'sequenzaFasi'(TEXT), 'sequenzaEventi'(TEXT)")
    if not connect.doesAViewExist(connection, "aliasgiudice"):
        query = "CREATE VIEW aliasgiudice AS SELECT giudice, CONCAT('giudice ', ROW_NUMBER() OVER ()) AS alias FROM (SELECT DISTINCT giudice FROM eventi WHERE giudice <> 'null' ORDER BY giudice) AS g"
        connect.createViewFromQuery(connection, 'aliasgiudice', query)
    if not connect.doesAViewExist(connection, "processicambiogiudice"):
        query = "CREATE VIEW processiCambioGiudice AS SELECT numProcesso, (CASE WHEN numProcesso IN (SELECT pc.numProcesso FROM ((SELECT numProcesso FROM eventi AS e WHERE (giudice <> 'null') GROUP BY numProcesso HAVING (COUNT(DISTINCT giudice) > 1)) AS e, processi AS pc) WHERE (e.numProcesso = pc.numProcesso)) THEN 1 ELSE 0 END) AS cambioGiudice FROM processi"
        connect.createViewFromQuery(connection, 'processiCambioGiudice', query)

# compare data with database data and return info about what has to be eliminated from or added to database.
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

# compare data with database data and return info about what has to be eliminated from or added to database.
# this method is for rows that requires an order such as phases and states.
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
