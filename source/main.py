from web import server_second

if __name__ == "__main__":
    server_second.app.run(host='127.0.0.1',port='80',debug=True) #執行的意思，debug的意思是如果你更改程式碼並儲存，那他將會重啟，變為你剛才更新後的樣子