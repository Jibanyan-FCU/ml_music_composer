import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rand
 
from keras.models import Sequential, load_model
from keras.utils import np_utils
from keras.utils.vis_utils import plot_model #need to goin file(vis_utils)
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, LeakyReLU
from keras.optimizers import adam_v2
from keras.layers import Reshape
from keras.layers import Conv2DTranspose

from numpy import expand_dims, zeros, ones
from numpy.random import randint, randn
from matplotlib import pyplot
# load dataset
from model.preprocess import *

#Generater
measure_len = 96 # amount
measure_pitch = 88 # amount

generate_data=np.zeros([measure_len,measure_pitch])
print(generate_data)
'''
for row in range(measure_len) :
  for column in range(measure_pitch) :
    generate_data[row][column] = rand.randint(0,1)

print('after random')
print(generate_data)
'''
# CNN
def define_generator(latent_dim): # function
	model = Sequential() # 線性
	n_nodes = 128 * 24 * 22 # 輸入層節點數量 128 node 96/4=24 88/4=22 
	model.add(Dense(n_nodes, input_dim=latent_dim)) # 全連接層 (輸入層節點, define input_dim=100)
	model.add(LeakyReLU(alpha=0.2)) # 0.2 default
	model.add(Reshape((24, 22, 128))) # feature vector 24*22*128
	# upsample to 48*44
	model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same')) #double to 48*44
	model.add(LeakyReLU(alpha=0.2))
	# upsample to 96*88
	model.add(Conv2DTranspose(128, (4,4), strides=(2,2), padding='same')) #double to 96*88
	model.add(LeakyReLU(alpha=0.2))
 
	model.add(Conv2D(1, (24,22), activation='sigmoid', padding='same'))
	return model

# generate points in latent space as input for the generator
def generate_latent_points(latent_dim, n_samples):
	# generate points in the latent space
	x_input = randn(latent_dim * n_samples)
	# reshape into a batch of inputs for the network
	x_input = x_input.reshape(n_samples, latent_dim)
	return x_input

# use the generator to generate n fake examples, with class labels
def generate_fake_samples(g_model, latent_dim, n_samples):
	# generate points in latent space
	x_input = generate_latent_points(latent_dim, n_samples)
	# predict outputs
	X = g_model.predict(x_input)
	# create 'fake' class labels (0)
	y = zeros((n_samples, 1))
	return X, y
 
# size of the latent space
latent_dim = 100
# define the discriminator model
model = define_generator(latent_dim)
# generate samples
n_samples = 10
X, _ = generate_fake_samples(model, latent_dim, n_samples)
# plot the generated samples
for i in range(n_samples):
	# define subplot
	pyplot.subplot(5, 5, 1 + i)
	# turn off axis labels
	pyplot.axis('off')
	# plot single image
	pyplot.imshow(X[i, :, :, 0], cmap='gray_r')
# show the figure
pyplot.show()

#Discriminator
def define_discriminator(in_shape=(96,88,1)):
	model = Sequential()
	model.add(Conv2D(64, (3,3), strides=(2, 2), padding='same', input_shape=in_shape)) # 48*44*64
	model.add(LeakyReLU(alpha=0.2))
	model.add(Dropout(0.4))
	model.add(Conv2D(64, (3,3), strides=(2, 2), padding='same')) # 24*22*64
	model.add(LeakyReLU(alpha=0.2))
	model.add(Dropout(0.4))
	model.add(Flatten()) # 33792
	model.add(Dense(1, activation='sigmoid'))
	# compile model
	opt = adam_v2.Adam(learning_rate=0.0002, beta_1=0.5)
	model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
	return model
 
# define model
model = define_discriminator()
# summarize the model
model.summary()
# plot the model
plot_model(model, to_file='discriminator_plot.png', show_shapes=True, show_layer_names=True)

#prepare data
#link with preprocess
scores = open_and_trafer_score()
score = scores[0]
s = score.get_all_measure_graphs_feature()
measure = s[0]
'''
x_train, y_train = measure['graph'], measure['feature']
'''
def load_real_sample():
	# x_train,Y_train is array
	x_train = measure['graph']
	# expand to 3d, e.g. add channels dimension
	X = expand_dims(x_train, axis=-1)
	# convert from unsigned ints to floats
	X = X.astype('float32')
	return X

# select real samples
def generate_real_samples(dataset, n_samples):
	# choose random instances
	ix = randint(0, dataset.shape[0], n_samples)
	# retrieve selected images
	X = dataset[ix]
	# generate 'real' class labels (1)
	y = ones((n_samples, 1))
	return X, y

# generate n fake samples with class labels
def generate_fake_samples(n_samples):
	# generate uniform random numbers in [0,1]
	X = rand(96 * 88 * n_samples)
	# reshape into a batch of grayscale images
	X = X.reshape((n_samples, 96, 88, 1))
	# generate 'fake' class labels (0)
	y = zeros((n_samples, 1))
	return X, y

#training