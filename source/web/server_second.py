from flask import Flask, render_template, request
from database import db_api

app = Flask(__name__)

COMPARE_PATH = '/static/music/compare'
@app.route('/', methods=['GET', "POST"])
def index():

    style = request.values.get('style')
    if style == None:
        style = ""
    print(">>> ", style)
    db_api.open_db()
    df = db_api.search_compare_by_style(style)
    df = df.sample(5)
    df = df.sort_values("id")

    c_path = COMPARE_PATH
    return render_template('result.html', dataframe=df, compare_storage=c_path)


if __name__ == '__main__':
    app.run(host="localhost", port=80, debug=True)