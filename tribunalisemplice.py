import mysql.connector as cnx
import matplotlib.pyplot as plt
import matplotlib.colors as col
import datetime as dtm
import numpy as np
import time as tm
import tkinter as tk
from heapq import nlargest
from operator import itemgetter

colors = ['blue', 'orange', 'red', 'green', 'purple']
daysOfYear = ['01/01', '02/01', '03/01', '04/01', '05/01', '06/01', '07/01', '08/01', '09/01', '10/01', '11/01', '12/01', '13/01', '14/01', '15/01', '16/01', '17/01', '18/01', '19/01', '20/01', '21/01', '22/01', '23/01', '24/01', '25/01', '26/01', '27/01', '28/01', '29/01', '30/01', '31/01', '01/02', '02/02', '03/02', '04/02', '05/02', '06/02', '07/02', '08/02', '09/02', '10/02', '11/02', '12/02', '13/02', '14/02', '15/02', '16/02', '17/02', '18/02', '19/02', '20/02', '21/02', '22/02', '23/02', '24/02', '25/02', '26/02', '27/02', '28/02', '29/02', '01/03', '02/03', '03/03', '04/03', '05/03', '06/03', '07/03', '08/03', '09/03', '10/03', '11/03', '12/03', '13/03', '14/03', '15/03', '16/03', '17/03', '18/03', '19/03', '20/03', '21/03', '22/03', '23/03', '24/03', '25/03', '26/03', '27/03', '28/03', '29/03', '30/03', '31/03', '01/04', '02/04', '03/04', '04/04', '05/04', '06/04', '07/04', '08/04', '09/04', '10/04', '11/04', '12/04', '13/04', '14/04', '15/04', '16/04', '17/04', '18/04', '19/04', '20/04', '21/04', '22/04', '23/04', '24/04', '25/04', '26/04', '27/04', '28/04', '29/04', '30/04', '01/05', '02/05', '03/05', '04/05', '05/05', '06/05', '07/05', '08/05', '09/05', '10/05', '11/05', '12/05', '13/05', '14/05', '15/05', '16/05', '17/05', '18/05', '19/05', '20/05', '21/05', '22/05', '23/05', '24/05', '25/05', '26/05', '27/05', '28/05', '29/05', '30/05', '31/05', '01/06', '02/06', '03/06', '04/06', '05/06', '06/06', '07/06', '08/06', '09/06', '10/06', '11/06', '12/06', '13/06', '14/06', '15/06', '16/06', '17/06', '18/06', '19/06', '20/06', '21/06', '22/06', '23/06', '24/06', '25/06', '26/06', '27/06', '28/06', '29/06', '30/06', '01/07', '02/07', '03/07', '04/07', '05/07', '06/07', '07/07', '08/07', '09/07', '10/07', '11/07', '12/07', '13/07', '14/07', '15/07', '16/07', '17/07', '18/07', '19/07', '20/07', '21/07', '22/07', '23/07', '24/07', '25/07', '26/07', '27/07', '28/07', '29/07', '30/07', '31/07', '01/08', '02/08', '03/08', '04/08', '05/08', '06/08', '07/08', '08/08', '09/08', '10/08', '11/08', '12/08', '13/08', '14/08', '15/08', '16/08', '17/08', '18/08', '19/08', '20/08', '21/08', '22/08', '23/08', '24/08', '25/08', '26/08', '27/08', '28/08', '29/08', '30/08', '31/08', '01/09', '02/09', '03/09', '04/09', '05/09', '06/09', '07/09', '08/09', '09/09', '10/09', '11/09', '12/09', '13/09', '14/09', '15/09', '16/09', '17/09', '18/09', '19/09', '20/09', '21/09', '22/09', '23/09', '24/09', '25/09', '26/09', '27/09', '28/09', '29/09', '30/09', '01/10', '02/10', '03/10', '04/10', '05/10', '06/10', '07/10', '08/10', '09/10', '10/10', '11/10', '12/10', '13/10', '14/10', '15/10', '16/10', '17/10', '18/10', '19/10', '20/10', '21/10', '22/10', '23/10', '24/10', '25/10', '26/10', '27/10', '28/10', '29/10', '30/10', '31/10', '01/11', '02/11', '03/11', '04/11', '05/11', '06/11', '07/11', '08/11', '09/11', '10/11', '11/11', '12/11', '13/11', '14/11', '15/11', '16/11', '17/11', '18/11', '19/11', '20/11', '21/11', '22/11', '23/11', '24/11', '25/11', '26/11', '27/11', '28/11', '29/11', '30/11', '01/12', '02/12', '03/12', '04/12', '05/12', '06/12', '07/12', '08/12', '09/12', '10/12', '11/12', '12/12', '13/12', '14/12', '15/12', '16/12', '17/12', '18/12', '19/12', '20/12', '21/12', '22/12', '23/12', '24/12', '25/12', '26/12', '27/12', '28/12', '29/12', '30/12', '31/12']
weeks = ['02/01', '08/01', '15/01', '22/01', '29/01', '05/02', '12/02', '19/02', '26/02', '05/03', '12/03', '19/03', '26/03', '02/04', '09/04', '16/04', '23/04', '30/04', '07/05', '14/05', '21/05', '28/05', '04/06', '11/06', '18/06', '25/06', '02/07', '09/07', '16/07', '23/07', '30/07', '06/08', '13/08', '20/08', '27/08', '03/09', '10/09', '17/09', '24/09', '01/10', '08/10', '15/10', '22/10', '29/10', '05/11', '12/11', '19/11', '26/11', '03/12', '10/12', '17/12', '24/12', '31/12']
months = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']
daysOfWeek = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']

