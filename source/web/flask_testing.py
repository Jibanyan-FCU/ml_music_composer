# model relative module
from keras.models import load_model
import numpy as np
import pickle
import music21
import time
from random import randint
import os

OUTPUT_PATH = 'static/file/'

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
        file_name = f'output_{t.tm_year}_{t.tm_mon}_{t.tm_mday}_{t.tm_hour}_{t.tm_min}_{t.tm_sec}.mid'
        file_path = f'{OUTPUT_PATH}/{file_name}'
        midi_stream = music21.stream.Stream(melody)
        
        try:
            midi_stream.write('midi', fp=file_path)
        except FileNotFoundError:
            os.system('mkdir output')
            midi_stream.write('midi', fp=file_path)

        return file_name


# API
_MODEL = Mu_Model()
def get_new_music(*args, **kwargs):
    return _MODEL.make_music()


# web server relative module
from datetime import timedelta

from flask import Flask, render_template, url_for, redirect
from flask.helpers import send_from_directory, url_for
#將flask中的Flask import 進來 以供使用
from flask import request
from flask_sqlalchemy import SQLAlchemy
import pymysql
import pymysql.cursors
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email,InputRequired
from flask_bootstrap import Bootstrap

model = Mu_Model
app = Flask(__name__)
Bootstrap(app)

app.config['SECRET_KEY'] = 'this is a secret'
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'hb88501323@'
# app.config['MYSQL_DB'] = 'bittobeat_db'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# mysql = MySQL(app)

class LoginForm(FlaskForm):
    user_account = StringField('account',validators=[InputRequired(),Length(min=4,max=20)])
    user_password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    remember = BooleanField('remember me')
#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1) 

class Register(FlaskForm):
    #user_email = StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    user_account = StringField('account',validators=[InputRequired(),Length(min=4,max=20)])
    user_password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])

@app.route("/",methods=['GET', 'POST'])  # 告訴你怎樣的url可以call怎樣的function
def index():  # 就是一個function的名稱 上方的裝飾器會call他
    get_time = request.values.get("time_btn")
    get_style = request.values.get("style_btn")
    get_mood = request.values.get("mood_btn")

    if(get_mood!=""):
        print("----------------------------------------------------------123132------------------")
    else:
        file_name = get_new_music()
        print(file_name)
    return render_template('index.html',time=get_time,style=get_style,mood=get_mood)

@app.route('/compose', methods=['GET', 'POST'])
def send_select():
    get_time = request.values.get("time_btn")
    get_style = request.values.get("style_btn")
    get_mood = request.values.get("mood_btn")
    print("1111111111111111111111111111111111111111111111111")
    print(get_time)
    print("1111111111111111111111111111111111111111111111111")
    return render_template('compose.html', time=get_time,style=get_style,mood=get_mood)

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    get_nickname =  request.values.get("nickname")
    get_account =  request.values.get("account")
    get_password =  request.values.get("password")
    get_repassword =  request.values.get("repassword")
    # database 
    return render_template('login.html',nickname = get_nickname,form = form)
    '''
	if request.method == 'POST':
        if request.values['userid'] in member:
			if member[request.values['userid']]['password'] == request.values['userpw']:
				return redirect(url_for('index'))
			else:
				return render_template('login.html', alert="Your password is wrong, please check again!")
		else:
			return render_template('login.html', alert="Your account is unregistered.")
    '''

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    return render_template('upload.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',user_name=name)

#can't find error
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

#service error
@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500

if __name__ == "__main__":
	app.run(host='0.0.0.0',port='5000',debug=True) #執行的意思，debug的意思是如果你更改程式碼並儲存，那他將會重啟，變為你剛才更新後的樣子