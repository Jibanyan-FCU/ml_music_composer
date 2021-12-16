from mu_model import model_api
from database import db_api

model_api.initial()
db_api.open_db()

STYLE = "game"
for _ in range(100):
    file_names = model_api.make_compare_music()
    real = file_names['real'].replace(".mid", ".mp3")
    fake = file_names['fake'].replace(".mid", ".mp3")
    print(real.replace(".mp3",""))
    db_api.insert_compare_command(real, fake, STYLE)

db_api.close_db()


