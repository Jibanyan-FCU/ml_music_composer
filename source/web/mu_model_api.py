import mu_model

def get_new_music(*args, **kwargs):
    model = mu_model.Mu_Model()
    return model.make_music()

# print(__name__)
if __name__ == '__main__':
    get_new_music()