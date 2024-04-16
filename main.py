def refreshData():
    import utils.DatabaseConnection as connect
    import utils.DataUpdate as update
    import utils.Getters as getter
    connection = connect.getDatabaseConnection()
    update.refreshData(connection)
    getter.updateCache()

def displayAllEvents():
    import utils.Getters as getter
    import utils.Graph.EventsGraph as event
    import utils.FileOperation as file
    allEvents = getter.getAllEvents()
    importantEvents = file.getDataFromTextFile('utils/Preferences/importantEvents.txt')
    event.displayEvents(allEvents, 'evento', importantEvents)

def displayImportantEvents():
    import utils.Getters as getter
    import utils.Graph.EventsGraph as event
    import utils.FileOperation as file
    importantEvents = getter.getImportantEvents()
    mustEvents = file.getDataFromTextFile('utils/Preferences/mustEvents.txt')
    event.displayEvents(importantEvents, 'evento', mustEvents)

def displayPhaseEvents():
    import utils.Getters as getter
    import utils.Graph.EventsGraph as event
    import utils.FileOperation as file
    phaseEvents = getter.getPhaseEvents()
    mustPhases = file.getDataFromTextFile('utils/Preferences/mustPhases.txt')
    event.displayEvents(phaseEvents, 'fase', mustPhases)

def displayStateEvents():
    import utils.Getters as getter
    import utils.Graph.EventsGraph as event
    import utils.FileOperation as file
    stateEvents = getter.getStateEvents()
    mustStates = file.getDataFromTextFile('utils/Preferences/mustStates.txt')
    event.displayEvents(stateEvents, 'stato', mustStates)
    
def displayProcessDuration():
    import utils.Getters as getter
    import utils.Graph.DurationGraph as duration
    processes = getter.getProcessesDuration()
    duration.displayProcessesDuration(processes)

def displayPhaseComparation():
    import utils.Getters as getter
    import utils.Graph.ComparationGraph as comparation
    phases = getter.getPhasesDuration()
    comparation.displayTypeComparation(phases, "M", "fase")
    
def displayPhaseDuration():
    import utils.Getters as getter
    import utils.Graph.DurationGraph as duration
    phases = getter.getPhasesDuration()
    duration.displayPhasesDuration(phases)

def displayStateDuration():
    import utils.Getters as getter
    import utils.Graph.DurationGraph as duration
    states = getter.getStatesDuration()
    duration.displayStatesDuration(states)

def displayComparation():
    import utils.Getters as getter
    import utils.Graph.ComparationGraph as comparation
    processes = getter.getProcessesDuration()
    comparation.displayComparation(processes, "W")

def startApp():
    import utils.App as app

    app.start()

if __name__ == '__main__':
    displayImportantEvents()
