from keras.models import load_model
import numpy as np
import pickle
import music21
import time
from random import randint

def sigleton(cls):
    
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@sigleton
class Mu_Model:
    
    def __init__(self):
        notes = []
        with open ("notes", "rb") as file:
            notes = pickle.load(file)
        pitch_names = sorted(set(notes))

        model = load_model("model.hdf5")

        # Create a mapping from int to element
        int_to_element = dict ((num, element) for num, element in enumerate (pitch_names))
        element_to_int = dict ((element, num) for num, element in int_to_element.items())

        sequence_length = 100

        test_input = []

        for i in range (len(notes) - sequence_length):
            seq_inp = notes[i:i+sequence_length]
            test_input.append([element_to_int[ch] for ch in seq_inp])

        vocab_len = 359

        self._notes = notes
        self._model = model
        self._int_to_element = int_to_element
        self._element_to_int = element_to_int
        self._sequence_length = sequence_length
        self._vocab_len = vocab_len

    def make_music(self, note_number=200):

        pattern = [randint(0, len(self._int_to_element)-1) for _ in range(100)]
        final_prediction = []

        for _ in range(note_number):
            predict_input = np.reshape(pattern, (1, len(pattern), 1))
            predict_input = predict_input / float(self._vocab_len)

            prediction = self._model.predict(predict_input, verbose=0)
            prediction = np.argmax(predict_input)
            final_prediction.append(self._int_to_element[prediction])

            pattern.pop(0)
            pattern.append(prediction)

        # create midi file
        offset = 0
        melody = []
        for note_or_chord in final_prediction:
            # chord
            if '+' in note_or_chord or note_or_chord.isdigit():
                notes = [int(x) for x in note_or_chord.split('+')]
                new_note_or_chord = music21.chord.Chord(notes, offset=offset)
            # note
            else:
                new_note_or_chord = music21.note.Note(note_or_chord, offset=offset)
            new_note_or_chord.storedInstrument = music21.instrument.Piano()
            melody.append(new_note_or_chord)
            offset += 0.5

        t = time.localtime()
        file_name = f'output/output_{t.tm_year}_{t.tm_mon}_{t.tm_mday}_{t.tm_hour}_{t.tm_min}_{t.tm_sec}.mid'
        midi_stream = music21.stream.Stream(melody)
        midi_stream.write('midi', fp=file_name)

        return file_name


m = Mu_Model()
m.make_music()