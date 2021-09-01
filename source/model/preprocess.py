from general.ver1 import *

import music21
import glob

def open_and_trafer_score(root_path:str=r'source\model\sheet'):
    '''
        Open mxl files and tranfer them to Score object.
    '''
    pathes = glob.glob(root_path + r'\*.mxl')
    
    scores = []

    bacth, fail = 0, 0
    for path in pathes:
        try:
            new_score = Score(path)
            scores.append(new_score)
        except:
            pass
    
    return scores




