import mysql.connector as cnx
import matplotlib.pyplot as plt
import datetime as dtm

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

def displayAllProcesses(cursor):
    findNrProcesses = "SELECT numProcesso FROM processifiniti"
    cursor.execute(findNrProcesses)
    nrProcesses = cursor.fetchall()
    for nr in nrProcesses:
        findProcesses = "SELECT * FROM eventi WHERE numProcesso = " + str(nr[0])
        cursor.execute(findProcesses)
        processes = cursor.fetchall()
        for p in processes:
            plt.scatter(p[4], p[1], s = 20, c = colors[p[8] - 1]) 
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0) 
    plt.xlabel("Data inizio processo") 
    plt.ylabel("Numero processo")   
    plt.title("Elenco di tutti i processi finiti") 
    plt.show()  
    
def displayProcessesOfYear(cursor, year):
    findNrProcesses = "SELECT numProcesso FROM processifiniti WHERE anno = " + str(year)
    cursor.execute(findNrProcesses)
    nrProcesses = cursor.fetchall()
    plt.yticks(range(10), rotation = 90)  
    for nr in nrProcesses:
        findProcesses = "SELECT * FROM eventi WHERE numProcesso = " + str(nr[0]) + " AND YEAR(data) = " + str(year)
        cursor.execute(findProcesses)
        processes = cursor.fetchall()
        for p in processes:
            plt.scatter(p[4], p[1], s = 20, c = colors[p[8] - 1]) 
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0) 
    plt.xlim([dtm.date(year, 1, 1), dtm.date(year, 12, 1)])  
    plt.xlabel("Data inizio processo")  
    plt.ylabel("Numero processo")
    plt.title("Elenco processi iniziati nell'anno " + str(year)) 
    plt.show()  

def displayAvgProcessDurationByDay(cursor):
    findProcesses = "SELECT DAYOFYEAR(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY DAYOFYEAR(dataInizio) ORDER BY DAYOFYEAR(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    day = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        day.append(daysOfYear[p[0] - 1])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]    
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0) 
    plt.plot(day, avgs, c = 'black') 
    plt.xticks(weeks) 
    plt.xticks(fontsize = 5)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Giorno di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giorno di inizio")
    plt.show()  

def displayAvgProcessDurationByWeek(cursor):
    findProcesses = "SELECT WEEK(dataInizio, 7), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY WEEK(dataInizio, 7) ORDER BY WEEK(dataInizio, 7)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    week = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        week.append(weeks[p[0] - 1])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(week, avgs, c = 'black')
    plt.xticks(fontsize = 5)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Settimana inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base alla settimana di inizio") 
    plt.show()  

def displayAvgProcessDurationByDayOfMonth(cursor):
    findProcesses = "SELECT DAY(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY DAY(dataInizio) ORDER BY DAY(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    day = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        day.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]   
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)  
    plt.plot(day, avgs, c = 'black')  
    plt.xticks(range(1, 32, 1)) 
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Giorno del mese di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giorno del mese di inizio") 
    plt.show()  

def displayAvgProcessDurationByMonth(cursor):
    findProcesses = "SELECT MONTH(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY MONTH(dataInizio) ORDER BY MONTH(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    month = []
    avgs = []
    max = 0
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
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Mese di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al mese di inizio")
    plt.show()  

def displayAvgProcessDurationByDayOfWeek(cursor):
    findProcesses = "SELECT DAYOFWEEK(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY DAYOFWEEK(dataInizio) ORDER BY DAYOFWEEK(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    day = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        day.append(daysOfWeek[p[0] - 1])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1] 
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)    
    plt.plot(day, avgs, c = 'black')
    plt.xticks(fontsize = 8)
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Giorno della settimana di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giorno della settimana di inizio")
    plt.show()  

def displayAvgProcessDurationByYear(cursor):
    findProcesses = "SELECT YEAR(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY YEAR(dataInizio) ORDER BY YEAR(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    year = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        year.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(year, avgs, c = 'black')   
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Anno di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base all'anno di inizio")
    plt.show()  

def displayAvgProcessDurationByJudge(cursor):
    findDurationEvents = "SELECT giudice, AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY giudice"
    cursor.execute(findDurationEvents)
    processes = cursor.fetchall()  
    judges = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(p[1])
        judges.append(p[0])
        avgs.append(avg)
        if avg > 2500:
            plt.text(p[0], avg, p[0])
        if avg < 450:   
            plt.text(p[0], avg, p[0]) 
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.plot(judges, avgs, c = 'black')   
    plt.xticks([], [])
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Giudice assegnato al processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giudice") 
    plt.show()   

