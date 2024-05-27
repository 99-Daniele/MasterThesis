# this page allows user to change court hearing parameters.

import dash as ds
import pandas as pd

import utils.DataUpdate as update
import utils.FileOperation as file
import utils.Getters as getter
import utils.utilities.Utilities as utilities

# get dataframe with state names. 
df = getter.getDataframeFromTextFile('preferences/courtHearingsEvents.txt')

# return initial layout of page.
def pageLayout():
    return None
