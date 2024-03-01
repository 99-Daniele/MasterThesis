import DatabaseConnection as dbc

from alive_progress import alive_bar

def refreshData(connection):
    updateProcesses(connection)

def updateProcesses(connection):
    processEvents = getProcessEvents(connection)
    query = "SELECT * FROM statinome"
    translation = dbc.getDataFromDatabase(connection, query)
    processes = translateProcessSequence(processEvents, translation)
    print(processes)
    exit()
    dbc.updateTable(connection, 'processitipo', processes)

def isProcessAlreadyPresent(processes, processId):
    for p in processes:
        if p[0] == processId:
            return True
    return False

def addState(processes, processId, processState, processTranslate):
    for p in processes:
        if p[0] == processId:
            p[1].append(processState)
            p[2].append(processTranslate)
            return
        
def addEvent(processes, processId, eventDate, eventTag):
    for p in processes:
        if p[0] == processId:
            p[1].append(eventDate)
            p[2].append(eventTag)
            return

def getProcessSequence(connection):
    findProcessesStates = "SELECT numProcesso, d.stato, abbreviazione FROM duratastati AS d, statinome AS s WHERE d.stato = s.stato ORDER BY numProcesso, dataInizioStato"
    processStates = dbc.getDataFromDatabase(connection, findProcessesStates)
    processes = []
    with alive_bar(int(len(processStates))) as bar:
        for p in processStates:
            if not isProcessAlreadyPresent(processes, p[0]):
                processes.append([p[0], [p[1]], [p[2]]])
            else:
                addState(processes, p[0], p[1], p[2])
            bar()
    return processes

def getProcessEvents(connection):
    findProcessesEvents = "SELECT numProcesso, data, s.etichetta FROM eventi AS e, statinome AS s WHERE e.statofinale = s.stato ORDER BY numEvento"
    processEvents = dbc.getDataFromDatabase(connection, findProcessesEvents)
    processes = []
    with alive_bar(int(len(processEvents))) as bar:
        for e in processEvents:
            if not isProcessAlreadyPresent(processes, e[0]):
                processes.append([e[0], [e[1]], [e[2]]])
            else:
                addEvent(processes, e[0], e[1], e[2])
            bar()
    return processes

def translateProcessSequence(processes, translation):
    for p in processes:
        shortSequence = p[2].copy()
        [shortSequence, lastDate] = findRestart(shortSequence, translation, p[1])
        p[1] = lastDate
        shortSequence = filterSequence(shortSequence) 
        p.append(shortSequence)
    return processes

def translateState(state, states):
    for s in states:
        print(s)
        if s[1] == state:
            return s[3]   
        
def findPhase(state, states): 
    for s in states:
        if s[3] == state:
            return s[2] 

def filterSequence(sequence):
    newSequence = []
    for s in sequence:
        if not(s in newSequence):
            newSequence.append(s)
    return newSequence   

def findRestart(sequence, states, dates):
    newSequence = []
    i = 0
    prevPhase = 0
    while i < len(sequence):
        phase = findPhase(sequence[i], states)
        if phase == '5':
            newSequence.append(sequence[i])  
            break
        elif phase != "-":
            if int(phase) < int(prevPhase):
                newSequence.append('REST')
                i = i + 1
                while i < len(sequence):
                    if findPhase(sequence[i], states) == "-" or int(findPhase(sequence[i], states)) < int(prevPhase):
                        i = i + 1
                    else:
                        break
                if i < len(sequence):
                    newSequence.append(sequence[i])        
            else:
                newSequence.append(sequence[i])  
            prevPhase = phase 
        else:
            if sequence[i] == 'REST':
                newSequence.append('REST')
                i = i + 1
                while i < len(sequence):
                    if findPhase(sequence[i], states) == "-" or int(findPhase(sequence[i], states)) < int(prevPhase):
                        i = i + 1
                    else:
                        break
                if i < len(sequence):
                    newSequence.append(sequence[i])  
            else:    
                newSequence.append(sequence[i]) 
        i = i + 1 

    return [newSequence, dates[i]]               

def translateStateSequence(connection):
    cursor = connection.cursor(buffered = True)
    findProcesses = "SELECT numProcesso, sequenzaOriginale FROM processicondurata"
    findStateTranslation = "SELECT * FROM statinome"
    findEventTranslation = "SELECT * FROM eventinome"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    cursor.execute(findStateTranslation)
    stateTranslation = cursor.fetchall()
    cursor.execute(findEventTranslation)
    eventTranslation = cursor.fetchall()
    cursor.execute('DELETE FROM frequenzaeventi')
    with alive_bar(int(len(processes))) as bar:
        for p in processes:
            pId = p[0]
            states = p[1].split(',')
            for s in states:
                sequence = []
                findEvents = "SELECT codice FROM eventi WHERE numProcesso = " + str(pId) + " AND statofinale = '" + s + "' ORDER BY numEvento"
                cursor.execute(findEvents)
                events = cursor.fetchall()
                for e in events:
                    sequence.append(translateEvent(e[0], eventTranslation)) 
                sequence = filterSequence(sequence)
                stringSequence = ",".join(str(e) for e in sequence)
                insertSequence = "INSERT INTO sequenzaeventi VALUES (%s, %s, %s, %s)"     
                values = (pId, translateState(s, stateTranslation), s, stringSequence)
                cursor.execute(insertSequence, values)
            bar()
    connection.commit()  

def filterSequence(sequence):
    newSequence = [sequence[0]]
    for s in sequence:
        if s != newSequence[-1]:
            newSequence.append(s)
    return newSequence   

def translateEvent(event, events):
    for e in events:
        if e[0] == event:
            return e[1]

def getCurrentPhase(cursor, numProcesso, id):
    findEvents = "SELECT id, fase FROM udienze WHERE numProcesso = " + str(numProcesso) + " AND id < " + str(id)
    cursor.execute(findEvents)
    events = cursor.fetchall()
    print(events)
    i = 1
    while i < len(events):
        phase = events[-i][1]
        print(phase)
        if phase != '-':
            exit()
            return int(phase)
        else:
            i = i + 1
    return 1

def translateTuple(tuple):
    processoFinito = isProcessFinished(tuple[3][-1])
    sequence = ",".join(str(e) for e in tuple[1])
    translateSequence = ",".join(str(e) for e in tuple[2])
    shortSequence = ",".join(str(e) for e in tuple[2])
    return [tuple[0], processoFinito, sequence, translateSequence, shortSequence]

def isProcessFinished(lastState):
    match lastState:
        case "STOP":
            return 2
        case "FINE":
            return 1
        case "STALLO":
            return -1
    return 0