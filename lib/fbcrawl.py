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
url = 'https://mbasic.facebook.com/' 
url = 'https://www.facebook.com/'  

# ------ 登入的帳號與密碼 ------
username = 'a29853602@gmail.com'
password = 'sally31613'

chrome_driver_path = '../chromedriver.exe'
# ------ 透過Browser Driver 開啟 Chrome ------
driver = webdriver.Chrome(options = options, executable_path = chrome_driver_path)

# ------ 前往該網址 ------
driver.get(url)        
print(driver.title)

# ------ 帳號密碼 ------
# time.sleep(1)
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
elem = driver.find_element_by_id("email")
elem.send_keys(username)

elem = driver.find_element_by_id("pass")
elem.send_keys(password)        

elem.send_keys(Keys.RETURN)
time.sleep(5)


#檢查有沒有被擋下來
if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
    driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

# 切換頁面
# spec_url = 'https://www.facebook.com/moea.gov.tw'
# driver.get(spec_url)

# 將網頁元素放入Beautifulsoup
soup = Soup(driver.page_source,"html.parser")

soup.find(class_ ='ecm0bbzt hv4rvrfc ihqw7lf3 dati1w0a').text
# print(soup)

postime = soup.find(class_ ='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw')
# <a class="oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw" href="https://www.facebook.com/hen.zhi.90/posts/4336971842997448?__cft__[0]=AZWL8TWF9anVXBY3pUznI15meWp2lB0UkUwbSrj8uZYQBCb_Ek3yGB21Y6gdGUKsBIFnG-W6qFF2NxHGnBQPV4jS1KptNREYlOKaL9c3pk5B5VWpgYN7NgxW9kRsr_U96STkZeITUtXfGmUHXWRiSm3628pkb7nRH553gur_8RtqXQ&amp;__tn__=%2CO%2CP-R" role="link" tabindex="0">
# postime.text.strip('=')
postime.text
print(postime.text)
print('b')

