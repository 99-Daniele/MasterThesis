# this file handles prediction test and calculation.

from alive_progress import alive_bar
import pandas as pd
import random as rd
from sklearn.tree import DecisionTreeRegressor

import utils.Dataframe as frame
import utils.Utilities as utilities

# predict duration of finished processes based on current events flow. This evaluate the error of the model.
# this test is performed on 20% of dataframe with a model based on other 80% of dataframe.
# it's faster than predictDurationsTestTotal() test.
def predictDurationsTest8020(df, codeJudgeTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, errorTag, finishedTag, numProcessTag, sectionTag):
    # columns are the columns of the dataframe to which model is created.
    # numProcess, process type, judge, dubject, section and date are not included in prediction model.
    # final duration is excluded because is the value to predict.
    columns = df.columns.values.tolist()
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(dateTag)
    columns.remove(durationFinalTag)
    # get list of all process Ids, shuffle them and take the first 1/5 of them.
    numProcesses = frame.getUniques(df, numProcessTag).tolist()
    rd.shuffle(numProcesses)
    lTrain = int(len(numProcesses) / 5)
    trainNumProcesses = numProcesses[lTrain:]
    testNumProcesses = list(set(numProcesses) - set(trainNumProcesses))
    predictions = []
    # train dataframe is created from train process Ids.
    trainDf = df[df[numProcessTag].isin(trainNumProcesses)].copy()
    # for each testProcessId referring to one process, prediction is performed.
    with alive_bar(int(len(testNumProcesses))) as bar:
        for i in range(int(len(testNumProcesses))):             
            # testDF is the dataframe of all processes containing current processId.   
            testDF = df[df[numProcessTag] == testNumProcesses[i]].copy()
            lTest = len(testDF)
            r = rd.randint(0, lTest - 2)
            # take one of dataframe rows excluding last one which is the terminal event.
            testDF_temp = testDF.iloc[r]
            # judge is the judge of the process, subject the subject of the process, section the sectoin of the process,
            # processID is process ID, count refers to the count of event that process snapshot contains (it's an incremental value),
            # currDuration is process current duration from start process, date is date of current process snapshot.
            judge = testDF_temp[codeJudgeTag]
            subject = testDF_temp[codeSubjectTag]
            section = testDF_temp[sectionTag]
            processID = testDF_temp[numProcessTag]
            count = testDF_temp[countTag]
            currDuration = testDF_temp[durationTag]
            date = testDF_temp[dateTag]
            # trainDF_temp is trainDf filtered to only processes which have same section, judge and subject of test process.
            # in case there isn't any process with same value, the related filter is not applied.
            trainDF_temp = trainDf.copy()
            if len(trainDF_temp[trainDF_temp[sectionTag] == section]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[sectionTag] == section]
            if len(trainDF_temp[trainDF_temp[codeJudgeTag] == judge]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeJudgeTag] == judge]
            if len(trainDF_temp[trainDF_temp[codeSubjectTag] == subject]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeSubjectTag] == subject]
            lenTrainTemp = len(trainDF_temp)
            if lenTrainTemp > 0:
                # trainX and trainY create regression model.
                # trainX refers to processes snapshot values, trainY to related real final process duration.
                trainX = trainDF_temp[columns]
                trainY = trainDF_temp[[durationFinalTag]]
                # testX and testY predict final process duration.
                # testX refers to process snapshot values, testY to real final process duration.
                testX = testDF_temp[columns]
                testY = testDF_temp[[durationFinalTag]]
                # finalDuration is the real duration of process.
                # since testY[durationFinalTag] contains the remaining days to end of process, the final duration is the sum of this value and current duration.
                finalDuration = currDuration + testY[durationFinalTag]
                # model is created with trainX and trainY values.
                model  = DecisionTreeRegressor()
                model.fit(trainX.values, trainY.values)
                # final predicted duration is the predicted duration of process.
                # since predicted duration predicts the reamaning days to end of process, the predicted final duration is the sum of this value and current duration.
                predictedDuration = model.predict([testX.values])[0]
                predictedFinalDuration = currDuration + predictedDuration 
                # calculates error and add to predictions list with other process info.
                # if finalDuration is 0, is not added bacause error will be infinite.
                if finalDuration > 0:
                    error = abs(predictedFinalDuration - finalDuration) * 100 / finalDuration
                    predictions.extend([{numProcessTag: str(processID), dateTag: date, countTag: str(count), durationTag: str(currDuration), durationFinalTag: str(finalDuration), durationPredictedTag: str(predictedFinalDuration), errorTag: error}])
            bar() 
    # predictionDf is the dataframe created from predictions.
    predictionDf = pd.DataFrame(predictions)
    return predictionDf

