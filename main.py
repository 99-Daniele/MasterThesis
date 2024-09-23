# this is the main file.

import os

# refresh database and cache data.
def restartData():
    import utils.DataUpdate as update
    update.restartData()

# refresh database and cache data.
def refreshData():
    import utils.DataUpdate as update
    update.refreshData()

# test unfinished processes predictor. Test on all processes.
def predictTotalTest():
    import utils.DataUpdate as update
    update.predictTotalTest()

# test unfinished processes predictor. Test on 80-20 processes.
def predict8020Test():
    import utils.DataUpdate as update
    update.predict8020Test()

# predicts duration of unfinished processes.
def predictDuration():
    import utils.DataUpdate as update
    update.predictDuration()
    update.refreshData()

# start app to allow user select graph to be displayed.
def startApp():
    import utils.App as app
    app.start()

# if cache is not present, restart data.
if not os.path.isdir('cache'):
    restartData()

if __name__ == '__main__':
    startApp()