#載入這次需要的所有套件和function
"""
Post the query to Google　Search and get the return results
"""
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Browser settings
chrome_driver_path = 'D://env//fb//chromedriver.exe'
chrome_options = Options()
chrome_options.add_argument('--incognito')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Chrome/51.0.2704.103 Safari/537.36')
browser = webdriver.Chrome(options=chrome_options, executable_path = chrome_driver_path)

# Query settings
query = 'US Stock'
browser.get('https://www.google.com/search?q={}'.format(query))
next_page_times = 10

chrome_options.add_argument('--incognito')

chrome_options.add_argument('user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0')



def Crawler(key):
    # chrome_driver_path = 'D://env//fb//chromedriver.exe'

    for _page in range(next_page_times):
        soup = BeautifulSoup(browser.page_source, 'html.parser')
        content = soup.prettify()

        # Get titles and urls
        titles = re.findall('<h3 class="[\w\d]{6} [\w\d]{6}">\n\ +(.+)', content)
        urls = re.findall('<div class="r">\ *\n\ *<a href="(.+)" onmousedown', soup.prettify())

        for n in range(min(len(titles), len(urls))):
            print(titles[n], urls[n])
            print('aaa')

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