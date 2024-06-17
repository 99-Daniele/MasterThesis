# this file handles the update of database data.

from alive_progress import alive_bar
import datetime as dt
import pandas as pd

import Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Prediction as prediction
import utils.Utilities as utilities

# restart current database data in case events or process table are changed.
def restartData():
    connection = connect.getDatabaseConnection()
    verifyDatabase(connection)
    file.removeFolder('cache')
    file.createFolder('cache')
    startProcessEvent = 'IA'
    endPhase = getter.getEndPhase()
    stallStates = getter.getStallStates()
    events = getter.getEvents()
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    countTag = utilities.getTagName("countTag")
    dateTag = utilities.getTagName("dateTag")
    distanceTag = utilities.getTagName("distanceTag")
    durationTag = utilities.getTagName("durationTag")
    durationFinalTag = utilities.getTagName("durationFinalTag")
    eventTag = utilities.getTagName("eventTag")
    eventsTag = utilities.getTagName("eventsTag")
    finishedTag = utilities.getTagName("finishedTag")
    loadTag = utilities.getTagName("loadTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    processDateTag = utilities.getTagName("processDateTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    getter.getEventsInfo()
    getter.getStatesInfo()
    getter.getSubjectsInfo()
    filteredEvents, processesEvents, processesInfo = getProcessEvents(events, startProcessEvent, stallStates, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, eventsTag, finishedTag, loadTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag)
    eventsDataframe = frame.createBasicEventsDataFrame(filteredEvents, dateTag, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, eventTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag)
    cache.updateCache('events.json', eventsDataframe)
    cache.updateCache('processesInfo.json', processesInfo)
    file.writeOnJsonFile('cache/processesEvents.json', processesEvents)
    predictDuration()
    refreshData()

# test unfinished processes prediction.
def predictTest():
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    countTag = utilities.getTagName("countTag")
    dateTag = utilities.getTagName("dateTag")
    distanceTag = utilities.getTagName("distanceTag")
    durationTag = utilities.getTagName("durationTag")
    durationFinalTag = utilities.getTagName("durationFinalTag")
    durationPredictedTag = utilities.getTagName("durationPredictedTag")
    errorTag = utilities.getTagName("errorTag")
    finishedTag = utilities.getTagName("finishedTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    sectionTag = utilities.getTagName("sectionTag")
    processInfo = getter.getProcessesInfo()
    finishedProcesses = processInfo[processInfo[finishedTag] == utilities.getProcessState('finished')]
    predictionDf = prediction.predictDurationsTestTotal(finishedProcesses, codeJudgeTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, durationPredictedTag, errorTag, finishedTag, numProcessTag, sectionTag)
    cache.updateCache('predictions.json', predictionDf)

# predict unfinished processes duration.
def predictDuration():
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    distanceTag = utilities.getTagName("distanceTag")
    durationTag = utilities.getTagName("durationTag")
    durationFinalTag = utilities.getTagName("durationFinalTag")
    durationPredictedTag = utilities.getTagName("durationPredictedTag")
    finishedTag = utilities.getTagName("finishedTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    sectionTag = utilities.getTagName("sectionTag")
    processInfo = getter.getProcessesInfo()
    unfinishedProcessesDurations = prediction.predictDurations(processInfo, codeJudgeTag, codeSubjectTag, dateTag, distanceTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag)
    file.writeOnJsonFile('cache/unfinishedProcessesDurations.json', unfinishedProcessesDurations)

# refresh current database data. 
# calcs event, phases, states, process, courtHearing durations, comprare with current database data and in case update them.
def refreshData():
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    durationTag = utilities.getTagName("durationTag")
    durationPredictedTag = utilities.getTagName("durationPredictedTag")
    eventTag = utilities.getTagName("eventTag")
    eventsTag = utilities.getTagName("eventsTag")
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    eventPhaseSequenceTag = utilities.getTagName("eventPhaseSequenceTag")
    nextDateTag = utilities.getTagName("nextDateTag")
    nextIdTag = utilities.getTagName("nextIdTag")
    numEventTag = utilities.getTagName("numEventTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseDBTag = utilities.getTagName("phaseDBTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    stateTag = utilities.getTagName("stateTag")
    subjectTag = utilities.getTagName("subjectTag")
    eventsDataframe = getter.getEventsDataframe()
    processEvents = getter.getProcessesEvents()
    unfinishedProcesses =getter.getUnfinishedProcessesDuration()
    statesInfoDataframe = getter.getStatesInfo()
    statesInfo = statesInfoDataframe.set_index(codeStateTag).T.to_dict('dict')
    endPhase = frame.getPhaseOfState(statesInfo, "DF", phaseTag)
    processesDuration = updateTypeDurationDataframe(processEvents, unfinishedProcesses, statesInfo, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, durationPredictedTag, eventTag, eventsTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    updateProcessDurationDataframe(processesDuration, codeSubjectTag, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag)
    updateEventsDataframe(eventsDataframe, statesInfoDataframe, endPhase, codeStateTag, dateTag, numEventTag, numProcessTag, phaseTag, phaseDBTag, stateTag)

# group events by process.
def getProcessEvents(events, startProcessEvent, stallStates, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, eventsTag, finishedTag, loadTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag):
    if len(events) == 0:
        raise Exception("\nThere isn't any event in database.")
    filteredEvents = []
    allProcessEvents = []
    allProcessDict = []
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, codeEventTag, eventTag, codeJudgeTag, dateTag, processDateTag, codeStateTag, stateTag, phaseDBTag, codeSubjectTag, subjectTag, sectionTag])
    eventsColumns = frame.getGroupBy(df, codeEventTag)
    statesColumns = frame.getGroupBy(df, codeStateTag)
    phasesColumns = frame.getGroupBy(df, phaseDBTag)
    eventsColumns = [eventTag + ": " + e for e in eventsColumns]
    statesColumns = [stateTag + ": " + s for s in statesColumns]
    phasesColumns = [phaseDBTag + ": " + p for p in phasesColumns]
    dfColumns = [numProcessTag, dateTag, codeJudgeTag, codeSubjectTag, sectionTag, finishedTag, durationTag, durationFinalTag, countTag] + eventsColumns + statesColumns + phasesColumns
    processEventSequence = []
    processPhaseSequence = []
    processStateSequence = []
    eventDurationSequence = []
    phaseDurationSequence = []
    stateDurationSequence = []
    processEventSequenceComplete = []
    processPhaseSequenceComplete = []
    processStateSequenceComplete = []
    durationSequenceComplete = []
    i = 0
    while i < int(len(events)):
        if events[i][codeEventTag] == startProcessEvent:
            start = True
            processId = events[i][numProcessTag]
            processCodeJudge = events[i][codeJudgeTag]
            processSubjectCode = events[i][codeSubjectTag]
            processSubject = events[i][subjectTag]
            processSection = events[i][sectionTag]
            processFinished = utilities.getProcessState('unfinished')
            processStartDate = events[i][dateTag]
            processStartDateDt = dt.datetime.strptime(processStartDate, '%Y-%m-%d %H:%M:%S')
            distance = utilities.distanceFromFirstOfTheYear(processStartDateDt)
            processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processSubjectCode, subjectTag: processSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
            end = False
            continuative = False
            break
        i += 1
    with alive_bar(int(len(events) - i)) as bar:
        while i < int(len(events)):
            if events[i][numProcessTag] != processId:
                start = False
                if events[i][codeEventTag] == startProcessEvent:
                    allProcessEvents.append(processEvents)
                    if len(durationSequenceComplete) > 0:
                        processDict = dict.fromkeys(dfColumns)
                        processDict = {x: 0 for x in processDict}
                        processDict.update({numProcessTag: processId})
                        processDict.update({dateTag: processStartDate})
                        processDict.update({distanceTag: distance})
                        processDict.update({codeJudgeTag: processCodeJudge})
                        processDict.update({codeSubjectTag: processSubjectCode})
                        processDict.update({sectionTag: processSection})
                        processDict.update({finishedTag: processFinished})
                        finalDuration = int(durationSequenceComplete[-1])
                        for j in range(len(processEventSequenceComplete)):
                            codeEvent = processEventSequenceComplete[j]
                            phase = processPhaseSequenceComplete[j]
                            if phase == None:
                                phase = '0.0'
                            codeState = processStateSequenceComplete[j]
                            duration = int(durationSequenceComplete[j])
                            eventCount = processDict.get(eventTag + ": " + codeEvent)
                            phaseCount = processDict.get(phaseDBTag + ": " + phase)
                            stateCount = processDict.get(stateTag + ": " + codeState)
                            processDict.update({eventTag + ": " + codeEvent: eventCount + 1})
                            processDict.update({phaseDBTag + ": " + phase: phaseCount + 1})
                            processDict.update({stateTag + ": " + codeState: stateCount + 1})
                            processDict.update({countTag: j + 1})
                            processDict.update({durationTag: duration})
                            processDict.update({durationFinalTag: finalDuration - duration})
                            if processFinished == utilities.getProcessState('finished'):
                                allProcessDict.append(processDict.copy())
                        if processFinished == utilities.getProcessState('unfinished'):
                            allProcessDict.append(processDict.copy())
                    processId = events[i][numProcessTag]
                    processCodeJudge = events[i][codeJudgeTag]
                    processSubjectCode = events[i][codeSubjectTag]
                    processSubject = events[i][subjectTag]
                    processSection = events[i][sectionTag]
                    processStartDate = events[i][dateTag]
                    processStartDateDt = dt.datetime.strptime(processStartDate, '%Y-%m-%d %H:%M:%S')
                    distance = utilities.distanceFromFirstOfTheYear(processStartDateDt)
                    processFinished = utilities.getProcessState('unfinished')
                    processEventSequence = []
                    processPhaseSequence = []
                    processStateSequence = []
                    eventDurationSequence = []
                    phaseDurationSequence = []
                    stateDurationSequence = []
                    processEventSequenceComplete = []
                    processPhaseSequenceComplete = []
                    processStateSequenceComplete = []
                    durationSequenceComplete = []
                    processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processSubjectCode, subjectTag: processSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
                    start = True
                    end = False
                    continuative = False
            if not end and start:
                if events[i][codeStateTag] in stallStates and not continuative:
                    processFinished = utilities.getProcessState('continuative')
                    processEvents[finishedTag] = processFinished
                    continuative = True
                if events[i][phaseDBTag] == endPhase and not continuative: 
                    processFinished = utilities.getProcessState('finished')
                    processEvents[finishedTag] = processFinished
                    end = True
                if events[i][codeJudgeTag] != processCodeJudge:
                    processCodeJudge = events[i][codeJudgeTag]
                    processEvents[codeJudgeTag] = processCodeJudge
                if events[i][sectionTag] != processSection:
                    processSection = events[i][sectionTag]
                    processEvents[sectionTag] = processSection
                processDate = events[i][dateTag]
                processDateDt = dt.datetime.strptime(processDate, '%Y-%m-%d %H:%M:%S')
                duration = (processDateDt - processStartDateDt).days
                processEvents[eventsTag].append(events[i])
                codeEvent = events[i][codeEventTag]
                phase = events[i][phaseDBTag]
                if phase == None:
                    phase = '0.0'
                codeState = events[i][codeStateTag]
                if len(processEventSequence) == 0 or codeEvent != processEventSequence[-1]:
                    processEventSequence.append(codeEvent)
                    eventDurationSequence.append(duration)
                processEventSequenceComplete.append(codeEvent)
                if len(processPhaseSequence) == 0 or phase != processPhaseSequence[-1]:
                    processPhaseSequence.append(phase)
                    phaseDurationSequence.append(duration)
                processPhaseSequenceComplete.append(phase)
                if len(processStateSequence) == 0 or codeState != processStateSequence[-1]:
                    processStateSequence.append(codeState)
                    stateDurationSequence.append(duration)
                processStateSequenceComplete.append(codeState)
                durationSequenceComplete.append(duration)
                newEvent = events[i].copy()
                newEvent.update({processDateTag: processStartDate})
                filteredEvents.append(newEvent)
            bar()
            i += 1
    if not end:
        allProcessEvents.append(processEvents)
        if len(durationSequenceComplete) > 0:
            processDict = dict.fromkeys(dfColumns)
            processDict = {x: 0 for x in processDict}
            processDict.update({numProcessTag: processId})
            processDict.update({dateTag: processStartDate})
            processDict.update({distanceTag: distance})
            processDict.update({codeJudgeTag: processCodeJudge})
            processDict.update({codeSubjectTag: processSubjectCode})
            processDict.update({sectionTag: processSection})
            processDict.update({finishedTag: processFinished})
            finalDuration = int(durationSequenceComplete[-1])
            for j in range(len(processEventSequenceComplete)):
                codeEvent = processEventSequenceComplete[j]
                phase = processPhaseSequenceComplete[j]
                if phase == None:
                    phase = '0.0'
                codeState = processStateSequenceComplete[j]
                duration = int(durationSequenceComplete[j])
                if j >= 0:
                    eventCount = processDict.get(eventTag + ": " + codeEvent)
                    phaseCount = processDict.get(phaseDBTag + ": " + phase)
                    stateCount = processDict.get(stateTag + ": " + codeState)
                    processDict.update({eventTag + ": " + codeEvent: eventCount + 1})
                    processDict.update({phaseDBTag + ": " + phase: phaseCount + 1})
                    processDict.update({stateTag + ": " + codeState: stateCount + 1})
                    processDict.update({countTag: j + 1})
                    processDict.update({durationTag: duration})
                    processDict.update({durationFinalTag: finalDuration - duration})
                    if processFinished == utilities.getProcessState('finished'):
                        allProcessDict.append(processDict.copy())
            if processFinished == utilities.getProcessState('unfinished'):
                allProcessDict.append(processDict.copy())
    processInfoDataframe = pd.DataFrame.from_dict(allProcessDict)
    return filteredEvents, allProcessEvents, processInfoDataframe

# update events dataframe.
def updateEventsDataframe(eventsDataframe, statesNameDataframe, endPhase, codeStateTag, dateTag, numEventTag, numProcessTag, phaseTag, phaseDBTag, stateTag):
    eventsDataframeComplete = frame.joinDataframe(eventsDataframe, statesNameDataframe, codeStateTag, phaseDBTag, [phaseDBTag, stateTag])
    allEventsDataframe = frame.createEventsDataFrame(eventsDataframeComplete, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    allEventsDataframe = allEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    updateAllEventsDataframe(allEventsDataframe)
    updateStateEventsDataframe(allEventsDataframe, codeStateTag, dateTag, numEventTag, numProcessTag)
    updatePhaseEventsDataframe(allEventsDataframe, dateTag, numEventTag, numProcessTag, phaseTag)

# update all events dataframe.
def updateAllEventsDataframe(allEventsDataframe):
    cache.updateCache('allEvents.json', allEventsDataframe)

# update state events dataframe.
def updateStateEventsDataframe(stateEventsDataframe, codeStateTag, dateTag, numEventTag, numProcessTag):
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, codeStateTag], as_index = False).first()
    importantStates = file.getDataFromTextFile('preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[codeStateTag].isin(importantStates)]
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(phaseEventsDataframe, dateTag, numEventTag, numProcessTag, phaseTag):
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCache('phaseEvents.json', phaseEventsDataframe)

# update types duration dataframe.
def updateTypeDurationDataframe(processEvents, unfinishedProcesses, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, durationPredictedTag, eventTag, eventsTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    [processesDuration, eventsDuration, phasesDuration, statesDuration] = calcTypeDuration(processEvents, unfinishedProcesses, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationPredictedTag, eventTag, eventsTag, finishedTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    [eventsDurationDataframe, eventsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(eventsDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    [phasesDurationDataframe, phasesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(phasesDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    [statesDurationDataframe, statesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(statesDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    cache.updateCache('eventsDuration.json', eventsDurationDataframe)
    cache.updateCache('eventsDurationFiltered.json', eventsDurationDataframeFiltered)
    cache.updateCache('phasesDuration.json', phasesDurationDataframe)
    cache.updateCache('phasesDurationFiltered.json', phasesDurationDataframeFiltered)
    cache.updateCache('statesDuration.json', statesDurationDataframe)
    cache.updateCache('statesDurationFiltered.json', statesDurationDataframeFiltered)
    return processesDuration

# calc types durations.
def calcTypeDuration(processEvents, unfinishedProcesses, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationPredictedTag, eventTag, eventsTag, finishedTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    processesDuration = []
    with alive_bar(int(len(processEvents))) as bar:
        for i in range(int(len(processEvents))):
            processId = processEvents[i][numProcessTag]
            processCodeJudge = processEvents[i][codeJudgeTag]
            processSubjectCode = processEvents[i][codeSubjectTag]
            processSubject = processEvents[i][subjectTag]
            processFinished = processEvents[i][finishedTag]
            processSection = processEvents[i][sectionTag]
            [processEventsDuration, eventsSequence, eventPhaseSequence, processPhasesDuration, phasesSequence, processStateDuration, statesSequence, duration, startDate, startEventId, endDate, endId] = getDurations(processEvents[i], processId, processSubjectCode, processSubject, processFinished, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, eventTag, eventsTag, numEventTag, phaseTag, sectionTag, stateTag)
            if duration != None:
                if processFinished == utilities.getProcessState('unfinished'):
                    if str(processId) in unfinishedProcesses.keys():
                        predictedDuration = unfinishedProcesses.get(str(processId))[durationPredictedTag]
                        endDatePredicted = utilities.finalDate(startDate, predictedDuration)
                        processDuration = (processId, predictedDuration, startDate, startEventId, processCodeJudge, processSubjectCode, processSubject, processSection, processFinished, utilities.fromListToString(statesSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence), utilities.fromListToString(eventPhaseSequence), endDatePredicted, endId)
                        processesDuration.append(processDuration)
                else:
                    processDuration = (processId, duration, startDate, startEventId, processCodeJudge, processSubjectCode, processSubject, processSection, processFinished, utilities.fromListToString(statesSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence), utilities.fromListToString(eventPhaseSequence), endDate, endId)
                    processesDuration.append(processDuration)
                eventsDuration.extend(processEventsDuration)
                phasesDuration.extend(processPhasesDuration)
                statesDuration.extend(processStateDuration)
            bar()
    return [processesDuration, eventsDuration, phasesDuration, statesDuration]

# return duration.
def getDurations(processEvents, processId, processSubjectCode, processSubject, processFinished, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, eventTag, eventsTag, numEventTag, phaseTag, sectionTag, stateTag):
    events = processEvents[eventsTag]
    if len(events) == 0:
        return [[], [], [], [], [], [], [], None, None, None, None, None]
    eventsDuration = []
    eventsSequence = []
    eventsPhaseSequence = []
    phasesDuration = []
    phasesSequence = []
    statesDuration = []
    statesSequence = []
    startPhaseEvent = events[0]
    startStateEvent = events[0]
    startProcessEventId = events[0][numEventTag]
    endProcessEventId = events[-1][numEventTag]
    startProcessDate = events[0][dateTag]
    endProcessDate = events[-1][dateTag]
    startProcessDateDt = dt.datetime.strptime(startProcessDate, '%Y-%m-%d %H:%M:%S')
    endProcessDateDt = dt.datetime.strptime(endProcessDate, '%Y-%m-%d %H:%M:%S')
    processDuration = (endProcessDateDt - startProcessDateDt).days
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        startPhase = frame.getPhaseOfState(statesName, startPhaseEvent[codeStateTag], phaseTag)
        currPhase = frame.getPhaseOfState(statesName, curr[codeStateTag], phaseTag)
        nextPhase = frame.getPhaseOfState(statesName, next[codeStateTag], phaseTag)
        currEventDateDt = dt.datetime.strptime(curr[dateTag], '%Y-%m-%d %H:%M:%S')
        nextEventDateDt = dt.datetime.strptime(next[dateTag], '%Y-%m-%d %H:%M:%S')
        eventDuration = (nextEventDateDt - currEventDateDt).days
        eventsDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], eventDuration, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, next[dateTag], next[numEventTag]])
        eventsPhaseSequence.append(currPhase)
        eventsSequence.append(curr[numEventTag])
        if nextPhase != '-' and startStateEvent[codeStateTag] != next[codeStateTag]:
            startStateDateDt = dt.datetime.strptime(startStateEvent[dateTag], '%Y-%m-%d %H:%M:%S')
            nextStateDateDt = dt.datetime.strptime(next[dateTag], '%Y-%m-%d %H:%M:%S')
            stateDuration = (nextStateDateDt - startStateDateDt).days
            statesDuration.append([startStateEvent[numEventTag], processId, startStateEvent[codeEventTag], startStateEvent[eventTag], stateDuration, startStateEvent[dateTag], startStateEvent[codeJudgeTag], startStateEvent[codeStateTag], startStateEvent[stateTag], startPhase, processSubjectCode, processSubject, startStateEvent[sectionTag], processFinished, next[dateTag], next[numEventTag]])
            if startStateEvent[stateTag] not in statesSequence and startPhase != '-':
                statesSequence.append(startStateEvent[stateTag])
            startStateEvent = next.copy()  
        if nextPhase != '-' and startPhase != nextPhase:
            startPhaseDateDt = dt.datetime.strptime(startPhaseEvent[dateTag], '%Y-%m-%d %H:%M:%S')
            nextPhaseDateDt = dt.datetime.strptime(next[dateTag], '%Y-%m-%d %H:%M:%S')
            phaseDuration = (nextPhaseDateDt - startPhaseDateDt).days
            phasesDuration.append([startPhaseEvent[numEventTag], processId, startPhaseEvent[codeEventTag], startPhaseEvent[eventTag], phaseDuration, startPhaseEvent[dateTag], startPhaseEvent[codeJudgeTag], startPhaseEvent[codeStateTag], startPhaseEvent[stateTag], startPhase, processSubjectCode, processSubject, startPhaseEvent[sectionTag], processFinished, next[dateTag], next[numEventTag]])
            if len(phasesSequence) == 0:
                phasesSequence.append(startPhase)
            elif phasesSequence[-1] == "RESTART":
                 if startPhase.isdigit() and int(startPhase) > int(phasesSequence[-2]):
                    phasesSequence.append(startPhase)
            else:
                if startPhase.isdigit() and int(startPhase) > int(phasesSequence[-1]):
                    phasesSequence.append(startPhase)
                elif startPhase.isdigit() and int(startPhase) < int(phasesSequence[-1]):
                    phasesSequence.append("RESTART")
            startPhaseEvent = next.copy()
    curr = events[-1]
    currPhase = frame.getPhaseOfState(statesName, curr[codeStateTag], phaseTag)
    eventDuration = 0
    eventsDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], eventDuration, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, curr[dateTag], curr[numEventTag]])
    eventsPhaseSequence.append(currPhase)
    eventsSequence.append(curr[numEventTag])
    if currPhase == endPhase:
        statesDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], 0, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, curr[dateTag], curr[numEventTag]])
        phasesDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], 0, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, curr[dateTag], curr[numEventTag]])
    if (len(statesSequence) == 0 or curr[stateTag] not in statesSequence):
        statesSequence.append(startStateEvent[stateTag])
    if len(phasesSequence) > 1 and phasesSequence[-1] == "RESTART":
        if currPhase != '-' and int(currPhase) > int(phasesSequence[-2]):
            phasesSequence.append(currPhase)
    elif len(phasesSequence) > 0:
        if currPhase != '-' and int(currPhase) > int(phasesSequence[-1]):
            phasesSequence.append(currPhase)
        elif currPhase != '-' and int(currPhase) < int(phasesSequence[-1]):
            phasesSequence.append("RESTART")
    else:
        if currPhase != '-':
            phasesSequence.append(currPhase)
    return [eventsDuration, eventsSequence, eventsPhaseSequence, phasesDuration, phasesSequence, statesDuration, statesSequence, processDuration, startProcessDate, startProcessEventId, endProcessDate, endProcessEventId]

