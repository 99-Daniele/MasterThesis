import datetime as dt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import utils.utilities.Utilities as utilities

# return how much finished process is like to unfinished one and duration of the finished process.
def getLikeness(process1, process2):
    likeness = 0
    l1 = len(process1[1])
    l2 = len(process2[1])
    maxPos = 0
    if l1 >= l2:
        return [0, 0, 0, 0]
    for i in range(l1):
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
                if process1[1][i][0] == process2[1][j][0]:
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
    return [likeness * 100, process2[1][maxPos][1], process2[0], process2[2]]

def predictDuration(model, process):
    exit()
    processTranslated = process.copy()
    df = pd.DataFrame(finishedProcesses, columns = ['numProcesso', 'durata', 'dataInizioProcesso', 'giudice', 'materia', 'sezione'])
    df['dataInizioProcesso'] = df['dataInizioProcesso'].apply(lambda x: utilities.distanceAtToday(x.to_pydatetime()))
    df['giudice'] = df['giudice'].apply(lambda x: utilities.fromAlphanumericStringToInt(x, 'cache/translation/judgeTranslation.json'))
    df['materia'] = df['materia'].apply(lambda x: utilities.fromAlphanumericStringToInt(x, 'cache/translation/subjectTranslation.json'))
    df['sezione'] = df['sezione'].apply(lambda x: utilities.fromAlphanumericStringToInt(x, 'cache/translation/sectionTranslation.json'))
    X = df[['dataInizioProcesso', 'giudice', 'materia', 'sezione']]
    y = df[['durata']]
    processTranslated[1] = utilities.distanceAtToday(processTranslated[1])
    processTranslated[2] = utilities.fromAlphanumericStringToInt(processTranslated[2], 'cache/translation/judgeTranslation.json')
    processTranslated[3] = utilities.fromAlphanumericStringToInt(processTranslated[3], 'cache/translation/subjectTranslation.json')
    processTranslated[4] = utilities.fromAlphanumericStringToInt(processTranslated[4], 'cache/translation/sectionTranslation.json')
    model  = DecisionTreeClassifier()
    model.fit(X, y)
    predictedDuration = model.predict([[processTranslated[1], processTranslated[2], processTranslated[3], processTranslated[4]]])
    print(predictedDuration)
    exit()

def trainModel(finishedProcesses, numProcessTag, durationTag, dateTag, codeJudgeTag, subjectTag, sectionTag):
    df = pd.DataFrame(finishedProcesses, columns = [numProcessTag, durationTag, dateTag, codeJudgeTag, subjectTag, sectionTag])
    encJudges = LabelEncoder()
    encSubjects = LabelEncoder()
    encSections = LabelEncoder()
    df[dateTag] = df[dateTag].apply(lambda x: utilities.distanceAtToday(x.to_pydatetime()))
    encJudges.fit(df[codeJudgeTag].values)
    encSubjects.fit(df[subjectTag].values)
    encSections.fit(df[sectionTag].values)
    df[codeJudgeTag] = df[codeJudgeTag].apply(lambda x: encJudges.transform([x])[0])
    df[subjectTag] = df[subjectTag].apply(lambda x: encSubjects.transform([x])[0])
    df[sectionTag] = df[sectionTag].apply(lambda x: encSections.transform([x])[0])
    x = df[[dateTag, codeJudgeTag, subjectTag, sectionTag]]
    y = df[[durationTag]]
    #xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 0.2)
    model  = DecisionTreeClassifier()
    model.fit(x, y)
    predictions = model.predict(xTest)
    score = accuracy_score(yTest, predictions)
    print(score)
    exit()

# return how much finished process is like to unfinished one and duration of the finished process.
def getLikeness(unfinished, finished):
    likeness = 0
    l1 = len(unfinished[1])
    l2 = len(finished[1])
    maxPos = 0
    if l1 >= l2:
        return [0, 0, 0]
    for i in range(l1):
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
    return [likeness * 100, finished[1][maxPos][1], finished[0]]

# return  how much finished process is like to unfinished one and predicted duration.
def getLikenessSequence(unfinished, finished):
    [like, duration, totDuration] = getLikeness(unfinished, finished)
    if like == 0:
        return [0, 0]
    if duration == 0:
        predicted = unfinished[0]
    else:
        predicted = unfinished[0] + ((totDuration - duration) * unfinished[0] / duration)
    return [like, predicted]

