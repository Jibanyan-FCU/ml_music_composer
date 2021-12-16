
import sqlite3
import pandas as pd

from database.db_command import make_db_command

_DB_PATH = './database/music_DB.db'

DB = None

def open_db():
    global DB
    DB = sqlite3.connect(_DB_PATH)

def close_db():
    DB.close()

def insert_compare_command(real, fake, style):
    
    cmd = f'''
        INSERT INTO compare(real, fake, style)
        VALUES("{real}", "{fake}", "{style}")
    '''

    cur = DB.cursor()

    cur.execute(cmd)
    DB.commit()


def search_compare_by_style(style):

    cmd = f'''
        SELECT * FROM compare WHERE style LIKE "%{style}%"
    '''

    df = pd.read_sql_query(cmd, DB)
    return df


