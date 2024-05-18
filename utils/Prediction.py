import datetime as dt
import pandas as pd
from sklearn import linear_model
from sklearn.preprocessing import StandardScaler

import utils.utilities.Utilities as utilities

def predictDuration(finishedProcesses, process):
    processTranslated = process.copy()
    df = pd.DataFrame(finishedProcesses, columns = ['numProcesso', 'durata', 'dataInizioProcesso', 'giudice', 'materia', 'sezione'])
    df['dataInizioProcesso'] = df['dataInizioProcesso'].apply(lambda x: utilities.distanceAtToday(x.to_pydatetime()))
    df['giudice'] = df['giudice'].apply(lambda x: utilities.fromAlphanumericStringToInt(x, 'cache/translation/judgeTranslation.json'))
    df['materia'] = df['materia'].apply(lambda x: utilities.fromAlphanumericStringToInt(x, 'cache/translation/subjectTranslation.json'))
    df['sezione'] = df['sezione'].apply(lambda x: utilities.fromAlphanumericStringToInt(x, 'cache/translation/sectionTranslation.json'))
    x = df[['dataInizioProcesso', 'giudice', 'materia', 'sezione']]
    y = df[['durata']]
    processTranslated[1] = utilities.distanceAtToday(processTranslated[1])
    processTranslated[2] = utilities.fromAlphanumericStringToInt(processTranslated[2], 'cache/translation/judgeTranslation.json')
    processTranslated[3] = utilities.fromAlphanumericStringToInt(processTranslated[3], 'cache/translation/subjectTranslation.json')
    processTranslated[4] = utilities.fromAlphanumericStringToInt(processTranslated[4], 'cache/translation/sectionTranslation.json')
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    predictedDuration = regr.predict([[processTranslated[1], processTranslated[2], processTranslated[3], processTranslated[4]]])
    print(predictedDuration)
    exit()