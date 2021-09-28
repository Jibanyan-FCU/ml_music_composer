
import keras
from model.preprocess import open_and_trafer_score

from keras import activations
from keras.layers import Input, Dense, Reshape, Flatten, Dropout
from keras.layers import BatchNormalization, Activation, ZeroPadding2D
from keras.layers.advanced_activations import LeakyReLU
from keras.layers.convolutional import UpSampling2D, Conv2D
from keras.models import Sequential, Model
from tensorflow.keras.optimizers import Adam

import numpy as np

class __ModelMeta(type):
    def __init__(cls, *args, **kwargs):
        cls._model = None

        cls._time_units = 96
        cls._pitches = 88
        cls._voices = 8
        cls._shape = (cls._voices, cls._time_units, cls._pitches)
        cls._latent_dim = 100

    @property
    def model(cls):
        if cls._model is None:
            cls._model = cls()
        return cls._model


class DCGAN(metaclass=__ModelMeta):
    '''
    Measure is made by DCGAN. The DCGAN model is singleton pattern.

    To get the model, suggest to use constructor to get the model.

    Sample
    ---
    ```python
    # new model
    dcgan = DCGAN(None)

    # load model from specified path
    dcgan = DCGAN('your path')

    # load model from default path
    dcgan = DCGAN()

    # train DCGAN (epochs = 10)
    dcgan.train(10)

    # save model
    dcgan.save_model('your path')
    ```
    '''
    
    def __new__(cls, load_path=r'.\source\model\trained') -> Model:
        '''
        If `load_path` is 'None', you will get a new discriminator and generator (meaning that it would has not been trained).
        If `load_path` is a `str`, the trained discriminator and generator will load in from the path.
        
        Default value of `load_path` is `r'source\model\trained'`.
        '''
        if cls._model is None:

            # build discriminator
            cls._discriminator = Discriminator(load_path)

            # build generator
            cls._generator = Generator(load_path)

            cls._combined = Combined()

            assert type(cls._combined) is Model
            cls._model = super().__new__(cls)

        return cls._model

    def save_model(cls, path=r'source\model\trained'):
        Discriminator.save_model(path)
        Generator.save_model(path)
        
    def train(self, epochs, batch_size=128, save_interval=50):
        
        # load data, don't need to rescale
        def get_all_graphs():
            graphs = []
            scores = open_and_trafer_score()
            
            for score in scores:
                for measure in score.measures:
                    try:
                        graph = measure.get_measure_graph()
                        if not graph.shape[1] == 96:
                            raise Warning('skip')
                        graphs.append(graph)
                    except:
                        pass
            
            graphs = np.array(graphs)
            return graphs
        
        X_train = get_all_graphs()
        
        valid = np.ones((batch_size, 1))
        fake = np.zeros((batch_size, 1))

        for epoch in range(epochs):
            # train discriminator
            idx = np.random.randint(0, X_train.shape[0], batch_size)
            imgs = X_train[idx]

            noise = np.random.normal(0, 1, (batch_size, self._latent_dim))
            gen_imgs = self._generator.predict(noise)

            d_loss_real = self._discriminator.train_on_batch(imgs, valid)
            d_loss_fack = self._discriminator.train_on_batch(gen_imgs, fake)
            d_loss = 0.5 * np.add(d_loss_real, d_loss_fack)

            # train generator
            g_loss = self._combined.train_on_batch(noise, valid)

            print("%d [D loss: %f, acc.: %.2f%%] [G loss: %f]" % (epoch, d_loss[0], 100*d_loss[1], g_loss))


class Discriminator(metaclass=__ModelMeta):

    def __new__(cls, load_path=r'.\source\model\trained'):
        if cls._model is None:
            if load_path is not None:
                model = keras.models.load_model(load_path + r'\discriminator.h5')
            else:
                model = Sequential()

                model.add(Conv2D(32, kernel_size=3, strides=2, input_shape=cls._shape, padding='same', data_format='channels_first'))
                model.add(LeakyReLU(alpha=0.2))
                model.add(Dropout(0.25))
                model.add(Conv2D(64, kernel_size=3, strides=2, padding='same', data_format='channels_first'))
                model.add(LeakyReLU(alpha=0.2))
                model.add(Dropout(0.25))
                model.add(Conv2D(128, kernel_size=3, strides=2, padding='same', data_format='channels_first'))
                model.add(LeakyReLU(alpha=0.2))
                model.add(Dropout(0.25))
                model.add(Conv2D(256, kernel_size=3, strides=1, padding='same', data_format='channels_first'))
                model.add(LeakyReLU(alpha=0.2))
                model.add(Dropout(0.25))
                model.add(Flatten(data_format='channels_first'))
                model.add(Dense(1, activation='sigmoid'))

                img = Input(shape=cls._shape)
                validity = model(img)

                model = Model(img, validity)
            
            model.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5), metrics=['accuracy'])
            cls._model = model

        assert type(cls._model) is Model
        return cls._model

    @classmethod
    def save_model(cls, path=r'source\model\trained'):
        full_path = path + r'\discriminator.h5'
        cls._model.save(full_path)

    def summary(cls):
        cls._model.summary(index=-1)


class Generator(metaclass=__ModelMeta):

    def __new__(cls, load_path=r'.\source\model\trained'):
        
        if cls._model == None:
            if load_path is not None:
                cls._model = keras.models.load_model(load_path + r'\generator.h5')
            else:
                    
                model = Sequential()

                model.add(Dense(128 * 12 * 11, activation='relu', input_dim=cls._latent_dim))
                model.add(Reshape((128, 12, 11)))
                model.add(UpSampling2D(data_format='channels_first'))
                model.add(Conv2D(128, kernel_size=3, padding='same', data_format='channels_first'))
                model.add(BatchNormalization(momentum=0.8))
                model.add(Activation('relu'))
                model.add(UpSampling2D(data_format='channels_first'))
                model.add(Conv2D(64, kernel_size=3, padding='same', data_format='channels_first'))
                model.add(BatchNormalization(momentum=0.8))
                model.add(Activation('relu'))
                model.add(UpSampling2D(data_format='channels_first'))
                model.add(Conv2D(32, kernel_size=3, padding='same', data_format='channels_first'))
                model.add(BatchNormalization(momentum=0.8))
                model.add(Activation('relu'))
                model.add(Conv2D(cls._voices, kernel_size=3, padding="same", data_format='channels_first'))
                model.add(Activation("tanh"))

                # model.summary()

                noise = Input(shape=(cls._latent_dim, ))
                img = model(noise)

                cls._model = Model(noise, img)
        
        assert type(cls._model) is Model
        return cls._model

    @classmethod
    def save_model(cls, path=r'source\model\trained'):
        full_path = path + r'\generator.h5'
        cls._model.save(full_path)

    def summary(cls):
        cls._model.summary(index=-1)


class Combined(metaclass=__ModelMeta):

    def __new__(cls):
        if cls._model is None:
            generator = Generator()
            z = Input(shape=(cls._latent_dim,))
            img = generator(z)

            discriminator = Discriminator()
            discriminator.trainable = False
            valid = discriminator(img)

            model = Model(z, valid)
            model.compile(loss='binary_crossentropy', optimizer=Adam(0.0002, 0.5))

            cls._model = model

        assert type(cls._model) is Model
        return cls._model

    @classmethod
    def save_model(cls, path=r'source\model\trained'):
        full_path = path + r'\combined.h5'
        cls._model.save(full_path)