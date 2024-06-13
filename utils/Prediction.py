from alive_progress import alive_bar
import pandas as pd
import random as rd
from sklearn.tree import DecisionTreeClassifier

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.utilities.Utilities as utilities

# predict duration of finished processes based on current events flow. This evaluate the error of the model.
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
    with alive_bar(int(len(numProcesses) / 20)) as bar:
        for i in range(int(len(numProcesses) / 20)):
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
    predictions = sorted(predictions, key = lambda x: x['errore'])
    file.writeOnJsonFile('cache/predictions.json', predictions)
    #plt.scatter(testY, predictedDurations)
    #plt.xlabel('Actual Petal Width')
    #plt.ylabel('Predicted Petal Width')
    #plt.title('Actual vs Predicted Petal Width')
    #plt.show()
    return meanError, medianError

# predict duration of finished processes based on current events flow.
def predictDurationsWithoutLikeness(df, codeJudgeTag, codeSubjectTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag):
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
