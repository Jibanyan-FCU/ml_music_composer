from model.preprocess import *

scores = open_and_trafer_score()

score = scores[0]
s = score.get_all_measure_graphs_and_feature()

measure = s[0]

measure['graph']
measure['feature']