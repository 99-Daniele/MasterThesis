# this file handles the update of database data.

from alive_progress import alive_bar

import utils.Database.DatabaseConnection as connect
import utils.FileOperation as file
import utils.Getters as getter
import utils.Utilities.Utilities as utilities

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData(connection):
    verifyDatabase(connection)
    maxDate = getter.getMaxDate()
    events = getter.getEvents()
    courtHearingsEventsType = str(tuple(file.getDataFromTextFile('preferences/courtHearingsEvents.txt')))
    eventsFiltered = []
    for e in events:
        eventsFiltered.append((e[0], e[1], e[6], e[3]))
    [eventsDuration, phasesDuration, statesDuration, processDuration, courtHearingsDuration, processSequence] = getDurations(events, courtHearingsEventsType, maxDate)
    eventsFiltered.sort(key = lambda x: x[0])
    eventsDuration.sort(key = lambda x: x[0])
    phasesDuration.sort(key = lambda x: [x[0], x[2]])
    statesDuration.sort(key = lambda x: [x[0], x[3]])
    processDuration.sort(key = lambda x: x[0])
    courtHearingsDuration.sort(key = lambda x: x[0])
    processSequence.sort(key = lambda x: x[0])
    eventsFilteredInfo = compareData(eventsFiltered, connection, "SELECT * FROM eventitipo ORDER BY numEvento")
    eventsDurationInfo = compareData(eventsDuration, connection, "SELECT * FROM durataeventi ORDER BY numEvento")
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

# return events, phases, process and court hearing durations based on events.
# in case of unfinished processes predicts final duration.
def getDurations(events, courtHearingsType, maxDate):
    processEvents = []
    processId = events[0][4]
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    courtHearingsDuration = []
    processSequences = []
    processDuration = []
    originalSequenceDict = {}
    translatedSequenceDict = {}
    shortSequenceDict = {}
    phaseSequenceDict = {}
    eventSequenceDict = {}
    unfinishedProcesses = []
    i = 0
    with alive_bar(int(len(events))) as bar:
        while i < (len(events)):
            if events[i][4] != processId:
                firstEventId = events[i][0]
                firstEventDate = events[i][5]
                [processEventsDuration, filteredEvents] = getEventsDuration(processEvents, maxDate)
                if len(filteredEvents) > 0:
                    eventsDuration = eventsDuration + processEventsDuration
                    phasesDuration = phasesDuration + getPhasesDuration(filteredEvents)
                    statesDuration = statesDuration + getStatesDuration(filteredEvents)
                    [processSequence, originalSequence, translatedSequence, shortSequence, phaseSequence, eventSequence, finished] = getProcessesSequence(filteredEvents)
                    courtHearingsDuration = courtHearingsDuration + getCourtHearingsDuration(filteredEvents, courtHearingsType, processSequence)
                    processSequences = processSequences + processSequence
                    if finished:
                        processDuration = processDuration + getProcessesDuration(filteredEvents)
                        addToDict(originalSequence, originalSequenceDict)
                        addToDict(translatedSequence, translatedSequenceDict)
                        addToDict(shortSequence, shortSequenceDict)
                        addToDict(phaseSequence, phaseSequenceDict)
                        addToDict(eventSequence, eventSequenceDict)
                    else:
                        if int(processSequence[0][5][-1]) > 2:
                            unfinishedProcesses.append([processId, firstEventDate, firstEventId, originalSequence, translatedSequence, shortSequence, phaseSequence, eventSequence])
                processEvents = []
                processId = events[i][4]
            else:
                processEvents.append(events[i])
            i = i + 1
            bar()
    with alive_bar(int(len(unfinishedProcesses))) as bar:
        for p in unfinishedProcesses:
            processDuration = processDuration + getPredictedDuration(p, originalSequenceDict, translatedSequenceDict, shortSequenceDict, phaseSequenceDict, eventSequenceDict)
            bar()
    return [eventsDuration, phasesDuration, statesDuration, processDuration, courtHearingsDuration, processSequences]

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
        i = 0
        while i < len(sequence[1]):
            s1 = id[1][i]
            s2 = sequence[1][i]
            new_sequence.append([s1[0], ((s1[1] * id[2]) + s2[1]) / new_count])
            i += 1
        dict.update({utilities.fromListToString(sequence[2]): [new_mean, new_sequence, new_count]})

