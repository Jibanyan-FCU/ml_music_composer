from model.model import *

dcgan = DCGAN(load_path=None)

dcgan.train(10)

dcgan.save_model()