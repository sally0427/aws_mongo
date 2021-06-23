# selenium
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import time
# from main import driver

def LoginFB(email, password, fan_page):
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
    # url = 'https://www.facebook.com/'  
    url = 'https://mbasic.facebook.com/' 

    # ------ 登入的帳號與密碼 ------
    username = email
    password = password

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
    elem.send_keys(fan_page)   

    elem.send_keys(Keys.RETURN)
    time.sleep(1)

    # elem = driver.find_element_by_xpath(".//html/body/div/div/div/div/div/div/div/div/div/div/div/div/div/table/tbody/tr/td/a/div/div").click()

    return driver

def GetArticleText():
    # 找到第一篇文章，點更多檢視完整文章
    # heading1 = driver.find_element_by_tag_name('p')
    Article = driver.find_element_by_tag_name('article').find_element_by_xpath(".//div/div/div/span")
    # Article = driver.find_element_by_tag_name('article').find_element_by_xpath(".//div/div/div/a")
    # Article.click()
    # # 點進第一篇文章
    # Article = Article.find_element_by_xpath(".//html/body/div/div/div/div/div/div/div/div/div/div/div") 
    # print('Article:', Article.text)

    #檢查有沒有被擋下來
    if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
        driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

    # 儲存文章成為txt
    with open('./dataset/article.txt', 'w', encoding='utf-8') as f:
        f.write(Article.text)
    

def GetCommentText():
    # 找到第一篇文章留言按鈕
    heading1 = driver.find_element_by_tag_name('footer').find_element_by_xpath(".//div/a").click()

    # 找到多則留言
    time.sleep(1)
    comments = driver.find_elements_by_xpath("/html/body/div/div/div/div/div/div/div/div/div/div/div[1]")
    comment_list = []
    for comment in comments:
        comment_list.append(comment.text)
        # print('comment:', comment.text)
   
    #檢查有沒有被擋下來
    if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
        driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

    return comment_list