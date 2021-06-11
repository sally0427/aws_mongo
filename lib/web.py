from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import re
import time

url ='https://mbasic.facebook.com/'

#今天講個特別的，我們可以不讓瀏覽器執行在前景，而是在背景執行（不讓我們肉眼看得見）
#如以下宣告 options
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

#打開瀏覽器,確保你已經有chromedriver在你的目錄下
# 然後將options加入Chrome方法裡面，至於driver請用executable_path宣告進入
chrome_driver_path = '../chromedriver.exe'
browser = webdriver.Chrome(options = options, executable_path = chrome_driver_path)
#在瀏覽器打上網址連入
browser.get(url) 
print(browser.title)

#這時候就可以分析網頁裡面的元素
element = browser.find_element_by_name('q')
element.send_keys('環團')
element.send_keys(Keys.RETURN)
# login_form = browser.find_element_by_id('tsf')
# print(login_form)
# sumbit = browser.find_element_by_class_name('Tg7LZd').click()

# 等待目標表格'id 為 web'的div出現
# element = WebDriverWait(browser, 5).until(
#     expected_conditions.presence_of_element_located((By.ID, 'web'))
# )

# #然後就是beautifulsoup的範疇了，將browser.page_source放進去分析
# soup=BeautifulSoup(browser.page_source,"html.parser")
# links = soup.select('div#web h3')

# for link in links:
#     print(link.get_text())

# browser.quit()

# Crawler
next_page_times = 1
for _page in range(next_page_times):
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    content = soup.prettify()
    print(content)
    # Get titles and urls
    titles = re.findall('<h3 class="[\w\d]{6} [\w\d]{6}">\n\ +(.+)', content)
    urls = re.findall('<div class="r">\ *\n\ *<a href="(.+)" onmousedown', soup.prettify())

    print(titles)
    print(urls)
    print(min(len(titles), len(urls)))
    for n in range(min(len(titles), len(urls))):
        print(titles[n], urls[n])

    # Wait
    time.sleep(5)

    # Turn to the next page
    try:
        browser.find_element_by_link_text('下一頁').click()
    except:
        print('Search Early Stopping.')
        browser.close()
        exit()


# Close the browser
browser.close()