import datetime as dt
import gym
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

def trainModel(finishedProcesses, numProcessTag, durationTag, dateTag, judgeTag, subjectTag, sectionTag):
    df = pd.DataFrame(finishedProcesses, columns = [numProcessTag, durationTag, dateTag, judgeTag, subjectTag, sectionTag])
    encJudges = LabelEncoder()
    encSubjects = LabelEncoder()
    encSections = LabelEncoder()
    df[dateTag] = df[dateTag].apply(lambda x: utilities.distanceAtToday(x.to_pydatetime()))
    encJudges.fit(df[judgeTag].values)
    encSubjects.fit(df[subjectTag].values)
    encSections.fit(df[sectionTag].values)
    df[judgeTag] = df[judgeTag].apply(lambda x: encJudges.transform([x])[0])
    df[subjectTag] = df[subjectTag].apply(lambda x: encSubjects.transform([x])[0])
    df[sectionTag] = df[sectionTag].apply(lambda x: encSections.transform([x])[0])
    x = df[[dateTag, judgeTag, subjectTag, sectionTag]]
    y = df[[durationTag]]
    #xTrain, xTest, yTrain, yTest = train_test_split(x, y, test_size = 0.2)
    model  = DecisionTreeClassifier()
    model.fit(x, y)
    predictions = model.predict(xTest)
    score = accuracy_score(yTest, predictions)
    print(score)
    exit()