def connectToDatabase():
    connection = cnx.connect(
        host = "127.0.0.1",
        #user = input("Inserisci username: "),
        #password = input("Inserisci password: "),
        #database = input("Inserisci database: "),
        user = "root",
        password = "Ropswot_@222",
        database = "tribunalisemplice",
        auth_plugin = 'mysql_native_password'
    )
    return connection

def getDataFromDatabase(cursor, query):
    cursor.execute(query)
    return cursor.fetchall()

def displayScatter(x_label, y_label, title, min, max):
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.xlim(min, max)  
    plt.yticks([], []) 
    plt.xlabel(x_label)  
    plt.ylabel(y_label)
    plt.title(title) 
    plt.show()  

def displayPlot(x, y, x_fontsize, x_label, y_label, title):
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(x, y, c = 'black')
    plt.xticks(fontsize = x_fontsize)
    plt.yticks(range(int(min(y)), int(max(y)),  int(((max(y) - min(y)) / 20))))
    plt.xlabel(x_label)         
    plt.ylabel(y_label)
    plt.title(title) 
    plt.show()

def displayTable(x, y, x_title, y_title, nr):
    top = nlargest(nr, y)
    table = []
    for i in range(nr):
        idx = y.index(top[i])
        table.append([x[idx], y[idx]])
    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    plt.axis('tight')
    plt.axis('off')
    plt.table(cellText = table, colLabels = (x_title, y_title), loc='center')
    plt.show()

def displayAllProcesses(cursor):
    start = tm.time()
    [min, max] = getAllProcesses(cursor)
    displayScatter("Data inizio e fine processo", "Codice processo", "Processi tribunale di Milano", min, max)
    print("--- %s seconds ---" % (tm.time() - start))

def getAllProcesses(cursor):
    findProcesses = "SELECT numProcesso, data FROM eventi WHERE ((statofinale = 'AS' AND codice = 'IA') OR (statofinale = 'DF' AND statofinale <> statoIniziale AND fase = 4)) AND numProcesso IN (SELECT numProcesso FROM processifiniti) ORDER BY numProcesso"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    color = list(col.to_rgb('cyan'))
    i = 0
    while i < len(processes):
        p1 = processes[i][0]
        p2 = processes[i + 1][0]
        d1 = processes[i][1]
        d2 = processes[i + 1][1]
        color[0] = color[0] + 1.0 / len(processes)
        plt.scatter(d1, p1, s = 20, color = col.hsv_to_rgb(color)) 
        plt.scatter(d2, p2, s = 20, color = col.hsv_to_rgb(color))
        i = i + 10
    processes = sorted(processes, key = itemgetter(1)) 
    return [processes[0][1], processes[-1][1]]    

