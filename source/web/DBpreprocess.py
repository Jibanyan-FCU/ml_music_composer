from random import random
import sqlite3
import os
from mu_model import *
from mu_model_api import get_new_music

def insert_pattern(pattern_name):
    #
    command = make_db_command(0,pattern_name) # 取得指令
    patterndb.execute(command) # 輸入指令
    
    return

def insert_fake_file(pattern_id):
    # 
    fake_file_name = get_new_music(pattern_id) # 呼叫model生成音樂
    command = make_db_command(fake_file_name) # 取得指令
    comparedb.execute(command)
    return
def ramdom_compare_music():
    compare_id = randint(0,100)
    comparedb = sqlite3.connect(compare)
    command_fake = make_db_command(fake,compare_id)
    fake_path = comparedb.execute(command_fake) # 取得此id的fake_path
    command_true = make_db_command(true,compare_id)
    true_path = comparedb.execute(command_true) # 取得此id的true_path
    comparedb.commit()
    comparedb.close()
    compare_list = [true_path,fake_path] # 包裝成list
    return compare_list
def main():
    # preprocess
    pattern_list = 家齊的程式 # 取得pattern的list

        # put all pattern into database
            # 取得pattern
    patterndb = sqlite3.connect(pattern) # 連接pattern資料庫

    for i in range(len(pattern_list)):
        pattern_name = "".join(pattern_list[i]) # 取出pattern_list中的值並轉為字串
        insert_pattern(pattern_name)
    
    patterndb.commit() # 提交變動
    patterndb.close() # 斷開連接

        # ramdon make music and put into db
    comparedb = sqlite3.connect(compare) # 連接compare資料庫

    for i in range(100):
        # 每首隨機取1到2段pattern
        pattern_id=0
        insert_fake_file(pattern_id)
    
    comparedb.commit()
    comparedb.close()

    print("successfully preprocess!")
    return
if __name__ == '__main__':
    main()