# predict duration of finished processes based on current events flow. This evaluate the error of the model.
# this test is performed on 100% of dataframe with a model created still with 100% of dataframe.
def predictDurationsTestTotal(df, codeJudgeTag, codeSubjectTag, countTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, errorTag, finishedTag, numProcessTag, sectionTag):
    # columns are the columns of the dataframe to which model is created.
    # numProcess, process type, judge, dubject, section and date are not included in prediction model.
    # final duration is excluded because is the value to predict.
    columns = df.columns.values.tolist()
    columns.remove(codeJudgeTag)
    columns.remove(codeSubjectTag)
    columns.remove(sectionTag)
    columns.remove(numProcessTag)
    columns.remove(finishedTag)
    columns.remove(durationFinalTag)
    columns.remove(dateTag)
    # get list of all process Ids and shuffle them.
    numProcesses = frame.getUniques(df, numProcessTag).tolist()
    rd.shuffle(numProcesses)
    predictions = []
    # for each processId referring to one process, prediction is performed.
    with alive_bar(int(len(numProcesses))) as bar:
        for i in range(int(len(numProcesses))):
            # testNumProcesses is the current processID, trainNumProcesses are the others.
            testNumProcesses = numProcesses[i]
            trainNumProcesses = numProcesses[:i] + numProcesses[i + 1:]
            # testDF is the dataframe of all processes containing current processId.  
            testDF = df[df[numProcessTag] == testNumProcesses].copy()
            lTest = len(testDF)
            r = rd.randint(0, lTest - 2)
            # take one of dataframe rows excluding last one which is the terminal event.
            testDF_temp = testDF.iloc[r]
            # judge is the judge of the process, subject the subject of the process, section the sectoin of the process,
            # processID is process ID, count refers to the count of event that process snapshot contains (it's an incremental value),
            # currDuration is process current duration from start process, date is date of current process snapshot.
            judge = testDF_temp[codeJudgeTag]
            subject = testDF_temp[codeSubjectTag]
            section = testDF_temp[sectionTag]
            processID = testDF_temp[numProcessTag]
            count = testDF_temp[countTag]
            currDuration = testDF_temp[durationTag]
            date = testDF_temp[dateTag]
            # trainDF_temp is the dataframe of all  others processes. 
            # trainDF_temp is trainDF filtered to only processes which have same section, judge and subject of test process.
            # in case there isn't any process with same value, the related filter is not applied.
            trainDF_temp = df[df[numProcessTag].isin(trainNumProcesses)].copy()
            if len(trainDF_temp[trainDF_temp[sectionTag] == section]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[sectionTag] == section]
            if len(trainDF_temp[trainDF_temp[codeJudgeTag] == judge]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeJudgeTag] == judge]
            if len(trainDF_temp[trainDF_temp[codeSubjectTag] == subject]) > 0:
                trainDF_temp = trainDF_temp[trainDF_temp[codeSubjectTag] == subject]
            lenTrainTemp = len(trainDF_temp)
            if lenTrainTemp > 0:
                # trainX and trainY create regression model.
                # trainX refers to processes snapshot values, trainY to related real final process duration.
                trainX = trainDF_temp[columns]
                trainY = trainDF_temp[[durationFinalTag]]
                # testX and testY predict final process duration.
                # testX refers to process snapshot values, testY to real final process duration.
                testX = testDF_temp[columns]
                testY = testDF_temp[[durationFinalTag]]
                # finalDuration is the real duration of process.
                # since testY[durationFinalTag] contains the remaining days to end of process, the final duration is the sum of this value and current duration.
                finalDuration = currDuration + testY[durationFinalTag]
                # model is created with trainX and trainY values.
                model  = DecisionTreeRegressor()
                model.fit(trainX.values, trainY)
                # final predicted duration is the predicted duration of process.
                # since predicted duration predicts the reamaning days to end of process, the predicted final duration is the sum of this value and current duration.
                predictedDuration = model.predict([testX.values])[0]
                predictedFinalDuration = currDuration + predictedDuration 
                # calculates error and add to predictions list with other process info.
                # if finalDuration is 0, is not added bacause error will be infinite.
                if finalDuration > 0:
                    error = abs(predictedFinalDuration - finalDuration) * 100 / finalDuration
                    predictions.extend([{numProcessTag: str(processID), dateTag: date, countTag: str(count), durationTag: str(currDuration), durationFinalTag: str(finalDuration), durationPredictedTag: str(predictedFinalDuration), errorTag: error}])
            bar() 
    # predictionDf is the dataframe created from predictions.
    predictionDf = pd.DataFrame(predictions)
    return predictionDf