def displayAllProcessEvents(cursor):
    start = tm.time()
    [min, max] = getAllProcessEvents(cursor)
    displayScatter("Data evento", "Codice processo", "Processi tribunale di Milano", min, max)
    print("--- %s seconds ---" % (tm.time() - start))

def getAllProcessEvents(cursor):
    findProcesses = "SELECT numProcesso, data, fase, statoFinale FROM eventi WHERE statoiniziale <> statofinale AND fase < 5 AND numProcesso IN (SELECT numProcesso FROM processifiniti)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    for p in processes:
        if p[3] == 'DF':
            plt.scatter(p[1], p[0], s = 20, c = colors[p[2]]) 
        else:
            plt.scatter(p[1], p[0], s = 20, c = colors[p[2] - 1]) 
    processes = sorted(processes, key = itemgetter(1)) 
    return [processes[0][1], processes[-1][1]] 

def displayProcessesOfYear(cursor, year):
    start = tm.time()
    [min, max] = getProcessesOfYear(cursor, year)
    displayScatter("Data inizio e fine processo", "Codice processo", "Processi iniziati nell'anno " + str(year), min, max)
    print("--- %s seconds ---" % (tm.time() - start))

def getProcessesOfYear(cursor, year):
    findProcesses = "SELECT numProcesso, data FROM eventi WHERE ((statofinale = 'AS' AND codice = 'IA') OR (statofinale = 'DF' AND statofinale <> statoIniziale AND fase = 4)) AND numProcesso IN (SELECT numProcesso FROM processifiniti WHERE anno = " + str(year) + ") ORDER BY numProcesso"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    color = list(col.to_rgb('cyan'))
    i = 0
    while i < len(processes):
        p1 = processes[i][0]
        p2 = processes[i + 1][0]
        d1 = processes[i][1]
        d2 = processes[i + 1][1]
        color[0] = color[0] + 1.0 / len(processes)
        plt.scatter(d1, p1, s = 20, color = col.hsv_to_rgb(color)) 
        plt.scatter(d2, p2, s = 20, color = col.hsv_to_rgb(color))
        i = i + 2
    processes = sorted(processes, key = itemgetter(1)) 
    return [processes[0][1], processes[-1][1]]    

def displayProcessEventsOfYear(cursor, year):
    start = tm.time()
    [min, max] = getProcessEventsOfYear(cursor, year)
    displayScatter("Data evento", "Codice processo", "Processi iniziati nell'anno " + str(year), min, max)
    print("--- %s seconds ---" % (tm.time() - start))

def getProcessEventsOfYear(cursor, year):
    findProcesses = "SELECT numProcesso, data, fase, statoFinale FROM eventi WHERE statoiniziale <> statofinale AND fase < 5 AND numProcesso IN (SELECT numProcesso FROM processifiniti WHERE anno = " + str(year) + ")"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    for p in processes:
        if p[3] == 'DF':
            plt.scatter(p[1], p[0], s = 20, c = colors[p[2]]) 
        else:
            plt.scatter(p[1], p[0], s = 20, c = colors[p[2] - 1]) 
    processes = sorted(processes, key = itemgetter(1)) 
    return [processes[0][1], processes[-1][1]]  

def displayAvgProcessDurationByWeek(cursor):
    start = tm.time()
    [weeks, avgs] = getAvgProcessDurationByWeek(cursor)
    displayPlot(weeks, avgs, 5, "Settimana inizio processo", "[giorni]", "Durata media processi in base alla settimana di inizio")
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgProcessDurationByWeek(cursor):
    tot_avg = float(getDataFromDatabase(cursor, "SELECT AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), dataInizio)) AS durata FROM processifiniti AS p")[0][0])
    [years, y_avgs] = getAvgProcessDurationByYear(cursor)
    processes = getDataFromDatabase(cursor, "SELECT WEEK(p.dataInizio, 7), YEAR(p.dataInizio), AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), p.dataInizio)) FROM processifiniti AS p GROUP BY WEEK(p.dataInizio, 7), YEAR(p.dataInizio) ORDER BY YEAR(p.dataInizio), WEEK(p.dataInizio, 7)")
    avgs = [0] * 53
    counts = [0] * 53
    for p in processes:
        w = int(p[0] - 1)
        y = int(p[1])
        y_avg = y_avgs[years.index(y) - 1]
        avg = float(p[2]) * tot_avg / y_avg
        count = counts[w]
        newAvg = (((avgs[w] * count) + avg) / (count + 1))
        counts[w] = count + 1
        avgs[w] = newAvg 
    return [weeks, avgs]    

