import utils.Cache as cache
import utils.DatabaseConnection as connect
import utils.DataFrame as frame
import utils.Utilities as utilities

def getAllEvents():
    query = "SELECT e.numProcesso AS numProcesso, e.data AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, (CASE WHEN ((SELECT pcg.numProcesso FROM processicambiogiudice AS pcg WHERE (pcg.numProcesso = p.numProcesso)) IS NOT NULL) THEN 1 ELSE 0 END) AS cambiogiudice FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice)) ORDER BY et.fase"
    events = cache.getData('eventi', query)
    return frame.createEventsDataFrame(events)

def getImportantEvents():
    query = "SELECT e.numProcesso AS numProcesso, e.data AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, (CASE WHEN ((SELECT pcg.numProcesso FROM processicambiogiudice AS pcg WHERE (pcg.numProcesso = p.numProcesso)) IS NOT NULL) THEN 1 ELSE 0 END) AS cambiogiudice FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (et.evento IN (" + str(utilities.importantEvents) + "))) ORDER BY et.fase"
    events = cache.getData('eventiimportanti', query)
    return frame.createEventsDataFrame(events)

def getCourtHearingEvents():
    query = "SELECT e.numProcesso AS numProcesso, e.data AS dataEvento, et.fase AS fase, et.evento AS tipoevento, e.numEvento AS numEvento, e.codice AS codiceEvento, et.stato AS tipostato, e.statofinale AS codiceStato, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, (CASE WHEN ((SELECT pcg.numProcesso FROM processicambiogiudice AS pcg WHERE (pcg.numProcesso = p.numProcesso)) IS NOT NULL) THEN 1 ELSE 0 END) AS cambiogiudice FROM eventitipo AS et, eventi AS e, durataprocessi AS d, aliasgiudice AS a, processi AS p, processitipo AS pt, materienome AS mn WHERE ((e.numEvento = et.numEvento) AND (e.numProcesso = d.numProcesso) AND (a.giudice = p.giudice) AND (p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (p.materia = mn.codice) AND (et.evento IN (" + str(utilities.courtHearingsEvents) + "))) ORDER BY et.fase"
    events = cache.getData('eventiudienze', query)
    return frame.createEventsDataFrame(events)

def getEvents():
    query = "SELECT e.numEvento AS numEvento, en.etichetta AS tipoEvento, s.stato AS codiceStato, s.fase AS faseStato, e.numProcesso AS numProcesso, e.data AS dataEvento, s.etichetta AS tipoStato, s.abbreviazione AS statoAbbr FROM eventi AS e, eventinome AS en, statinome AS s WHERE ((e.codice = en.codice) AND (e.statofinale = s.stato)) ORDER BY e.numEvento"
    eventsType = cache.getData('tipoeventi', query)
    return eventsType

def getTestEvents():
    query = "SELECT e.numEvento AS numEvento, en.etichetta AS tipoEvento, s.stato AS codiceStato, s.fase AS faseStato, e.numProcesso AS numProcesso, e.data AS dataEvento, s.etichetta AS tipoStato, s.abbreviazione AS statoAbbr FROM eventi AS e, eventinome AS en, statinome AS s WHERE ((e.codice = en.codice) AND (e.statofinale = s.stato) AND (e.numProcesso = 109848 OR e.numProcesso = 109855 OR e.numProcesso = 109850 OR e.numProcesso = 109959)) ORDER BY e.numEvento"
    eventsType = connect.getDataFromDatabase(query)
    return eventsType

def getProcessesDuration():
    query = "SELECT d.dataInizioProcesso AS dataInizioProcesso, d.durata AS durataProcesso, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambioGiudice, p.numProcesso AS numProcesso, pt.sequenzaCorta AS sequenzaStati, pt.sequenzaFasi AS sequenzaFasi FROM durataprocessi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambiogiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioProcesso"
    processes = cache.getData('durataprocessi', query)
    return frame.createProcessesDurationDataFrame(processes)

def getStatesDuration():
    query = "SELECT d.dataInizioStato AS dataInizioStato, d.durata AS durataStato, a.alias AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambiogiudice, p.numProcesso AS numProcesso, d.etichetta AS tipoStato, d.stato AS codiceStato, sn.fase AS faseStato FROM duratastati AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, statinome AS sn, processicambiogiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (p.materia = mn.codice) AND (d.stato = sn.stato) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioStato"
    processes = cache.getData('duratastati', query)
    return frame.createStatesDurationsDataFrame(processes)

def getPhasesDuration():
    query = "SELECT d.dataInizioFase AS dataInizioFase, d.durata AS duratFase, a.alias AS giudice, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambiogiudice, p.numProcesso AS numProcesso, d.fase AS fase, d.ordine AS ordineFase FROM duratafasi AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambioGiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (d.fase <> 0) AND (mn.codice = p.materia) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioFase"
    processes = cache.getData('duratafasi', query)
    return frame.createPhasesDurationsDataFrame(processes)

def getEventsDuration():
    query = "SELECT d.dataInizio AS dataInizioEvento, d.durata AS durataEvento, a.alias AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processofinito, pcg.cambioGiudice AS cambioGiudice, e.numEvento AS numEvento, p.numProcesso AS numProcesso, et.evento AS tipoEvento, e.codice AS codiceEvento, et.fase AS faseEvento FROM durataeventi AS d, eventi AS e, eventitipo AS et, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambiogiudice AS pcg WHERE ((d.numEvento = e.numEvento) AND (e.numProcesso = p.numProcesso) AND (e.numEvento = et.numEvento) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizio"
    processes = cache.getData('durataeventi', query)
    return frame.createEventsDurationsDataFrame(processes)

def getCourtHearingsDuration():
    query = "SELECT d.dataInizioUdienza AS dataInizioUdienza, d.durata AS durataUdienza, a.alias AS giudiceProcesso, mn.etichetta AS materiaProcesso, p.sezione AS sezioneProcesso, pt.processofinito AS processoFinito, pcg.cambioGiudice AS cambioGiudice, p.numProcesso AS numProcesso FROM durataudienze AS d, processi AS p, processitipo AS pt, aliasgiudice AS a, materienome AS mn, processicambiogiudice AS pcg WHERE ((p.numProcesso = d.numProcesso) AND (pt.numProcesso = p.numProcesso) AND (a.giudice = p.giudice) AND (mn.codice = p.materia) AND (p.numProcesso = pcg.numProcesso)) ORDER BY p.numProcesso, d.dataInizioUdienza"
    courtHearings = cache.getData('durataudienze', query)
    return frame.createCourtHearingsDurationDataFrame(courtHearings)
