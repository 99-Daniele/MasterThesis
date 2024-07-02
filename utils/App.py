# this file handles whole app management. Needed imports are inside 'start' method and not outside for faster initialization.

# create links for all pages.
def start():
    import dash as ds

    import pages.Home as homePage
    import pages.Comparison as comparisonPage
    import pages.Event as eventPage
    import pages.Preference as preferencePage
    import pages.Composition as typeEventPage
    import pages.comparisonGraph.EventComparison as eventComparisonPage
    import pages.comparisonGraph.PhaseComparison as phaseComparisonPage
    import pages.comparisonGraph.ProcessComparison as processComparisonPage
    import pages.comparisonGraph.StateComparison as stateComparisonPage
    import pages.comparisonGraph.ProcessComparisonByType as typeComparisonPage
    import pages.eventGraph.AllEventsScatter as allEventsPage
    import pages.eventGraph.PhaseEventsScatter as phaseEventsPage
    import pages.eventGraph.StateEventsScatter as stateEventsPage
    import pages.predictionGraph.PredictionError as predictionErrorPage
    import pages.preferenceTable.EventPreference as eventPreferencePage
    import pages.preferenceTable.StatePreference as statePreferencePage
    import pages.preferenceTable.SubjectPreference as subjectPreferencePage
    import pages.compositionGraph.EventSequence as sequenceEventPage
    import pages.compositionGraph.PhaseEvents as eventsPhasePage
    import pages.compositionGraph.PhaseSequence as sequencePhasePage
    import pages.compositionGraph.StateEvents as eventsStatePage
    import pages.compositionGraph.StateSequence as sequenceStatePage

    app = ds.Dash(__name__, suppress_callback_exceptions = True)
    app.layout = ds.html.Div([
        ds.html.H2('COURT OF MILAN PROCESSES'),
        ds.dcc.Location(id = 'url', refresh = False),
        ds.html.Div(id = 'page-content')
    ])
    @ds.callback(
            ds.Output('page-content', 'children'),
            ds.Input('url', 'pathname'))
    def display_page(pathname):
        match pathname:
            case '/comparison':
                return comparisonPage.pageLayout()
            case '/event':
                return eventPage.pageLayout()
            case '/preference':
                return preferencePage.pageLayout()
            case '/composition':
                return typeEventPage.pageLayout()
            case '/comparison/eventcomparison':
                return eventComparisonPage.pageLayout()
            case '/comparison/phasecomparison':
                return phaseComparisonPage.pageLayout()
            case '/comparison/processcomparison':
                return processComparisonPage.pageLayout()
            case '/comparison/statecomparison':
                return stateComparisonPage.pageLayout()
            case '/comparison/typecomparison':
                return typeComparisonPage.pageLayout()
            case '/event/allevents':
                return allEventsPage.pageLayout()
            case '/event/phaseevents':
                return phaseEventsPage.pageLayout()
            case '/event/stateevents':
                return stateEventsPage.pageLayout()
            case '/prediction':
                return predictionErrorPage.pageLayout()
            case '/preference/eventpreference':
                return eventPreferencePage.pageLayout()
            case '/preference/statepreference':
                return statePreferencePage.pageLayout()
            case '/preference/subjectpreference':
                return subjectPreferencePage.pageLayout()
            case '/composition/stateevent':
                return eventsStatePage.pageLayout()
            case '/composition/phaseevent':
                return eventsPhasePage.pageLayout()
            case '/composition/statesequence':
                return sequenceStatePage.pageLayout()
            case '/composition/phasesequence':
                return sequencePhasePage.pageLayout()
            case '/composition/eventsequence':
                return sequenceEventPage.pageLayout()
            case _:
                return homePage.pageLayout()
    app.run_server(debug = True)
