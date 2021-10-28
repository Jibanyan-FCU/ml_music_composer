from datetime import timedelta
from flask import Flask, render_template, url_for, redirect
from flask.helpers import url_for
#將flask中的Flask import 進來 以供使用
from flask import request

app = Flask(__name__) # 創建一個Flask的 instance

#app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1) 
@app.route("/",methods=['POST','GET'])  # 告訴你怎樣的url可以call怎樣的function 許的method有什麼

@app.route("/")  # 告訴你怎樣的url可以call怎樣的function
def index():  # 就是一個function的名稱 上方的裝飾器會call他
    return render_template('index.html')
    '''
    if request.method == 'POST':
        if request.values['send'] == '送出':
            return render_template('index.html', name=request.values['user'])
    '''
    '''if name==None:
        return render_template("index.html")
    else:
        #return "Hello " + name + "!"
        return redirect(url_for('index')) #只要有name重新導向到index
    '''

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
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

'''if __name__ == "__main__":
	app.run(host='0.0.0.0',port='5000',debug=True) '''
#執行的意思，debug的意思是如果你更改程式碼並儲存，那他將會重啟，變為你剛才更新後的樣子
#ip = http://192.168.1.103:5000/