def displayAvgProcessDurationByMonth(cursor):
    start = tm.time()
    [months, avgs] = getAvgProcessDurationByMonth(cursor)
    displayPlot(months, avgs, 8, "Mese inizio processo", "[giorni]", "Durata media processi in base al mese di inizio")
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgProcessDurationByMonth(cursor):
    tot_avg = float(getDataFromDatabase(cursor, "SELECT AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), dataInizio)) AS durata FROM processifiniti AS p")[0][0])
    [years, y_avgs] = getAvgProcessDurationByYear(cursor)
    processes = getDataFromDatabase(cursor, "SELECT MONTH(p.dataInizio), YEAR(p.dataInizio), AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), p.dataInizio)) FROM processifiniti AS p GROUP BY MONTH(p.dataInizio), YEAR(p.dataInizio) ORDER BY YEAR(p.dataInizio), MONTH(p.dataInizio)")
    avgs = [0] * 12
    counts = [0] * 12
    for p in processes:
        m = int(p[0] - 1)
        y = int(p[1])
        y_avg = y_avgs[years.index(y) - 1]
        avg = float(p[2]) * tot_avg / y_avg
        count = counts[m]
        newAvg = (((avgs[m] * count) + avg) / (count + 1))
        counts[m] = count + 1
        avgs[m] = newAvg 
    return [months, avgs] 

def displayAvgProcessDurationByYear(cursor):
    start = tm.time()
    [years, avgs] = getAvgProcessDurationByYear(cursor)
    displayPlot(years, avgs, 10, "Anno inizio processo", "[giorni]", "Durata media processi in base all'anno di inizio")
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgProcessDurationByYear(cursor):
    processes = getDataFromDatabase(cursor, "SELECT YEAR(p.dataInizio), AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), p.dataInizio)) FROM processifiniti AS p GROUP BY YEAR(p.dataInizio) ORDER BY YEAR(p.dataInizio)")
    years = []
    avgs = []
    for p in processes:
        y = p[0]
        avg = float(p[1])
        years.append(y)
        avgs.append(avg)
    return [years, avgs] 

def displayAvgProcessDurationByJudge(cursor):
    start = tm.time()
    [judges, avgs] = getAvgProcessDurationByJudge(cursor)
    displayTable(judges, avgs, "Giudice incaricato del processo", "Durata media in giorni", 15)
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgProcessDurationByJudge(cursor):
    tot_avg = float(getDataFromDatabase(cursor, "SELECT AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), dataInizio)) AS durata FROM processifiniti AS p")[0][0])
    [years, y_avgs] = getAvgProcessDurationByYear(cursor)
    processes = getDataFromDatabase(cursor, "SELECT giudice, YEAR(p.dataInizio), AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), p.dataInizio)) FROM processifiniti AS p WHERE giudice IN (SELECT giudice FROM processifiniti GROUP BY giudice HAVING COUNT(*) > 100) GROUP BY giudice, YEAR(p.dataInizio) ORDER BY giudice, YEAR(p.dataInizio)")
    judges = []
    avgs = []
    counts = []
    for p in processes:
        j = p[0]
        y = int(p[1])
        y_avg = y_avgs[years.index(y) - 1]
        if j not in judges:
            judges.append(j)  
            avgs.append(0)
            counts.append(0)
        pos = judges.index(j) 
        avg = float(p[2]) * tot_avg / y_avg
        count = counts[pos]
        newAvg = (((avgs[pos] * count) + avg) / (count + 1))
        counts[pos] = count + 1
        avgs[pos] = newAvg 
    return [judges, avgs]  
  
