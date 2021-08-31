from general.ver1 import *

import music21
import glob

def open_and_trafer_score():
    pathes = glob.glob(r'source\model\sheet\*.mxl')
    
    scores = []

    bacth, fail = 0, 0
    for path in pathes:
        try:
            bacth += 1
            new_score = Score(path)
            scores.append(new_score)
        except:
            fail += 1
    
    return scores