# predict duration of finished processes based on current events flow.
def predictDurations(df, codeJudgeTag, codeSubjectTag, dateTag, durationTag, durationFinalTag, durationPredictedTag, finishedTag, numProcessTag, sectionTag):
    # separates finished processes from unfinished ones.
    finishedProcesses = df[df[finishedTag] == utilities.getProcessState('finished')]
    unfinishedProcesses = df[df[finishedTag] == utilities.getProcessState('unfinished')] 
    # columns are the columns of the dataframe to which model is created.
    # numProcess, process type, judge, dubject, section and date are not included in prediction model.
    # final duration is excluded because is the value to predict. 
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
            # u is the i-th unfinished process.
            u = unfinishedProcesses.iloc[i]
            judge = u[codeJudgeTag]
            subject = u[codeSubjectTag]
            section = u[sectionTag]
            processID = u[numProcessTag]
            currDuration = u[durationTag]
            # f filter finishedProcess to only processes which have same section, judge and subject of current unfinished process.
            # in case there isn't any process with same value, the related filter is not applied.
            f = finishedProcesses.copy()
            if len(f[f[sectionTag] == section]) > 0:
                f = f[f[sectionTag] == section]
            if len(f[f[codeJudgeTag] == judge]) > 0:
                f = f[f[codeJudgeTag] == judge]
            if len(f[f[codeSubjectTag] == subject]) > 0:
                f = f[f[codeSubjectTag] == subject]
            lenFinished = len(f)
            if lenFinished > 0:
                # trainX and trainY create regression model.
                # trainX refers to processes snapshot values, trainY to related real final process duration.
                trainX = f[columns]
                trainY = f[[durationFinalTag]]
                # testX predict final process duration.
                # testX refers to process snapshot values.
                testX = u[columns]
                # model is created with trainX and trainY values.
                model  = DecisionTreeRegressor()
                model.fit(trainX.values, trainY.values)
                # final predicted duration is the predicted duration of process.
                predictedDuration = model.predict([testX.values])[0]
                predictedFinalDuration = currDuration + predictedDuration 
                # add predicted duration to predictions.
                predictions.update({str(processID): {durationTag: str(currDuration), durationPredictedTag: str(predictedFinalDuration)}})
            bar()
    # predictions is a dictornay with process IDs as keys, and current duration and predicted duration as values.
    return predictions
