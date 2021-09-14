import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random as rand

from keras.models import Sequential, load_model
from keras.utils import np_utils
from keras.utils.vis_utils import plot_model #need to goin file(vis_utils)
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPool2D, LeakyReLU
from keras.optimizers import Adam
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

# set picture size
fig = plt.gcf()
fig.set_size_inches(40,40)

# 1 or 0
for sample_number in range(n_samples) :
  for row in range(measure_len) :
    for column in range(measure_pitch) :
      if X[sample_number][row][column]>0.5:
        X[sample_number][row][column] = 1
      else :
        X[sample_number][row][column] = 0

print("after only 1 and 0\n")

for i in range(n_samples):
	# define subplot
	plt.subplot(5, 5, 1 + i)
	# turn off axis labels
	plt.axis('off')
	# plot single image
	plt.imshow(X[i, :, :, 0], cmap='gray_r')
# show the figure
plt.show()

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
	opt = Adam(learning_rate=0.0002, beta_1=0.5)
	model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
	return model
 
# define model
model = define_discriminator()
# summarize the model
model.summary()
# plot the model
# plot_model(model, to_file='discriminator_plot.png', show_shapes=True, show_layer_names=True)

#prepare data
#link with preprocess
scores = open_and_trafer_score()
score = scores[0]
s = score.get_all_measure_graphs_and_feature()
measure = s[0]
def loda_data():
	'''
	i : uint8, 曲子數量, index of scores[]
	j : uint8, 每首曲子小節數量, index of s[]
	x_train : nparray([?,96,88])，裝用來訓練的100首曲子的小節圖
	y_train : nparray([?,96,88])，裝用來訓練的100首曲子的小節圖的label
	x_test : nparray([?,96,88])，裝用來測試的20首曲子的小節圖
	y_test : nparray([?,96,88])，裝用來測試的20首曲子的小節圖的label
	counter_train : uint8, counter of x_train and y_train([measure, , ])
	counter_test : uint8, counter of x_test and y_test([measure, , ])
	'''
	x_train=np.zeros([60,96,88])
	y_train=np.zeros([60,96,88])
	x_test=np.zeros([60,96,88])
	y_test=np.zeros([60,96,88])
	counter_train=0
	counter_test=0
	for i in range(0,100): #train
		score = scores[i] #曲子
		s = score.get_all_measure_graphs_and_feature()
		for j in range(len(s)):
			measure=s[j] #小節
			x_train[counter_train], y_train[counter_train] = measure['graph'], measure['feature']
			counter_train+=1
	for i in range(100,120): #test
		score = scores[i] #曲子
		s = score.get_all_measure_graphs_and_feature()
		for j in range():
			measure=s[j] #小節
			x_test[counter_test],y_test[counter_test] = measure['graph'], measure['feature']
			counter_test+=1
	return x_train, y_train, x_test, y_test


def load_real_sample():
	# x_train,Y_train is array
	(trainX,trainY), (testX, testY) = loda_data()
	# expand to 3d, e.g. add channels dimension
	X = expand_dims(trainX, axis=-1)
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
	y = measure['feature']
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

# train the discriminator model
def train_discriminator(model, dataset, n_iter=100, n_batch=256):
	half_batch = int(n_batch / 2)
	# manually enumerate epochs
	for i in range(n_iter):
		# get randomly selected 'real' samples
		X_real, y_real = generate_real_samples(dataset, half_batch)
		# update discriminator on real samples
		_, real_acc = model.train_on_batch(X_real, y_real)
		# generate 'fake' examples
		X_fake, y_fake = generate_fake_samples(half_batch)
		# update discriminator on fake samples
		_, fake_acc = model.train_on_batch(X_fake, y_fake)
		# summarize performance
		print('>%d real=%.0f%% fake=%.0f%%' % (i+1, real_acc*100, fake_acc*100))