def displayAvgProcessDurationBySubject(cursor):
    start = tm.time()
    [subjects, avgs] = getAvgProcessDurationBySubject(cursor)
    displayTable(subjects, avgs, "Materia di discussione del processo", "Durata media in giorni", 15)
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgProcessDurationBySubject(cursor):
    tot_avg = float(getDataFromDatabase(cursor, "SELECT AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), dataInizio)) AS durata FROM processifiniti AS p")[0][0])
    [years, y_avgs] = getAvgProcessDurationByYear(cursor)
    processes = getDataFromDatabase(cursor, "SELECT materia, YEAR(p.dataInizio), AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), p.dataInizio)) FROM processifiniti AS p WHERE materia IN (SELECT materia FROM processifiniti GROUP BY materia HAVING COUNT(*) > 100) GROUP BY materia, YEAR(p.dataInizio) ORDER BY materia, YEAR(p.dataInizio)")
    subjects = []
    avgs = []
    counts = []
    for p in processes:
        s = p[0]
        y = int(p[1])
        y_avg = y_avgs[years.index(y) - 1]
        if s not in subjects:
            subjects.append(s)  
            avgs.append(0)
            counts.append(0)
        pos = subjects.index(s) 
        avg = float(p[2]) * tot_avg / y_avg
        count = counts[pos]
        newAvg = (((avgs[pos] * count) + avg) / (count + 1))
        counts[pos] = count + 1
        avgs[pos] = newAvg 
    return [subjects, avgs] 

def displayAvgProcessDurationBySection(cursor):
    start = tm.time()
    [sections, avgs] = getAvgProcessDurationBySection(cursor)
    displayPlot(sections, avgs, 10, "Sezione del Tribunale di Milano", "[giorni]", "Durata media processi in base alla sezione")
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgProcessDurationBySection(cursor):
    tot_avg = float(getDataFromDatabase(cursor, "SELECT AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), dataInizio)) AS durata FROM processifiniti AS p")[0][0])
    [years, y_avgs] = getAvgProcessDurationByYear(cursor)
    processes = getDataFromDatabase(cursor, "SELECT sezione, YEAR(p.dataInizio), AVG(DATEDIFF((SELECT e.data FROM eventi AS e WHERE e.numProcesso = p.numProcesso AND e.statoFinale = 'DF' AND e.statoIniziale <> 'DF' AND e.fase = 4), p.dataInizio)) FROM processifiniti AS p GROUP BY sezione, YEAR(p.dataInizio) ORDER BY sezione, YEAR(p.dataInizio)")
    sections = []
    avgs = []
    counts = []
    for p in processes:
        s = p[0]
        y = int(p[1])
        y_avg = y_avgs[years.index(y) - 1]
        if s not in sections:
            sections.append(s)  
            avgs.append(0)
            counts.append(0)
        pos = sections.index(s) 
        avg = float(p[2]) * tot_avg / y_avg
        count = counts[pos]
        newAvg = (((avgs[pos] * count) + avg) / (count + 1))
        counts[pos] = count + 1
        avgs[pos] = newAvg 
    return [sections, avgs]     

def displayAvgPhasesDuration(cursor):
    start = tm.time()
    [phases, avgs] = getAvgPhasesDuration(cursor)
    displayPlot(phases, avgs, 6, "Fasi del processo", "[giorni]", "Durata media fasi del processo")
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgPhasesDuration(cursor):
    processes = getDataFromDatabase(cursor, "SELECT e.fase, DATEDIFF((SELECT data FROM eventi WHERE numEvento = (SELECT MIN(ev.numEvento) FROM eventi as ev WHERE ((ev.fase = e.fase + 1) OR (ev.fase = 4 AND ev.statoFinale = 'DF')) AND ev.numProcesso = e.numProcesso)), e.data) AS durata FROM eventi AS e WHERE e.numEvento = (SELECT MIN(ev.numEvento) FROM eventi as ev WHERE e.numProcesso = ev.numProcesso AND e.fase = ev.fase AND e.numProcesso IN (SELECT numProcesso FROM processiFiniti) AND e.numProcesso NOT IN (SELECT DISTINCT numProcesso FROM eventi AS e2 WHERE e2.fase > ANY (SELECT ev2.fase FROM eventi AS ev2 WHERE ev2.numProcesso = e2.numProcesso AND ev2.numEvento > e2.numEvento))) AND e.fase < 5 ORDER BY e.numProcesso, e.fase")
    phases = ["1 - Inizio processo", "2 - Fase introduttiva", "3 - Fase trattiva", "4 - Fase decisoria"]
    avgs = [0] * 4
    counts = [0] * 4
    for p in processes:
        phase = int(p[0] - 1)
        avg = float(p[1])
        count = counts[phase]
        newAvg = (((avgs[phase] * count) + avg) / (count + 1))
        counts[phase] = count + 1
        avgs[phase] = newAvg   
    return [phases, avgs] 

