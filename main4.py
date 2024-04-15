from bs4 import BeautifulSoup
import requests, random


AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')

#create headers
HEADERS               = requests.utils.default_headers()
HEADERS['User-Agent'] = random.choice(AGENTS)

url = "https://www.metacritic.com/browse/movie/all/all/all-time/new/?releaseYearMin=1910&releaseYearMax=2023&page=1"

page = requests.get(url, headers=HEADERS)
soup = BeautifulSoup(page.content, 'html.parser')
target_div = soup.find("div", {"class": "c-productListings"})
titles = soup.find_all('h3', {"class": "c-finderProductCard_titleHeading"})
rates = soup.find_all('div', {"class": "c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall"})
descriptions = soup.find_all('div', {"class": "c-finderProductCard_description"})
dates = soup.find_all('div', {"class": "c-finderProductCard_meta"})


tittle_tab = []

for i,page in enumerate(titles):
    if i ==0:
        continue
    else:
        tittle_tab.append((page.find_all('span'))[0].text)

description_tab = []
for i,description in enumerate(descriptions):
    if i ==0:
        continue
    else:
        description_tab.append((description.find_all('span'))[0].text)

meta_tab = []
for i,rate in enumerate(rates):
    if i ==0:
        continue
    else:
        meta_tab.append((rate.find_all('span'))[0].text)



