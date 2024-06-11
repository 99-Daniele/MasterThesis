from alive_progress import alive_bar
import matplotlib.pyplot as plt
import pandas as pd
import random as rd
from sklearn.tree import DecisionTreeClassifier

import utils.Dataframe as frame
import utils.FileOperation as file
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

def predictDurationsWithoutLikenessTest(df, codeJudgeTag, codeSubjectTag, countTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag):
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(durationFinalTag)
    numProcesses = frame.getUniques(df, numProcessTag).tolist()
    errors = []
    predictions = []
    with alive_bar(int(len(numProcesses))) as bar:
        for i in range(int(len(numProcesses))):
            testNumProcesses = [numProcesses[i]]
            trainNumProcesses = numProcesses[:i] + numProcesses[i + 1:]
            testDF = df[df[numProcessTag].isin(testNumProcesses)].copy()
            lTest = len(testDF)
            r = rd.randint(0, lTest - 1)
            testDF_temp = testDF.iloc[r]
            judge = testDF_temp[codeJudgeTag]
            subject = testDF_temp[codeSubjectTag]
            section = testDF_temp[sectionTag]
            processID = testDF_temp[numProcessTag]
            count = testDF_temp[countTag]
            currDuration = testDF_temp[durationTag]
            trainDF_temp = df[df[numProcessTag].isin(trainNumProcesses)].copy()
            trainDF_temp = trainDF_temp[trainDF_temp[codeJudgeTag] == judge]
            trainDF_temp = trainDF_temp[trainDF_temp[codeSubjectTag] == subject]
            trainDF_temp = trainDF_temp[trainDF_temp[sectionTag] == section]
            lenTrainTemp = len(trainDF_temp)
            if lenTrainTemp > 0:
                trainX = trainDF_temp[columns]
                trainY = trainDF_temp[[durationFinalTag]]
                testX = testDF_temp[columns]
                testY = testDF_temp[[durationFinalTag]]
                model  = DecisionTreeClassifier()
                model.fit(trainX.values, trainY)
                predictedDuration = model.predict([testX.values])[0]
                currDuration = testX[durationTag]
                finalDuration = currDuration + testY[durationFinalTag]
                predictedFinalDuration = currDuration + predictedDuration 
                if finalDuration > 0:
                    error = abs(predictedFinalDuration - finalDuration) * 100 / finalDuration
                    errors.extend([error])
                    predictions.extend([{numProcessTag: str(processID), countTag: str(count), durationTag: str(currDuration), durationFinalTag: str(finalDuration), durationPredictedTag: str(predictedFinalDuration), 'errore': error}])
            bar() 
    errors = sorted(errors)
    m = int(len(errors) / 2)
    if len(errors) % 2 != 0:
        medianError = errors[m]
    else:
        medianError = (errors[m - 1] + errors[m]) / 2.0
    meanError = sum(errors) / len(errors)
    print(len(errors), int(len(numProcesses) / 10), meanError, medianError)
    predictions = sorted(predictions, key = lambda x: x['errore'])
    file.writeOnJsonFile('cache/predictions.json', predictions)
    #plt.scatter(testY, predictedDurations)
    #plt.xlabel('Actual Petal Width')
    #plt.ylabel('Predicted Petal Width')
    #plt.title('Actual vs Predicted Petal Width')
    #plt.show()
    return meanError

def predictDurationsWithoutLikeness(df, codeJudgeTag, codeSubjectTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag):
    countTag = utilities.getTagName("countTag")
    finishedProcesses = df[df[finishedTag] == utilities.getProcessState('finished')]
    unfinishedProcesses = df[df[finishedTag] == utilities.getProcessState('unfinished')]  
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(durationFinalTag)
    predictions = {}
    with alive_bar(int(len(unfinishedProcesses))) as bar:
        for i in range(len(unfinishedProcesses)):
            u = unfinishedProcesses.iloc[i]
            judge = u[codeJudgeTag]
            subject = u[codeSubjectTag]
            section = u[sectionTag]
            f = finishedProcesses.copy()
            f = f[f[codeJudgeTag] == judge]
            f = f[f[codeSubjectTag] == subject]
            f = f[f[sectionTag] == section]
            lenFinished = len(f)
            processID = u[numProcessTag]
            currDuration = u[durationTag]
            if lenFinished > 0:
                trainX = f[columns]
                trainY = f[[durationFinalTag]]
                testX = u[columns]
                model  = DecisionTreeClassifier()
                model.fit(trainX.values, trainY)
                predictedDuration = model.predict([testX.values])[0]
                currDuration = testX[durationTag]
                predictedFinalDuration = currDuration + predictedDuration 
                predictions.update({str(processID): {durationTag: str(currDuration), durationPredictedTag: str(predictedFinalDuration)}})
            bar()
    return predictions