def displayAvgProcessDurationBySubject(cursor):
    findDurationEvents = "SELECT materia, AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY materia ORDER BY materia"
    cursor.execute(findDurationEvents)
    processes = cursor.fetchall()  
    subjects = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(p[1])
        subjects.append(p[0])
        avgs.append(avg)
        if avg > 2500:
            plt.text(p[0], avg, p[0])
        if avg < 350:   
            plt.text(p[0], avg, p[0]) 
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.plot(subjects, avgs, c = 'black')   
    plt.xticks([], [])
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Materia di discussione del processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base alla materia") 
    plt.show()

def displayAvgProcessDurationBySection(cursor):
    findDurationEvents = "SELECT sezione, AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY sezione ORDER BY sezione"
    cursor.execute(findDurationEvents)
    processes = cursor.fetchall()  
    subjects = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(p[1])
        subjects.append(p[0])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.plot(subjects, avgs, c = 'black')
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Sezione del tribunale")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base alla sezione di Milano del tribunale") 
    plt.show()      

def displayAvgPhasesDuration(cursor):
    phases = []
    avgs = []
    min = 1000.0
    max = 0.0
    for i in range(5):
        findDurationPhase = "SELECT DATEDIFF(MAX(data), MIN(data)) FROM eventi WHERE fase = " + str(i + 1) + " GROUP BY numProcesso"
        cursor.execute(findDurationPhase)
        processes = cursor.fetchall()
        sum = 0
        for p in processes:
            sum = p[0] + sum
        phases.append(i + 1)
        avg = sum / len(processes) 
        avgs.append(avg) 
        if avg < min:
            min = avg
        if avg > max:
            max = avg    
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)     
    plt.plot(phases, avgs, c = 'black')   
    plt.xticks(range(1, 6, 1))
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Fasi del processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media fasi del processo") 
    plt.show()

def displayAvgEventsDuration(cursor):
    findDurationEvents = "SELECT e.codice, AVG(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data AND ev.statoIniziale = e.statoFinale), e.data)), COUNT(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data), e.data)) FROM eventi as e GROUP BY e.codice ORDER BY e.codice"
    cursor.execute(findDurationEvents)
    processes = cursor.fetchall()  
    codes = []
    avgs = []
    max = float(0)
    min = float(processes[0][1])
    for p in processes:
        avg = float(0)
        if p[1] is not None:
            avg = float(p[1])
        codes.append(p[0])
        avgs.append(avg)
        if avg > 350:
            plt.text(p[0], avg, p[0])
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(codes, avgs, c = 'black')   
    plt.xticks([], [])
    plt.yticks(range(int(min), int(max),  int((max - min) / 20)))
    plt.xlabel("Codice evento")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media eventi")     
    plt.show() 

def displayAvgProcessDurationOfYearByMonth(cursor, year):
    findProcesses = "SELECT MONTH(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti WHERE anno = " + str(year) + " GROUP BY MONTH(dataInizio) ORDER BY MONTH(dataInizio)"
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
    findDurationEvent = "SELECT MONTH(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti WHERE giudice = '" + judge + "' GROUP BY MONTH(dataInizio) ORDER BY MONTH(datainizio)"
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
    findDurationEvent = "SELECT MONTH(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti WHERE materia = '" + subject + "' GROUP BY MONTH(dataInizio) ORDER BY MONTH(datainizio)"
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
    findDurationEvent = "SELECT MONTH(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti WHERE sezione = '" + section + "' GROUP BY MONTH(dataInizio) ORDER BY MONTH(datainizio)"
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
        month.append(months(i))
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
    findDurationEvent = "SELECT MONTH(e.data), AVG(DATEDIFF((SELECT MIN(ev.data) as durataMedia FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data AND ev.statoIniziale = e.statoFinale), e.data)) FROM eventi as e WHERE e.codice = '" + event + "' GROUP BY MONTH(e.data) ORDER BY MONTH(e.data)"
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

