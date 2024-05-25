# this file contains various utilities.

import datetime as dt
import pandas as pd
from win32api import GetSystemMetrics

import utils.FileOperation as file

# from given dataframe return a list of colors based on events phases.
def phaseColorList(df, type):
    types = df[type].unique().tolist()
    c = []
    colors = file.getDataFromJsonFile('utils/utilities/phaseColors.json')
    dateTag = getTagName("dateTag")
    phaseTag = getTagName("phaseTag")
    for t in types:
        df_count = df[df[type] == t].groupby([phaseTag], as_index = False).count()
        max = df_count[dateTag].max()
        phase = df_count[df_count[dateTag] == max][phaseTag].tolist()[0]
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

# return trimester number based on given month.
def getTrimesterNumber(month):
    if month <= 3:
        return 1
    elif month <= 6:
        return 2
    elif month <= 9:
        return 3
    else:
        return 4

# return trimester date based on given date.
def getTrimesterDate(date):
    month = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S').month
    return getTrimesterNumber(month)

# return datetime of 1st of the trimester with month and year of given date.
def getTrimesterYearDate(date):
    datetime = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    m = datetime.month
    month = (getTrimesterNumber(m) - 1) * 3 + 1
    year = datetime.year
    new_date = pd.Timestamp(day = 1, month = month, year = year)
    return new_date

# return year datetime from given date. 
def getYearNumber(date):
    new_date = dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return new_date.year

# get given week from weeks.
def getWeek(weekNumber):
    weeks = file.getDataFromJsonFile('utils/utilities/weeks.json')
    return weeks[weekNumber - 1]

# get given month from months.
def getMonth(monthNumber):
    months = file.getDataFromJsonFile('utils/utilities/months.json')
    return months[monthNumber - 1]

# get given month from months and given year.
def getMonthYear(date):
    m = date.month
    month = getMonth(m)
    y = date.year
    return month + " " + str(y)

# get given trimester from trimesters.
def getTrimester(trimesterNumber):
    trimesters = file.getDataFromJsonFile('utils/utilities/trimesters.json')
    return trimesters[trimesterNumber - 1]

# get given trimester from trimesters and given year.
def getTrimesterYear(date):
    m = date.month
    t = getTrimesterNumber(m)
    trimester = getTrimester(t)
    y = date.year
    return trimester + " " + str(y)

# get given process state from processStates text file.
def getProcessState(state):
    processState = list(file.getDataFromTextFile('utils/utilities/processStates.txt'))
    return processState[state]

# get all process states from processStates text file.
def getAllProcessState():
    processState = file.getDataFromTextFile('utils/utilities/processStates.txt')
    return processState

# transform list into string by "," join.
def fromListToString(list):
    string = ",".join(str(l) for l in list)
    return string

# transform string into list by "," split.
def fromStringToList(string):
    list = string.split(",")
    return list

# find substring between from given string two characters.
def findSubstringBetweenChars(string, startChar, endChar):
    startIndex = string.find(startChar)
    endIndex = string.find(endChar)
    return string[startIndex + 1: endIndex]

# get width based on screen dimension
def getWidth(perc):
    width = GetSystemMetrics(0)
    return width * perc

# get height based on screen dimension
def getHeight(perc):
    height = GetSystemMetrics(1)
    return height * perc

# return date distance to current day.
def distanceAtToday(date):
    todayDate = dt.datetime.today().strftime('%d-%m-%Y')
    todayDate = dt.datetime.strptime(todayDate, '%d-%m-%Y')
    return abs((date - todayDate).days)

# translate alphanumeric string to integer.
def fromAlphanumericStringToInt(string, filename):
    translation = file.getDataFromJsonFile(filename)
    if translation == {}:
        translation = {string: 1}
        file.writeOnJsonFile(filename, translation)
        return 1
    else:
        number = translation.get(string)
        if number == None:
            last = sorted(translation.values())[-1]
            translation.update({string: last + 1})
            file.writeOnJsonFile(filename, translation)
            return last + 1
        else:
            return number

# get tagName from tag.
def getTagName(tag):
    tags = file.getDataFromJsonFile('utils/utilities/tags.json')
    tagName = tags.get(tag)
    return tagName

# get placeholderName from placeholder.
def getPlaceholderName(placeholder):
    placeholders = file.getDataFromJsonFile('utils/utilities/placeholder.json')
    placeholderName = placeholders.get(placeholder)
    return placeholderName
