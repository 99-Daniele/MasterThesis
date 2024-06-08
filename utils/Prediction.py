from alive_progress import alive_bar
import datetime as dt
import math
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

import utils.utilities.Utilities as utilities

# return how much finished process is like to unfinished one and duration of the finished process. 
def getLikenessInfo(processSequenceU, processSequenceF, processDurationF): 
    l1 = len(processSequenceU)
    l2 = len(processSequenceF)
    likeness = 0
    curr = 0
    i = 0
    for i in range(l1):
        idU = processSequenceU[i]
        plus = True
        count = 0
        while True:
            if i >= l2:
                j = (l2 - 1) - count
                if j < 0:
                    break
            if plus:
                j = i + count
                plus = False
                if j < 0 or j >= l2:
                    j = i - count
                    plus = True
                    if j < 0 or j >= l2:
                        break
            else:
                j = i - count
                plus = True
                if j < 0 or j >= l2:
                    j = i + count
                    plus = False
                    if j < 0 or j >= l2:
                        break
            idF = processSequenceF[j]
            if idU == idF:
                likeness += (l1 - count) / l1
                if j > curr:
                    curr = j
                break
            else:
                count += 1
    likeness = likeness * 100 / l1
    return pd.Series([likeness, processDurationF[curr]])

def predictDurations(finishedProcesses, unfinishedProcesses, codeJudgeTag, codeSubjectTag, durationTag, eventDurationSequenceTag, eventSequenceTag, finishedTag, numProcessTag, phaseDurationSequenceTag, phaseSequenceTag, sectionTag, stateDurationSequenceTag, stateSequenceTag):
    processesDurations = {}
    import time
    with alive_bar(int(len(unfinishedProcesses))) as bar:
        for u in unfinishedProcesses:
            processId = u[numProcessTag]
            judge = u[codeJudgeTag]
            subject = u[codeSubjectTag]
            section = u[sectionTag]
            eventSequence = u[eventSequenceTag]
            phaseSequence = u[phaseSequenceTag]
            stateSequence = u[stateSequenceTag]
            duration = u[eventDurationSequenceTag][-1]
            start = time.time()
            df = pd.DataFrame(finishedProcesses, columns = [codeJudgeTag, codeSubjectTag, sectionTag, finishedTag, eventSequenceTag, phaseSequenceTag, stateSequenceTag, eventDurationSequenceTag, phaseDurationSequenceTag, stateDurationSequenceTag])
            df[codeJudgeTag] = df[codeJudgeTag].apply(lambda x: 100 if x == judge else 0)
            df[codeSubjectTag] = df[codeSubjectTag].apply(lambda x: 100 if x == subject else 0)
            df[sectionTag] = df[sectionTag].apply(lambda x: 100 if x == section else 0)
            df[durationTag] = df[eventDurationSequenceTag].apply(lambda x: x[-1])
            df[[eventSequenceTag, eventDurationSequenceTag]] = df.apply(lambda x: getLikenessInfo(eventSequence, x[eventSequenceTag], x[eventDurationSequenceTag]), axis = 1)
            df[[stateSequenceTag, stateDurationSequenceTag]] = df.apply(lambda x: getLikenessInfo(stateSequence, x[stateSequenceTag], x[stateDurationSequenceTag]), axis = 1)
            df[[phaseSequenceTag, phaseDurationSequenceTag]] = df.apply(lambda x: getLikenessInfo(phaseSequence, x[phaseSequenceTag], x[phaseDurationSequenceTag]), axis = 1)
            X = df[[codeJudgeTag, codeSubjectTag, sectionTag, eventSequenceTag, eventDurationSequenceTag, stateSequenceTag, stateDurationSequenceTag, phaseSequenceTag, phaseDurationSequenceTag]]
            y = df[[durationTag]]
            model  = DecisionTreeClassifier()
            model.fit(X.values, y)
            predictedDuration = model.predict([[100, 100, 100, 100, duration, 100, duration, 100, duration]])
            processesDurations.update({processId: predictedDuration})            
            print(time.time() - start)
            bar()
    return processesDurations

def predictDurationsWithoutLikeness(df, codeJudgeTag, codeSubjectTag, durationTag, eventDurationSequenceTag, eventSequenceTag, finishedTag, numProcessTag, phaseDurationSequenceTag, phaseSequenceTag, sectionTag, stateDurationSequenceTag, stateSequenceTag):
    print(df)
    exit()
    processesDurations = {}
    import time
    with alive_bar(int(len(df))) as bar:
        for u in unfinishedProcesses:
            processId = u[numProcessTag]
            judge = u[codeJudgeTag]
            subject = u[codeSubjectTag]
            section = u[sectionTag]
            eventSequence = u[eventSequenceTag]
            phaseSequence = u[phaseSequenceTag]
            stateSequence = u[stateSequenceTag]
            duration = u[eventDurationSequenceTag][-1]
            start = time.time()
            df = pd.DataFrame(finishedProcesses, columns = [codeJudgeTag, codeSubjectTag, sectionTag, finishedTag, eventSequenceTag, phaseSequenceTag, stateSequenceTag, eventDurationSequenceTag, phaseDurationSequenceTag, stateDurationSequenceTag])
            df[codeJudgeTag] = df[codeJudgeTag].apply(lambda x: 100 if x == judge else 0)
            df[codeSubjectTag] = df[codeSubjectTag].apply(lambda x: 100 if x == subject else 0)
            df[sectionTag] = df[sectionTag].apply(lambda x: 100 if x == section else 0)
            df[durationTag] = df[eventDurationSequenceTag].apply(lambda x: x[-1])
            df[[eventSequenceTag, eventDurationSequenceTag]] = df.apply(lambda x: getLikenessInfo(eventSequence, x[eventSequenceTag], x[eventDurationSequenceTag]), axis = 1)
            df[[stateSequenceTag, stateDurationSequenceTag]] = df.apply(lambda x: getLikenessInfo(stateSequence, x[stateSequenceTag], x[stateDurationSequenceTag]), axis = 1)
            df[[phaseSequenceTag, phaseDurationSequenceTag]] = df.apply(lambda x: getLikenessInfo(phaseSequence, x[phaseSequenceTag], x[phaseDurationSequenceTag]), axis = 1)
            X = df[[codeJudgeTag, codeSubjectTag, sectionTag, eventSequenceTag, eventDurationSequenceTag, stateSequenceTag, stateDurationSequenceTag, phaseSequenceTag, phaseDurationSequenceTag]]
            y = df[[durationTag]]
            model  = DecisionTreeClassifier()
            model.fit(X.values, y)
            predictedDuration = model.predict([[100, 100, 100, 100, duration, 100, duration, 100, duration]])
            processesDurations.update({processId: predictedDuration})            
            print(time.time() - start)
            bar()
    return processesDurations

