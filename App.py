# this file handles whole app management. Needed imports are inside 'start' method and not outside for faster initialization.

# create links for all pages.
def start():
    import dash as ds

    import pages.Home as homePage
    import pages.Comparation as comparationPage
    import pages.Event as eventPage
    import pages.comparationGraph.EventComparation as eventComparationPage
    import pages.comparationGraph.PhaseComparation as phaseComparationPage
    import pages.comparationGraph.ProcessComparation as processComparationPage
    import pages.comparationGraph.StateComparation as stateComparationPage
    import pages.eventGraph.AllEvents as allEventsPage
    import pages.eventGraph.ImportantEvents as importantEventsPage
    import pages.eventGraph.PhaseEvents as phaseEventsPage
    import pages.eventGraph.StateEvents as stateEventsPage

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
    app.run_server(debug = False)
