from datetime import timedelta

from flask import Flask, render_template, url_for, redirect
from flask.helpers import send_from_directory, url_for
#將flask中的Flask import 進來 以供使用
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email,InputRequired
from flask_bootstrap import Bootstrap


from mu_model import model_api

app = Flask(__name__) # 創建一個Flask的 instance
Bootstrap(app)

app.config['SECRET_KEY'] = 'this is a secret'
'''app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'hb88501323@'
app.config['MYSQL_DB'] = 'bittobeat_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)''' 

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
    
    '''file_name = get_new_music()
    file_path = 'static/file'
    if file_name:
        return send_from_directory('index.html',file_path, file_name,as_attachment=True)'''
    # file_name = model_api.make_music()
    return render_template('index.html')
   
    
    '''
    if request.method == 'POST':
        if request.values['send'] == '送出':
            return render_template('index.html', name=request.values['user'])
    
    if name==None:
        return render_template("index.html")
    else:
        #return "Hello " + name + "!"
        return redirect(url_for('index')) #只要有name重新導向到index
    

@app.route("/aaaaa", methods=['GET', 'POST'])
def make_new_song():
    file_name = get_new_music()

    return send_from_directory(OUTPUT_PATH, file_name, as_attachment=True)'''

@app.route('/result', methods=['GET', 'POST'])
def result():
    return render_template('result.html')

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
#ip = http://192.168.1.103:5000/
#ip = http://10.22.30.249:5000/