# return events duration.
# in case of unfinished events, uses as endDate given maxDate (which is the date of the last event in the database).
def getEventsDuration(events, maxDate):
    if len(events) == 0:
        return [(), ()]
    curr = events[0]
    if len(events) == 1:
        eventsDuration = [(curr[0], 0, curr[5], curr[5], curr[0])]
        correctEvents = [curr]
        return [eventsDuration, correctEvents]
    next = events[1]
    first = (curr[0], (next[5] - curr[5]).days, curr[5], next[5], next[0])
    eventsDuration = [first]
    correctEvents = [curr]
    i = 1
    end = False
    while i < len(events) - 1:
        curr = events[i]
        next = events[i + 1]
        prev = events[i - 1]
        if curr[3] == '5' and not end:
            end = True
            correctEvents.append(curr)
        if curr[7] == prev[7] or curr[7] == next[7]:
            if end:
                duration = 0
                nextDate = curr[5]
                nextId = curr[0]
            else:
                duration = (next[5] - curr[5]).days
                nextDate = next[5]
                nextId = next[0]
                correctEvents.append(curr)
            eventsDuration.append((curr[0], duration, curr[5], nextDate, nextId))
        i = i + 1
    curr = events[i]
    prev = events[i - 1]
    if curr[3] == '5' and not end:
        end = True
        correctEvents.append(curr)
    if curr[7] == prev[7]:
        if end:
            duration = 0
            nextDate = curr[5]
            nextId = curr[0]
        else:
            duration = (maxDate - curr[5]).days
            nextDate = maxDate
            nextId = None
            correctEvents.append(curr)  
        eventsDuration.append((curr[0], duration, curr[5], nextDate, nextId))
    return [eventsDuration, correctEvents]

# return phases duration.
def getPhasesDuration(events):
    phasesDuration = []
    i = 0
    firstEvent = events[0]
    order = 1
    while i < len(events) - 1:
        curr = events[i]
        next = events[i + 1]
        if next[3] != curr[3]:
            duration = (curr[5] - firstEvent[5]).days
            phasesDuration.append((curr[4], curr[3], order, duration, firstEvent[5], curr[5], firstEvent[0], curr[0]))
            firstEvent = next
            order = order + 1
            if next[3] == '5':
                phasesDuration.append((next[4], '5', order, 0, next[5], next[5], next[0], next[0]))
                return phasesDuration
        i = i + 1
    return phasesDuration

# return states duration.
def getStatesDuration(events):
    statesDuration = []
    i = 0
    firstEvent = events[0]
    order = 1
    while i < len(events) - 1:
        curr = events[i]
        next = events[i + 1]
        if next[2] != curr[2]:
            duration = (curr[5] - firstEvent[5]).days
            statesDuration.append((curr[4], curr[6], curr[2], order, duration, firstEvent[5], curr[5], firstEvent[0], curr[0]))
            firstEvent = next
            order = order + 1
            if next[3] == '5':
                statesDuration.append((next[4], next[6], next[2], order, 0, next[5], next[5], next[0], next[0]))
                return statesDuration
        i = i + 1
    return statesDuration

# return court hearings duration.
def getCourtHearingsDuration(events, courtHearingsType, processSequence):
    firstEvent = None
    lastEvent = None
    if processSequence[0][5][-1] != '4' and processSequence[0][5][-1] != '5':
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
def getProcessesSequence(events):
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
        if phasesSequence[-1] == '5':
            if shortSequence[-1] == 'FINE':
                processType = 1
            else:
                processType = 1
                #processType = 2
    return [[(processId, processType, utilities.fromListToString(originalSequence), utilities.fromListToString(translatedSequence), utilities.fromListToString(shortSequence), utilities.fromListToString(phasesSequence))], originalSequenceDuration, translatedSequenceDuration, shortSequenceDuration, phasesSequenceOriginalDuration, eventsSequenceDuration, processType != 0]

# return process duration of finished process.
def getProcessesDuration(events):
    duration = (events[-1][5] - events[0][5]).days
    return [(events[0][4], duration, events[0][5], events[-1][5], events[0][0], events[-1][0])]

