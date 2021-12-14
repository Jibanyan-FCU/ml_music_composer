#from mu_model.model_api import initial
from web import web_flask

#initial()
if __name__ == "__main__":
    web_flask.app.run(host='0.0.0.0',port='5000',debug=True) #執行的意思，debug的意思是如果你更改程式碼並儲存，那他將會重啟，變為你剛才更新後的樣子