# update process duration dataframe.
def updateProcessDurationDataframe(processDuration, codeSubjectTag, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag):
    [processDurationDataframe, processDurationDataframeFiltered] = frame.createProcessDurationsDataFrame(processDuration, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag, codeSubjectTag)
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
    if not connect.doesATableExist(connection, "tipoeventi"):
        raise Exception("\n'tipoeventi' table is not present or is called differently than 'tipoeventi'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "tipoeventi", ['CCDOEV', 'CDESCR'], ['VARCHAR(10)', 'TEXT']):
        raise Exception("\n'tipoeventi' table does not have all requested columns. The requested columns are: 'CCDOEV'(VARCHAR(10)), 'CDESCR'(TEXT)")
    if not connect.doesATableExist(connection, "tipomaterie"):
        raise Exception("\n'tipomaterie' table is not present or is called differently than 'tipomaterie'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "tipomaterie", ['codice', 'DESCCOMPLETA', 'rituale'], ['BIGINT', 'TEXT', 'VARCHAR(5)']):
        raise Exception("\n'tipomaterie' table does not have all requested columns. The requested columns are: 'codice'(BIGINT), 'DESCCOMPLETA'(TEXT), 'rituale'(VARCHAR(5))")
    if not connect.doesATableExist(connection, "tipostato"):
        raise Exception("\n'tipostato' table is not present or is called differently than 'tipostato'. Please change name or add such table because it's fundamental for the analysis")
    if not connect.doesATableHaveColumns(connection, "tipostato", ['CCODST', 'CDESCR', 'FKFASEPROCESSO'], ['VARCHAR(2)', 'TEXT', 'VARCHAR(3)']):
        raise Exception("\n'tipostato' table does not have all requested columns. The requested columns are: 'CCODST'(VARCHAR(2)), 'CDESCR'(TEXT), 'FKFASEPROCESSO'(VARCHAR(3))")