def getLikenessDate(date1, date2, maxDuration):
    return (1 - (abs((date2 - date1).days) / maxDuration)) * 100

def getLikenessType(type1, type2):
    if type1 == type2:
        return 100
    else:
        return 0
    
def getLikenessDuration(unfinished, finished, maxDuration):
    likeDate = getLikenessDate(unfinished[3], finished[2], maxDuration)
    likeSubject = getLikenessType(unfinished[5], finished[4])
    likeSection = getLikenessType(unfinished[6], finished[5])
    [likeSequence, predicted] = getLikenessSequence(unfinished, finished[6])
    if likeSequence <= 90:
        return [0, 0]
    totLike = (likeSequence + likeDate + likeSubject * 0.6 + likeSection * 0.4) / 3
    return [totLike, predicted]

# return best prediction of unfinished process.
def getPrediction(unfinished, finished, maxDuration):
    prediction = 0
    tot = 0
    for f in finished:
        [like, predicted] = getLikenessDuration(unfinished, f, maxDuration)
        if like > 0:
            prediction = prediction * tot
            prediction += like * predicted
            tot += like
            prediction = prediction / tot
    if tot > 0:
        return prediction
    else:
        return None

def trainModel(finishedProcessesInfo, minDate, maxDate):
    maxDuration = (maxDate - minDate).days
    accuracy = 100
    minAccuracy = 100
    maxTarget = 1
    chosenK = 0
    finished = False
    k = 0
    while not finished:
        errors = []
        count = 0
        with alive_bar(int(len(finishedProcessesInfo))) as bar:
            for i in range(len(finishedProcessesInfo)):
                p = finishedProcessesInfo[i]
                exactDuration = p[1]
                date = p[2]
                judge = p[3]
                subject = p[4]
                section = p[5]
                sequence = p[6][1]
                sequenceUnion = p[6][2]
                if len(sequence) > k + 2:
                    count += 1
                    newDuration = sequence[j + k][1]
                    newSequence = sequence[:j + k]
                    newSequenceUnion = sequenceUnion[:j + k]
                    newSequenceInfo = [newDuration, newSequence, newSequenceUnion, date, judge, subject, section]
                    prediction = getPrediction(newSequenceInfo, finishedProcessesInfo[:i] + finishedProcessesInfo[i + 1:], maxDuration)
                    if prediction != None:
                        error = abs(prediction - exactDuration) * 100 / exactDuration
                        if error <= 20:
                            errors.append(error)
                        else:
                            break
                    else:
                        break
                bar()
        if len(errors) >= count / 10 and count > 0:
            accuracy = sum(errors) / len(errors)
        else:
            accuracy = 100
        if count == 0:
            finished = True
        if len(errors) / accuracy < maxTarget / minAccuracy:
            minAccuracy = accuracy
            maxTarget = len(errors)
            minK = k
        print(accuracy, len(errors), count, k) 
        k += 1
    print(minAccuracy, minK)
    exit()
    return None

# return predicted duration of unfinished process based on states, phases and events sequences.
def getPredictedDuration(unfinishedProcessInfo, originalSequenceDict, translatedSequenceDict, shortSequenceDict, phaseSequenceDict, eventSequenceDict):
    [processId, firstEventDate, firstEventId, originalSequence, translatedSequence, shortSequence, phaseSequence, eventSequence] = unfinishedProcessInfo
    eventSequenceDuration = getPrediction(eventSequence, eventSequenceDict)
    if eventSequenceDuration == None:
        originalSequenceDuration = getPrediction(originalSequence, originalSequenceDict)
        if originalSequenceDuration == None:
            translatedSequenceDuration = getPrediction(translatedSequence, translatedSequenceDict)
            if translatedSequenceDuration == None:
                shortSequenceDuration = getPrediction(shortSequence, shortSequenceDict)
                if shortSequenceDuration == None:
                    phaseSequenceDuration = getPrediction(phaseSequence, phaseSequenceDict)
                    if phaseSequenceDuration == None:
                        return []
                    else:
                        predictedDuration =  phaseSequenceDuration
                else:
                    predictedDuration = shortSequenceDuration
            else:
                predictedDuration = translatedSequenceDuration
        else:
            predictedDuration = originalSequenceDuration
    else:
        predictedDuration = eventSequenceDuration
    return [(processId, predictedDuration, firstEventDate, None, firstEventId, None)]
