import dash as ds

import pages.Home as homePage
import pages.Comparation as comparationPage
import pages.Duration as durationPage
import pages.Event as eventPage
import pages.ComparationGraph.ComparationByMonth as comparationMonthPage
import pages.ComparationGraph.ComparationByMonthYear as comparationMonthYearPage
import pages.ComparationGraph.ComparationByWeek as comparationWeekPage
import pages.ComparationGraph.PhaseComparation as phaseComparation
import pages.ComparationGraph.StateComparation as stateComparation
import pages.DurationGraph.PhaseDuration as phaseDurationPage
import pages.DurationGraph.CourtHearingDuration as courtHearingDurationPage
import pages.DurationGraph.EventDuration as eventDurationPage
import pages.DurationGraph.ProcessDuration as processDurationPage
import pages.DurationGraph.StateDuration as stateDurationPage
import pages.EventGraph.AllEvents as allEventsPage
import pages.EventGraph.ImportantEvents as importantEventsPage
import pages.EventGraph.PhaseEvents as phaseEventsPage
import pages.EventGraph.StateEvents as stateEventsPage

def start():

    app = ds.Dash(__name__, use_pages = True, suppress_callback_exceptions = True)
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
            case '/durationgraph/courthearingduration':
                return courtHearingDurationPage.pageLayout()
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