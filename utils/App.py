import time
start = time.time()
import dash as ds
end1 = time.time()
print("DS: ", end1 - start)

import pages.Home as homePage
end2 = time.time()
print("HOME: ", end2 - end1)
import pages.Comparation as comparationPage
end3 = time.time()
print("COMP: ", end3 - end2)
import pages.Duration as durationPage
end4 = time.time()
print("DUR: ", end4 - end3)
import pages.Event as eventPage
end5 = time.time()
print("EV: ", end5 - end4)
import pages.ComparationGraph.ComparationByMonth as comparationMonthPage
end6 = time.time()
print("COMP_M: ", end6 - end5)
import pages.ComparationGraph.ComparationByMonthYear as comparationMonthYearPage
end7 = time.time()
print("COMP_MY: ", end7 - end6)
import pages.ComparationGraph.ComparationByWeek as comparationWeekPage
end8 = time.time()
print("COMP_W: ", end8 - end7)
import pages.ComparationGraph.PhaseComparation as phaseComparation
end9 = time.time()
print("COMP_PH: ", end9 - end8)
import pages.ComparationGraph.StateComparation as stateComparation
end10 = time.time()
print("COMP_S: ", end10 - end9)
import pages.DurationGraph.PhaseDuration as phaseDurationPage
end11 = time.time()
print("DUR_PH: ", end11 - end10)
import pages.DurationGraph.CourtHearingsDuration as courtHearingsDurationPage
end12 = time.time()
print("DUR_CH: ", end12 - end11)
import pages.DurationGraph.EventDuration as eventDurationPage
end13 = time.time()
print("DUR_E: ", end13 - end12)
import pages.DurationGraph.ProcessDuration as processDurationPage
end14 = time.time()
print("DUR_PR: ", end14 - end13)
import pages.DurationGraph.StateDuration as stateDurationPage
end15 = time.time()
print("DUR_S: ", end15 - end14)
import pages.EventGraph.AllEvents as allEventsPage
end16 = time.time()
print("ALL_E: ", end16 - end15)
import pages.EventGraph.ImportantEvents as importantEventsPage
end17 = time.time()
print("IMP_E: ", end17 - end16)
import pages.EventGraph.PhaseEvents as phaseEventsPage
end18 = time.time()
print("PH_E: ", end18 - end17)
import pages.EventGraph.StateEvents as stateEventsPage
end19 = time.time()
print("S_E: ", end19 - end18)

def start():

    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('PROGETTO TRIBUNALI'),
        ds.dcc.Location(id = 'url', refresh = False),
        ds.html.Div(id = 'page-content')
    ])
    @ds.callback(
            ds.Output('page-content', 'children'),
            ds.Input('url', 'pathname'))
    def display_page(pathname):
        match pathname:
            case '/comparationgraph':
                return comparationPage.pageLayout()
            case '/durationgraph':
                return durationPage.pageLayout()
            case '/eventgraph':
                return eventPage.pageLayout()
            case '/comparationgraph/weekcomparation':
                return comparationWeekPage.pageLayout()
            case '/comparationgraph/monthcomparation':
                return comparationMonthPage.pageLayout()
            case '/comparationgraph/monthyearcomparation':
                return comparationMonthYearPage.pageLayout()
            case '/comparationgraph/phasecomparation':
                return phaseComparation.pageLayout()
            case '/comparationgraph/statecomparation':
                return stateComparation.pageLayout()
            case '/durationgraph/courthearingsduration':
                return courtHearingsDurationPage.pageLayout()
            case '/durationgraph/eventduration':
                return eventDurationPage.pageLayout()
            case '/durationgraph/phaseduration':
                return phaseDurationPage.pageLayout()
            case '/durationgraph/processduration':
                return processDurationPage.pageLayout()
            case '/durationgraph/stateduration':
                return stateDurationPage.pageLayout()
            case '/eventgraph/allevents':
                return allEventsPage.pageLayout()
            case '/eventgraph/importantevents':
                return importantEventsPage.pageLayout()
            case '/eventgraph/phaseevents':
                return phaseEventsPage.pageLayout()
            case '/eventgraph/stateevents':
                return stateEventsPage.pageLayout()
            case _:
                return homePage.pageLayout()
    app.run_server(debug = True)