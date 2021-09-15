import music21
import numpy as np

class Measure:
    '''
    Class `Measure` is used to record some information of a measure.
    In version 1, there are melody, measure number, key and meter.

    Constant
    ---
    `DEFAULT_UNITS_PER_QUARTER`: 24
        A unit is one twenty-fourth of a quarter length.

    `DEFAULT_PITCH_NUMBER`: 88
        Pitch number of 88-key piano.

    `PITCH_A0_MIDI_CODE`: 21
        The midi code of lowest pitch on piano.

    Note
    ---
    This version dosen't deal with pickup measure, candenza and other special notation.
    Constructing object by np.array(sharp(2,_,88)) hasn't been finished.

    It will be tried to fix or add the function above.
    '''
    DEFAULT_UNITS_PER_QUARTER = 24
    DEFAULT_PITCH_NUMBER = 88

    PITCH_A0_MIDI_CODE = 21

    @classmethod
    def tranfer_graph_to_music21_measure(graph:np.array) -> music21.stream.Measure:
        voices = [[] for _ in range(8)]
        for k in range(8):
            for j in range(1):
                pass

                    
        
    def __init__(self, measure:dict, feature: dict):
        '''
        Arguments
        ---
        `notes`: list(list(musci21.note.Note))
            All notes in each voice part

        `number`: int
            Number of a measure.

        `feature`: dict
            - `"key"`: int, sharps number of the key signature. It would be negative number to show how many flat.
            - `"meter"`: tuple(int,int), time signature '3/4' be recorded as (3,4)

        Parameters
        ---
        `measure`: dict
            The dictionary must has three keys: `measure_number`, `right` and `left`.
            - `"measure_number"`: int, number of measure.
            - `"right"`: music21.stream.Measure, part of right head staff of measure.
            - `"left"`: music21.stream.Measure, part of left head staff of measure.

        `feature`: dict
            A dictionary record meter and key signature of a measure.
            - `"key"`: music21.key.keySignature, key signature of a measure
            - `"meter"`: music21.meter.TimeSignature, meter of a measure

        '''

        # parse feature info
        key = feature['key'].sharps
        meter = feature['meter']
        meter = (meter.numerator, meter.denominator)

        voice_start_index = {'right': 0, 'left': 4}
        notes = [[] for _ in range(8)]

        # get all notes information
        measure_lables = ['right', 'left']
        for measure_lable in measure_lables:
            start_index = voice_start_index[measure_lable]
            voices = measure[measure_lable].voices
            if len(voices) == 0:
                for note in measure[measure_lable].notes:
                    notes[start_index].append(note)
            else:
                for i in range(len(voices)):
                    insert_voice = voice_start_index[measure_lable] + i
                    for note in voices[i].notes:
                        notes[insert_voice].append(note)

        # save to object
        self.notes = notes
        self.number = measure['measure_number']
        self.feature = {'key': key, 'meter': meter}

    def get_measure_graph(self) -> np.array:
        '''
            Tranfer to measure graph (pianoroll like).

            Returns
            ---
            A pianoroll-like graph made from np.array
        '''
        meter = self.feature['meter']
        total_time_unit = int(self.DEFAULT_UNITS_PER_QUARTER * meter[0] / meter[1] * 4)

        graph = np.zeros((8, total_time_unit, self.DEFAULT_PITCH_NUMBER), dtype='int8')

        for i in range(8):
            current_voice = self.notes[i]
            for note_or_chord in current_voice:
                start_index = int(note_or_chord.offset * self.DEFAULT_UNITS_PER_QUARTER)
                end_index = start_index + int(note_or_chord.quarterLength * self.DEFAULT_UNITS_PER_QUARTER) - 1
                pitches = self.__make_pitches_index_list(note_or_chord)
                
                for k in pitches:
                    for j in range(start_index, end_index):
                        graph[i][j][k] = 1

                    graph[i][end_index][k] = -1

        return graph
    
    def __make_pitches_index_list(self, note):
        if type(note) is music21.note.Note:
            return [int(note.pitch.ps) - self.PITCH_A0_MIDI_CODE]
        elif type(note) is music21.chord.Chord:
            return [int(x.ps) - self.PITCH_A0_MIDI_CODE for x in note.pitches]

    def get_measure_graph_and_feature(self, mode:str='train'):
        '''
        An API to get all the infomation of the measure.

        Parameters
        ---
        `mode`: str='training'
            The return format. `"training"` will `return np.array(shape(2,_,88)`,
            other words will return `dict`.

        Return
        ---
        It will return by a dictionary.

        `"graph"`: np.array
            A pianoroll-like graph made from np.array

        `"feature"`: dict
            The feature of the measure. See `Measure.feature`.
        '''
        graph = self.get_measure_graph()

        return {'graph':graph, 'feature': self.feature}

        


        