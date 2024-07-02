# this file handles the update of database data.

from alive_progress import alive_bar
import datetime as dt
import pandas as pd

import utils.Cache as cache
import utils.database.DatabaseConnection as connect
import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Prediction as prediction
import utils.Utilities as utilities

# restart current database data in case events or process table are changed.
def restartData():
    connection = connect.getDatabaseConnection()
    # verifies if database has needed tables.
    verifyDatabase(connection)
    # reset cache folder.
    file.removeFolder('cache')
    file.createFolder('cache')
    # IA is the event that starts processes.
    startProcessEvent = 'IA'
    # when a state has endPhase as phase is a terminal state.
    endPhase = getter.getEndPhase()
    # when a stall state occurs process is set as continuative.
    stallStates = getter.getStallStates()
    # retrieve events from database
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
    # reset eventsInfo, statesInfo and subjectsInfo json file in cache folder.
    getter.getEventsInfo()
    getter.getStatesInfo()
    getter.getSubjectsInfo()
    # filteredEvents are the events filtered by not useful.
    # processesEventa are the events correctly orderer and filtered.
    # processesInfo are the info of each process for predictions.
    filteredEvents, processesEvents, processesInfo = getProcessEvents(events, startProcessEvent, stallStates, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, eventsTag, finishedTag, loadTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag)
    # eventsDataframe is the basic event dataframe.
    eventsDataframe = frame.createBasicEventsDataFrame(filteredEvents, dateTag, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, eventTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag)
    # eventsDataframe, processesInfo, processesEvents are saved in cache.
    cache.updateCacheDataframe('events.json', eventsDataframe)
    cache.updateCacheDataframe('processesInfo.json', processesInfo)
    cache.updateCacheData('processesEvents.json', processesEvents)
    predictDuration()
    refreshData()

