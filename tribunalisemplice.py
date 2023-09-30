import mysql.connector as cnx
import matplotlib.pyplot as plt
import datetime as dtm

colors = ['blue', 'orange', 'red', 'green', 'purple']
months = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

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
    days = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        days.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]    
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0) 
    plt.plot(days, avgs, c = 'black')   
    plt.xticks(range(1, 366, 10))
    plt.yticks(range(int(min), int(max), 100))
    plt.xlabel("Giorno di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giorno di inizio")
    plt.show()  

def displayAvgProcessDurationByWeek(cursor):
    findProcesses = "SELECT WEEK(dataInizio, 7), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY WEEK(dataInizio, 7) ORDER BY WEEK(dataInizio, 7)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    weeks = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        weeks.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(weeks, avgs, c = 'black')   
    plt.xticks(range(1, 54, 1))
    plt.yticks(range(int(min), int(max), 50))
    plt.xlabel("Settimana inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base alla settimana di inizio") 
    plt.show()  

def displayAvgProcessDurationByDayOfMonth(cursor):
    findProcesses = "SELECT DAY(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti WHERE DAY(dataInizio) < 29 GROUP BY DAY(dataInizio) ORDER BY DAY(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    daysOfMonth = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        daysOfMonth.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]   
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)  
    plt.plot(daysOfMonth, avgs, c = 'black')   
    plt.xticks(range(1, 29, 1))
    plt.yticks(range(int(min), int(max), 10))
    plt.xlabel("Giorno del mese di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giorno del mese di inizio") 
    plt.show()  

def displayAvgProcessDurationByMonth(cursor):
    findProcesses = "SELECT MONTH(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY MONTH(dataInizio) ORDER BY MONTH(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    months = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        months.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)  
    plt.plot(months, avgs, c = 'black')   
    plt.xticks(range(1, 13, 1))
    plt.yticks(range(int(min), int(max), 10))
    plt.xlabel("Mese di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al mese di inizio")
    plt.show()  

def displayAvgProcessDurationByDayOfWeek(cursor):
    findProcesses = "SELECT DAYOFWEEK(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY DAYOFWEEK(dataInizio) ORDER BY DAYOFWEEK(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    daysOfWeek = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        daysOfWeek.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1] 
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)    
    plt.plot(daysOfWeek, avgs, c = 'black')   
    plt.xticks(range(1, 8, 1))
    plt.yticks(range(int(min), int(max), 50))
    plt.xlabel("Giorno della settimana di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base al giorno della settimana di inizio")
    plt.show()  

def displayAvgProcessDurationByYear(cursor):
    findProcesses = "SELECT YEAR(dataInizio), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti GROUP BY YEAR(dataInizio) ORDER BY YEAR(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    years = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        years.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(years, avgs, c = 'black')   
    plt.xticks(range(2007, 2023, 1))
    plt.yticks(range(int(min), int(max), 100))
    plt.xlabel("Anno di inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base all'anno di inizio")
    plt.show()  

def displayAvgProcessDurationOfYear(cursor, year):
    findProcesses = "SELECT WEEK(dataInizio, 7), AVG(DATEDIFF(dataFine, dataInizio)) FROM processifiniti WHERE anno = " + str(year) + " GROUP BY WEEK(dataInizio, 7) ORDER BY WEEK(dataInizio, 7)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    weeks = []
    avgs = []
    max = 0.0
    min = processes[0][1]
    for p in processes:
        weeks.append(p[0])
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)   
    plt.plot(weeks, avgs, c = 'black')    
    plt.xticks(range(1, 54, 1))
    plt.yticks(range(int(min - 100), int(max + 100), 100))
    plt.xlabel("Settimana inizio processo")         
    plt.ylabel("[giorni]")   
    plt.title("Durata media processi nell'anno " + str(year) + " in base alla settimana di inizio") 
    plt.show()  

def displayPhaseDuration(cursor, phase):
    months = []
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
        months.append(i)
        avg = sum / len(processes) 
        avgs.append(avg) 
        if avg < min:
            min = avg
        if avg > max:
            max = avg    
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)     
    plt.plot(months, avgs, c = 'black')   
    plt.xticks(range(1, 13, 1))
    plt.yticks(range(int(min), int(max), 10))
    plt.xlabel("Data inizio processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media fase " + str(phase)) 
    plt.show()  

