# this file handles whole app management. Needed imports are inside 'start' method and not outside for faster initialization.

# create links for all pages.
def start():
    import dash as ds

    import pages.Home as homePage
    import pages.Comparation as comparationPage
    import pages.Duration as durationPage
    import pages.Event as eventPage
    import pages.ComparationGraph.EventComparation as eventComparationPage
    import pages.ComparationGraph.PhaseComparation as phaseComparationPage
    import pages.ComparationGraph.ProcessComparation as processComparationPage
    import pages.ComparationGraph.StateComparation as stateComparationPage
    import pages.DurationGraph.CourtHearingsDuration as courtHearingsDurationPage
    import pages.DurationGraph.ProcessDuration as processDurationPage
    import pages.EventGraph.AllEvents as allEventsPage
    import pages.EventGraph.ImportantEvents as importantEventsPage
    import pages.EventGraph.PhaseEvents as phaseEventsPage
    import pages.EventGraph.StateEvents as stateEventsPage

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
            case '/comparationgraph/eventcomparation':
                return eventComparationPage.pageLayout()
            case '/comparationgraph/phasecomparation':
                return phaseComparationPage.pageLayout()
            case '/comparationgraph/processcomparation':
                return processComparationPage.pageLayout()
            case '/comparationgraph/statecomparation':
                return stateComparationPage.pageLayout()
            case '/durationgraph/courthearingsduration':
                return courtHearingsDurationPage.pageLayout()
            case '/durationgraph/processduration':
                return processDurationPage.pageLayout()
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
    app.run_server()
