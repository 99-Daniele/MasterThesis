# Analysis of the Trials of the Civil Court of Milan


## Introduction

This project present the analysis of the Trials of the Civil Court of Milan.

The application acquires data from a database, converts them in table with the computation of durations, and allows the analysis thourght the visualization and comparison of data.

Moreover is present a predictor of unfinished trials duration, which 

Inoltre è presente un predittore della durata dei processi non finiti, of which it is possible to view the error of the calculated predicted values.

## Installation

Software is based on Python, 

Il software si basa su Python, therefore its installation is mandatory.

To install the required libraries, use the command:

```bash
pip install -r requirements.txt
```

## First usage

Upon first use, user will be asked to give credentials to connect to the database: host, username, password and database name.
The credentials will then be saved locally and at each subsequent login they will be retrieved from the 'utils/database/databaseCredentials.json' file without having to ask the user for them again.

Subsequently there will be the creation of the tables necessary for the analysis and the prediction of unfinished trials. This action may take some time, but it will be performed only the first time user interact with the application.

## Usage

Usage of the software is managed in the 'main.py' file. To start the analysis user need to type command:

```bash
python main.py
```

From the 'main.py' file it is possible to modify the use of the software by modifying the code on line 207 with the chosen function to execute.

The possibilities are always present in the 'main.py' file and are the following:
* displayAllEventsScatter(): display distribution of all events of the trial.
* displayPhaseEventsScatter(): display distribution of events that starts the phases of the trial.
* displayStateEventsScatter(): display distribution of events that starts the states of the trial.
* displayProcessComparison(): displays the duration of the trials and allows comparison based on various parameters, on the trial start date.
* displayPhaseComparison(): displays the duration of the phases of the trials and allows comparison based on various parameters, on the trial start date.
* displayStateComparison(): displays the duration of the states of the trials and allows comparison based on various parameters, on the trial start date.
* displayEventComparison(): displays the duration of the eventsof the trials and allows comparison based on various parameters, on the trial start date.
* displayTypeComparison(): displays the duration of trials, based on various parameters.
* displayStatesEvents(): displays the events that are part of each trial state.
* displayPhasesEvents(): displays the events and states that are part of each trial phase.
* displayStatesSequence(): displays the states following each trial state.
* displayPhaseSequence(): displays the phases following each trial phase.
* displayEventSequence(): displays the events following each trial event.
* displayStatePreferences(): displays the list of all type of trial states and allows user to modify some parameters and choose the most important ones.
* displayEventPreferences(): displays the list of all type of trial events and allows user to choose the most important ones.
* displaySubjectPreferences(): displays the list of all type of trial subjects and allows user to choose the most important ones.
* displaySectionPreferences(): displays the list of sections of the Court of Milan and allows user to choose the most important ones.
* displayProcessTypePreferences(): displays the list of trial types and allows user to choose the most important ones.
* displayPredictionError(): display the error related to the unfinished trials duration predictor.
* restartData(): resets the tables to their initial state, removing any user choices. This function runs on first use, and user need to run it every time the database is modified. Otherwise, there is no need to perform it.
* refreshData(): recalculate tables based on user choices. It runs automatically every time the user changes tables from the related page.
* predictTotalTest(): use the predictor on all finished trials, with a model based on 100% of finished trials, to calculate its prediction error.
* predict8020Test(): use the predictor on 20% finished trials, with a model based on 80% of finished trials, to calculate its prediction error.
* predictDuration(): runs the predictor on unfinished trials, calculating their predicted duration.
* startApp(): runs the app for the dynamic use of the software. In fact, this is the standard usage of the application. Through pages and links it is possible to view all types of graphs, without having to modify the 'main.py' file.