def displayAvgEventsDuration(cursor):
    findDurationEvents = "SELECT e.codice, AVG(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data), e.data)), COUNT(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data), e.data)) FROM eventi as e GROUP BY e.codice ORDER BY e.codice"
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
    plt.yticks(range(int(min), int(max), 100))
    plt.xlabel("Codice evento")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media eventi")     
    plt.show()  

def displayAvgEventDuration(cursor, event):
    findDurationEvent = "SELECT MONTH(e.data), AVG(DATEDIFF((SELECT MIN(ev.data) as durataMedia FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data), e.data)) FROM eventi as e WHERE e.codice = '" + event + "' GROUP BY MONTH(e.data) ORDER BY MONTH(e.data)"
    cursor.execute(findDurationEvent)
    processes = cursor.fetchall()  
    months = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(0)
        if p[1] is not None:
            avg = float(p[1])
        months.append(p[0])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(months, avgs, c = 'black')   
    plt.xticks(range(1, 13, 1))
    plt.yticks(range(int(min), int(max), 10))
    plt.xlabel("Data inizio evento")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media evento " + event) 
    plt.show()  

def displayAvgEventsDurationByMonth(cursor):
    findDurationEvents = "SELECT MONTH(e.data), AVG(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data), e.data)) FROM eventi as e GROUP BY MONTH(e.data) ORDER BY MONTH(e.data)"
    cursor.execute(findDurationEvents)
    processes = cursor.fetchall()  
    months = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        avg = float(0)
        if p[1] is not None:
            avg = float(p[1])
        months.append(p[0])
        avgs.append(avg)
        if avg > max:
            max = avg
        if avg < min:
            min = avg  
    plt.grid()
    plt.subplots_adjust(0.07, 0.07, 0.97, 0.95) 
    plt.margins(0, 0)
    plt.plot(months, avgs, c = 'black')   
    plt.xticks(range(1, 13, 1))
    plt.yticks(range(int(min), int(max), 10))
    plt.xlabel("Data inizio evento")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media eventi in base al mese") 
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
    plt.yticks(range(int(min), int(max), 100))
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
    plt.yticks(range(int(min), int(max), 100))
    plt.xlabel("Materia di discussione del processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi in base alla materia") 
    plt.show() 

try:
    connection = connectToDatabase()
    cursor = connection.cursor(buffered = True)
    while True:
        print("Press number to make chosen graph:\n1 - All processes\n2 - Processes of selected year\n3 - Average process duration\n4 - Average phase duration\n5 - Average events duration\n0 - End")
        c = int(input())
        if c == 1:
            displayAllProcesses(cursor)
        elif c == 2:
            print("Choose one year (2007-2022): ") 
            y = int(input())
            while y < 2007 or y > 2022:
                print("You have chosen a wrong year!\nChoose one year (2007-2022): ")
                y = int(input())
            displayProcessesOfYear(cursor, y)
        elif c == 3:
            print("Do you want to group by:\n1 - Date\n2 - Judge\n3 - Suject")
            c2 = int(input())
            while c2 < 1 or c2 > 3:
                print("Wrong input!\nDo you want to group by:\n1 - Date\n2 - Judge\n3 - Suject")   
                c2 = int(input())
            if c2 == 1:
                print("Do you want to group by:\n1 - Day of the Year\n2 - Week\n3 - Day of Month\n4 - Month\n5 - Day of week\n6 - Year")
                c3 = int(input())
                while c3 < 1 or c3 > 6:
                    print("Wrong input!\nDo you want to group by:\n1 - Day of the Year\n2 - Week\n3 - Day of Month\n4 - Month\n5 - Day of week\n6 - Year")
                    c3 = int(input())
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
            else:
                displayAvgProcessDurationBySubject(cursor)
        elif c == 4:
            print("Which phase you want to see (1 - 5)?")
            c2 = int(input())
            while c2 < 1 or c2 > 5:
                print("Wrong input!\nWhich phase you want to see (1 - 5)?")
                c2 = int(input())
            displayPhaseDuration(cursor, c2)
        elif c == 5:
            displayAvgEventsDuration(cursor)
        else:
            break                                                    

except cnx.Error as e:
        print("ERROR:", e)  