# tests processes predictor.
def predictTest():
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    countTag = utilities.getTagName("countTag")
    dateTag = utilities.getTagName("dateTag")
    durationTag = utilities.getTagName("durationTag")
    durationFinalTag = utilities.getTagName("durationFinalTag")
    durationPredictedTag = utilities.getTagName("durationPredictedTag")
    errorTag = utilities.getTagName("errorTag")
    finishedTag = utilities.getTagName("finishedTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    sectionTag = utilities.getTagName("sectionTag")
    # retrieve processInfo from cache.
    processInfo = getter.getProcessesInfo()
    # keep only finished processes to be tested.
    finishedProcesses = processInfo[processInfo[finishedTag] == utilities.getProcessState('finished')]
    # calculate error prediction dataframe and save in cache.
    erorrPredictionDF = prediction.predictDurationsTestTotal(finishedProcesses, codeJudgeTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, errorTag, finishedTag, numProcessTag, sectionTag)
    cache.updateCacheDataframe('predictions.json', erorrPredictionDF)

# predict unfinished processes duration.
def predictDuration():
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    dateTag = utilities.getTagName("dateTag")
    durationTag = utilities.getTagName("durationTag")
    durationFinalTag = utilities.getTagName("durationFinalTag")
    durationPredictedTag = utilities.getTagName("durationPredictedTag")
    finishedTag = utilities.getTagName("finishedTag")
    numProcessTag = utilities.getTagName("numProcessTag")
    sectionTag = utilities.getTagName("sectionTag")
    # retrieve processInfo from cache.
    processInfo = getter.getProcessesInfo()
    # calculate duration prediction dataframe and save in cache.
    unfinishedProcessesDurations = prediction.predictDurations(processInfo, codeJudgeTag, codeSubjectTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag)
    cache.updateCacheData('unfinishedProcessesDurations.json', unfinishedProcessesDurations)

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
    # retrieve eventsDataframe, processEvents, unfinishedProcesses, statesInfoDataframe from cache.
    eventsDataframe = getter.getEventsDataframe()
    processEvents = getter.getProcessesEvents()
    unfinishedProcesses = getter.getUnfinishedProcessesDuration()
    statesInfoDataframe = getter.getStatesInfo()
    # convert statesInfoDataframe into dictionary.
    statesInfo = statesInfoDataframe.set_index(codeStateTag).T.to_dict('dict')
    # endPhase is the phase associated to state "DF".
    endPhase = frame.getPhaseOfState(statesInfo, "DF", phaseTag)
    # calculate durations of events, states, phases and processes.
    updateDurationsDataframe(processEvents, unfinishedProcesses, statesInfo, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, durationPredictedTag, eventTag, eventsTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, phaseSequenceTag, sectionTag, stateTag, stateSequenceTag, subjectTag)
    # update events dataframe and save in cache.
    updateEventsDataframe(eventsDataframe, statesInfoDataframe, endPhase, codeStateTag, dateTag, numEventTag, numProcessTag, phaseTag, phaseDBTag, stateTag)

# group events by process.
def getProcessEvents(events, startProcessEvent, stallStates, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, eventsTag, finishedTag, loadTag, numEventTag, numProcessTag, phaseDBTag, processDateTag, sectionTag, stateTag, subjectTag):
    if len(events) == 0:
        raise Exception("\nThere isn't any event in database.")
    # filteredEvents contains all useful events.
    filteredEvents = []
    # allProcessEvents contains a list of dictonaries with process info and events.
    allProcessEvents = []
    # allProcessDict contains a list of dictonaries with process info useful for prediction.
    allProcessDict = []
    # df is the dataframe created from events.
    df = pd.DataFrame(events, columns = [numEventTag, numProcessTag, codeEventTag, eventTag, codeJudgeTag, dateTag, processDateTag, codeStateTag, stateTag, phaseDBTag, codeSubjectTag, subjectTag, sectionTag])
    # eventsColumns is the list of all registered type of events.
    eventsColumns = frame.getGroupBy(df, codeEventTag)
    # statesColumns is the list of all registered type of states.
    statesColumns = frame.getGroupBy(df, codeStateTag)
    # phasesColumns is the list of all registered type of phases.
    phasesColumns = frame.getGroupBy(df, phaseDBTag)
    # transform eventsColumns, statesColumns, phasesColumns by adding ":" for each item.
    eventsColumns = [eventTag + ": " + e for e in eventsColumns]
    statesColumns = [stateTag + ": " + s for s in statesColumns]
    phasesColumns = [phaseDBTag + ": " + p for p in phasesColumns]
    # dfColumns are the columns of the dataframe used for predictions.
    # contains numProcess, date, judgeCode, subjectCode, section, process finished type, process current duration,
    # process final duration, current events count.
    # this is concatenated with eventsColumns, statesColumns, phasesColumns.
    dfColumns = [numProcessTag, dateTag, codeJudgeTag, codeSubjectTag, sectionTag, finishedTag, durationTag, durationFinalTag, countTag] + eventsColumns + statesColumns + phasesColumns
    # processEventSequence is the current process sequence of events. Initialized as [].
    processEventSequence = [] 
    # processPhaseSequence is the current process sequence of phases. Initialized as [].
    processPhaseSequence = []
    # processStateSequence is the current process sequence of states. Initialized as [].
    processStateSequence = []
    # eventDurationSequence is the current process sequence of event durations. Initialized as [].
    eventDurationSequence = []
    # phaseDurationSequence is the current process sequence of event durations. Initialized as [].
    phaseDurationSequence = []
    # stateDurationSequence is the current process sequence of event durations. Initialized as [].
    stateDurationSequence = []
    # processEventSequenceComplete is the current process sequence of events. Initialized as [].
    # processEventSequenceComplete contains all events even when there are duplicates.
    processEventSequenceComplete = []
    # processPhaseSequenceComplete is the current process sequence of phases. Initialized as [].
    # processPhaseSequenceComplete contains all phases even when there are duplicates.
    processPhaseSequenceComplete = []
    # processStateSequenceComplete is the current process sequence of states. Initialized as [].
    # processStateSequenceComplete contains all states even when there are duplicates.
    processStateSequenceComplete = []
    # durationSequenceComplete is the current process sequence of process duration. Initialized as [].
    durationSequenceComplete = []
    # judgeDict is a dictonary for coding judge string code into integer.
    judgeDict = {}
    # sectionDict is a dictonary for coding judge string code into integer.
    sectionDict = {}
    # subjectDict is a dictonary for coding judge string code into integer.
    subjectDict = {}
    # findFirstEvent() loop until first initial event IA is found.
    [i, processId, processCodeJudge, processSubjectCode, processSection, processFinished, processStartDate, distance, processStartDateDt, processEvents] = findFirstEvent(events, startProcessEvent, codeEventTag, codeJudgeTag, eventsTag, finishedTag, numProcessTag, codeSubjectTag, dateTag, sectionTag, subjectTag)
    # start is True when starting event is found.
    start = True
    # end is False until end state is found.
    end = False
    # continuative is False until stall state is found.
    continuative = False
    with alive_bar(int(len(events) - i)) as bar:
        while i < int(len(events)):
            # when i-th event has different processId means a new process has been found.
            if events[i][numProcessTag] != processId:
                # start is set to false until a start event is found.
                start = False
                # if start event or stall state is found, previous process is added to allProcessEvents and a new process loop starts.
                if events[i][codeEventTag] == startProcessEvent or events[i][codeStateTag] in stallStates:
                    allProcessEvents.append(processEvents)
                    # if process has at least one event, allProcessDict, judgeDict, sectionDict, subjectDict are updated with process data. 
                    if len(durationSequenceComplete) > 0:
                        [allProcessDict, judgeDict, sectionDict, subjectDict] = updateDict(dfColumns, allProcessDict, judgeDict, sectionDict, subjectDict, durationSequenceComplete, processEventSequenceComplete, processStateSequenceComplete, processPhaseSequenceComplete, processId, processStartDate, distance, processCodeJudge, processSubjectCode, processSection, processFinished, codeJudgeTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, finishedTag, numProcessTag, phaseDBTag, sectionTag, stateTag)
                    # new process info are reset for new loop.
                    [processId, processCodeJudge, processSubjectCode, processSection, processStartDate, processStartDateDt, distance, processFinished, processEventSequence, processPhaseSequence, processStateSequence, eventDurationSequence, phaseDurationSequence, stateDurationSequence, processEventSequenceComplete, processPhaseSequenceComplete, processStateSequenceComplete, durationSequenceComplete, processEvents] = reset(events, i, codeJudgeTag, codeSubjectTag, dateTag, eventsTag, finishedTag, numProcessTag, sectionTag, subjectTag)
                    start = True
                    end = False
                    continuative = False
            # when end = False and start = True means that process loop holds.
            if not end and start:
                # if i-th event state is a stall state then process is set as continuative.
                if events[i][codeStateTag] in stallStates and not continuative:
                    processFinished = utilities.getProcessState('continuative')
                    processEvents[finishedTag] = processFinished
                    continuative = True
                # if i-th event phase is end phase then process is set as finished, end is set True meaning that following events are no longer considerer until new process.
                if events[i][phaseDBTag] == endPhase and not continuative: 
                    processFinished = utilities.getProcessState('finished')
                    processEvents[finishedTag] = processFinished
                    end = True
                # if i-th event judge is different from process one, then is changed.
                if events[i][codeJudgeTag] != processCodeJudge:
                    processCodeJudge = events[i][codeJudgeTag]
                    processEvents[codeJudgeTag] = processCodeJudge
                # if i-th event section is different from process one, then is changed.
                if events[i][sectionTag] != processSection:
                    processSection = events[i][sectionTag]
                    processEvents[sectionTag] = processSection
                processDate = events[i][dateTag]
                processDateDt = dt.datetime.strptime(processDate, '%Y-%m-%d %H:%M:%S')
                # duration is the current duration of process at i-th event. Is calculated as the difference between event date and start date.
                duration = (processDateDt - processStartDateDt).days
                # event is added to process list of evens.
                processEvents[eventsTag].append(events[i])
                codeEvent = events[i][codeEventTag]
                phase = events[i][phaseDBTag]
                # in case db phase is None is set to '0.0'
                if phase == None:
                    phase = '0.0'
                codeState = events[i][codeStateTag]
                # if processEventSequence is empty or event type is different from the previous, is added to event and event duration list.
                if len(processEventSequence) == 0 or codeEvent != processEventSequence[-1]:
                    processEventSequence.append(codeEvent)
                    eventDurationSequence.append(duration)
                # processEventSequenceComplete add event even if is the same of previous one.
                processEventSequenceComplete.append(codeEvent)
                # if processPhaseSequence is empty or event phase is different from the previous, is added to state and state duration list.
                if len(processPhaseSequence) == 0 or phase != processPhaseSequence[-1]:
                    processPhaseSequence.append(phase)
                    phaseDurationSequence.append(duration)
                # processPhaseSequenceComplete add event even if is the same of previous one.
                processPhaseSequenceComplete.append(phase)
                # if processStateSequence is empty or event state is different from the previous, is added to phase and phase duration list.
                if len(processStateSequence) == 0 or codeState != processStateSequence[-1]:
                    processStateSequence.append(codeState)
                    stateDurationSequence.append(duration)
                # processStateSequenceComplete add event even if is the same of previous one.
                processStateSequenceComplete.append(codeState)
                # duration is added to durationSequenceComplete.
                durationSequenceComplete.append(duration)
                # since process start date is firstly chosen as the fisr event of the process, but not necessary is true because the first useful event is IA,
                # start date might be wrong. To avoid this is changed with founded process start date.
                newEvent = events[i].copy()
                newEvent.update({processDateTag: processStartDate})
                # newEvent is then added to filteredEvents.
                filteredEvents.append(newEvent)
            bar()
            i += 1
    # when list of events loop end, theremight a pendant process loop if process is unfinished. If end = False is then added as unfinished.
    if not end:
        allProcessEvents.append(processEvents)
        if len(durationSequenceComplete) > 0:
            [allProcessDict, judgeDict, sectionDict, subjectDict] = updateDict(dfColumns, allProcessDict, judgeDict, sectionDict, subjectDict, durationSequenceComplete, processEventSequenceComplete, processStateSequenceComplete, processPhaseSequenceComplete, processId, processStartDate, distance, processCodeJudge, processSubjectCode, processSection, processFinished, codeJudgeTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, finishedTag, numProcessTag, phaseDBTag, sectionTag, stateTag)
    # allProcessDict is converted to dataframe.
    processInfoDataframe = pd.DataFrame.from_dict(allProcessDict)
    return filteredEvents, allProcessEvents, processInfoDataframe

# loop events until is founded a startProcessEvent which is the first relevant event of the list.
# return index i, founded process ID, judge, subject, section, process type as unfinished, start date, distance from first day of the year, start Date as datetime, process initial dict.
def findFirstEvent(events, startProcessEvent, codeEventTag, codeJudgeTag, eventsTag, finishedTag, numProcessTag, codeSubjectTag, dateTag, sectionTag, subjectTag):
    i = 0
    while i < int(len(events)):
        # when startProcessEvent is founded loop is broken.
        if events[i][codeEventTag] == startProcessEvent:
            # processID is i-th event numProcess.
            processId = events[i][numProcessTag]
            # processCodeJudge is i-th event judge.
            processCodeJudge = events[i][codeJudgeTag]
            # processSubjectCode is i-th event subject code.
            processSubjectCode = events[i][codeSubjectTag]
            # processSubjectCode is i-th event subject.
            processSubject = events[i][subjectTag]
            # processSubjectCode is i-th event section.
            processSection = events[i][sectionTag]
            # processFinished is initialized as unfinished.
            processFinished = utilities.getProcessState('unfinished')
            # processStartDate is date of start process.
            processStartDate = events[i][dateTag]
            # processStartDateDt is date of start process as datetime.
            processStartDateDt = dt.datetime.strptime(processStartDate, '%Y-%m-%d %H:%M:%S')
            # distance is the distance from first of the year of sart process date. This is used to code date to integer.
            distance = utilities.distanceFromFirstOfTheYear(processStartDateDt)
            # processEvents is the dict with process info and events list.
            processEvents = {numProcessTag: processId, codeJudgeTag: processCodeJudge, codeSubjectTag: processSubjectCode, subjectTag: processSubject, sectionTag: processSection, finishedTag: processFinished, eventsTag: []}
            break
        i += 1
    return [i, processId, processCodeJudge, processSubjectCode, processSection, processFinished, processStartDate, distance, processStartDateDt, processEvents]

# reset initialize new process info values and set lists as [].
def reset(events, i, codeJudgeTag, codeSubjectTag, dateTag, eventsTag, finishedTag, numProcessTag, sectionTag, subjectTag):
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
    return [processId, processCodeJudge, processSubjectCode, processSection, processStartDate, processStartDateDt, distance, processFinished, processEventSequence, processPhaseSequence, processStateSequence, eventDurationSequence, phaseDurationSequence, stateDurationSequence, processEventSequenceComplete, processPhaseSequenceComplete, processStateSequenceComplete, durationSequenceComplete, processEvents]

# update dictionaries based on collected process info.
def updateDict(dfColumns, allProcessDict, judgeDict, sectionDict, subjectDict, durationSequenceComplete, processEventSequenceComplete, processStateSequenceComplete, processPhaseSequenceComplete, processId, processStartDate, distance, processCodeJudge, processSubjectCode, processSection, processFinished, codeJudgeTag, codeSubjectTag, countTag, dateTag, distanceTag, durationTag, durationFinalTag, eventTag, finishedTag, numProcessTag, phaseDBTag, sectionTag, stateTag):
    # processDict is created from dfColumns all initialized as 0.
    # processDict shows each stage of the process.
    processDict = dict.fromkeys(dfColumns)
    processDict = {x: 0 for x in processDict}
    # numProcess, date and distance are stored as input values.
    processDict.update({numProcessTag: processId})
    processDict.update({dateTag: processStartDate})
    processDict.update({distanceTag: distance})
    # if judge is in judgeDict the stored value is the one of the dict. Othwerise creates a new one.
    if processCodeJudge in judgeDict.keys():
        judgeID = judgeDict.get(processCodeJudge)
    else:
        # in case judgeDict is empty initial judge code is 0.
        if len(list(judgeDict.values())) == 0:
            judgeID = 0
        # if judge code is not in judgeDict, last value is taken and new value is last value + 10000.
        else:
            judgeID = list(judgeDict.values())[-1] + 10000
        judgeDict.update({processCodeJudge: judgeID})
    processDict.update({codeJudgeTag: judgeID})
    # if subject is in subjectDict the stored value is the one of the dict. Othwerise creates a new one.
    if processSubjectCode in subjectDict.keys():
        subjectID = subjectDict.get(processSubjectCode)
    else:
        # in case subjectDict is empty initial subject code is 0.
        if len(list(subjectDict.values())) == 0:
            subjectID = 0
        # if subject code is not in subjectDict, last value is taken and new value is last value + 10000.
        else:
            subjectID = list(subjectDict.values())[-1] + 10000
        subjectDict.update({processSubjectCode: subjectID})
    processDict.update({codeSubjectTag: subjectID})
    # if section is in sectionDict the stored value is the one of the dict. Othwerise creates a new one.
    if processSection in sectionDict.keys():
        sectionID = sectionDict.get(processSection)
    else:
        # in case sectionDict is empty initial subject code is 0.
        if len(list(sectionDict.values())) == 0:
            sectionID = 0
        # if section code is not in sectionDict, last value is taken and new value is last value + 10000.
        else:
            sectionID = list(sectionDict.values())[-1] + 10000
        sectionDict.update({processSection: sectionID})
    processDict.update({sectionTag: sectionID})
    processDict.update({finishedTag: processFinished})
    # final process duration is the last stored duration in duration list.
    finalDuration = int(durationSequenceComplete[-1])
    # for each event, state and phase stored in list,the loop will increment by 1 the correlated variable and save duration at tht time.
    # by doing this a list of all snapshot of process is created.
    for j in range(len(processEventSequenceComplete)):
        codeEvent = processEventSequenceComplete[j]
        phase = processPhaseSequenceComplete[j]
        if phase == None:
            phase = '0.0'
        codeState = processStateSequenceComplete[j]
        duration = int(durationSequenceComplete[j])
        # get old count of j-th event, phase and state, increment by 1 and store.
        eventCount = processDict.get(eventTag + ": " + codeEvent)
        phaseCount = processDict.get(phaseDBTag + ": " + phase)
        stateCount = processDict.get(stateTag + ": " + codeState)
        processDict.update({eventTag + ": " + codeEvent: eventCount + 1})
        processDict.update({phaseDBTag + ": " + phase: phaseCount + 1})
        processDict.update({stateTag + ": " + codeState: stateCount + 1})
        processDict.update({countTag: j + 1})
        # store duration of process at j-th iteration.
        processDict.update({durationTag: duration})
        # store residual suration to process end at j-th iteration.
        processDict.update({durationFinalTag: finalDuration - duration})
        # if process is a finished process add all snapshots.
        if processFinished == utilities.getProcessState('finished'):
            allProcessDict.append(processDict.copy())
    # if process is an unfinished process add only last snapshot, which is the one used for predictions.
    if processFinished == utilities.getProcessState('unfinished'):
        allProcessDict.append(processDict.copy())
    return [allProcessDict, judgeDict, sectionDict, subjectDict]

# update events dataframe.
def updateEventsDataframe(eventsDataframe, statesNameDataframe, endPhase, codeStateTag, dateTag, numEventTag, numProcessTag, phaseTag, phaseDBTag, stateTag):
    # joins basic event dataframe with statesNameDataframe with user choices.
    eventsDataframeComplete = frame.joinDataframe(eventsDataframe, statesNameDataframe, codeStateTag, phaseDBTag, [phaseDBTag, stateTag])
    # create the allEventsDataframe and sort by numProcess, date and numEvent.
    allEventsDataframe = frame.createEventsDataFrame(eventsDataframeComplete, endPhase, dateTag, numEventTag, numProcessTag, phaseTag)
    allEventsDataframe = allEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    # update all dataframes and store in cache.
    cache.updateCacheDataframe('allEvents.json', allEventsDataframe)
    updateStateEventsDataframe(allEventsDataframe, codeStateTag, dateTag, numEventTag, numProcessTag)
    updatePhaseEventsDataframe(allEventsDataframe, dateTag, numEventTag, numProcessTag, phaseTag)

# update state events dataframe.
def updateStateEventsDataframe(stateEventsDataframe, codeStateTag, dateTag, numEventTag, numProcessTag):
    # takes only the first event of each process state.
    stateEventsDataframe = stateEventsDataframe.groupby([numProcessTag, codeStateTag], as_index = False).first()
    # filter by important states chosen by user.
    importantStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantStates != None and len(importantStates) > 0:
        stateEventsDataframe = stateEventsDataframe[stateEventsDataframe[codeStateTag].isin(importantStates)]
    # sort by numProcess, date and numEvent and store in cache.
    stateEventsDataframe = stateEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCacheDataframe('stateEvents.json', stateEventsDataframe)

# update phase events dataframe.
def updatePhaseEventsDataframe(phaseEventsDataframe, dateTag, numEventTag, numProcessTag, phaseTag):
    # takes only the first event of each process phase.
    phaseEventsDataframe = phaseEventsDataframe.groupby([numProcessTag, phaseTag], as_index = False).first()
    # sort by numProcess, date and numEvent and store in cache.
    phaseEventsDataframe = phaseEventsDataframe.sort_values(by = [numProcessTag, dateTag, numEventTag]).reset_index(drop = True)
    cache.updateCacheDataframe('phaseEvents.json', phaseEventsDataframe)

# update types duration dataframe.
def updateDurationsDataframe(processEvents, unfinishedProcesses, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationTag, durationPredictedTag, eventTag, eventsTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, phaseSequenceTag, sectionTag, stateTag, stateSequenceTag, subjectTag):
    # calcs process, events, phases and states duration.
    [processesDuration, eventsDuration, phasesDuration, statesDuration] = calcDurations(processEvents, unfinishedProcesses, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationPredictedTag, eventTag, eventsTag, finishedTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag)
    # create allEvents and filteredEvents duration dataframes.
    [eventsDurationDataframe, eventsDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(eventsDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    # create allPhases and filteredPhases duration dataframes.
    [phasesDurationDataframe, phasesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(phasesDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    # create allState and filteredStates duration dataframe.
    [statesDurationDataframe, statesDurationDataframeFiltered] = frame.createTypeDurationsDataFrame(statesDuration, codeEventTag, codeJudgeTag, codeSubjectTag, dateTag, durationTag, eventTag, finishedTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, codeStateTag, subjectTag)
    # create allProcess and filteredProcesses duration dataframe.
    [processDurationDataframe, processDurationDataframeFiltered] = frame.createProcessDurationsDataFrame(processesDuration, dateTag, durationTag, eventSequenceTag, eventPhaseSequenceTag, finishedTag, codeJudgeTag, nextDateTag, nextIdTag, numEventTag, numProcessTag, phaseSequenceTag, sectionTag, stateSequenceTag, subjectTag, codeSubjectTag)
    # stores dataframe in cache.
    cache.updateCacheDataframe('eventsDuration.json', eventsDurationDataframe)
    cache.updateCacheDataframe('eventsDurationFiltered.json', eventsDurationDataframeFiltered)
    cache.updateCacheDataframe('phasesDuration.json', phasesDurationDataframe)
    cache.updateCacheDataframe('phasesDurationFiltered.json', phasesDurationDataframeFiltered)
    cache.updateCacheDataframe('statesDuration.json', statesDurationDataframe)
    cache.updateCacheDataframe('statesDurationFiltered.json', statesDurationDataframeFiltered)
    cache.updateCacheDataframe('processesDuration.json', processDurationDataframe)
    cache.updateCacheDataframe('processesDurationFiltered.json', processDurationDataframeFiltered)

# calc processes, events, states and phases durations.
def calcDurations(processes, unfinishedProcesses, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, codeSubjectTag, dateTag, durationPredictedTag, eventTag, eventsTag, finishedTag, numEventTag, numProcessTag, phaseTag, sectionTag, stateTag, subjectTag):
    eventsDuration = []
    phasesDuration = []
    statesDuration = []
    processesDuration = []
    with alive_bar(int(len(processes))) as bar:
        # each element of processes list is a dictornay which contains informatoin about the process and process events list.
        for i in range(int(len(processes))):
            processId = processes[i][numProcessTag]
            processCodeJudge = processes[i][codeJudgeTag]
            processSubjectCode = processes[i][codeSubjectTag]
            processSubject = processes[i][subjectTag]
            processFinished = processes[i][finishedTag]
            processSection = processes[i][sectionTag]
            # calculate events duration, events sequence, phase of all events sequence, phase duration, phase sequence, state duration, state sequence, processDuration, process start date, process start event, process end date, process end event are calculated with getDurations().
            [processEventsDuration, eventsSequence, eventPhaseSequence, processPhasesDuration, phasesSequence, processStateDuration, statesSequence, processDuration, startDate, startEventId, endDate, endId] = getDurations(processes[i], processId, processSubjectCode, processSubject, processFinished, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, eventTag, eventsTag, numEventTag, phaseTag, sectionTag, stateTag)
            # if process events list is empty getDurations() return None.
            # if not process, events, states, phases duration list is integrated with new calculated ones.
            if processDuration != None:
                # if process is unfinished process duration is changed to previously predicted process duration.
                if processFinished == utilities.getProcessState('unfinished'):
                    if str(processId) in unfinishedProcesses.keys():
                        predictedDuration = unfinishedProcesses.get(str(processId))[durationPredictedTag]
                        endDatePredicted = utilities.finalDate(startDate, predictedDuration)
                        processDuration = (processId, predictedDuration, startDate, startEventId, processCodeJudge, processSubjectCode, processSubject, processSection, processFinished, utilities.fromListToString(statesSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence), utilities.fromListToString(eventPhaseSequence), endDatePredicted, endId)
                        processesDuration.append(processDuration)
                else:
                    processDuration = (processId, processDuration, startDate, startEventId, processCodeJudge, processSubjectCode, processSubject, processSection, processFinished, utilities.fromListToString(statesSequence), utilities.fromListToString(phasesSequence), utilities.fromListToString(eventsSequence), utilities.fromListToString(eventPhaseSequence), endDate, endId)
                    processesDuration.append(processDuration)
                eventsDuration.extend(processEventsDuration)
                phasesDuration.extend(processPhasesDuration)
                statesDuration.extend(processStateDuration)
            bar()
    return [processesDuration, eventsDuration, phasesDuration, statesDuration]

# return processes, events, states and phases durations.
def getDurations(processDict, processId, processSubjectCode, processSubject, processFinished, statesName, endPhase, codeEventTag, codeJudgeTag, codeStateTag, dateTag, eventTag, eventsTag, numEventTag, phaseTag, sectionTag, stateTag):
    # events are taken from process dict events list. In case is empty return empty and None values.
    events = processDict[eventsTag]
    if len(events) == 0:
        return [[], [], [], [], [], [], [], None, None, None, None, None]
    # lists are initialized as empty.
    eventsDuration = []
    eventsSequence = []
    eventsPhaseSequence = []
    phasesDuration = []
    phasesSequence = []
    statesDuration = []
    statesSequence = []
    # startPhaseEvent is the event that start current phase.
    startPhaseEvent = events[0]
    # startPhase is the current phase.
    startPhase = frame.getPhaseOfState(statesName, startPhaseEvent[codeStateTag], phaseTag)
    # startStateEvent is the event that start current state.
    startStateEvent = events[0]
    # startProcessEventId is the event that start process.
    startProcessEventId = events[0][numEventTag]
    # endProcessEventId is the event that end process.
    endProcessEventId = events[-1][numEventTag]
    # startProcessDate is the date of the event that start process.
    startProcessDate = events[0][dateTag]
    # endProcessDate is the date of the event that end process.
    endProcessDate = events[-1][dateTag]
    # startProcessDateDt is the date of the event that start process in datetime.
    startProcessDateDt = dt.datetime.strptime(startProcessDate, '%Y-%m-%d %H:%M:%S')
    # endProcessDateDt is the date of the event that end process in datetime.
    endProcessDateDt = dt.datetime.strptime(endProcessDate, '%Y-%m-%d %H:%M:%S')
    # processDuration is calculated as the difference between end and start process dates.
    processDuration = (endProcessDateDt - startProcessDateDt).days
    # iterate on process events by inpecting current and next event,
    for i in range(len(events) - 1):
        curr = events[i]
        next = events[i + 1]
        # currPhase and nextPhase are the phase of curr and next events.
        currPhase = frame.getPhaseOfState(statesName, curr[codeStateTag], phaseTag)
        nextPhase = frame.getPhaseOfState(statesName, next[codeStateTag], phaseTag)
        # currPhaseDt and nextPhaseDt are the date of curr and next events.
        currEventDateDt = dt.datetime.strptime(curr[dateTag], '%Y-%m-%d %H:%M:%S')
        nextEventDateDt = dt.datetime.strptime(next[dateTag], '%Y-%m-%d %H:%M:%S')
        # eventDuration is calculated as the difference between next and curr event dates.
        eventDuration = (nextEventDateDt - currEventDateDt).days
        # append to eventsDuration all info about current event: numEvent, processId, eventCode, eventType, eventDuration, eventDate, eventJudge, eventStateCode, eventStateType, eventStatePhase, processSubjectCode, processSubject, processSection, process type, next event date, next event numEvent.
        eventsDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], eventDuration, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, next[dateTag], next[numEventTag]])
        eventsPhaseSequence.append(currPhase)
        eventsSequence.append(curr[eventTag])
        # when next state is different from curr state, current state duration is a calculated and info are added to list.
        # phase "-" is not considered.
        if nextPhase != '-' and curr[codeStateTag] != next[codeStateTag]:
            # startStateDateDt and nextStateDateDt are the date of start and end state events.
            startStateDateDt = dt.datetime.strptime(startStateEvent[dateTag], '%Y-%m-%d %H:%M:%S')
            nextStateDateDt = dt.datetime.strptime(next[dateTag], '%Y-%m-%d %H:%M:%S')
            # stateDuration is calculated as the difference between end and start state dates.
            stateDuration = (nextStateDateDt - startStateDateDt).days
            # append to statesDuration all info about current state: start state numEvent, processId, start state eventCode, start state eventType, stateDuration, start state eventDate, start state eventJudge, stateCode, stateType, statePhase, processSubjectCode, processSubject, processSection, process type, next state date, next state numEvent.
            statesDuration.append([startStateEvent[numEventTag], processId, startStateEvent[codeEventTag], startStateEvent[eventTag], stateDuration, startStateEvent[dateTag], startStateEvent[codeJudgeTag], startStateEvent[codeStateTag], startStateEvent[stateTag], startPhase, processSubjectCode, processSubject, startStateEvent[sectionTag], processFinished, next[dateTag], next[numEventTag]])
            # if state is not in statesSequence and currPhase is not "-" add state to statesSequence.
            if startStateEvent[stateTag] not in statesSequence and currPhase != '-':
                statesSequence.append(startStateEvent[stateTag])
            # the new startStateEvent is next event.
            startStateEvent = next.copy()  
        # when next phase is different from curr phase, current phase duration is a calculated and info are added to list.
        # phase "-" is not considered.    
        if nextPhase != '-' and currPhase != nextPhase:
            # startPhaseDateDt and nextPhaseDateDt are the date of start and end phase events.
            startPhaseDateDt = dt.datetime.strptime(startPhaseEvent[dateTag], '%Y-%m-%d %H:%M:%S')
            nextPhaseDateDt = dt.datetime.strptime(next[dateTag], '%Y-%m-%d %H:%M:%S')
            # phaseDuration is calculated as the difference between end and start phase dates.
            phaseDuration = (nextPhaseDateDt - startPhaseDateDt).days
            # append to phasesDuration all info about current phase: start phase numEvent, processId, start phase eventCode, start phase eventType, phaseDuration, start phase eventDate, start phase eventJudge, start phase stateCode, start phase stateType, phase, processSubjectCode, processSubject, processSection, process type, next phase date, next phase numEvent.
            phasesDuration.append([startPhaseEvent[numEventTag], processId, startPhaseEvent[codeEventTag], startPhaseEvent[eventTag], phaseDuration, startPhaseEvent[dateTag], startPhaseEvent[codeJudgeTag], startPhaseEvent[codeStateTag], startPhaseEvent[stateTag], startPhase, processSubjectCode, processSubject, startPhaseEvent[sectionTag], processFinished, next[dateTag], next[numEventTag]])
            # add phase to phasesSequence.
            phasesSequence.append(startPhase)
            # the new startPhaseEvent is next event and startPhase its phase.
            startPhaseEvent = next.copy()
            startPhase = frame.getPhaseOfState(statesName, startPhaseEvent[codeStateTag], phaseTag)
    # since loop is on curr and next events, the last event is not considered. Following code is for the last event.
    curr = events[-1]
    currPhase = frame.getPhaseOfState(statesName, curr[codeStateTag], phaseTag)
    eventDuration = 0
    eventsDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], eventDuration, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, curr[dateTag], curr[numEventTag]])
    eventsPhaseSequence.append(currPhase)
    eventsSequence.append(curr[eventTag])
    if currPhase == endPhase:
        statesDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], 0, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, curr[dateTag], curr[numEventTag]])
        phasesDuration.append([curr[numEventTag], processId, curr[codeEventTag], curr[eventTag], 0, curr[dateTag], curr[codeJudgeTag], curr[codeStateTag], curr[stateTag], currPhase, processSubjectCode, processSubject, curr[sectionTag], processFinished, curr[dateTag], curr[numEventTag]])
    if (len(statesSequence) == 0 or curr[stateTag] not in statesSequence) and currPhase != '-':
        statesSequence.append(curr[stateTag])
    if len(phasesSequence) == 0 or currPhase != phasesSequence[-1]:
        phasesSequence.append(currPhase)
    return [eventsDuration, eventsSequence, eventsPhaseSequence, phasesDuration, phasesSequence, statesDuration, statesSequence, processDuration, startProcessDate, startProcessEventId, endProcessDate, endProcessEventId]

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
