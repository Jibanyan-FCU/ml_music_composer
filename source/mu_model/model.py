from .general import sigleton
from .processer import Preprocesser, Pattern_Manager

import numpy as np
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import  LSTM, Dense, Dropout
from tensorflow.keras.utils import np_utils
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau, TerminateOnNaN, CSVLogger

import matplotlib.pyplot as plt

from random import randint        

MODEL_PATH = 'mu_model/model'
LOG_PATH = 'mu_model/log'

def make_callback_list(save_dir, file_name):
    callback_list = [
        ModelCheckpoint(
            filepath = save_dir + file_name + '.h5py',
            monitor = 'accurancy',
            save_best_only = True,
            save_weights_only= False,
            mode = 'max' 
        ),

        ModelCheckpoint(
            filepath = save_dir + file_name + '.h5py',
            monitor = 'loss',
            save_best_only = True,
            save_weights_only= False,
            mode = 'min' 
        ),

        EarlyStopping(
            monitor = 'loss',
            min_delta = 0,
            patience = 100,
            verbose = 1,
            mode = 'min',
            restore_best_weights = True
        ),

        ReduceLROnPlateau(
            monitor = 'loss',
            factor = 0.1,
            patience = 40,
            verbose = 1,
            mode = 'min',
            min_lr = 0
        ),

        CSVLogger(LOG_PATH + file_name + '.log'),

        TerminateOnNaN()
    ]

    return callback_list

@sigleton
class Melody_Model:
    def __init__(self):
        self._model = None
        self._history = None
        self._pattern_manager = Pattern_Manager()

    def create_model(self):

        pitch_num = len(self._pattern_manager.int_to_pitch)
        print(pitch_num)

        # model = Sequential()

        # model.add(LSTM(units=512, input_shape=(None, self._pattern_manager.SEQUENCE_LENGTH), return_sequences=True))
        # model.add(Dropout(0.3))
        # model.add(LSTM(units=512))
        # model.add(Dense(512))
        # model.add(Dropout(0.3))
        # model.add(Dense(256))
        # model.add(Dropout(0.3))
        # model.add(Dense(pitch_num, activation='softmax'))

        model = Sequential()

        model.add(LSTM(units=1024, input_shape=(None, self._pattern_manager.SEQUENCE_LENGTH), return_sequences=True))
        model.add(Dropout(0.3))
        model.add(LSTM(units=1024))
        model.add(Dense(1024))
        model.add(Dropout(0.3))
        model.add(Dense(512))
        model.add(Dropout(0.3))
        model.add(Dense(pitch_num, activation='softmax'))

        self._model = model

    def load_model(self, dir_path=MODEL_PATH):
        self._model = load_model(dir_path + '/melody_model.h5py')

    def train(self, sequence_X, sequence_y, epochs, batch_size, save_dir=MODEL_PATH):

        self._model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        seq_num = len(sequence_X)
        sequence_X = np.reshape(sequence_X, (seq_num, 1, self._pattern_manager.SEQUENCE_LENGTH))
        sequence_X = sequence_X / seq_num

        sequence_y = np_utils.to_categorical(sequence_y)
        print(sequence_y.shape)

        self._history = self._model.fit(
            x = sequence_X,
            y = sequence_y,
            batch_size = batch_size,
            epochs = epochs,
            callbacks = make_callback_list(save_dir, '/melody_model'),
            shuffle = True
        )

    def predict_sequence(self, pattern, num):
        sequence = []

        for _ in range(num):
            np_pattern = np.reshape(pattern, (1, 1, self._pattern_manager.SEQUENCE_LENGTH))
            np_pattern = np_pattern / len(self._pattern_manager.int_to_pitch)

            prediction = self._model.predict(np_pattern, verbose=0)
            index = np.argmax(prediction)

            sequence.append(self._pattern_manager.int_to_pitch[index])

            pattern = pattern[1:]
            pattern.append(index)
            
        return sequence

    def get_history(self):
        return self._history


