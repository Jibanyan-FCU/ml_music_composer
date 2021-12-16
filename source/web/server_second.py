from mu_model import model_api
from database import db_api

from flask import Flask, render_template, request, send_from_directory


app = Flask(__name__)
model_api.initial()

COMPARE_PATH = '/static/music/compare'
OUTPUT_PATH = '../mu_model/output'

@app.route('/', methods=['GET', "POST"])
def index():

    style = request.values.get('style')
    generate = request.values.get('generate')
    file = ""

    if style == None:
        style = ""

    if generate == "true":
        hidden = ""
        file = model_api.make_music()
        file = file.split('/')[-1]
    else:
        hidden = "hidden"

    db_api.open_db()
    df = db_api.search_compare_by_style(style)
    df = df.sample(5)
    df = df.sort_values("id")

    c_path = COMPARE_PATH
    return render_template('result.html', dataframe=df, compare_storage=c_path, hidden=hidden, download_file=file)

@app.route("/download/<filename>")
def download(filename):
    print(app.root_path)
    return send_from_directory(OUTPUT_PATH, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="localhost", port=80, debug=True)