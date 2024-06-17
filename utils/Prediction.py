# this file handles prediction test and calculation.

from alive_progress import alive_bar
import pandas as pd
import random as rd
from sklearn.tree import DecisionTreeClassifier

import utils.Dataframe as frame
import utils.Utilities as utilities

# predict duration of finished processes based on current events flow. This evaluate the error of the model.
def predictDurationsTest8020(df, codeJudgeTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, errorTag, finishedTag, numProcessTag, sectionTag):
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(durationFinalTag)
    columns.remove(dateTag)
    numProcesses = frame.getUniques(df, numProcessTag).tolist()
    rd.shuffle(numProcesses)
    lTrain = int(len(numProcesses) / 5)
    trainNumProcesses = numProcesses[lTrain:]
    testNumProcesses = list(set(numProcesses) - set(trainNumProcesses))
    predictions = []
    with alive_bar(int(len(testNumProcesses))) as bar:
        for i in range(int(len(testNumProcesses))):
            testDF = df[df[numProcessTag] == testNumProcesses[i]].copy()
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
            if len(trainDF_temp[trainDF_temp[sectionTag] == section]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[sectionTag] == section]
            if len(trainDF_temp[trainDF_temp[codeJudgeTag] == judge]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeJudgeTag] == judge]
            if len(trainDF_temp[trainDF_temp[codeSubjectTag] == subject]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeSubjectTag] == subject]
            lenTrainTemp = len(trainDF_temp)
            if lenTrainTemp > 0:
                trainX = trainDF_temp[columns]
                trainY = trainDF_temp[[durationFinalTag]]
                testX = testDF_temp[columns]
                testY = testDF_temp[[durationFinalTag]]
                currDuration = testX[durationTag]
                finalDuration = currDuration + testY[durationFinalTag]
                model = DecisionTreeClassifier()
                model.fit(trainX.values, trainY)
                predictedDuration = model.predict([testX.values])[0]
                predictedFinalDuration = currDuration + predictedDuration
                if finalDuration > 0:
                    error = abs(predictedFinalDuration - finalDuration) * 100 / finalDuration
                    predictions.extend([{numProcessTag: str(processID), countTag: str(count), durationTag: str(currDuration), durationFinalTag: str(finalDuration), durationPredictedTag: str(predictedFinalDuration), errorTag: error}])
            bar() 
    predictionDf = pd.DataFrame(predictions)
    return predictionDf

# predict duration of finished processes based on current events flow. This evaluate the error of the model.
def predictDurationsTestTotal(df, codeJudgeTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, errorTag, finishedTag, numProcessTag, sectionTag):
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(durationFinalTag)
    columns.remove(dateTag)
    numProcesses = frame.getUniques(df, numProcessTag).tolist()
    rd.shuffle(numProcesses)
    predictions = []
    with alive_bar(int(len(numProcesses))) as bar:
        for i in range(int(len(numProcesses))):
            testNumProcesses = numProcesses[i]
            trainNumProcesses = numProcesses[:i] + numProcesses[i + 1:]
            testDF = df[df[numProcessTag] == testNumProcesses].copy()
            lTest = len(testDF)
            r = rd.randint(0, lTest - 1)
            r = 4
            testDF_temp = testDF.iloc[r]
            judge = testDF_temp[codeJudgeTag]
            subject = testDF_temp[codeSubjectTag]
            section = testDF_temp[sectionTag]
            processID = testDF_temp[numProcessTag]
            count = testDF_temp[countTag]
            currDuration = testDF_temp[durationTag]
            trainDF_temp = df[df[numProcessTag].isin(trainNumProcesses)].copy()
            if len(trainDF_temp[trainDF_temp[sectionTag] == section]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[sectionTag] == section]
            if len(trainDF_temp[trainDF_temp[codeJudgeTag] == judge]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeJudgeTag] == judge]
            if len(trainDF_temp[trainDF_temp[codeSubjectTag] == subject]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeSubjectTag] == subject]
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
                    predictions.extend([{numProcessTag: str(processID), countTag: str(count), durationTag: str(currDuration), durationFinalTag: str(finalDuration), durationPredictedTag: str(predictedFinalDuration), errorTag: error}])
            bar() 
    predictionDf = pd.DataFrame(predictions)
    return predictionDf

# predict duration of finished processes based on current events flow.
def predictDurations(df, codeJudgeTag, codeSubjectTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag):
    finishedProcesses = df[df[finishedTag] == utilities.getProcessState('finished')]
    unfinishedProcesses = df[df[finishedTag] == utilities.getProcessState('unfinished')]  
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(dateTag)
    columns.remove(durationFinalTag)
    predictions = {}
    with alive_bar(int(len(unfinishedProcesses))) as bar:
        for i in range(len(unfinishedProcesses)):
            u = unfinishedProcesses.iloc[i]
            judge = u[codeJudgeTag]
            subject = u[codeSubjectTag]
            section = u[sectionTag]
            f = finishedProcesses.copy()
            if len(f[f[sectionTag] == section]) > 0:
                f = f[f[sectionTag] == section]
            if len(f[f[codeJudgeTag] == judge]) > 0:
                f = f[f[codeJudgeTag] == judge]
            if len(f[f[codeSubjectTag] == subject]) > 0:
                f = f[f[codeSubjectTag] == subject]
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
