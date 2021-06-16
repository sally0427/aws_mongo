# selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as Soup
from selenium.webdriver.common.action_chains import ActionChains

import time
import pandas as pd
# from main import driver

def LoginFB():
    options = webdriver.ChromeOptions()
    prefs = {
        'profile.default_content_setting_values':
            {
                'notifications': 2
            }
    }
    options.add_experimental_option('prefs', prefs)
    options.add_argument("--incognito") 
    options.add_argument("disable-infobars")

    # ------ 設定要前往的網址 ------
    url = 'https://www.facebook.com/'  
    url = 'https://mbasic.facebook.com/' 

    # ------ 登入的帳號與密碼 ------
    username = 'a29853602@gmail.com'
    password = 'sally31613'

    chrome_driver_path = './chromedriver.exe'
    # ------ 透過Browser Driver 開啟 Chrome ------
    global driver
    driver = webdriver.Chrome(options = options, executable_path = chrome_driver_path)

    # ------ 前往該網址 ------
    driver.get(url)        
    print(driver.title)

    # ------ 帳號密碼 ------
    # time.sleep(1)
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@name="email"]')))
    elem = driver.find_element_by_name("email")
    elem.send_keys(username)

    elem = driver.find_element_by_name("pass")
    elem.send_keys(password)        

    elem.send_keys(Keys.RETURN)
    time.sleep(1)

    # 點下"稍後再說"
    click=driver.find_element_by_link_text("稍後再說").click()

    # 前往蔡英文粉專
    elem = driver.find_element_by_name("query")
    elem.send_keys("蔡英文")   

    elem.send_keys(Keys.RETURN)
    time.sleep(1)

    return driver

def GetArticleText():
    # 找到第一篇文章
    heading1 = driver.find_element_by_tag_name('p')
    # print('heading1:', heading1.text)

    #檢查有沒有被擋下來
    if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
        driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

    # 儲存文章成為txt
    with open('./dataset/article.txt', 'w', encoding='utf-8') as f:
        f.write(heading1.text)
    

def GetCommentText():
    # 找到第一篇文章留言按鈕
    commentaires = driver.find_elements_by_xpath("//a[@class='ea']")
    for item in commentaires:
        # print('item:', item.text)    
        item.click()
        break

    # 找到多則留言
    # WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, "//div[@class='en']")))
    time.sleep(1)
    comments = driver.find_elements_by_class_name('el')
    comment_list = []
    for comment in comments:
        comment_list.append(comment.text)
        # print('comment:', comment.text)
   
    #檢查有沒有被擋下來
    if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
        driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

    return comment_list