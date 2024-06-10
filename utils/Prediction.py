from alive_progress import alive_bar
import matplotlib.pyplot as plt
import numpy
import pandas as pd
import random
from sklearn.tree import DecisionTreeClassifier

import utils.Dataframe as frame
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

def predictDurationsWithoutLikenessTest(df, codeJudgeTag, codeSubjectTag, countTag, durationFinalTag, finishedTag, numProcessTag, sectionTag):
    count = 0
    maxL = len(df)
    bestCount = 0
    bestL = 0
    bestMeanErr = 0
    bestMedianErr = 0
    bestCoeff = 0
    while True:
        df_temp = df[df[countTag] > count].copy()
        length = len(df_temp)
        if length < int(maxL / 3):
            break
        columns = df_temp.columns.values.tolist()
        columns.remove(codeJudgeTag)
        columns.remove(codeSubjectTag)
        columns.remove(sectionTag)
        columns.remove(numProcessTag)
        columns.remove(finishedTag)
        columns.remove(durationFinalTag)
        numProcesses = frame.getUniques(df_temp, numProcessTag).tolist()
        random.shuffle(numProcesses)
        l = len(numProcesses)
        lStart = 0
        lEnd = int(l / 4)
        testNumProcesses = numProcesses[lStart:lEnd]
        trainNumProcesses = list(set(numProcesses) - set(testNumProcesses))
        trainDF = df_temp[df_temp[numProcessTag].isin(trainNumProcesses)]
        testDF = df_temp[df_temp[numProcessTag].isin(testNumProcesses)]
        testDF = testDF.groupby(numProcessTag).apply(lambda x: x.sample(1)).reset_index(drop = True)
        errors = []
        with alive_bar(int(len(testDF))) as bar:
            for i in range(len(testDF)):
                testDF_temp = testDF.iloc[i]
                judge = testDF_temp[codeJudgeTag]
                subject = testDF_temp[codeSubjectTag]
                section = testDF_temp[sectionTag]
                trainDF_temp = trainDF.copy()
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
                    predictedDuration = model.predict([testX.values])
                    duration = testY[durationFinalTag]
                    if duration > 0:
                        error = abs(predictedDuration - duration) / duration
                        errors.extend([error])
                bar()
        errors = sorted(errors)
        m = int(len(errors) / 2)
        if len(errors) % 2 != 0:
            medianError = errors[m]
        else:
            medianError = (errors[m - 1] + errors[m]) / 2.0
        meanError = sum(errors) / len(errors)
        if meanError > 0:
            newCoeff = len(errors) / meanError
            if newCoeff > bestCoeff:
                bestCoeff = newCoeff
                bestMeanErr = meanError
                bestMedianErr = medianError
                bestCount = count
                bestL = len(errors)
        print(count, len(errors), meanError, medianError)
        count += 1
    print(bestCount, bestL, bestMeanErr, bestMedianErr)
    exit()
    #plt.scatter(testY, predictedDurations)
    #plt.xlabel('Actual Petal Width')
    #plt.ylabel('Predicted Petal Width')
    #plt.title('Actual vs Predicted Petal Width')
    #plt.show()
    return avgError

def predictDurationsWithoutLikeness(df, codeJudgeTag, codeSubjectTag, durationTag, durationFinalTag, finishedTag, numProcessTag, sectionTag):
    finishedProcesses = df[df[finishedTag] == utilities.getProcessState('finished')]
    unfinishedProcesses = df[df[finishedTag] == utilities.getProcessState('unfinished')]
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(durationFinalTag)
    trainX = finishedProcesses[columns]
    trainY = finishedProcesses[[durationFinalTag]]
    predictX = unfinishedProcesses[columns]
    predictY = unfinishedProcesses[[numProcessTag, durationTag]]
    model = DecisionTreeClassifier()
    model.fit(trainX.values, trainY)
    predictedDurations = model.predict(predictX.values).tolist()
    predictY[durationFinalTag] = predictedDurations
    print(predictY)
    exit()
    processesDurations = predictY.set_index(numProcessTag).to_dict("index")
    return processesDurations