def displayAvgStatesDuration(cursor):
    start = tm.time()
    [states, avgs] = getAvgStatesDuration(cursor)
    displayPlot(states, avgs, 10, "Stati del processo", "[giorni]", "Durata media stati del processo")
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgStatesDuration(cursor):
    processes = getDataFromDatabase(cursor, "SELECT e.statoFinale, DATEDIFF((SELECT data FROM eventi WHERE numEvento = (SELECT min(ev.numEvento) FROM eventi AS ev WHERE ev.numProcesso = e.numProcesso AND ev.statoiniziale = e.statofinale AND ev.data >= e.data)), e.data) AS durata FROM eventi AS e WHERE e.statoiniziale <> e.statofinale AND statofinale <> 'DF' AND fase < 5 ORDER BY e.numProcesso, e.numEvento")
    states = []
    avgs = []
    counts = []
    for p in processes:
        s = p[0]
        if s not in states:
            states.append(s)  
            avgs.append(0)
            counts.append(0)
        pos = states.index(s) 
        avg = float(0)
        if p[2] is not None:
            avg = float(p[1])
        count = counts[pos]
        newAvg = (((avgs[pos] * count) + avg) / (count + 1))
        counts[pos] = count + 1
        avgs[pos] = newAvg
    i = 0    
    while i < (len(counts)): 
        if counts[i] < 10:
            states.pop(i)  
            avgs.pop(i)  
            counts.pop(i)
        else:
            states[i] = str(states[i]) + " (" + str(counts[i]) + " volte)"
            i = i + 1         
    return [states, avgs]

def displayAvgEventsDuration(cursor):
    start = tm.time()
    [events, avgs] = getAvgEventsDuration(cursor)
    displayPlot(events, avgs, 10, "Eventi in un processo", "[giorni]", "Durata media eventi in un processo")
    #displayTable(events, avgs, "Eventi in un processo", "Durata dell'evento in giorni", len(events))
    print("--- %s seconds ---" % (tm.time() - start))

def getAvgEventsDuration(cursor):
    processes = getDataFromDatabase(cursor, "SELECT e.codice, DATEDIFF((SELECT data FROM eventi WHERE numEvento = (SELECT min(ev.numEvento) FROM eventi AS ev WHERE ev.numProcesso = e.numProcesso AND ev.statoiniziale <> e.statofinale AND ev.data >= e.data)), e.data) AS durata FROM eventi AS e WHERE e.statoiniziale = e.statofinale AND statofinale <> 'DF' AND fase < 5 ORDER BY e.numProcesso, e.numEvento")
    events = []
    avgs = []
    counts = []
    for p in processes:
        e = p[0]
        if e not in events:
            events.append(e)  
            avgs.append(0)
            counts.append(0)
        pos = events.index(e) 
        avg = float(0)
        if p[2] is not None:
            avg = float(p[1])
        count = counts[pos]
        newAvg = (((avgs[pos] * count) + avg) / (count + 1))
        counts[pos] = count + 1
        avgs[pos] = newAvg
    i = 0    
    while i < (len(counts)): 
        if counts[i] < 100:
            events.pop(i)  
            avgs.pop(i)  
            counts.pop(i)
        else:
            i = i + 1         
    return [events, avgs]

def displayAvgProcessDurationOfYearByMonth(cursor, year):
    findProcesses = "SELECT MONTH(dataInizio), AVG(DATEDIFF(inizioFase5, dataInizio)) FROM processifiniti WHERE anno = " + str(year) + " GROUP BY MONTH(dataInizio) ORDER BY MONTH(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    month = []
    avgs = []
    max = 0.0
    min = processes[0][1]
    for p in processes:
        month.append(months[p[0] - 1])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(month, avgs, c = 'black') 
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min - 100), int(max + 100), 100))
    plt.xlabel("Mese inizio processo")         
    plt.ylabel("[giorni]")   
    plt.title("Durata media processi nell'anno " + str(year) + " in base alla settimana di inizio") 
    plt.show()  

