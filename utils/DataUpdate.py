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

# restart current database data in case events or process table are changed.
def restartData():
    connection = connect.getDatabaseConnection()
    verifyDatabase(connection)
    minDate = getter.getMinDate()
    maxDate = getter.getMaxDate()
    endPhase = getter.getEndPhase()
    stallStates = getter.getStallStates()
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codePhaseTag = utilities.getTagName("codePhaseTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    eventsTag = utilities.getTagName("eventsTag")
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    processDateTag = utilities.getTagName("processDateTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    events = getter.getEvents()
    processesEvents, processesInfo = getProcessEvents(events, stallStates, endPhase, codeEventTag, codeJudgeTag, codePhaseTag, codeStateTag, codeSubjectTag, eventsTag, eventSequenceTag, finishedTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag)
    eventDatagrame = frame.createBasicEventsDataFrame(events, dateTag, codeEventTag, codeJudgeTag, numEventTag, numProcessTag, codePhaseTag, processDateTag, sectionTag, codeStateTag, codeSubjectTag)
    cache.updateCache('events.json', eventDatagrame)
    file.writeOnJsonFile('cache/processesEvents.json', processesEvents)
    refreshData()

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData():
    import time
    start = time.time()
    eventsDataframe = cache.getDataframe('events.json')
    if eventsDataframe is None:
        restartData()
        eventsDataframe = cache.getDataframe('events.json')
    processEvents = cache.getData('processesEvents.json')
    if processEvents is None:
        restartData()
        processEvents = cache.getData('processesEvents.json')
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    descriptionTag = utilities.getTagName("descriptionTag")
    durationTag = utilities.getTagName("durationTag")
    eventTag = utilities.getTagName("eventTag")
    eventsTag = utilities.getTagName("eventsTag")
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    judgeTag = utilities.getTagName("judgeTag")
    eventPhaseSequenceTag = utilities.getTagName("eventPhaseSequenceTag")
    nextDateTag = utilities.getTagName("nextDateTag")
    nextIdTag = utilities.getTagName("nextIdTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    ritualTag = utilities.getTagName("ritualTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    tagTag = utilities.getTagName("tagTag")
    courtHearingsEventsType = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
    eventsName = file.getDataFromJsonFile('preferences/eventsName.json')
    judgesName = file.getDataFromJsonFile('preferences/judgesName.json')
    statesName = file.getDataFromJsonFile('preferences/statesName.json')
    subjectsName = file.getDataFromJsonFile('preferences/subjectsName.json')
    endPhase = statesName['DF'][phaseTag]    
    eventsNameDataframe = pd.DataFrame.from_dict(eventsName, orient = 'index').reset_index().rename(columns = {'index': codeEventTag})
    judgesNameDataframe = pd.DataFrame.from_dict(judgesName, orient = 'index').reset_index().rename(columns = {'index': codeJudgeTag})
    statesNameDataframe = pd.DataFrame.from_dict(statesName, orient = 'index').reset_index().rename(columns = {'index': codeStateTag})
    subjectsNameDataframe = pd.DataFrame.from_dict(subjectsName, orient = 'index').reset_index().rename(columns = {'index': codeSubjectTag})
    subjectsNameDataframe[codeSubjectTag] = subjectsNameDataframe[codeSubjectTag].astype('Int64')
    processesDuration = updateTypeDurationDataframe(processEvents, eventsName, judgesName, statesName, subjectsName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, eventTag, eventsTag, eventPhaseSequenceTag, finishedTag, judgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    updateProcessDurationDataframe(processesDuration, codeSubjectTag, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, judgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag)
    updateEventsDataframe(eventsDataframe, eventsNameDataframe, judgesNameDataframe, statesNameDataframe, subjectsNameDataframe, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, descriptionTag, eventTag, numEventTag, numProcessTag, phaseTag, ritualTag, stateTag, tagTag)
    print(str(time.time() - start) + " seconds")

# group events by process.
def getProcessEvents(events, stallStates, endPhase, codeEventTag, codeJudgeTag, codePhaseTag, codeStateTag, codeSubjectTag, eventsTag, eventSequenceTag, finishedTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag):
    if len(events) == 0:
        raise Exception("\nThere isn't any event in database.")
    allProcessEvents = []
    processesInfo = []
    processId = events[0][numProcessTag]
    processCodeJudge = events[0][codeJudgeTag]
    processCodeSubject = events[0][codeSubjectTag]
    processSection = events[0][sectionTag]
    processFinished = utilities.getProcessState('unfinished')
    processEventSequence = []
    processPhaseSequence = []
    processStateSequence = []
    processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processCodeSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
    end = False
    continuative = False
    i = 0
    with alive_bar(int(len(events))) as bar:
        while i < int(len(events)):
            if events[i][numProcessTag] != processId or end:
                allProcessEvents.append(processEvents)
                processesInfo.append({codeJudgeTag: processCodeJudge, codeSubjectTag: processCodeSubject, sectionTag: processSection, finishedTag: processFinished, eventSequenceTag: processEventSequence, phaseSequenceTag: processPhaseSequence, stateSequenceTag: processStateSequence})
                if events[i][numProcessTag] == processId:
                    while i < len(events) - 1 and events[i][numProcessTag] == processId:
                        bar()
                        i += 1
                processId = events[i][numProcessTag]
                processCodeJudge = events[i][codeJudgeTag]
                processCodeSubject = events[i][codeSubjectTag]
                processSection = events[i][sectionTag]
                processFinished = utilities.getProcessState('unfinished')
                processEventSequence = []
                processPhaseSequence = []
                processStateSequence = []
                processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processCodeSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
                if i < len(events) - 1:
                    end = False
                continuative = False
            else:
                if events[i][codeSubjectTag] in stallStates and not continuative:
                    processFinished = utilities.getProcessState('continuatived')
                    continuative = True
                if events[i][codePhaseTag] == endPhase and not continuative: 
                    processFinished = utilities.getProcessState('finished')
                    processEvents[finishedTag] = processFinished
                    end = True
                if events[i][codeJudgeTag] != processCodeJudge:
                    processCodeJudge = events[i][codeJudgeTag]
                    processEvents[codeJudgeTag] = processCodeJudge
                if events[i][sectionTag] != processSection:
                    processSection = events[i][sectionTag]
                    processEvents[sectionTag] = processSection
                processEvents[eventsTag].append(events[i])
                processEventSequence.append(events[i][codeEventTag])
                processPhaseSequence.append(events[i][codePhaseTag])
                processStateSequence.append(events[i][codeStateTag])
            bar()
            i += 1
    if not end:
        allProcessEvents.append(processEvents)
        processesInfo.append({codeJudgeTag: processCodeJudge, codeSubjectTag: processCodeSubject, sectionTag: processSection, finishedTag: processFinished, eventSequenceTag: processEventSequence, phaseSequenceTag: processPhaseSequence, stateSequenceTag: processStateSequence})
    return allProcessEvents, processesInfo

# update events dataframe.
def updateEventsDataframe(eventsDataframe, eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, descriptionTag, eventTag, numEventTag, numProcessTag, phaseTag, ritualTag, stateTag, tagTag):
    eventsDataframeComplete = frame.joinDataframe(eventsDataframe, judgesName, codeJudgeTag, None, None)
    eventsDataframeComplete = frame.joinDataframe(eventsDataframeComplete, subjectsName, codeSubjectTag, None, [descriptionTag, ritualTag, tagTag])
    eventsDataframeComplete = frame.joinDataframe(eventsDataframeComplete, eventsName, codeEventTag, None, None)
    eventsDataframeCompleteEventPhase = frame.joinDataframe(eventsDataframeComplete, statesName, codeStateTag, None, phaseTag)
    eventsDataframeCompleteStatePhase = frame.joinDataframe(eventsDataframeComplete, statesName, codeStateTag, phaseTag, None)
    updateAllEventsDataframe(eventsDataframeCompleteEventPhase, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    updateImportantEventsDataframe(eventsDataframeCompleteEventPhase, endPhase, dateTag, eventTag, numEventTag, numProcessTag, phaseTag)
    updateCourtHearingEventsDataframe(eventsDataframeCompleteEventPhase, endPhase, dateTag, numEventTag, numProcessTag, phaseTag, stateTag)
    updateStateEventsDataframe(eventsDataframeCompleteStatePhase, endPhase, dateTag, stateTag, numEventTag, numProcessTag, stateTag)
    updatePhaseEventsDataframe(eventsDataframeCompleteStatePhase, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)

# update all events dataframe.
def updateAllEventsDataframe(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag):
    allEventsDataframe = frame.createEventsDataFrame(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    cache.updateCache('allEvents.json', allEventsDataframe)

# update important events dataframe.
def updateImportantEventsDataframe(df, endPhase, dateTag, eventTag, numEventTag, numProcessTag, phaseTag):
    importantEventsDataframe = frame.createEventsDataFrame(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    try:
        importantEvents = list(file.getDataFromTextFile('preferences/importantEvents.txt'))
        importantEventsDataframe = importantEventsDataframe[importantEventsDataframe[eventTag].isin(importantEvents)]
    except:
        pass
    cache.updateCache('importantEvents.json', importantEventsDataframe)

# update important events dataframe.
def updateCourtHearingEventsDataframe(df, endPhase, dateTag, eventTag, numEventTag, numProcessTag, phaseTag):
    courtHearingEventsDataframe = frame.createEventsDataFrame(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    try:
        courtHearingsEvents = list(file.getDataFromTextFile('preferences/courtHearingsEvents.txt'))
        courtHearingEventsDataframe = courtHearingEventsDataframe[courtHearingEventsDataframe[eventTag].isin(courtHearingsEvents)]
    except:
        pass
    cache.updateCache('courtHearingEvents.json', courtHearingEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag, stateTag):
    stateEventsDataframe = frame.createEventsDataFrame(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, stateTag], as_index = False).first()
    try:
        importantStates = list(file.getDataFromTextFile('preferences/importantStates.txt'))
        stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[stateTag].isin(importantStates)]
    except:
        pass
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag):
    phaseEventsDataframe = frame.createEventsDataFrame(df, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# update types duration dataframe.
def updateTypeDurationDataframe(processEvents, eventsName, judgesName, statesName, subjectsName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, eventTag, eventsTag, eventPhaseSequenceTag, finishedTag, judgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    [processesDuration, eventsDuration, phasesDuration, statesDuration, courtHearingsDuration] = calcTypeDuration(processEvents, eventsName, judgesName, statesName, subjectsName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, eventPhaseSequenceTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    [eventsDurationDataframe, eventsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(eventsDuration, dateTag, durationTag, eventTag, codeEventTag, finishedTag, judgeTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag, codeSubjectTag)
    [phasesDurationDataframe, phasesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(phasesDuration, dateTag, durationTag, eventTag, codeEventTag, finishedTag, judgeTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag, codeSubjectTag)
    [statesDurationDataframe, statesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(statesDuration, dateTag, durationTag, eventTag, codeEventTag, finishedTag, judgeTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag, codeSubjectTag)
    [courtHearingsDurationDataframe, courtHearingsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(courtHearingsDuration, dateTag, durationTag, eventTag, codeEventTag, finishedTag, judgeTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag, codeSubjectTag)
    cache.updateCache('eventsDuration.json', eventsDurationDataframe)
    cache.updateCache('eventsDurationFiltered.json', eventsDurationDataframeFiltered)
    cache.updateCache('phasesDuration.json', phasesDurationDataframe)
    cache.updateCache('phasesDurationFiltered.json', phasesDurationDataframeFiltered)
    cache.updateCache('statesDuration.json', statesDurationDataframe)
    cache.updateCache('statesDurationFiltered.json', statesDurationDataframeFiltered)
    cache.updateCache('courtHearingsDuration.json', courtHearingsDurationDataframe)
    cache.updateCache('courtHearingsDurationFiltered.json', courtHearingsDurationDataframeFiltered)
    return processesDuration

# calc types durations.
def calcTypeDuration(processEvents, eventsName, judgesName, statesName, subjectsName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, eventPhaseSequenceTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    courtHearingsDuration = []
    processesDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processId = processEvents[i][numProcessTag]
            processJudgeCode = processEvents[i][codeJudgeTag]
            processJudge = judgesName.get(processJudgeCode)[judgeTag]
            processSubjectCode = str(int(processEvents[i][codeSubjectTag]))
            processSubject = subjectsName.get(processSubjectCode)[subjectTag]
            processFinished = processEvents[i][finishedTag]
            processSection = processEvents[i][sectionTag]
            [processEventsDuration, eventsSequence, eventPhaseSequence, duration, startDate, startEventId, endDate, endId] = getEventInfo(processEvents[i], eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
            if duration != None:
                [processPhasesDuration, phasesSequence] = getPhaseInfo(processEvents[i], eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
                [processStateDuration, statesSequence] = getStateInfo(processEvents[i], eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
                courtHearingDuration = getCourtHearingDuration(processEvents[i], eventsName, judgesName, statesName, subjectsName, courtHearingsEventsType, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
                processDuration = (processId, duration, startDate, startEventId, processJudge, processSubjectCode, processSubject, processSection, processFinished, utilities.fromListToString(statesSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence), utilities.fromListToString(eventPhaseSequence), endDate, endId)
                eventsDuration.extend(processEventsDuration)
                phasesDuration.extend(processPhasesDuration)
                statesDuration.extend(processStateDuration)
                courtHearingsDuration.extend(courtHearingDuration) 
                processesDuration.append(processDuration)
            bar()
    return [processesDuration, eventsDuration, phasesDuration, statesDuration, courtHearingsDuration]

# return events duration.
def getEventInfo(processEvents, eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    processId = processEvents[numProcessTag]
    processSubjectCode = str(int(processEvents[codeSubjectTag]))
    processSubject = subjectsName.get(processSubjectCode)[subjectTag]
    processFinished = processEvents[finishedTag]
    events = processEvents[eventsTag]
    if len(events) == 0:
        return [[], [], [], None, None, None, None, None]
    eventsDuration = []
    eventsSequence = []
    eventsPhaseSequence = []
    startDate = events[0][dateTag]
    startEventId = events[0][numEventTag]
    endDate = events[-1][dateTag]
    endEventId = events[-1][numEventTag]
    startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
    endDateDt = dt.datetime.strptime(endDate, '%Y-%m-%d %H:%M:%S')
    processDuration = (endDateDt - startDateDt).days
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        if curr[codeEventTag] != next[codeEventTag]:
            currEventId = curr[numEventTag]
            nextEventId = next[numEventTag]
            currEventCode = curr[codeEventTag]
            nextEventCode = next[codeEventTag]
            currEventTag = eventsName.get(currEventCode)[eventTag]
            nextEventTag = eventsName.get(nextEventCode)[eventTag]
            currJudgeCode = curr[codeJudgeTag]
            currJudge = judgesName.get(currJudgeCode)[judgeTag]
            currDate = curr[dateTag]
            nextDate = next[dateTag]
            currStateCode = curr[codeStateTag]
            currStateTag = statesName.get(currStateCode)[stateTag]
            currPhase = eventsName.get(currEventCode)[phaseTag]
            currSection = curr[sectionTag]
            currDateDt = dt.datetime.strptime(currDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - currDateDt).days
            eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, processSubjectCode, processSubject, currSection, processFinished, nextDate, nextEventId])
            if currEventTag != nextEventTag:
                eventsSequence.append(currEventTag)
                eventsPhaseSequence.append(currPhase)
    curr = events[-1]
    currDateDt = dt.datetime.strptime(curr[dateTag], '%Y-%m-%d %H:%M:%S')
    currEventCode = curr[codeEventTag]
    currPhase = eventsName.get(currEventCode)[phaseTag]
    currEventTag = eventsName.get(currEventCode)[eventTag]
    if currPhase == endPhase:
        currEventId = curr[numEventTag]
        currJudgeCode = curr[codeJudgeTag]
        currJudge = judgesName.get(currJudgeCode)[judgeTag]
        currDate = curr[dateTag]
        nextDate = next[dateTag]
        currStateCode = curr[codeStateTag]
        currStateTag = statesName.get(currStateCode)[stateTag]
        currSection = curr[sectionTag]
        duration = 0
        eventsDuration.append([currEventId, processId, currEventCode, currEventTag, duration, currDate, currJudgeCode, currJudge, currStateCode, currStateTag, currPhase, processSubjectCode, processSubject, currSection, processFinished, currDate, currEventId])
    if len(eventsSequence) == 0 or currEventTag != eventsSequence[-1]:
        eventsSequence.append(currEventTag)
        eventsPhaseSequence.append(currPhase)
    return [eventsDuration, eventsSequence, eventsPhaseSequence, processDuration, startDate, startEventId, endDate, endEventId]

# return phases duration.
def getPhaseInfo(processEvents, eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    processId = processEvents[numProcessTag]
    processSubjectCode = str(int(processEvents[codeSubjectTag]))
    processSubject = subjectsName.get(processSubjectCode)[subjectTag]
    processFinished = processEvents[finishedTag]
    events = processEvents[eventsTag]
    if len(events) == 0:
        return [[], []]
    phasesDuration = []
    phasesSequence = []
    startPhaseEvent = events[0]
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currStateCode = curr[codeStateTag]
        nextStateCode = next[codeStateTag]
        currPhase = statesName.get(currStateCode)[phaseTag]
        nextPhase = statesName.get(nextStateCode)[phaseTag]
        if currPhase != nextPhase:
            nextPhaseEvent = next
            startEventId = startPhaseEvent[numEventTag]
            nextEventId = nextPhaseEvent[numEventTag]
            startEventCode = startPhaseEvent[codeEventTag]
            startEventTag = eventsName.get(startEventCode)[eventTag]
            startJudgeCode = startPhaseEvent[codeJudgeTag]
            startJudge = judgesName.get(startJudgeCode)[judgeTag]
            startDate = startPhaseEvent[dateTag]
            nextDate = nextPhaseEvent[dateTag]
            startStateCode = startPhaseEvent[codeStateTag]
            startStateTag = statesName.get(startStateCode)[stateTag]
            startPhase = statesName.get(startStateCode)[phaseTag]
            startSection = startPhaseEvent[sectionTag]
            startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - startDateDt).days
            phasesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startJudge, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
            if startPhase != '-':
                phasesSequence.append(startPhase)
            startPhaseEvent = next
    curr = events[-1]
    currStateCode = curr[codeStateTag]
    currPhase = statesName.get(currStateCode)[phaseTag]
    if currPhase == endPhase:
        startEventId = startPhaseEvent[numEventTag]
        nextEventId = curr[numEventTag]
        startEventCode = startPhaseEvent[codeEventTag]
        startEventTag = eventsName.get(startEventCode)[eventTag]
        startJudgeCode = startPhaseEvent[codeJudgeTag]
        startJudge = judgesName.get(startJudgeCode)[judgeTag]
        startDate = startPhaseEvent[dateTag]
        nextDate = curr[dateTag]
        startStateCode = startPhaseEvent[codeStateTag]
        startStateTag = statesName.get(startStateCode)[stateTag]
        startPhase = statesName.get(startStateCode)[phaseTag]
        startSection = startPhaseEvent[sectionTag]
        duration = 0
        phasesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startJudge, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    if len(phasesSequence) == 0 or currPhase != phasesSequence[-1]:
        phasesSequence.append(currPhase)
    return [phasesDuration, phasesSequence]

# return states duration.
def getStateInfo(processEvents, eventsName, judgesName, statesName, subjectsName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    processId = processEvents[numProcessTag]
    processSubjectCode = str(int(processEvents[codeSubjectTag]))
    processSubject = subjectsName.get(processSubjectCode)[subjectTag]
    processFinished = processEvents[finishedTag]
    events = processEvents[eventsTag]
    if len(events) == 0:
        return [[], []]
    statesDuration = []
    statesSequence = []
    startStateEvent = events[0]
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currStateCode = curr[codeStateTag]
        nextStateCode = curr[codeStateTag]
        currStateTag = statesName.get(currStateCode)[stateTag]
        nextStateTag = statesName.get(nextStateCode)[stateTag]
        currPhase = statesName.get(currStateCode)[phaseTag]
        if currStateCode != nextStateCode:
            nextStateEvent = next
            startEventId = startStateEvent[numEventTag]
            nextEventId = nextStateEvent[numEventTag]
            startEventCode = startStateEvent[codeEventTag]
            startEventTag = eventsName.get(startEventCode)[eventTag]
            startJudgeCode = startStateEvent[codeJudgeTag]
            startJudge = judgesName.get(startJudgeCode)[judgeTag]
            startDate = startStateEvent[dateTag]
            nextDate = nextStateEvent[dateTag]
            startStateCode = startStateEvent[codeStateTag]
            startStateTag = statesName.get(startStateCode)[stateTag]
            startPhase = statesName.get(startStateCode)[phaseTag]
            startSection = startStateEvent[sectionTag]
            startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - startDateDt).days
            statesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startJudge, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
            if currStateTag != nextStateTag and currPhase != '-':
                statesSequence.append(currStateTag)
            startStateEvent = next
    curr = events[-1]
    currStateCode = curr[codeStateTag]
    currStateTag = statesName.get(currStateCode)[stateTag]
    currPhase = statesName.get(currStateCode)[phaseTag]
    if currPhase == endPhase:
        startEventId = startStateEvent[numEventTag]
        nextEventId = curr[numEventTag]
        startEventCode = startStateEvent[codeEventTag]
        startEventTag = eventsName.get(startEventCode)[eventTag]
        startJudgeCode = startStateEvent[codeJudgeTag]
        startJudge = judgesName.get(startJudgeCode)[judgeTag]
        startDate = startStateEvent[dateTag]
        nextDate = curr[dateTag]
        startStateCode = startStateEvent[codeStateTag]
        startStateTag = statesName.get(startStateCode)[stateTag]
        startPhase = statesName.get(startStateCode)[phaseTag]
        startSection = startStateEvent[sectionTag]
        duration = 0
        statesDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startJudge, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    if len(statesSequence) == 0 or currStateTag != statesSequence[-1]:
        statesSequence.append(currStateTag)
    return [statesDuration, statesSequence]

# return court hearing duration.
def getCourtHearingDuration(processEvents, eventsName, judgesName, statesName, subjectsName, courtHearingTypes, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, eventTag, eventsTag, finishedTag, judgeTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    processId = processEvents[numProcessTag]
    processSubjectCode = str(int(processEvents[codeSubjectTag]))
    processSubject = subjectsName.get(processSubjectCode)[subjectTag]
    processFinished = processEvents[finishedTag]
    events = processEvents[eventsTag]
    if len(events) == 0:
        return []
    courtHearingsDuration = []
    courtHearing = False
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        currEventCode = curr[codeEventTag]
        nextEventCode = next[codeEventTag]
        currEventTag = eventsName.get(currEventCode)[eventTag]
        nextEventTag = eventsName.get(nextEventCode)[eventTag]
        if currEventTag in courtHearingTypes and not courtHearing:
            startCourtHearingEvent = curr
            courtHearing = True
        if nextEventTag not in courtHearingTypes and courtHearing:
            endCourtHearingEvent = curr
            courtHearing = False
            startEventId = startCourtHearingEvent[numEventTag]
            nextEventId = endCourtHearingEvent[numEventTag]
            startEventCode = startCourtHearingEvent[codeEventTag]
            startEventTag = eventsName.get(startEventCode)[eventTag]
            startJudgeCode = startCourtHearingEvent[codeJudgeTag]
            startJudge = judgesName.get(startJudgeCode)[judgeTag]
            startDate = startCourtHearingEvent[dateTag]
            nextDate = endCourtHearingEvent[dateTag]
            startStateCode = startCourtHearingEvent[codeStateTag]
            startStateTag = statesName.get(startStateCode)[stateTag]
            startPhase = eventsName.get(startEventCode)[phaseTag]
            startSection = startCourtHearingEvent[sectionTag]
            startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
            nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
            duration = (nextDateDt - startDateDt).days
            courtHearingsDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startJudge, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    curr = events[-1]
    currEventCode = curr[codeEventTag]
    currEventTag = eventsName.get(currEventCode)[eventTag]
    if currEventTag in courtHearingTypes:
        if not courtHearing:
            startCourtHearingEvent = curr
        endCourtHearingEvent = curr
        startEventId = startCourtHearingEvent[numEventTag]
        nextEventId = endCourtHearingEvent[numEventTag]
        startEventCode = startCourtHearingEvent[codeEventTag]
        startEventTag = eventsName.get(startEventCode)[eventTag]
        startJudgeCode = startCourtHearingEvent[codeJudgeTag]
        startJudge = judgesName.get(startJudgeCode)[judgeTag]
        startDate = startCourtHearingEvent[dateTag]
        nextDate = endCourtHearingEvent[dateTag]
        startStateCode = startCourtHearingEvent[codeStateTag]
        startStateTag = statesName.get(startStateCode)[stateTag]
        startPhase = eventsName.get(startEventCode)[phaseTag]
        startSection = startCourtHearingEvent[sectionTag]
        startDateDt = dt.datetime.strptime(startDate, '%Y-%m-%d %H:%M:%S')
        nextDateDt = dt.datetime.strptime(nextDate, '%Y-%m-%d %H:%M:%S')
        duration = (nextDateDt - startDateDt).days
        courtHearingsDuration.append([startEventId, processId, startEventCode, startEventTag, duration, startDate, startJudgeCode, startJudge, startStateCode, startStateTag, startPhase, processSubjectCode, processSubject, startSection, processFinished, nextDate, nextEventId])
    return courtHearingsDuration

# update process duration dataframe.
def updateProcessDurationDataframe(processDuration, codeSubjectTag, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, judgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag):
    [processDurationDataframe, processDurationDataframeFiltered] = frame.createProcessDurationsDataFrame(processDuration, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, judgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag, codeSubjectTag)
    cache.updateCache('processesDuration.json', processDurationDataframe)
    cache.updateCache('processesDurationFiltered.json', processDurationDataframeFiltered)

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