Whenever is used the command
```bash
python main.py
```
in which Dash is started to view the graphs, user have simply to click on the link or go to the page ['127.0.0.1:8050/'](http://127.0.0.1:8050/) to use the application.

## Author

[Daniele Cicala](https://github.com/99-Daniele)


## ITA

# Analisi dei Processi del Tribunale Civile di Milano


## Introduzione

Questo progetto presenta l'analisi dei Processi del Tribunale Civile di Milano.

Il software acquisce i dati da un database, li converte in tabelle per il calcolo delle durate, e permette di effettuare l'analisi tramite la visualizzazione e il confronto dei dati.

Inoltre è presente un predittore della durata dei processi non finiti, di cui è possibile visualizzarne l'errore dei valori predetti calcolati.

## Installazione

Il software si basa su Python, pertanto è necessaria una sua installazione.

Per installare le librerie richieste, utilizzare il comando:

```bash
pip install -r requirements.txt
```

## Primo utilizzo

Al primo utilizzo verrano richieste le credenziali per la connessione al database: host, username, password e nome del database.
Le credenziali verrano salvate localmente e ad ogni accesso successivo verrano recuperate dal file 'utils/database/databaseCredentials.json' senza doverle chiedere all'utente nuovamente.

Successivamente ci sarà la creazione delle tabelle necessarie per l'analisi e la predizione dei processi non finiti. Questa azione può richiedere un po' di tempo, ma verrà effettuata solo al primo utilizzo del software.

## Utilizzo

L'utilizzo del sotware è gestito nel file 'main.py'. Per far partire l'analisi è necessario digitare il comando:

```bash
python main.py
```

Dal file 'main.py' è possibile modificare l'utlizzo del software, modificando il codice alla riga 207 con la funzione scelta da eseguire.
Le possibilità sono presenti all'interno sempre del file 'main.py' e sono le seguenti:
* displayAllEventsScatter(): visualizza la distribuzione di tutti gli eventi del processo.
* displayPhaseEventsScatter(): visualizza la distrubuzione degli eventi che iniziano le fasi del processo.
* displayStateEventsScatter(): visualizza la distribuzione degli eventi che iniziano gli stati del processo.
* displayProcessComparison(): visualizza la durata dei processi e permette il confronto in base a vari parametri, sulla data di inizio processo.
* displayPhaseComparison(): visualizza la durata delle fasi del processo e permette il confronto in base ai vari parametri, sulla data di inizio processo.
* displayStateComparison(): visualizza la durata degli stati del processo e permette il confronto in base ai vari parametri, sulla data di inizio processo.
* displayEventComparison(): visualizza la durata degli eventi del processo e permette il confronto in base ai vari parametri, sulla data di inizio processo.
* displayTypeComparison(): visualizza la durata dei processi, su vari parametri.
* displayStatesEvents(): visualizza gli eventi facenti parte di ogni stato del processo.
* displayPhasesEvents(): visualizza gli eventi e gli stati facenti parte di ogni fase del processo.
* displayStatesSequence(): visualizza gli stati successivi ad ogni stato del processo.
* displayPhaseSequence(): visualizza le fasi successive ad ogni fase del processo.
* displayEventSequence(): visualizza gli eventi successivi ad ogni evento del processo.
* displayStatePreferences(): visualizza l'elenco di tutti i tipi di stati dei processi e consente all'utente di modificare alcuni parametri e scegliere quelli più importanti.
* displayEventPreferences(): visualizza l'elenco di tutti i tipi di eventi dei processi e consente all'utente di scegliere quelli più importanti.
* displaySubjectPreferences(): visualizza l'elenco di tutti i tipi di materie dei processi e consente all'utente di scegliere quelli più importanti.
* displaySectionPreferences(): visualizza l'elenco delle sezioni del Tribunale di Milano e permette all'utente di scegliere quelle più importanti.
* displayProcessTypePreferences(): visualizza l'elenco dei tipi di processi e consente all'utente di scegliere quelli più importanti.
* displayPredictionError(): visualizza l'errore relativo al predittore della durata dei processi non finiti.
* restartData(): resetta le tabelle allo stato iniziale, rimuovendo ogni scelta fatta dell'utente. Questa funzione viene eseguita al primo utilizzo, ed è necessaria eseguirla ogni volta che il database viene modificato. Altrimenti non è necessario eseguirlo in nessun caso.
* refreshData(): ricalcola le tabelle in base alle scelte dell'utente. Viene eseguito automaticamente ogni volta che l'utente cambia le tabelle dalla pagina apposita.
* predictTotalTest(): utilizza il predittore su tutti i processi finiti, con un modello basato sul 100% dei processi finiti, per calcolarne l'errore di predizione.
* predict8020Test(): utilizza il predittore su l 20% dei processi finiti, con un modello basato sul restante 80%, per calcolarne l'errore di predizione.
* predictDuration(): esegue il predittore sui processi non finiti, calcolandone la durata.
* startApp(): esegue l'app per l'utilizzo dinamico del software. Di fatto è l'utilizzo standard dell'applicazione. Attraverso pagine e link è  possibile visualizzare tutti i tipi di grafici, senza dover modificare il file 'main.py'.

Nel momento in cui viene utilizzato il comando
```bash
python main.py
```
in cui viene avviata Dash per la visualizzazione dei grafici, basterà cliccare sul link o andare alla pagina ['127.0.0.1:8050/'](http://127.0.0.1:8050/) per utilizzare l'applicazione.

## Autore

[Daniele Cicala](https://github.com/99-Daniele)