from pickle import load
from .processer import *
from .model import *

_pattern_manager = Pattern_Manager()
_preprocesser = Preprocesser()
_postprocesser = Postprocesser()

_mu_model = Mu_Model(load_model=True, load_note=True)
_is_implemented = False

def _check_initial(function):
    def warpper(*args, **kwargs):
        if not _is_implemented:
            raise NotImplementedError('Please call `initial()` to implement model and pattern.')
        return function(*args, **kwargs)
    return warpper


def initial(load_note=True, load_model=True):
    global _is_implemented

    if not _is_implemented:
        if load_note:
            _pattern_manager.load_notes()
        else:
            _pattern_manager.prepare_sequences()
        
        if load_model:
            _mu_model.load_model()
        else:
            _mu_model.create_model()

        _is_implemented = True

@_check_initial
def train_model(epochs=2000, batch_size=100, train_melody=True, train_rhythm=True):
    _mu_model.create_model()
    _mu_model.train(epochs, batch_size, train_melody=train_melody, train_rhythm=train_rhythm)
    _mu_model.draw_line_chat()

@_check_initial
def make_music(pattern_index=None):    
    file_name = _postprocesser.make_music(pattern_index=pattern_index)
    return file_name

@_check_initial
def make_compare_music(pattern_index=None):
    file_names = _postprocesser.make_compare(pattern_index=pattern_index)
    return file_names

    


    
    
    
