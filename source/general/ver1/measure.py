import music21
import numpy as np
from numpy.core.fromnumeric import shape

class Measure:
    '''
    Class `Measure` is used to record some information of a measure.
    In version 1, there are melody, measure number, key and meter.
    '''
    DEFAULT_UNITS_PER_QUARTER = 24
    DEFAULT_PITCH_NUMBER = 88

    PITCH_A0_MIDI_CODE = 21
    def __init__(self, measure:dict, feature: dict):
        '''
        Arguments
        ---
        `notes`:
        `number`: int
            Number of a measure.
        `feature`:
            - `key`: int, sharps number of the key signature. It would be negative number to show how many flat.
            - `meter`: tuple(int,int), time signature '3/4' be recorded as (3,4)
        Parameters
        ---
        `measure`: dict
            The dictionary must has three keys: `measure_number`, `right` and `left`.
            - `measure_number`: int, number of measure.
            - `right`: music21.stream.Measure, part of right head staff of measure.
            - `left`: music21.stream.Measure, part of left head staff of measure.
        `feature`: dict
            A dictionary record meter and key signature of a measure.
            - `key`: music21.key.keySignature, key signature of a measure
            - `meter`: music21.meter.TimeSignature, meter of a measure
        Note
        ---
        This version dosen't deal with pickup measure and candenza (etc.) so those case might have problem.
        It should be tried to find a solution in next version.
        '''

        # parse feature info
        key = feature['key'].sharps
        meter = feature['meter']
        meter = (meter.numerator, meter.denominator)

        # get all notes information
        right_notes = measure['right'].recurse().notes
        left_notes = measure['left'].recurse().notes

        # save to object
        self.notes = {'right': right_notes, 'left': left_notes}
        self.number = measure['measure_number']
        self.feature = {'key': key, 'meter': meter}

    def get_measure_graph(self) -> dict:
        '''
            Tranfer to measure graph (pianoroll like).
            Returns
            ---
            A dictionary including two key:
            - `right`: np.array(shape=(__,88), dtype=np.uint8), measure graph on the right part of measure.
            - `left`: np.array(shape=(__,88), dtype=np.int8), measure graph on the left part of measure.
        '''
        meter = self.feature['meter']
        total_time_unit = int(self.DEFAULT_UNITS_PER_QUARTER * meter[0] / meter[1] * 4)

        right_graph = np.zeros((total_time_unit, self.DEFAULT_PITCH_NUMBER), dtype='uint8')
        left_graph = np.zeros((total_time_unit, self.DEFAULT_PITCH_NUMBER), dtype='uint8')

        graph = {'right': right_graph, 'left': left_graph}

        for part in self.notes:
            # make right part of measure graph
            for note in self.notes[part]:
                # pitch index
                pitch_index_list = self.__make_pitchs_index_list(note)
                
                # time range
                begin_unit_index = int(note.offset * self.DEFAULT_UNITS_PER_QUARTER)
                end_unit_index = int((note.offset + note.quarterLength) * self.DEFAULT_UNITS_PER_QUARTER)
                end_unit_index = min(end_unit_index, total_time_unit)

                # fill block
                for j in pitch_index_list:
                    for i in range(begin_unit_index, end_unit_index):
                        graph[part][i][j] = 1

        return graph
    
    def __make_pitchs_index_list(self, note):
        if type(note) is music21.note.Note:
            return [int(note.pitch.ps) - self.PITCH_A0_MIDI_CODE]
        elif type(note) is music21.chord.Chord:
            return [int(x.ps) - self.PITCH_A0_MIDI_CODE for x in note.pitches]

    def get_measure_graph_and_feature(self, mode='training'):
        graph = self.get_measure_graph()
        if mode == 'training':
            total_time_unit = len(graph['right'])
            graph = np.append(graph['right'], graph['left']).reshape(2, total_time_unit, self.DEFAULT_PITCH_NUMBER)
        
        return {'graph':graph, 'feature': self.feature}


        