# return how much finished process is like to unfinished one and duration of the finished process.
def getLikeness(unfinished, finished):
    i = 0
    likeness = 0
    l1 = len(unfinished[1])
    l2 = len(finished[1])
    maxPos = 0
    if l1 >= l2:
        return [0, 0, 0, 0]
    while i < l1:
        k = 0
        start = True
        end = True
        while start or end:
            if k % 2 == 0:
                j = int(i - (k / 2))
            else:
                j = int(i + ((k + 1) / 2))
            if j < 0:
                start = False
            elif j >= l2:
                end = False
            else:
                if unfinished[1][i][0] == finished[1][j][0]:
                    break
            k += 1
        likeness = likeness * i
        if start or end:
            likeness += (l2 - abs(i - j)) / l2
            maxPos = j + 1
            if maxPos == l2:
                maxPos -= 1
        else:
            likeness -= 1
        likeness = likeness / (i + 1)
        i = i + 1
    return [likeness * 100, finished[1][maxPos][1], finished[0], finished[2]]

# return  how much finished process is like to unfinished one and predicted duration.
def getLikenessDuration(unfinished, finished):
    [like, duration, totDuration, count] = getLikeness(unfinished, finished)
    if like == 0:
        return [0, 0, 0]
    if duration == 0:
        predicted = unfinished[0]
    else:
        predicted = unfinished[0] + ((totDuration - duration) * unfinished[0] / duration)
    return [like, predicted, count]

# return best prediction of unfinished process.
def getPrediction(unfinished, finished):
    prediction = 0
    tot = 0
    for f in finished.values():
        [like, predicted, count] = getLikenessDuration(unfinished, f)
        if like == 100:
            prediction = prediction * tot
            prediction += like * predicted * count
            tot += like * count
            prediction = prediction / tot
    if tot == 0:
        return None
    return prediction

# return predicted duration of unfinished process based on states, phases and events sequences.
def getPredictedDuration(unfinishedProcessInfo, originalSequenceDict, translatedSequenceDict, shortSequenceDict, phaseSequenceDict, eventSequenceDict):
    [processId, firstEventDate, firstEventId, originalSequence, translatedSequence, shortSequence, phaseSequence, eventSequence] = unfinishedProcessInfo
    originalCoeff = 1
    translatedCoeff = 0.9
    shortCoeff = 0.8
    phaseCoeff = 0.6
    eventCoeff = 1.5
    originalSequenceDuration = getPrediction(originalSequence, originalSequenceDict)
    translatedSequenceDuration = getPrediction(translatedSequence, translatedSequenceDict)
    shortSequenceDuration = getPrediction(shortSequence, shortSequenceDict)
    phaseSequenceDuration = getPrediction(phaseSequence, phaseSequenceDict)
    eventSequenceDuration = getPrediction(eventSequence, eventSequenceDict)
    totCoeff = 0
    if originalSequenceDuration != None:
        totCoeff += originalCoeff
        originalSequenceDuration = originalSequenceDuration * originalCoeff
    else:
        originalSequenceDuration = 0
    if translatedSequenceDuration != None:
        totCoeff += translatedCoeff
        translatedSequenceDuration = translatedSequenceDuration * translatedCoeff
    else:
        translatedSequenceDuration = 0
    if shortSequenceDuration != None:
        totCoeff += shortCoeff
        shortSequenceDuration = shortSequenceDuration * shortCoeff
    else:
        shortSequenceDuration = 0
    if phaseSequenceDuration != None:
        totCoeff += phaseCoeff
        phaseSequenceDuration = phaseSequenceDuration * phaseCoeff
    else:
        phaseSequenceDuration = 0
    if eventSequenceDuration != None:
        totCoeff += eventCoeff
        eventSequenceDuration = eventSequenceDuration * eventCoeff
    else:
        eventSequenceDuration = 0
    if totCoeff == 0:
        return []
    predictedDuration = int((originalSequenceDuration + translatedSequenceDuration + shortSequenceDuration + phaseSequenceDuration + eventSequenceDuration) / totCoeff)
    return [(processId, predictedDuration, firstEventDate, None, firstEventId, None)]