@sigleton
class Rhythm_Model:
    def __init__(self):
        self._model = None
        self._history = None
        self._pattern_manager = Pattern_Manager()

    def create_model(self):

        beat_num = len(self._pattern_manager.int_to_beat)

        model = Sequential()

        model.add(LSTM(units=512, input_shape=(None, self._pattern_manager.SEQUENCE_LENGTH), return_sequences=True))
        model.add(Dropout(0.3))
        model.add(LSTM(units=512))
        model.add(Dense(512))
        model.add(Dropout(0.3))
        model.add(Dense(256))
        model.add(Dropout(0.3))
        model.add(Dense(beat_num, activation='softmax'))

        self._model = model

    def load_model(self, dir_path=MODEL_PATH):
        self._model = load_model(dir_path + '/rhythm_model.h5py')

    def train(self, sequence_X, sequence_y, epochs, batch_size, save_dir=MODEL_PATH):
        
        self._model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        seq_num = len(sequence_X)
        sequence_X = np.reshape(sequence_X, (seq_num, 1, self._pattern_manager.SEQUENCE_LENGTH))
        sequence_X = sequence_X / seq_num

        sequence_y = np_utils.to_categorical(sequence_y)
        sequence_y = np.concatenate((sequence_y, np.zeros((sequence_y.shape[0], 1))), axis=1)

        self._history = self._model.fit(
            x = sequence_X,
            y = sequence_y,
            batch_size = batch_size,
            epochs = epochs,
            callbacks = make_callback_list(save_dir, '/rhythm_model'),
            shuffle = True
        )

    def predict_sequence(self, pattern, num):
        sequence = []

        for _ in range(num):
            np_pattern = np.reshape(pattern, (1, 1, self._pattern_manager.SEQUENCE_LENGTH))
            np_pattern = np_pattern / len(self._pattern_manager.int_to_beat)

            prediction = self._model.predict(np_pattern, verbose=0)
            index = np.argmax(prediction)

            sequence.append(self._pattern_manager.int_to_beat[index])

            pattern = pattern[1:]
            pattern.append(index)
            
        return sequence
    
    def get_history(self):
        return self._history

@sigleton
class Mu_Model:
    def __init__(self):
        self._melody_model = Melody_Model()
        self._rhythm_model = Rhythm_Model()    

    def create_model(self):
        self._melody_model.create_model()
        self._rhythm_model.create_model()

    def load_model(self, dir_path=MODEL_PATH):
        self._melody_model.load_model(dir_path)
        self._rhythm_model.load_model(dir_path)

    def train(self, epochs=1000, batch_size=50, train_melody=True, train_rhythm=True, log_path=LOG_PATH):
        (melody_X, melody_y), (rhythm_X, rhythm_y) = Preprocesser().prepare_sequences()
        
        if train_melody:
            self._melody_model.train(melody_X, melody_y, epochs, batch_size)

        if train_rhythm:
            self._rhythm_model.train(rhythm_X, rhythm_y, epochs, batch_size)

    def predict_sequence(self, pattern_index=None, num=200, compare=False):
        (melody_X, _), (rhythm_X, _) = Preprocesser().prepare_sequences()
        
        if pattern_index == None:
            index = randint(0, len(melody_X)-1)
        else:
            index = pattern_index

        if compare:
            num -= 50
            index -= 50
            if index < 0:
                index = 0
        
        melody_pattern = melody_X[index]
        rhythm_pattern = rhythm_X[index]
        
        melody = self._melody_model.predict_sequence(melody_pattern, num)
        rhythm = self._rhythm_model.predict_sequence(rhythm_pattern, num)

        if not compare:
            music = zip(melody, rhythm)
            return music
        else:
            origin = zip(melody_X[index+50], rhythm_X[index+50])
            music = origin[:50] + zip(melody, rhythm)
            return music, origin

    def draw_line_chat(self, dir_path=LOG_PATH):
        melody_history = self._melody_model.get_history()
        rhythm_history = self._rhythm_model.get_history()

        # loss
        plt.plot(melody_history.history['loss'],'r')
        plt.plot(rhythm_history.history['loss'],'g')
        plt.title('Model Loss')
        plt.ylabel('Loss')
        plt.xlabel('Epoch')
        plt.legend(['melody', 'rhythm'], loc='upper left')
        plt.savefig(dir_path  +'/loss.png')
        plt.clf()

        # accuracy
        plt.plot(melody_history.history['accuracy'])
        plt.plot(rhythm_history.history['accuracy'])
        plt.title('Model Accuracy')
        plt.ylabel('Accuracy')
        plt.xlabel('Epoch')
        plt.legend(['melody', 'rhythm'], loc='upper left')
        plt.savefig(dir_path  +'/accuracy.png')
        plt.clf()
        