def displayAvgProcessDurationOfJudgeByMonth(cursor, judge):
    findDurationEvent = "SELECT MONTH(dataInizio), AVG(DATEDIFF(inizioFase5, dataInizio)) FROM processifiniti WHERE giudice = '" + judge + "' GROUP BY MONTH(dataInizio) ORDER BY MONTH(datainizio)"
    cursor.execute(findDurationEvent)
    processes = cursor.fetchall()  
    month = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(p[1])
        month.append(months[p[0] - 1])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(month, avgs, c = 'black')   
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Mese inizio processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media processi del giudice " + judge) 
    plt.show()  

def displayAvgProcessDurationOfSubjectByMonth(cursor, subject):
    findDurationEvent = "SELECT MONTH(dataInizio), AVG(DATEDIFF(inizioFase5, dataInizio)) FROM processifiniti WHERE materia = '" + subject + "' GROUP BY MONTH(dataInizio) ORDER BY MONTH(datainizio)"
    cursor.execute(findDurationEvent)
    processes = cursor.fetchall()  
    month = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(p[1])
        month.append(months[p[0] - 1])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(month, avgs, c = 'black') 
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Mese inizio processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media processi di materia " + subject) 
    plt.show() 

def displayAvgProcessDurationOfSectionByMonth(cursor, section):
    findDurationEvent = "SELECT MONTH(dataInizio), AVG(DATEDIFF(inizioFase5, dataInizio)) FROM processifiniti WHERE sezione = '" + section + "' GROUP BY MONTH(dataInizio) ORDER BY MONTH(datainizio)"
    cursor.execute(findDurationEvent)
    processes = cursor.fetchall()  
    month = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(p[1])
        month.append(months[p[0] - 1])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(month, avgs, c = 'black')
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Mese inizio processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media processi della sezione " + section + " del tribunale di Milano") 
    plt.show() 

def displayAvgPhaseDurationByMonth(cursor, phase):
    month = []
    avgs = []
    min = 1000.0
    max = 0.0
    for i in range(12):
        findDurationPhase = "SELECT DATEDIFF(MAX(data), MIN(data)) FROM eventi WHERE fase = " + str(phase + 1) + " GROUP BY numProcesso HAVING MONTH(MIN(data)) = " + str(i + 1)
        cursor.execute(findDurationPhase)
        processes = cursor.fetchall()
        sum = 0
        for p in processes:
            sum = p[0] + sum
        month.append(months[i])
        avg = sum / len(processes) 
        avgs.append(avg) 
        if avg < min:
            min = avg
        if avg > max:
            max = avg    
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)     
    plt.plot(month, avgs, c = 'black') 
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Mese inizio processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media fase " + str(phase)) 
    plt.show()  

def displayAvgEventDurationByMonth(cursor, event):
    findDurationEvent = "SELECT MONTH(e.data), AVG(DATEDIFF((SELECT MIN(ev.data) AS durataMedia FROM eventi AS ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data AND ev.statoIniziale = e.statoFinale), e.data)) FROM eventi AS e WHERE e.codice = '" + event + "' GROUP BY MONTH(e.data) ORDER BY MONTH(e.data)"
    cursor.execute(findDurationEvent)
    processes = cursor.fetchall()  
    month = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(0)
        if p[1] is not None:
            avg = float(p[1])
        month.append(months[p[0] - 1])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(month, avgs, c = 'black') 
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min), int(max), int((max - min) / 20)))
    plt.xlabel("Mese inizio evento")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media evento " + event) 
    plt.show()  

