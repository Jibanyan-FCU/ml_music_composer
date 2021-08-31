from general.ver1.measure import Measure

import music21

class Score:

    def __init__(self, score: str or music21.stream.Score):
        '''
        Record information of a score and all measures in it.

        Arguments
        ---
        `measures`: list(Measure)
            All measures in a score.

        Parameters
        ---
        `score`: str or music21.stream.Score
            If it is str object, it must be a path of a mxl file.
        '''
        if type(score) is str:
            score = music21.converter.parse(score)
        elif type(score) is not music21.stream.Score:
            raise ValueError("Parameter 'score' must be a path of MXML file or music21.stream.Score: object")
        
        # Seperate right staff and left staff
        staffs = score.recurse().getElementsByClass(music21.stream.PartStaff)
        right_staff = staffs[0].recurse().getElementsByClass(music21.stream.Measure)
        left_staff = staffs[1].recurse().getElementsByClass(music21.stream.Measure)

        # Group measures by same measure numbers.
        all_measures = {}
        for m in right_staff:
            m_num = m.measureNumber
            all_measures[m_num] = {'measure_number': m_num, 'right': m, 'left': None}
        for m in left_staff:
            m_num = m.measureNumber
            if m_num not in all_measures:
                all_measures[m_num] = {'measure_number': m_num, 'right': None, 'left': m}
            else:
                all_measures[m_num]['left'] = m

        all_measures = list(all_measures.values())
        all_measures.sort(key = lambda m: m['measure_number'])

        # Find first meter and key signature.
        first_measure = all_measures[0]['right']
        meter = first_measure.timeSignature
        key = first_measure.keySignature
        measure_feature = {'key': key, 'meter': meter}
        
        self.measures = []

        for current_measure in all_measures:
            # check new signature
            if current_measure['right'].keySignature is not None:
                measure_feature['key'] = current_measure['right'].keySignature
            if current_measure['right'].timeSignature is not None:
                measure_feature['meter'] = current_measure['right'].timeSignature
            
            # record measure infomation
            new_measure = Measure(current_measure, measure_feature)
            self.measures.append(new_measure)

    def get_all_measure_graphs_and_feature(self, mode='training'):
        measure_graphs = []
        for measure in self.measures:
            measure_graph = measure.get_measure_graph_and_feature(mode=mode)
            measure_graphs.append(measure_graph)
        return measure_graphs
