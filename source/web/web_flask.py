from database import db_api
from mu_model import model_api

from flask import Flask, render_template
from flask.helpers import send_from_directory
#將flask中的Flask import 進來 以供使用
from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import Length, InputRequired
from flask_bootstrap import Bootstrap

OUTPUT_PATH = r"source\mu_model\output"
app = Flask(__name__) # 創建一個Flask的 instance
Bootstrap(app)

app.config['SECRET_KEY'] = 'this is a secret'

class LoginForm(FlaskForm):
    user_account = StringField('account',validators=[InputRequired(),Length(min=4,max=20)])
    user_password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])
    remember = BooleanField('remember me')

class Register(FlaskForm):
    #user_email = StringField('email',validators=[InputRequired(),Email(message='Invalid email'),Length(max=50)])
    user_account = StringField('account',validators=[InputRequired(),Length(min=4,max=20)])
    user_password = PasswordField('password',validators=[InputRequired(),Length(min=8,max=80)])

@app.route("/",methods=['GET', 'POST'])  # 告訴你怎樣的url可以call怎樣的function
def index():  # 就是一個function的名稱 上方的裝飾器會call他
    file_name = 'Bach_G_minor_arr._Luo_Ni.mxl'
    '''file_name = get_new_music()
    file_path = 'static/file'
    if file_name:
        return send_from_directory('index.html',file_path, file_name,as_attachment=True)'''
    if request.method == 'POST': # form action要指回這個檔案&method = post
        if request.values['send'] == 'Composing': # in html(nmae = 'send')
            return send_from_directory('static/file',file_name, as_attachment=True)
    return render_template('index.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

@app.route('/compose', methods=['GET', 'POST'])
def send_select():
    style_dict= {
        "遊戲配樂": "game",
        "貝多芬": "Beethoven",
        "莫札特": "Mozart",
        "蕭邦": "Chopin"
    }
    style = request.values.get('style_btn')
    style = style_dict[style]
    
    compose = model_api.make_music()
    compose = compose[1:]
    print(compose)
    return send_from_directory(OUTPUT_PATH, "output_2021-12-15_23''48'49.mid", as_attachment=True)

    

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    get_nickname =  request.values.get("nickname")
    get_account =  request.values.get("account")
    get_password =  request.values.get("password")
    get_repassword =  request.values.get("repassword")
    # database 
    return render_template('login.html',nickname = get_nickname,form = form)

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

