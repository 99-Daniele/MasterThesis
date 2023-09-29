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

def displayProcesses(cursor):
    findNrProcesses = "SELECT numProcesso FROM processifiniti"
    cursor.execute(findNrProcesses)
    nrProcesses = cursor.fetchall()
    for nr in nrProcesses:
        findProcesses = "SELECT * FROM eventi WHERE numProcesso = " + str(nr[0])
        cursor.execute(findProcesses)
        processes = cursor.fetchall()
        for p in processes:
            plt.scatter(p[4], p[1], s = 20, c = colors[p[8] - 1]) 
    plt.xlabel("Data inizio processo")   
    plt.title("Elenco eventi") 
    
def displayYearProcesses(cursor, year):
    findNrProcesses = "SELECT numProcesso FROM processifiniti WHERE anno = " + year
    cursor.execute(findNrProcesses)
    nrProcesses = cursor.fetchall()
    plt.yticks(range(10), rotation = 90)  
    for nr in nrProcesses:
        findProcesses = "SELECT * FROM eventi WHERE numProcesso = " + str(nr[0]) + " AND YEAR(data) = " + year
        cursor.execute(findProcesses)
        processes = cursor.fetchall()
        for p in processes:
            plt.scatter(p[4], p[1], s = 20, c = colors[p[8] - 1]) 
    plt.xlim([dtm.datetime(int(year), 1, 1), dtm.datetime(int(year), 12, 1)])  
    plt.xlabel("Data inizio processo")  
    plt.title("Elenco eventi nell'anno " + year ) 

def displayAvgProcessesDuration(cursor):
    findProcesses = "SELECT MONTH(dataInizio), AVG(((YEAR(dataFine) - YEAR(dataInizio)) * 365) + ((MONTH(dataFine) - MONTH(dataInizio)) * 30) + DAY(dataFine) - DAY(dataInizio)) FROM processifiniti GROUP BY MONTH(dataInizio) ORDER BY MONTH(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    dates = []
    avgs = []
    max = 0
    min = processes[0][1]
    for p in processes:
        dates.append(dtm.datetime(2000, p[0], 1))
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]    
    plt.plot(dates, avgs, c = 'black')   
    plt.xlim([dtm.datetime(2000, 1, 1), dtm.datetime(2000, 12, 1)]) 
    plt.yticks(range(int(min - 100), int(max + 100), 100))
    plt.xlabel("Data inizio processo")         
    plt.ylabel("[giorni]")
    plt.title("Durata media processi per ogni mese") 

def displayAvgProcessesDurationOfYear(cursor, year):
    findProcesses = "SELECT MONTH(dataInizio), AVG(((YEAR(dataFine) - YEAR(dataInizio)) * 365) + ((MONTH(dataFine) - MONTH(dataInizio)) * 30) + DAY(dataFine) - DAY(dataInizio)) FROM processifiniti WHERE anno = " + year + " GROUP BY MONTH(dataInizio) ORDER BY MONTH(dataInizio)"
    cursor.execute(findProcesses)
    processes = cursor.fetchall()
    dates = []
    avgs = []
    max = 0.0
    min = processes[0][1]
    for p in processes:
        dates.append(dtm.datetime(int(year), p[0], 1))
        avgs.append(p[1])
        if p[1] > max:
            max = p[1]
        if p[1] < min:
            min = p[1]    
    plt.plot(dates, avgs, c = 'black')   
    plt.xlim([dtm.datetime(int(year), 1, 1), dtm.datetime(int(year), 12, 1)]) 
    plt.yticks(range(int(min - 100), int(max + 100), 100))
    plt.xlabel("Data inizio processo")         
    plt.ylabel("[giorni]")   
    plt.title("Durata media processi nell'anno " + year + " per ogni mese") 

def displayPhaseDuration(cursor, phase):
    months = []
    avgs = []
    min = 1000.0
    max = 0.0
    for i in range(12):
        findDurationPhase = "SELECT (YEAR(MAX(data)) - YEAR(MIN(data))) * 365 + (MONTH(MAX(data)) - MONTH(MIN(data))) * 30 + (DAY(MAX(data)) - DAY(MIN(data))) FROM eventi WHERE fase = " + str(phase + 1) + " GROUP BY numProcesso HAVING MONTH(MIN(data)) = " + str(i + 1)
        cursor.execute(findDurationPhase)
        processes = cursor.fetchall()
        sum = 0
        for p in processes:
            sum = p[0] + sum
        months.append(dtm.datetime(2000, i + 1, 1))
        avg = sum / len(processes) 
        avgs.append(avg) 
        if avg < min:
            min = avg
        if avg > max:
            max = avg        
    plt.plot(months, avgs, c = 'black')   
    plt.xlim([dtm.datetime(2000, 1, 1), dtm.datetime(2000, 12, 1)]) 
    plt.yticks(range(int(min - 10), int(max + 10), 10))
    plt.xlabel("Data inizio processo")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media fase " + str(phase)) 

def displayEventsDuration(cursor):
    findDurationEvents = "SELECT e.codice, AVG(DATEDIFF((SELECT MIN(ev.data) FROM eventi as ev WHERE ev.numProcesso = e.numProcesso AND ev.data > e.data), e.data)) FROM eventi as e GROUP BY e.codice ORDER BY e.codice"
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
    plt.plot(codes, avgs, c = 'black')   
    plt.xticks([], [])
    plt.yticks(range(int(min - 10), int(max + 10), 100))
    plt.xlabel("Codice evento")         
    plt.ylabel("[giorni]") 
    plt.title("Durata media eventi")     

try:
    connection = connectToDatabase()
    cursor = connection.cursor(buffered = True) 
    plt.grid()
    displayEventsDuration(cursor)
    plt.show()  

except cnx.Error as e:
        print("ERROR:", e)  

#SELECT MONTH(dataInizio), YEAR(dataInizio), AVG(((YEAR(dataFine) - YEAR(dataInizio)) * 365) + ((MONTH(dataFine) - MONTH(dataInizio)) * 30) + DAY(dataFine) - DAY(dataInizio)) FROM tribunalisemplice.processifiniti GROUP BY MONTH(dataInizio), YEAR(dataInizio)           