try:
    connection = connectToDatabase()
    cursor = connection.cursor(buffered = True)
    while True:
        c = int(input("Press number to make chosen graph:\n1 - Process events\n2 - Average process duration\n3 - Average phases duration\n4 - Average events duration\n5 - Duration by a chosen parameter\n0 - End\n"))
        if c == 1:
            c2 = int(input("1 - All Processes\n2 - Processes of selected year\n"))
            while c2 < 1 or c2 > 2:
                c2 = int(input("Wrong input!\n1 - All Processes\n2 - Processes of selected year\n"))
            if c2 == 1:
                displayAllProcesses(cursor)
            elif c2 == 2:
                y = int(input("Choose one year (2007-2022): "))
                while y < 2007 or y > 2022:
                    y = int(input("You have chosen a wrong year!\nChoose one year (2007-2022): "))
                displayProcessesOfYear(cursor, y)
        elif c == 2:
            c2 = int(input("Do you want to group by:\n1 - Date\n2 - Judge\n3 - Subject\n4 - Section\n"))
            while c2 < 1 or c2 > 4:
                c2 = int(input("Wrong input!\nDo you want to group by:\n1 - Date\n2 - Judge\n3 - Subject\n4 - Section\n"))
            if c2 == 1:
                c3 = int(input("Do you want to group by:\n1 - Day of the Year\n2 - Week\n3 - Day of Month\n4 - Month\n5 - Day of week\n6 - Year\n"))
                while c3 < 1 or c3 > 6:
                    c3 = int(input("Wrong input!\nDo you want to group by:\n1 - Day of the Year\n2 - Week\n3 - Day of Month\n4 - Month\n5 - Day of week\n6 - Year\n"))
                if c3 == 1:
                    displayAvgProcessDurationByDay(cursor)
                elif c3 == 2:
                    displayAvgProcessDurationByWeek(cursor)
                elif c3 == 3:
                    displayAvgProcessDurationByDayOfMonth(cursor)
                elif c3 == 4:
                    displayAvgProcessDurationByMonth(cursor)
                elif c3 == 5:
                    displayAvgProcessDurationByDayOfWeek(cursor)
                else:
                    displayAvgProcessDurationByYear(cursor)
            elif c2 == 2:
                displayAvgProcessDurationByJudge(cursor)
            elif c2 == 3:
                displayAvgProcessDurationBySubject(cursor)
            elif c2 == 4:    
                displayAvgProcessDurationBySection(cursor)
        elif c == 3:
            displayAvgPhasesDuration(cursor)
        elif c == 4:
            displayAvgEventsDuration(cursor)
        elif c == 5:
            c2 = int(input("What do you want to see?\n1 - Display process duration of chosen year by month\n2 - Display process duration of chosen judge by month\n3 - Display process duration of chosen subject by month\n4 - Display process duration of chosen section by month\n5 - Display chosen phase duration by month\n6 - Display chosen event duration by month\n"))  
            while c2 < 1 or c2 > 6:
                c2 = int(input("Wrong input!\nWhat do you want to see?\n1 - Display process duration of chosen year by month\n2 - Display process duration of chosen judge by month\n3 - Display process duration of chosen subject by month\n4 - Display process duration of chosen section by month\n5 - Display chosen phase duration by month\n6 - Display chosen event duration by month\n"))  
            if c2 == 1:
                y = int(input("Chose one year (2007-2022): "))
                while y < 2007 or y > 2022:
                    y = int(input("Wrong input!\nChose one year (2007-2022): "))
                displayAvgProcessDurationOfYearByMonth(cursor, y)
            elif c2 == 2:
                j = input("Chose judge: ")
                displayAvgProcessDurationOfJudgeByMonth(cursor, j) 
            elif c2 == 3:
                su = input("Chose subject: ")
                displayAvgProcessDurationOfSubjectByMonth(cursor, su) 
            elif c2 == 4:
                se = input("Chose section (01, 02, 03, 04, 05, PI, TI): ")
                while se != "01" and se != "02" and se != "03" and se != "04" and se != "05" and se != "PI" and se != "TI":
                    se = input("Wrong input!\nChose section (01, 02, 03, 04, 05, PI, TI): ")
                displayAvgProcessDurationOfSectionByMonth(cursor, se)
            elif c2 == 5:    
                p = int(input("Chose one phase (1-5): "))
                while p < 1 or p > 5:
                    p = int(input("Wrong input!\nChose one phase (1-5): "))
                displayAvgPhaseDurationByMonth(cursor, p)
            elif c2 == 6:    
                e = input("Chose one event: ")
                displayAvgEventDurationByMonth(cursor, e)
        else:
            break                                                    

except cnx.Error as e:
        print("ERROR:", e)  
