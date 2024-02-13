from utils.DatabaseConnection import connectToDatabase

import utils.Getters as gt
import utils.Graphs as gr


if __name__ == '__main__':
    connection = connectToDatabase('localhost', 'root', 'Ropswot_@222', 'tribunali2020')
    e = gt.getCourtHearingsEvents(connection)
    gr.displayEvents(e, "EVENTI")