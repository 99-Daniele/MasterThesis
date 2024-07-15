# this file handles comparison graph management.

import dash as ds
import plotly.express as px

import utils.Dataframe as frame
import utils.FileOperation as file
import utils.Getters as getter
import utils.Utilities as utilities

# hide page components if user select it.
# for each user choices set style of correlated component as not displayed and parameter of correlated componenets as None.
def hideChosen(choices, tags, styles, parameters):
    for i in range(len(tags)):
        if tags[i] in choices:
            styles[i] = {'display':'none'}
            parameters[i] = None
    return [styles, parameters]

# return the style of dropdown as hidden or not based on user choices: if user choices one, then corresponding dropdown will be hidden and his values will reset.
# this method is only for process comparison graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase):
    judgeStyle = {'width': 400}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    finishedStyle = {'width': 400}
    sequenceStyle = {'width': 400}
    phaseSequenceStyle = {'width': 400}
    eventStyle = {'width': 400}
    eventRadioStyle = {'display': 'contents'}
    stateStyle = {'width': 400}
    stateRadioStyle = {'display': 'contents'}
    phaseStyle = {'width': 400}
    phaseRadioStyle = {'display': 'contents'}
    finishedTag = utilities.getTagName('finishedTag')
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    phaseSequenceTag = utilities.getTagName('phaseSequenceTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    stateSequenceTag = utilities.getTagName('stateSequenceTag')
    [[sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle], [sections, subjects, judges, finished, sequences, phaseSequences]] = hideChosen(choices, [sectionTag, subjectTag, codeJudgeTag, finishedTag, stateSequenceTag, phaseSequenceTag], [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle], [sections, subjects, judges, finished, sequences, phaseSequences])
    if event == None:
        eventRadioStyle = {'display': 'none'}
    elif event in choices:
        eventStyle = {'display': 'none'}
        eventRadioStyle = {'display': 'none'}
        event = None
    if state == None:
        stateRadioStyle = {'display': 'none'}
    elif state in choices:
        stateStyle = {'display': 'none'}
        stateRadioStyle = {'display': 'none'}
        state = None
    if phase == None:
        phaseRadioStyle = {'display': 'none'}
    elif phase in choices:
        phaseStyle = {'display': 'none'}
        phaseRadioStyle = {'display': 'none'}
        phase = None
    return [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase]

# show all hidden object such as dropdown, radioitem, checklist.
def showAll():
    dateRangeStyle = {'display':'block'}
    resetStyle = {'display':'block'}
    dateCheckStyle = {'display': 'inline'}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    judgeStyle = {'width': 400}
    finishedStyle = {'width': 400}
    choiceCheckStyle = {'display': 'inline'}
    orderRadioStyle = {'display': 'block'}
    return [dateRangeStyle, resetStyle, dateCheckStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle]

# hide all shown object such as dropdown, radioitem, checklist.
def hideAll():
    dateRangeStyle = {'display':'none'}
    resetStyle = {'display':'none'}
    dateCheckStyle = {'display': 'none'}
    sectionStyle = {'display': 'none'}
    subjectStyle = {'display': 'none'}
    judgeStyle = {'display': 'none'}
    finishedStyle = {'width': 400}
    choiceCheckStyle = {'display': 'none'}
    orderRadioStyle = {'display': 'none'}
    return [dateRangeStyle, dateCheckStyle, resetStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle]

# return the style of dropdown as hidden or not based on user choices: if user choices one, then corresponding dropdown will be hidden and his values will reset.
# this method is only for parameter comparison graph since there are only 3 paramters: sections, judges and subjects.
def hideParameterChosen(choice):
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeSubjectTag = utilities.getTagName("codeSubjectTag")
    sectionTag = utilities.getTagName("sectionTag")
    judgeStyle = {'width': 400}
    sectionStyle = {'width': 400}
    subjectStyle = {'width': 400}
    if choice == codeJudgeTag:
        judgeStyle = {'display': 'none'}
    elif choice == sectionTag:
        sectionStyle = {'display': 'none'}
    elif choice == codeSubjectTag:
        subjectStyle = {'display': 'none'}
    return [sectionStyle, judgeStyle, subjectStyle]

# update data based on user choices on different parameters.
# this method is only for process comparison graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessData(df, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio, stateChoice, stateRadio, phaseChoice, phaseRadio):
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    dateTag = utilities.getTagName("dateTag")
    eventTag = utilities.getTagName("eventTag")
    finishedTag = utilities.getTagName("finishedTag")
    phaseTag = utilities.getTagName("phaseTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    subjectTag = utilities.getTagName("subjectTag")
    withOut = utilities.getPlaceholderName("without")
    # modify dataframe based on user chosen filters.
    newDF = df.copy()
    newDF = frame.getDateDataFrame(newDF, dateTag, startDate, endDate)
    newDF = frame.getTypesDataFrame(newDF, sectionTag, sections)
    newDF = frame.getTypesDataFrame(newDF, subjectTag, subjects)
    newDF = frame.getTypesDataFrame(newDF, codeJudgeTag, judges)
    newDF = frame.getTypesDataFrame(newDF, finishedTag, finished)
    newDF = frame.getTypesDataFrame(newDF, stateSequenceTag, sequences)
    newDF = frame.getTypesDataFrame(newDF, phaseSequenceTag, phaseSequences)
    if eventChoice != None:
        # eventTag == withOut + " " + eventChoice are processes where chosen event is not present.
        # The others are processes where event is present.
        newDF = frame.getEventDataFrame(newDF, eventChoice)
        if eventRadio == withOut:
            return newDF[newDF[eventTag] == withOut + " " + eventChoice]
        else:
            return newDF[newDF[eventTag] != withOut + " " + eventChoice]
    if stateChoice != None:
        # stateTag == withOut + " " + stateChoice are processes where chosen state is not present.
        # The others are processes where state is present.
        newDF = frame.getStateDataFrame(newDF, stateChoice)
        if stateRadio == withOut:
            return newDF[newDF[stateTag] == withOut + " " + stateChoice]
        else:
            return newDF[newDF[stateTag] != withOut + " " + stateChoice]
    if phaseChoice != None:
        # phaseTag == withOut + " " + phaseChoice are processes where chosen phase is not present.
        # The others are processes where phase is present.
        newDF = frame.getPhaseDataFrame(df, phaseChoice)
        if phaseRadio == withOut:
            return newDF[newDF[phaseTag] == withOut + " " + phaseTag + " " + phaseChoice]
        else:
            return newDF[newDF[phaseTag] != withOut + " " + phaseTag + " " + phaseChoice]
    return newDF

# update data based on user choices on different parameters.
def updateTypeData(df, startDate, endDate, sections, subjects, judges, finished):
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    dateTag = utilities.getTagName("dateTag")
    finishedTag = utilities.getTagName("finishedTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    # modify dataframe based on user chosen filters.
    newDF = df.copy()
    newDF = frame.getDateDataFrame(newDF, dateTag, startDate, endDate)
    newDF = frame.getTypesDataFrame(newDF, sectionTag, sections)
    newDF = frame.getTypesDataFrame(newDF, subjectTag, subjects)
    newDF = frame.getTypesDataFrame(newDF, codeJudgeTag, judges)
    newDF = frame.getTypesDataFrame(newDF, finishedTag, finished)
    return newDF

# update data based on user choices on different parameters.
# this method is only for process comparison by type graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessTypeData(df, sections, subjects, judges, months):
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    # modify dataframe based on user chosen filters.
    newDF = df.copy()
    newDF = frame.getTypesDataFrame(newDF, sectionTag, sections)
    newDF = frame.getTypesDataFrame(newDF, subjectTag, subjects)
    newDF = frame.getTypesDataFrame(newDF, codeJudgeTag, judges)
    newDF = frame.getMonthDataFrame(newDF, months)
    return newDF

# update types based on user choices on different parameters. In order to do that is used 'updateProcessData' method with chosen parameter as None. 
# this is done because when user select a parameter, analysed dataframe is filtered to only processes where chosen parameters holds.
# by doing that other chooseable parameters would disappear since they are calculated from input datafram which contains only processes with selected ones.
# so it calculates paramers like if no one was chosen and it set them in dropdown.
# this method is only for process comparison graph since there are more parameters such as 'sequences' and 'phaseSequences'.
def updateProcessDataframeFromSelection(newDF, df_data, eventsInfoDataframe, statesInfoDataframe, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio):
    codeEventTag = utilities.getTagName("codeEventTag")
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    codeStateTag = utilities.getTagName("codeStateTag")
    eventTag = utilities.getTagName("eventTag")
    eventSequenceTag = utilities.getTagName("eventSequenceTag")
    finishedTag = utilities.getTagName("finishedTag")
    phaseSequenceTag = utilities.getTagName("phaseSequenceTag")
    sectionTag = utilities.getTagName("sectionTag")
    stateTag = utilities.getTagName("stateTag")
    stateSequenceTag = utilities.getTagName("stateSequenceTag")
    subjectTag = utilities.getTagName("subjectTag")
    # for each parameter evaluate if is not None, which is when user makes a selection,
    # and in case modify to a new df using updateProcessData() with correlated parameter as None.
    if sections != None and len(sections) > 0:
        newDF_1 = updateProcessData(newDF, startDate, endDate, None, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        newDF_1 = df_data
    if subjects != None and len(subjects) > 0:
        newDF_2 = updateProcessData(newDF, startDate, endDate, sections, None, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        newDF_2 = df_data
    if judges != None and len(judges) > 0:
        newDF_3 = updateProcessData(newDF, startDate, endDate, sections, subjects, None, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        newDF_3 = df_data
    if finished != None and len(finished) > 0:
        newDF_4 = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, None, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        newDF_4 = df_data
    if sequences != None and len(sequences) > 0:
        newDF_5 = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, finished, None, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        newDF_5 = df_data
    if phaseSequences != None and len(phaseSequences) > 0:
        newDF_6 = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, finished, sequences, None, event, eventRadio, state, stateRadio, phase, phaseRadio)
    else:
        newDF_6 = df_data
    if event != None and len(event) > 0:
        newDF_7 = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, None, None, state, stateRadio, phase, phaseRadio)
    else:
        newDF_7 = df_data
    if state != None and len(state) > 0:
        newDF_8 = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, None, None, phase, phaseRadio)
    else:
        newDF_8 = df_data
    if phase != None and len(phase) > 0:
        newDF_9 = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, None, None)
    else:
        newDF_9 = df_data
    sections = frame.getGroupBy(newDF_1, sectionTag)
    subjects = frame.getGroupBy(newDF_2, subjectTag)
    judges = frame.getGroupBy(newDF_3, codeJudgeTag)
    finished = frame.getGroupBy(newDF_4, finishedTag)
    sequences = frame.getGroupBy(newDF_5, stateSequenceTag)
    phaseSequences = frame.getGroupBy(newDF_6, phaseSequenceTag)
    events = frame.getGroupByFromString(newDF_7, eventSequenceTag)
    importantCodeEvents = file.getDataFromTextFile('utils/preferences/importantEvents.txt')
    if importantCodeEvents != None and len(importantCodeEvents) > 0:
        eventsInfo = eventsInfoDataframe.to_dict('records')
        importantEvents = []
        for e in eventsInfo:
            eventCode = e[codeEventTag]
            eventEvent = e[eventTag]
            if eventCode in importantCodeEvents:
                importantEvents.append(eventEvent)
        events = list(set(importantEvents) & set(events))
    states = frame.getGroupByFromString(newDF_8, stateSequenceTag)
    importantCodeStates = file.getDataFromTextFile('utils/preferences/importantStates.txt')
    if importantCodeStates != None and len(importantCodeStates) > 0:
        statesInfo = statesInfoDataframe.to_dict('records')
        importantStates = []
        for s in statesInfo:
            stateCode = s[codeStateTag]
            stateState = s[stateTag]
            if stateCode in importantCodeStates:
                importantStates.append(stateState)
        states = list(set(importantStates) & set(states))
    phases = frame.getGroupByFromString(newDF_9, phaseSequenceTag)
    return [sections, subjects, judges, finished, sequences, phaseSequences, events, states, phases]

# update types based on user choices on different parameters. In order to do that is used 'updateTypeData' method with chosen parameter as None. 
# this is done because when user select a parameter, analysed dataframe is filtered to only processes where chosen parameters holds.
# by doing that other chooseable parameters would disappear since they are calculated from input datafram which contains only processes with selected ones.
# so it calculates paramers like if no one was chosen and it set them in dropdown.
def updateTypeDataframeFromSelection(newDF, df_data, startDate, endDate, sections, subjects, judges, finished):
    codeJudgeTag = utilities.getTagName("codeJudgeTag")
    finishedTag = utilities.getTagName("finishedTag")
    sectionTag = utilities.getTagName("sectionTag")
    subjectTag = utilities.getTagName("subjectTag")
    # for each parameter evaluate if is not None, which is when user makes a selection,
    # and in case modify to a new df using updateTypeData() with correlated parameter as None.
    if sections != None and len(sections) > 0:
        newDF_1 = updateTypeData(newDF, startDate, endDate, None, subjects, judges, finished)
    else:
        newDF_1 = df_data
    if subjects != None and len(subjects) > 0:
        newDF_2 = updateTypeData(newDF, startDate, endDate, sections, None, judges, finished)
    else:
        newDF_2 = df_data
    if judges != None and len(judges) > 0:
        newDF_3 = updateTypeData(newDF, startDate, endDate, sections, subjects, None, finished)
    else:
        newDF_3 = df_data
    if finished != None and len(finished) > 0:
        newDF_4 = updateTypeData(newDF, startDate, endDate, sections, subjects, judges, None)
    else:
        newDF_4 = df_data
    sections = frame.getGroupBy(newDF_1, sectionTag)
    subjects = frame.getGroupBy(newDF_2, subjectTag)
    judges = frame.getGroupBy(newDF_3, codeJudgeTag)
    finished = frame.getGroupBy(newDF_4, finishedTag)
    return [sections, subjects, judges, finished]

# return all needed parameters in order to change graph after any user choice.
# this method is only for process comparison graph.
#
# input data are: df is the dataframe, avgChoice is the user choice on how aggregate data on median or mean, dateType is the user choice on the type of data to show graph,
# startDate is the chosen start date of analyzed time interval, endDate is the chosen end date of analyzed time interval, minDate is the minimum start date, maxDate is the maximum end date,
# sections are the sections chosen by user to filter data, subjects are the subjects chosen by user to filter data, judges are the judges chosen by user to filter data, 
# finished are the type of processes chosen by user to filter data, sequences are the type of state sequence processes chosen by user to filter data, 
# phaseSequences are the type of phase sequence processes chosen by user to filter data, event is the event chosen by user to filter data based on presence or absence, eventRadio is chosen by user
# to select if he want processes with ou without chosen event, state is the state chosen by user to filter data based on presence or absence, stateRadio is chosen by user to select if he want processes 
# with ou without chosen state, phase is the phase chosen by user to filter data based on presence or absence, phaseRadio is chosen by user to select if he want processes with ou without chosen phase,
# choices are the parameters chosen by user to compare processes, choicesOptions is the list of posssiblr choices, order is chosen by user to select in which order show legend by load or mean, 
# text is chosen by user to decide to show load of processes or not.
#
# return data are: fig is the figure shown, startDate is the new startDate if reset was clicked, endDate is the new endDate is reset was clicked, sectionStyle is the new style of section dropdown, 
# subjectStyle is the new style of subject dropodown, judgeStyle is the new style of judge dropdown, finishedStyle is the new style of finished dropdown, sequenceStyle is the new style of sequence dropdown, 
# phaseSequenceStyle is the new style of phase sequence dropdown, eventStyle is the new style of event dropdown, eventRadioStyle is the new style of event radioitem, stateStyle is the new style of state dropdown, 
# stateRadioStyle is the new style of state radioitem, phaseStyle is the new style of phase dropdown, phaseRadioStyle is the new style of phase radioitem, orderRadioStyle is the new style of order radiotiem, 
# sections are the new updated chooseable sections, subjects are the new updated chooseable subjects, judges are the new updated chooseable judges, finished are the new updated chooseable process types, 
# sequences are the new updated chooseable state sequences, phaseSequences are the new updated chooseable phase sequences, event are the new updated chooseable events, state are the new updated chooseable states, 
# phase are the new updated chooseable phases, choicesOptions are the new updated chooseable parameters for comparison.
def processComparisonUpdate(df, avgChoice, dateType, startDate, endDate, minDate, maxDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio, choices, choicesOptions, order, text):
    # if reset button is clicked time interval is set to default.
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    # choicesOptions is the list of all possible parameter to compare processes. 
    # at the beggining there are only six: section, subject, judge, finished, sequence, phaseSequence.
    # if user hase chosen a state, phase or event is added to choiceOptions.
    choicesOptions = choicesOptions[:6]
    if event != None:
        eventChoice = event
        choicesOptions.append(event)
    else:
        eventChoice = None
    if state != None:
        stateChoice = state
        choicesOptions.append(state)
    else:
        stateChoice = None
    if phase != None:
        phaseChoice = phase
        choicesOptions.append(phase)
    else:
        phaseChoice = None
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    filterTag = utilities.getTagName('filterTag')
    quantileTag = utilities.getTagName('quantileTag')
    textTag = utilities.getPlaceholderName("text")
    eventsInfo = getter.getEventsInfo()
    statesInfo = getter.getStatesInfo()
    newDF = df.copy()
    # based on user choices dropdowns are hidden or shown. 
    [sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase] = hideProcessChosen(choices, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, stateChoice, phaseChoice)
    # df_data is calculated as newDF filtered based on user choices.
    df_data = updateProcessData(newDF, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, event, eventRadio, state, stateRadio, phase, phaseRadio)
    # parameters remaining choices are calculated based on user choices.
    [sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase] = updateProcessDataframeFromSelection(newDF, df_data, eventsInfo, statesInfo, startDate, endDate, sections, subjects, judges, finished, sequences, phaseSequences, eventChoice, eventRadio, stateChoice, stateRadio, phaseChoice, phaseRadio)
    # if user didn't select any parameter to compare, a simple process duration graph is shown.
    if choices == None or len(choices) == 0:
        orderRadioStyle = {'display': 'none'}
        # allData contains all data with duration and date value.
        # avgData contains for each different date the calculated average duration.
        [allData, avgData] = frame.getAvgStdDataFrameByDate(df_data, dateType, avgChoice)
        xticks = frame.getUniques(avgData, dateTag)
        fig = px.box(allData, x = dateTag, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Process Duration [days]', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95), points = False)
        fig.add_traces(
            px.line(avgData, x = dateTag, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
        )
        if text == [textTag]:
            fig.add_traces(
                px.line(avgData, x = dateTag, y = quantileTag, text = countTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 18)).data
            )
        else:
            fig.add_traces(
                px.line(avgData, x = dateTag, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 18)).data
            )
        fig.update_layout(xaxis_tickvals = xticks, font = dict(size = 14))
        fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
        return fig, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, orderRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase, choicesOptions
    # if user has selected a parameter to compare, a process comparison duration graph is shown.
    else:
        orderRadioStyle = {'display': 'block'}
        # typeData contains all different types with average duration for all type.
        # allData contains average duration of all data.
        # infoData contains load info for all different types.
        [typeData, allData, infoData] = frame.getAvgDataFrameByTypeChoices(df_data, avgChoice, dateType, choices, order, eventChoice, stateChoice, phaseChoice)
        xticks = frame.getUniques(allData, dateTag)
        if text == [textTag]:
            fig = px.line(allData, x = dateTag, y = durationTag, labels = {durationTag:'Process Duration [days]', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
            fig.add_traces(
                px.line(typeData, x = dateTag, y = durationTag, text = countTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1)).data
            )
        else:
            fig = px.line(allData, x = dateTag, y = durationTag, labels = {durationTag:'Process Duration [days]', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
            fig.add_traces(
                px.line(typeData, x = dateTag, y = durationTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1)).data
            )
        fig.for_each_trace(
            lambda t: t.update(name = frame.addCountToName(infoData, t.name, filterTag, countTag)) if t.name != frame.addTotCountToName(allData, countTag) else False
        )
        fig.for_each_trace(
            lambda t: t.update(textfont_color = t.line.color, textposition = "top center", textfont_size = 18)
        )
        fig.update_layout(xaxis_tickvals = xticks, font = dict(size = 14))
        fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != frame.addTotCountToName(allData, countTag) else False))
        fig.update_xaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
        fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
        return fig, startDate, endDate, sectionStyle, subjectStyle, judgeStyle, finishedStyle, sequenceStyle, phaseSequenceStyle, eventStyle, eventRadioStyle, stateStyle, stateRadioStyle, phaseStyle, phaseRadioStyle, orderRadioStyle, sections, subjects, judges, finished, sequences, phaseSequences, event, state, phase, choicesOptions

# return all needed parameters in order to change graph after any user choice.
# this method is only for all comparison graphs except process ones.
#
# input data are: df is the dataframe, typeChoice is the user chosen type to analyse, avgChoice is the user choice on how aggregate data on median or mean, dateType is the user choice on the type of data to show graph,
# startDate is the chosen start date of analyzed time interval, endDate is the chosen end date of analyzed time interval, minDate is the minimum start date, maxDate is the maximum end date,
# type refers to what type graph is shown (event, state or phase), sections are the sections chosen by user to filter data, subjects are the subjects chosen by user to filter data, judges are the judges chosen by user to filter data, 
# finished are the type of processes chosen by user to filter data, choices are the parameters chosen by user to compare processes, choicesOptions is the list of posssiblr choices, 
# order is chosen by user to select in which order show legend by load or mean, text is chosen by user to decide to show load of processes or not.
#
# return data are: fig is the figure shown, startDate is the new startDate if reset was clicked, endDate is the new endDate is reset was clicked, sectionStyle is the new style of section dropdown, 
# dateRangeStyle is the new style of data range, resetStyle is the new style of reset button, dateRadioStyle is the new style of date type radioitem, subjectStyle is the new style of subject dropdown, 
# judgeStyle is the new style of judge dropdown, finishedStyle is the new style of finished dropdown, choiceCheckStyle is the new style of choices cjelist, orderRadioStyle is the new style of order radiotiem, 
# sections are the new updated chooseable sections, subjects are the new updated chooseable subjects, judges are the new updated chooseable judges, finished are the new updated chooseable process types, 
# title is the new title of the graph.
def typeComparisonUpdate(df, typeChoice, avgChoice, dateType, startDate, endDate, minDate, maxDate, type, sections, subjects, judges, finished, choices, order, text):
    # if reset button is clicked time interval is set to default.    
    if ds.ctx.triggered_id != None and 'reset-button' in ds.ctx.triggered_id:
        startDate = minDate
        endDate = maxDate
    codeJudgeTag = utilities.getTagName('codeJudgeTag')
    countTag = utilities.getTagName('countTag')
    dateTag = utilities.getTagName('dateTag')
    durationTag = utilities.getTagName('durationTag')
    eventTag = utilities.getTagName('eventTag')
    filterTag = utilities.getTagName('filterTag')
    finishedTag = utilities.getTagName('finishedTag')
    quantileTag = utilities.getTagName('quantileTag')
    sectionTag = utilities.getTagName('sectionTag')
    subjectTag = utilities.getTagName('subjectTag')
    textTag = utilities.getPlaceholderName("text")
    statesInfo = getter.getStatesInfo()
    newDF = df.copy()
    # if user didn't select anything, a simple duration of types graph is shown.
    if typeChoice == None:
        title = 'PROCESS ' + type.upper() + 'S DURATION'
        newDF = updateTypeData(newDF, startDate, endDate, sections, subjects, judges, finished)
        # allData contains all data with duration and type value.
        # avgData contains for each different type the calculated average duration.
        [allData, avgData] = frame.getAvgStdDataFrameByType(newDF, type, avgChoice) 
        xticks = frame.getUniques(allData, type)
        # since no selection has been made all components are hidden.
        [dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = hideAll()
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(newDF, newDF, startDate, endDate, sections, subjects, judges, finished)
        # if text is selected by user then an histogram graph is shown, otherwise boxplot.
        # phaseColorMap maps to each phase the correlated color.
        if text == [textTag]:
            if type == eventTag:   
                fig = px.histogram(allData, x = type, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Number of ' + type + 's of process', type:type.title() + ' of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1))
            else:
                colorMap = frame.phaseColorMap(type, statesInfo)
                fig = px.histogram(allData, x = type, color = type, color_discrete_map = colorMap, labels = {durationTag:'Number of ' + type + 's of process', type:type.title() + ' of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1))
        else:
            if type == eventTag:        
                fig = px.box(allData, x = type, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Duration ' + type + 's of process [days]', type:type.title() + ' of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1), points  = False)
            else:
                colorMap = frame.phaseColorMap(type, statesInfo)
                fig = px.box(allData, x = type, y = durationTag, color = type, color_discrete_map = colorMap, labels = {durationTag:'Duration ' + type + 's of process [days]', type:type.title() + ' of process'}, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1), points  = False)
            fig.add_traces(
                px.line(avgData, x = type, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
        fig.update_layout(xaxis_tickvals = xticks, legend_itemclick = False, legend_itemdoubleclick = False, font = dict(size = 14))
        fig.update_xaxes(tickangle = 45)
        fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
        return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title
    # if user select one type, type duration graph is shown.
    else:
        title = 'COMPARISON OF ' + type.upper() + ' ' + str(typeChoice).upper() + " DURATION" 
        # since a selection has been made all components are shown.
        [dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle] = showAll()
        # based on user choice, chosen compare parameters hide the related components.
        [[sectionStyle, subjectStyle, judgeStyle, finishedStyle], [sections, subjects, judges, finished]] = hideChosen(choices, [sectionTag, subjectTag, codeJudgeTag, finishedTag], [sectionStyle, subjectStyle, judgeStyle, finishedStyle], [sections, subjects, judges, finished])
        # newDF is filtered by only user chosen type.
        newDF = frame.getTypesDataFrame(newDF, type, [typeChoice])
        # df_data is calculated as newDF filtered based on user choices.
        df_data = updateTypeData(newDF, startDate, endDate, sections, subjects, judges, finished)
        # parameters remaining choices are calculated based on user choices.
        [sections, subjects, judges, finished] = updateTypeDataframeFromSelection(newDF, df_data, startDate, endDate, sections, subjects, judges, finished)
        # if no comparison parameter is chosen by user, a simple type duration graph is shown.
        if choices == None or len(choices) == 0:
            orderRadioStyle = {'display': 'none'}
            # allData contains all data with duration and date value.
            # avgData contains for each different date the calculated average duration.
            [allData, avgData] = frame.getAvgStdDataFrameByDate(df_data, dateType, avgChoice)
            xticks = frame.getUniques(avgData, dateTag)
            fig = px.box(allData, x = dateTag, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Duration ' + type + " " + str(typeChoice) + ' [days]', dateTag:'Start Date ' + type + " " + str(typeChoice)}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95), points = False)
            fig.add_traces(
                px.line(avgData, x = dateTag, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
            )
            if text == [textTag]:
                fig.add_traces(
                    px.line(avgData, x = dateTag, y = quantileTag, text = countTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 18)).data
                )
            else:
                fig.add_traces(
                    px.line(avgData, x = dateTag, y = quantileTag, markers = False).update_traces(line_color = utilities.getInvisibleColor(), textposition = "top center", textfont = dict(color = utilities.getCharColor(), size = 14)).data
                )
            fig.update_layout(xaxis_tickvals = xticks, font = dict(size = 14))
            fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
            return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title
        # if user selects comparison parameter, comparison type duration graph is shown.
        else:
            orderRadioStyle = {'display': 'block'}
            # typeData contains all different types with average duration for all type.
            # allData contains average duration of all data.
            # infoData contains load info for all different types.
            [typeData, allData, infoData] = frame.getAvgDataFrameByTypeChoices(df_data, avgChoice, dateType, choices, order, None, None, None)
            xticks = frame.getUniques(allData, dateTag)
            if text == [textTag]:
                fig = px.line(allData, x = dateTag, y = durationTag, labels = {durationTag:'Process Duration [days]', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
                fig.add_traces(
                    px.line(typeData, x = dateTag, y = durationTag, text = countTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1)).data
                )
            else:
                fig = px.line(allData, x = dateTag, y = durationTag, labels = {durationTag:'Duration Process [days]', dateTag:'Process Start Date'}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95)).update_traces(showlegend = True, name = frame.addTotCountToName(allData, countTag), line_color = 'rgb(0, 0, 0)', line = {'width': 3})
                fig.add_traces(
                    px.line(typeData, x = dateTag, y = durationTag, color = filterTag, markers = True, width = utilities.getWidth(1.1), height = utilities.getHeight(1.1)).data
                )
            fig.for_each_trace(
                lambda t: t.update(name = frame.addCountToName(infoData, t.name, filterTag, countTag)) if t.name != frame.addTotCountToName(allData, countTag) else False
            )
            fig.for_each_trace(
                lambda t: t.update(textfont_color = t.line.color, textposition = "top center", textfont_size = 18)
            )
            fig.update_layout(xaxis_tickvals = xticks, font = dict(size = 14))
            fig.update_traces(visible = "legendonly", selector = (lambda t: t if t.name != frame.addTotCountToName(allData, countTag) else False))
            fig.update_xaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
            fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
            return fig, startDate, endDate, dateRangeStyle, resetStyle, dateRadioStyle, sectionStyle, subjectStyle, judgeStyle, finishedStyle, choiceCheckStyle, orderRadioStyle, sections, subjects, judges, finished, title

# return all needed parameters in order to change graph after any user choice.
# this method is only for process comparison graph.
#
# input data are: df is the dataframe, avgChoice is the user choice on how aggregate data on median or mean, tag refers on which aggregator is shown (judge, section, subject, month), 
# sections are the sections chosen by user to filter data, judges are the judges chosen by user to filter data, subjects are the subjects chosen by user to filter data, 
# months are the months chosen by user to filter data, text is chosen by user to decide to show load of processes or not.
#
# return data are: fig is the figure shown, title is the new title of the graph.
def parameterComparisonUpdate(df, avgChoice, tag, sections, judges, subjects, months, text):
    title = "COMPARISON OF PROCESSES DURATION BASED ON " + tag.upper()
    durationTag = utilities.getTagName('durationTag')
    textTag = utilities.getPlaceholderName("text")
    newDF = df.copy()
    # newDF is calculated as df filtered based on user choices.
    newDF = updateProcessTypeData(newDF, sections, subjects, judges, months)
    # based on user choice, chosen compare parameters hide the related components.
    [sectionStyle, judgeStyle, subjectStyle] = hideParameterChosen(tag)
    # allData contains all data with duration and type value.
    # avgData contains for each different type the calculated average duration.
    [allData, avgData] = frame.getAvgStdDataFrameByTypeQuantileFilter(newDF, tag, avgChoice)
    xticks = frame.getUniques(avgData, tag)
    # if text is selected by user then an histogram graph is shown, otherwise boxplot.
    if text == [textTag]:
        fig = px.histogram(allData, x = tag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Number of processes', tag:tag}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95))
    else:
        fig = px.box(allData, x = tag, y = durationTag, color_discrete_sequence = utilities.getBoxColor(), labels = {durationTag:'Process Duration [days]', tag:tag}, width = utilities.getWidth(0.95), height = utilities.getHeight(0.95), points = False)
        fig.add_traces(
            px.line(avgData, x = tag, y = durationTag, markers = True).update_traces(line_color = utilities.getLineColor()).data
        )
    fig.update_layout(xaxis_tickvals = xticks, font = dict(size = 14))
    fig.update_xaxes(tickangle = 45)
    fig.update_yaxes(gridcolor = utilities.getGridColor(), griddash = 'dash')
    return fig, title, sectionStyle, judgeStyle, subjectStyle
