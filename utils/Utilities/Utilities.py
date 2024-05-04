# this file contains various utilities.

import datetime as dt
import pandas as pd

import utils.FileOperation as file

# weeks, months, trimesters, daysOfWeek are lists of visualization of week, month, trimester and day of week.
weeks = ['02/01', '08/01', '15/01', '22/01', '29/01', '05/02', '12/02', '19/02', '26/02', '05/03', '12/03', '19/03', '26/03', '02/04', '09/04', '16/04', '23/04', '30/04', '07/05', '14/05', '21/05', '28/05', '04/06', '11/06', '18/06', '25/06', '02/07', '09/07', '16/07', '23/07', '30/07', '06/08', '13/08', '20/08', '27/08', '03/09', '10/09', '17/09', '24/09', '01/10', '08/10', '15/10', '22/10', '29/10', '05/11', '12/11', '19/11', '26/11', '03/12', '10/12', '17/12', '24/12', '31/12']
months = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
trimesters = ['Gen-Mar', 'Apr-Giu', 'Lug-Set', 'Ott-Dic']
daysOfWeek = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

# from given dataframe return a list of colors based on events phases.
def phaseColorList(df, type):
    types = df[type].unique().tolist()
    c = []
    colors = file.getDataFromJsonFile('utils/Utilities/phaseColors.json')
    for t in types:
        df_count = df[df[type] == t].groupby(['fase'], as_index = False).count()
        max = df_count['data'].max()
        phase = df_count[df_count['data'] == max]['fase'].tolist()[0]
        c.append(colors.get(str(phase)))
    return c

# return week datetime from given date. 
def getWeekNumber(date):
    datetime = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    new_date = pd.Timestamp(day = datetime.day, month = datetime.month, year = 2024)
    return new_date.week

# return month datetime from given date. 
def getMonthNumber(date):
    new_date = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return new_date.month

# return datetime of 1st of the month with month and year of given date.
def getMonthYearDate(date):
    datetime = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    m = datetime.month
    y = datetime.year
    new_date = pd.Timestamp(day = 1, month = m, year = y)
    return new_date

# return trimester based on given date.
def getTrimesterNumber(date):
    month = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').month
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4

# return datetime of 1st of the trimester with month and year of given date.
def getTrimesterYearDate(date):
    datetime = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    if datetime.month <= 3:
        m = 1
    elif datetime.month <= 6:
        m = 4
    elif datetime.month <= 9:
        m = 7
    else:
        m = 10
    y = datetime.year
    new_date = pd.Timestamp(day = 1, month = m, year = y)
    return new_date

# return year datetime from given date. 
def getYearNumber(date):
    new_date = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return new_date.year

# get given week from weeks.
def getWeek(weekNumber):
    return weeks[weekNumber - 1]

# get given month from months.
def getMonth(monthNumber):
    return months[monthNumber - 1]

# get given trimester from trimesters.
def getTrimester(trimesterNumber):
    return trimesters[trimesterNumber - 1]

# get given day of week from daysOfWeek.
def getDayOfWeek(dowNumber):
    return daysOfWeek[dowNumber - 1]

# get given process state from processStates text file.
def getProcessState(state):
    processState = file.getDataFromTextFile('utils/Utilities/processStates.txt')
    return processState[state]

# get all process states from processStates text file.
def getAllProcessState():
    processState = file.getDataFromTextFile('utils/Utilities/processStates.txt')
    return processState

# transform list into string by "," join.
def fromListToString(list):
    string = ",".join(str(l) for l in list)
    return string

# transform string into list by "," split.
def fromStringToList(string):
    list = string.split(",")
    return list