# verify if user database has all needed tables and views with all needed columns.
def verifyDatabase(connection):
    if not connect.doesATableExist(connection, "eventi"):
        raise Exception("\nEvents table is not present or is called differently than 'eventi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "eventi", ['numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale']):
        raise Exception("\nEvents table does not have all requested columns. The requested columns are: 'numEvento', 'numProcesso', 'codice', 'giudice', 'data', 'statoiniziale', 'statofinale'")
    if not connect.doesATableExist(connection, "processi"):
        raise Exception("\nProcesses table is not present or is called differently than 'processi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "processi", ['numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione']):
        raise Exception("\nProcesses table does not have all requested columns. The requested columns are: 'numProcesso', 'dataInizio', 'giudice', 'materia', 'sezione'")
    if not connect.doesATableExist(connection, "eventinome"):
        connect.createTable(connection, 'eventinome', ['codice', 'etichetta', 'fase'], ['VARCHAR(10)', 'TEXT', 'VARCHAR(5)'], [0], [])
        eventsName = file.getDataFromTextFile('utils/Utilities/eventsName.txt')
        connect.insertIntoDatabase(connection, 'eventinome', eventsName)
    else:
        if not connect.doesATableHaveColumns(connection, "eventinome", ['codice', 'etichetta', 'fase']):
            raise Exception("\nNameEvents table does not have all requested columns. The requested columns are: 'codice', 'etichetta', 'fase'")
        eventsName = file.getDataFromTextFile('utils/Utilities/eventsName.txt')
        eventsNameInfo = compareData(eventsName, connection, "SELECT * FROM eventinome ORDER BY codice")
        connect.updateTable(connection, 'eventinome', eventsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "materienome"):
        connect.createTable(connection, 'materienome', ['codice', 'etichetta'], ['VARCHAR(10)', 'TEXT'], [0], [])
        subjectsName = file.getDataFromTextFile('utils/Utilities/subjectsName.txt')
        connect.insertIntoDatabase(connection, 'materienome', subjectsName)
    else:
        if not connect.doesATableHaveColumns(connection, "materienome", ['codice', 'etichetta']):
            raise Exception("\nNameSubjects table does not have all requested columns. The requested columns are: 'codice', 'etichetta'")
        subjectsName = file.getDataFromTextFile('utils/Utilities/subjectsName.txt')
        subjectsNameInfo = compareData(subjectsName, connection, "SELECT * FROM materienome ORDER BY codice")
        connect.updateTable(connection, 'materienome', subjectsNameInfo, 'codice')
    if not connect.doesATableExist(connection, "statinome"):
        connect.createTable(connection, 'statinome', ['stato', 'etichetta', 'abbreviazione', 'fase'], ['VARCHAR(5)', 'TEXT', 'VARCHAR(10)', 'VARCHAR(5)'], [0], [])
        statesName = file.getDataFromTextFile('utils/Utilities/statesName.txt')
        connect.insertIntoDatabase(connection, 'statinome', statesName)
    else:
        if not connect.doesATableHaveColumns(connection, "statinome", ['stato', 'etichetta', 'abbreviazione', 'fase']):
            raise Exception("\nNameEvents table does not have all requested columns. The requested columns are: 'stato', 'etichetta', 'abbreviazione', 'fase'")
        statesName = file.getDataFromTextFile('utils/Utilities/statesName.txt')
        statesNameInfo = compareData(statesName, connection, "SELECT * FROM statinome ORDER BY stato")
        connect.updateTable(connection, 'statinome', statesNameInfo, 'stato')
    if not connect.doesATableExist(connection, "eventitipo"):
        connect.createTable(connection, 'eventitipo', ['numEvento', 'evento', 'stato', 'fase'], ['BIGINT', 'TEXT', 'TEXT', 'VARCHAR(5)'], [0], [])
    if not connect.doesATableExist(connection, "durataeventi"):
        connect.createTable(connection, 'durataeventi', ['numEvento', 'durata', 'dataInizio', 'dataFine', 'numEventoSuccessivo'], ['BIGINT', 'INT', 'DATETIME', 'DATETIME', 'BIGINT'], [0], [])
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
