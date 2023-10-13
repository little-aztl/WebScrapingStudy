from urllib.request import urlopen
from urllib.parse import urlparse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import re
import pandas as pd

def getBeautifulSoup(url) -> BeautifulSoup:
    try:
        html = urlopen(url)
    except HTTPError as e:
        print('This url' + url + 'has a HTTPError:', end=' ')
        print(e)
        return None
    except URLError as e:
        print('This url' + url + 'has an URLError:', end=' ')
        print(e)
        return None
    else:
        return BeautifulSoup(html, 'lxml')

visitedSite = []
problemSet = {}

def explore(url):
    bs = getBeautifulSoup(url)
    if not bs:
        return
    print("Arrived at the site:   " + url)
    # print(bs.h1.get_text())
    try:
        title = bs.find('div', attrs={'id' : 'pagebody'}).h2.get_text()
        problemSet[url] = title
    except:
        pass
    for link in bs.find_all('a', attrs={'href' : re.compile('^(/|.*http://dsa.openjudge.cn)((?!solution|submit|statistics|clarify).)*$')}):
        # print(link)
        if link.attrs['href']:
            newUrl = link.attrs['href']
            if newUrl[0] == '/':
                newUrl = 'http://dsa.openjudge.cn' + newUrl
            if newUrl in visitedSite:
                continue
            visitedSite.append(newUrl)
            print('the length of visitedSite is', len(visitedSite))
            explore(newUrl)
    pass

visitedSite.append('http://dsa.openjudge.cn/')
explore('http://dsa.openjudge.cn/')
print("finish the visiting process")
print(problemSet)

result_excel = pd.DataFrame()
result_excel['题目'] = list(problemSet.values())
result_excel['网址'] = list(problemSet.keys())
result_excel.to_excel('rsl.xlsx')