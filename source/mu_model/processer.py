from .general import *

from fractions import Fraction
from music21 import converter, note, chord, stream
import glob

from time import ctime, localtime, strftime
import pickle

@sigleton
class Pattern_Manager:

    SEQUENCE_LENGTH = 100
    
    DATASET_DIR_PATH = 'mu_model/dataset'
    NOTE_INFO_PATH = 'mu_model/notes_info.dat'

    sequence_X = []
    sequence_y = []

    int_to_beat = []
    beat_to_int = {}
    int_to_pitch = []
    pitch_to_int = {}

    def __init__(self):
        self._music_manager = Music_Manager()

    def prepare_sequences(self, dir_path=None, for_train=True):
    
        if dir_path == None:
            dir_path = self.DATASET_DIR_PATH
        
        sequence_X = self.sequence_X
        sequence_y = self.sequence_y

        if sequence_X == [] and sequence_y == []:
            
            self.load_dataset()            
            note_sequences = self._music_manager.get_note_sequences()

            for note_sequence in note_sequences:
                
                for n in note_sequence:
                    # record pitch name
                    if n[0] not in self.int_to_pitch:
                        self.int_to_pitch.append(n[0])
                        self.pitch_to_int[n[0]] = len(self.int_to_pitch) - 1
                    # record beat name
                    if n[1] not in self.int_to_beat:
                        self.int_to_beat.append(n[1])
                        self.beat_to_int[n[1]] = len(self.int_to_beat) - 1

                for i in range(len(note_sequence) - self.SEQUENCE_LENGTH - 1):
                    sequence_X.append(note_sequence[i : i + self.SEQUENCE_LENGTH])
                    sequence_y.append(note_sequence[i + self.SEQUENCE_LENGTH + 1])

            self.sequence_X = sequence_X
            self.sequence_y = sequence_y

            self.save_notes()

        if for_train:

            sequence_X = [[(self.pitch_to_int[n[0]], self.beat_to_int[n[1]]) for n in x] for x in [X for X in sequence_X]]
            sequence_y = [(self.pitch_to_int[n[0]], self.beat_to_int[n[1]]) for n in [y for y in sequence_y]]

            melody_X = [[n[0] for n in x] for x in [X for X in sequence_X]]
            rhythm_X = [[n[1] for n in x] for x in [X for X in sequence_X]]
            melody_y = [n[0] for n in [y for y in sequence_y]]
            rhythm_y = [n[1] for n in [y for y in sequence_y]]

            return (melody_X, melody_y), (rhythm_X, rhythm_y)
        else:
            return sequence_X[:], sequence_y[:]

    def load_dataset(self, dir_path=None):
        if dir_path is None:
            dir_path = self.DATASET_DIR_PATH
        
        for music_file in glob.glob(dir_path + '/*.mid'):
            self._music_manager.load_music(music_file)

    def load_notes(self, dir_path=None):
        if dir_path == None:
            dir_path = self.NOTE_INFO_PATH

        with open(dir_path, 'rb') as f:
            contexts = pickle.load(f)

        for c in contexts:
            setattr(self, c, contexts[c])

    def save_notes(self, dir_path=None):
        if dir_path == None:
            dir_path = self.NOTE_INFO_PATH

        contexts = {
            'sequence_X': self.sequence_X,
            'sequence_y': self.sequence_y,
            'int_to_beat': self.int_to_beat,
            'beat_to_int': self.beat_to_int,
            'int_to_pitch': self.int_to_pitch,
            'pitch_to_int': self.pitch_to_int
        }

        with open(dir_path, 'wb') as f:
            pickle.dump(contexts, f)



@sigleton
class Preprocesser:

    def __init__(self):
        self._pattern_manager = Pattern_Manager()

    def load_notes(self):
        self._pattern_manager.load_notes()

    def prepare_sequences(self, dir_path=None, for_train=True):
        return self._pattern_manager.prepare_sequences(dir_path=None, for_train=True)


@sigleton
class Postprocesser:
    
    OUTPUT_PATH = 'mu_model/output'
    COMPARE_PATH = 'mu_model/compare'
    
    def __init__(self):
        from .model import Mu_Model
        self._model = Mu_Model()
        self._pattern_manager = Pattern_Manager()

    def load_notes(self):
        self._pattern_manager.load_notes()
        
    def make_music(self, pattern_index=None, output_path=None, *args, **kwargs):
        if output_path == None:
            output_path = self.OUTPUT_PATH

        music_sequence = self._model.predict_sequence(pattern_index=pattern_index)
        midi_stream = Music.combine_music(music_sequence)

        file_name = strftime("/output_%Y-%m-%d_%H''%M'%S.mid", localtime())
        midi_stream.write('midi', fp=output_path + file_name)

        return file_name

    def make_compare(self, output_path=None):
        if output_path == None:
            output_path = self.COMPARE_PATH

        fake_sequence, real_sequence = self._model.predict_sequence(compare=True)

        fake_stream = Music.combine_music(fake_sequence)
        real_stream = Music.combine_music(real_sequence)

        t = strftime("/%Y-%m-%d_%H''%M'%S", localtime())
        fake_path = self.COMPARE_PATH + t + '_fake.mid'
        real_path = self.COMPARE_PATH + t + '_real.mid'

        fake_stream.write('midi', fp=fake_path)
        real_stream.write('midi', fp=real_path)

        return {'fake': fake_path, 'real': real_path}

