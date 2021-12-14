from selenium import webdriver
from selenium.webdriver.common.by import By
import time

__USER_NAME = "XXXXXXXXXXXX"
__PASSWORD = 'XXXXXXXXXXXX'

sheet = "_1objW"
#sheet的element 比較麻煩一點 對樂譜圖片右鍵檢查 找到div class = "_xxxxxx"類似這樣的

# 關閉通知
def login():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument("disable-infobars")
    page = 0
    addr = "https://musescore.com/sheetmusic?instrumentation=114&musicxml_instruments=1&recording_type=public-domain"
    # 打啟動selenium 務必確認driver 檔案跟python 檔案要在同個資料夾中
    driver = webdriver.Chrome(options=options)
    driver.get("https://musescore.com/user/login?destination=%2F")
    time.sleep(3)

    #輸入email
    context = driver.find_element_by_css_selector('#username')
    context.send_keys(__USER_NAME)
    time.sleep(0.5)

    #輸入password
    context = driver.find_element_by_css_selector('#password')
    context.send_keys(__PASSWORD)
    time.sleep(0.5)

    #
    commit = driver.find_element_by_xpath('/html/body/div/div/section/section/main/div/section/div/form/div/div[1]/button')
    commit.click()
    time.sleep(1)

    #
    driver.get(addr)
    time.sleep(0.5)
    test = driver.find_elements(By.CLASS_NAME, sheet)
    print(len(test))
    if page == 0:
        for i in range (0,len(test)):
            test[i].click()
            time.sleep(1)
            try:
                commit = driver.find_element_by_xpath("//span[text()='Download']")
                commit.click()
                time.sleep(1)
                download = driver.find_element_by_xpath('/html/body/article/section/div/section/section/section/div[3]/div/div[1]/h3/button/span')
                download.click()
                time.sleep(1)
            except:
                print("No element")
            driver.get(addr)
            test = driver.find_elements(By.CLASS_NAME, sheet)
        time.sleep(1)
        page += 1
    for page in (2,100):
        print(page)
        addr1 = "https://musescore.com/sheetmusic?instrumentation=114&musicxml_instruments=1&page="
        addr2 = "&recording_type=public-domain"
        addr3 = addr1+str(page)+addr2
        driver.get(addr3)
        time.sleep(1.5)
        test = driver.find_elements(By.CLASS_NAME, sheet)
        for i in range (0,len(test)):
            test[i].click()
            time.sleep(1.5)
            try:
                commit = driver.find_element_by_xpath("//span[text()='Download']")
                commit.click()
                time.sleep(1.5)
                download = driver.find_element_by_xpath('/html/body/article/section/div/section/section/section/div[3]/div/div[1]/h3/button/span')
                download.click()
                time.sleep(1.5)
            except:
                print("No element")
            driver.get(addr3)
            test = driver.find_elements(By.CLASS_NAME, sheet)
        time.sleep(1.5)

if __name__ == '__main__':
        login()