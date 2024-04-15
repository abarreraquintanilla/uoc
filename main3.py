# Importing packages

import pandas as pd
import requests, random
import time
from bs4 import BeautifulSoup


pd.options.mode.chained_assignment = None
# Scraping the data

data_dict = {'name':[], 'platform':[], 'release_date':[], 'metascore':[], 'user_score':[]}

def webpage(pageNum):
    #HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
    AGENTS = (
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')

    # create headers
    HEADERS = requests.utils.default_headers()
    HEADERS['User-Agent'] = random.choice(AGENTS)

    url = 'https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page=' + str(pageNum)
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=HEADERS)
    return response

def numberPages(response):
    soup = BeautifulSoup(response.text, 'html.parser')
    pages = soup.find_all('li', {"class": "active_page"})
    pages2 = soup.find_all('span', class_='c-navigationPagination_itemButtonContent u-flexbox u-flexbox-alignCenter u-flexbox-justifyCenter')
    pagesCleaned = pages[0].find('span', {"class":"page_num"})
    return (pagesCleaned.text)

def scraper(num_loops, content):
    tblnum = 0
    while tblnum < num_loops:
        #get game name
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr)<1:
                continue
            td = tr.find_all('td')
            a = td[1].find('a', {"class":"title"})
            data_dict['name'].append(a.find('h3').text)
            #print(a.find('h3').text)

# get game release date

        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr) < 1:
                continue
            td = tr.find_all('td')
            date = td[1].find('span', {"class": ""})
            data_dict['release_date'].append(date.text)
            # print(date.text)

        # get artist
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr) < 1:
                continue
            td = tr.find_all('td')
            p1 = td[1].find('div', {"class": "platform"})
            platform = p1.find('span', {"class": "data"})
            data_dict['platform'].append(platform.text.strip())
            # print(platform.text.strip())
        # get userscore
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr) < 1:
                continue
            td = tr.find_all('td')
            div_score = td[1].find('div', {"class": "clamp-userscore"})
            user = div_score.find('div', {"class": "metascore_w"})
            data_dict['user_score'].append(user.text.strip())
            # print(user.text.strip())

        # get metascore
        table_rows = content[tblnum].find_all('tr')
        for tr in table_rows:
            if len(tr) < 1:
                continue
            td = tr.find_all('td')
            score = td[1].find('div', {"class": "metascore_w"})
            data_dict['metascore'].append(score.text)
            # print(score.text)
        tblnum += 1
def pages(lastPageNum):
    currentPage = lastPageNum
    url = url = 'https://www.metacritic.com/browse/game/?releaseYearMin=1958&releaseYearMax=2024&page=' + str(currentPage)
    userAgent = {'User-agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=userAgent)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find_all('table')

    num_loops = len(content)
    # print(num_loops)
    scraper(num_loops, content)
    # print(data_dict)
    # time.sleep(6)
def main():
    # The link need to be checked to verify how many pages that have
    pgs = list(range(0, 199))
    for pg in pgs:
        numPage = (numberPages(webpage(pg)))
        pages(int(pg))
        time.sleep(5)
        print("Page " + str(pg + 1) + " completed")
    xData = (pd.DataFrame.from_dict(data_dict))
    xData.to_csv('allgames.csv')


main()