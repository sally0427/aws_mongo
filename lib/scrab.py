import requests
from bs4 import BeautifulSoup

def scrab_title(url, keyword):
    address = url + "search.aspx?q=" + keyword
    r = requests.get(address)

    soup = BeautifulSoup(r.text,"html.parser")
    sel_url = soup.select("div.newsimg-area-info a")
    sel_title = soup.select("div.image-container img")
    result = []
    
    s_url = []
    s_title = []
    for address in sel_url:
        if address:
            address = url + address["href"]
            s_url.append(address)
        else:
            s_url.append("")

    for title in sel_title:
        if title:
            s_title.append(title["alt"])
        else:
            s_title.append("")        

    for i in range(len(s_url)):
        s = []
        if s_title[i] != "" and s_url[i] != "":
            s.append(s_title[i])
            s.append(s_url[i])
            result.append(s)
    
    return result