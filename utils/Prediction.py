import datetime as dt
import pandas as pd
from sklearn import linear_model

import utils.utilities.Utilities as utilities

def predictDuration(finishedProcesses, process):
    df = pd.DataFrame(finishedProcesses, columns = ['numProcesso', 'durata', 'dataInizioProcesso', 'giudice', 'materia', 'sezione'])
    df['dataInizioProcesso'] = df['dataInizioProcesso'].map(dt.datetime.toordinal)
    df['giudice'] = df['giudice'].apply(lambda x: utilities.fromAlphanumericStringToInt(x))
    print(df)
    exit()
    X = vector_data[['dataInizioProcesso', 'giudice', 'materia', 'sezione']]
    y = vector_data[['durata']]
    regr = linear_model.LinearRegression()
    regr.fit(X, y)
    predictedDuration = regr.predict([[process[0], process[1], process[2], process[3]]])
    print(predictedDuration)
    exit()