def displayNumberOfEventsOfLongestProcess(cursor):
    findCountEvents = "SELECT codice, COUNT(*) FROM eventi WHERE numProcesso IN  (SELECT numProcesso FROM processiFIniti WHERE DATEDIFF(dataFine, dataInizio) > (SELECT DATEDIFF(dataFine, dataInizio) FROM processifiniti ORDER BY DATEDIFF(dataFIne, dataInizio) DESC LIMIT 1 OFFSET 100)) GROUP BY codice"
    cursor.execute(findCountEvents)
    events = cursor.fetchall()  
    counts = []
    codes = []
    max = 0
    min = int(events[0][1])
    for e in events:
        count = e[1]
        codes.append(e[0])
        counts.append(count)
        if count > 130:
            plt.text(e[0], count, e[0])
        if count > max:
            max = count
        if count < min:
            min = count  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.plot(codes, counts, c = 'black')  
    plt.xticks([], [])
    plt.yticks(range(min, max,  int((max - min) / 20)))
    plt.xlabel("Eventi")         
    plt.ylabel("[nr]")
    plt.title("Numero di eventi presenti nei 100 processi piu lunghi") 
    plt.show()

def displayEventDurationPercProcessDuration(cursor):
    findPercEvents = "SELECT e.codice, AVG(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data AND ev.statoIniziale = e.statoFinale), e.data) * 100 /  (SELECT DATEDIFF(dataFIne, dataInizio) FROM processifiniti AS p WHERE e.numProcesso = p.numProcesso)) AS durataPerc FROM eventi AS e GROUP BY e.codice"
    cursor.execute(findPercEvents)
    events = cursor.fetchall()  
    percs = []
    codes = []
    max = 0
    min = float(events[0][1])
    for e in events:
        perc = float(0)
        if e[1] is not None:
            perc = float(e[1])
        codes.append(e[0])
        percs.append(perc)
        if perc > 25:
            plt.text(e[0], perc, e[0])
        if perc > max:
            max = perc
        if perc < min:
            min = perc  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.plot(codes, percs, c = 'black')  
    plt.xticks([], [])
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Eventi")         
    plt.ylabel("[%]")
    plt.title("Event duration percentage of process duration") 
    plt.show()

try:
    connection = connectToDatabase()
    cursor = connection.cursor(buffered = True)
    window = tk.Tk()
    #width = window.winfo_screenwidth()               
    #height = window.winfo_screenheight()               
    #window.geometry("%dx%d" % (width, height))
    window.geometry("600x480")
    window.title("Tesi")     
    window.configure(background="white")
    process_btn = tk.Button(window, text = "Processi", command = lambda: displayAllProcesses(cursor))   
    process_btn.grid(row = 0, column = 0, padx = 100, pady = 20)  
    event_process_btn = tk.Button(window, text = "Eventi dei processi", command = lambda: displayProcessEventsOfYear(cursor, 2019))   
    event_process_btn.grid(row = 0, column = 1, padx = 60, pady = 20)   
    process_duration_btn = tk.Button(window, text = "Durata processi", command = lambda: displayAvgProcessDurationByMonth(cursor))   
    process_duration_btn.grid(row = 1, column = 0, padx = 100, pady = 20)    
    phase_duration_btn = tk.Button(window, text = "Fasi del processo", command = lambda: displayAvgPhasesDuration(cursor))   
    phase_duration_btn.grid(row = 1, column = 1, padx = 60, pady = 20)     
    state_duration_btn = tk.Button(window, text = "Stati del processo", command = lambda: displayAvgStatesDuration(cursor))   
    state_duration_btn.grid(row = 2, column = 0, padx = 100, pady = 20)     
    event_duration_btn = tk.Button(window, text = "Eventi del processo", command = lambda: displayAvgEventsDuration(cursor))   
    event_duration_btn.grid(row = 2, column = 1, padx = 60, pady = 20)    
    judge_duration_btn = tk.Button(window, text = "Giudici processi", command = lambda: displayAvgProcessDurationByJudge(cursor))   
    judge_duration_btn.grid(row = 3, column = 0, padx = 100, pady = 20)    
    section_duration_btn = tk.Button(window, text = "Sezione del processo", command = lambda: displayAvgProcessDurationBySection(cursor))   
    section_duration_btn.grid(row = 3, column = 1, padx = 60, pady = 20)     
    subject_duration_btn = tk.Button(window, text = "Materie del processo", command = lambda: displayAvgProcessDurationBySection(cursor))   
    subject_duration_btn.grid(row = 4, column = 0, padx = 60, pady = 20)                                     

    window.mainloop()

except cnx.Error as e:
        print("ERROR:", e)  

