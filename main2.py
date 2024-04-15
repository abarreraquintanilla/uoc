from bs4 import BeautifulSoup
import requests, random
import pandas as pd

movie_dict = {'title':[], 'url':[], 'description':[], 'meta':[]}
films = []

AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36')

#create headers
HEADERS               = requests.utils.default_headers()
HEADERS['User-Agent'] = random.choice(AGENTS)

url_tab = []
for page in range(1,10): #Remember to update the number of pages
    url = 'https://www.metacritic.com/browse/movie/?releaseYearMin=1910&releaseYearMax=2024&page='+str(page)

    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    urls = soup.find_all('a', class_='c-finderProductCard_container g-color-gray80 u-grid')
    #titles = soup.find_all('h3', {"class": "c-finderProductCard_titleHeading"})
    #rates = soup.find_all('div', {"class": "c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_xsmall"})
    #descriptions = soup.find_all('div', {"class": "c-finderProductCard_description"})

    for i,url in enumerate(urls):
        if i ==0:
            continue
        else:
            url_tab.append((url['href']))

print(url_tab)

for url in url_tab:
    film_info = {}
    url = 'https://www.metacritic.com' + str(url)
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.find('div', {"class": "c-productHero_title g-inner-spacing-bottom-medium g-outer-spacing-top-medium"})
    film_info['title'] = title.text.strip()
    rate_meta = soup.find('div', {"class":'c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green g-color-gray90 c-siteReviewScore_medium'})
    film_info['rate_meta'] = rate_meta.text
    rate_user = soup.find('div',{"class":'c-siteReviewScore u-flexbox-column u-flexbox-alignCenter u-flexbox-justifyCenter g-text-bold c-siteReviewScore_green c-siteReviewScore_user g-color-gray90 c-siteReviewScore_medium'})
    try:
        film_info['rate_user'] = rate_user.text
    except AttributeError:
        pass
    genre = soup.find('a',{"class":'c-globalButton_container g-text-normal g-height-100 u-flexbox u-flexbox-alignCenter u-pointer u-flexbox-justifyCenter g-width-fit-content'})
    film_info['genre'] = genre.text.strip()

    director = soup.find('a',{"class":'c-crewList_link u-text-underline'})
    film_info['director'] = director.text.strip()

    #writers = soup.find_all('div',{"class":'c-crewList g-inner-spacing-bottom-small c-productDetails_staff_directors'})

    header_info = soup.find_all('div',{"class":'c-heroVariant_headerInfo g-inner-spacing-medium g-text-bold u-flexbox u-flexbox-alignCenter'})
    for i,header in enumerate(header_info):
        if i ==0:
            continue
        else:
            film_info['year'] = (header.find_all('span'))[0].text.strip()
            try:
                film_info['studio'] = (header.find_all('span'))[2].text.strip()
            except IndexError:
                pass
            try:
                film_info['duration'] = (header.find_all('span'))[3].text.strip()
            except IndexError:
                pass

    films.append(film_info)


print(films)
df = pd.DataFrame(films)
df.to_csv('films.csv')

#https://towardsdatascience.com/web-scraping-metacritic-reviews-using-beautifulsoup-63801bbe200e


