from general.ver2.measure import Measure

import music21

class Score:

    def __init__(self, path: str):
        '''
        Record information of a score and all measures in it.

        Arguments
        ---
        `measures`: list(Measure)
            All measures in a score.

        `features`: list(Measure)
            All measures in a score.

        Parameters
        ---
        `score`: str
            str object, it must be a path of a mxl file.
        '''
        score = music21.converter.parse(path)
        
        # get title
        strings = path.split('\\')
        title = strings[-1]

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
        
        measures = []

        # record all measure information
        for current_measure in all_measures:
            # check new signature
            if current_measure['right'].keySignature is not None:
                measure_feature['key'] = current_measure['right'].keySignature
            if current_measure['right'].timeSignature is not None:
                measure_feature['meter'] = current_measure['right'].timeSignature
            
            # save to Measure object
            new_measure = Measure(current_measure, measure_feature)
            measures.append(new_measure)

        self.title = title
        self.measures = measures
        self.features = None

    def get_all_measure_graphs_and_feature(self, mode='train'):
        '''
        Get all measures graph and measure feature of the score.

        Returns
        ---
        list(dict)

        Note
        ---
        See `Measure.get_measure_graph_and_feature()`
        '''
        measure_graphs = []
        for measure in self.measures:
            measure_graph = measure.get_measure_graph_and_feature(mode=mode)
            measure_graphs.append(measure_graph)
        return measure_graphs
