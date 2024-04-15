from bs4 import BeautifulSoup
import requests
import pandas as pd
import unicodedata
import numpy as np
import datetime as dt

# Read in existing weather history

url = 'https://weather.com/weather/tenday/l/c6148c650a003d5bbc56e014e5f6161ca4f80b14eba0d1d761c18e0961fd8932'
res = requests.get(url)
print(res.status_code)
soup = BeautifulSoup(res.content, 'html.parser')


body = soup.body
body.prettify

date_headers = body.find_all('h3', class_='DetailsSummary--daypartName--kbngc')

forecast_dates = [date.text for date in date_headers]

dates = []

for date in date_headers:
    dates.append(date.text)

# Convert the numbers to actual dates

tomorrow = dt.date.today() + dt.timedelta(1)
dates = [tomorrow + dt.timedelta(days=i) for i in range(len(dates))]

# Create list of days
# In future, just extract from the datetime column. Having issues with this though.
days = []
months = []
years = []

for i, date in enumerate(dates):
    if (i + 1) == len(dates):
        continue
    else:
        days.append(date.day)
        months.append(date.month)
        years.append(date.year)



Htemps = soup.find_all(class_='DetailsSummary--highTempValue--3PjlX')
high_temps = []
for i, temp in enumerate(Htemps):
    if i == 0:
        continue
    else:
        high_temps.append(int(temp.text.strip('°')))

Ltemps = soup.find_all(class_='DetailsSummary--lowTempValue--2tesQ')
low_temps = []
for i, temp in enumerate(Ltemps):
    if i == 0:
        continue
    else:
        low_temps.append(temp.text)

for i in range(min(len(low_temps), len(high_temps))):
    low_temps[i] = int(low_temps[i].strip('°'))
    high_temps[i] = int(high_temps[i])

# Pull the precipitation probability

precip_headers = soup.find_all(class_='DetailsSummary--precip--1a98O')

precip_prob = []

for i,day in enumerate(precip_headers):
    if i ==0:
        continue
    else:
        precip_prob.append((day.find_all('span'))[0].text)

# Convert precip probability to a decimal

precip_prob = [float(x.strip('%')) / 100 for x in precip_prob]

# Pull in wind stats

wind_stats = []

wind_scrape = soup.find_all(class_='Wind--windWrapper--3Ly7c undefined')

for i,day in enumerate(wind_scrape):
    if i == 0:
        continue
    else:
        clean_text = unicodedata.normalize("NFKD", day.text)
        wind_stats.append(clean_text)

# Create a dictionary with all the information

num_days = len(high_temps)

forecast_detail = {}
forecast_dict = {}

forecast_date = dt.date.today()

for i in range(num_days):
    forecast_detail[dates[i]] = {'high_temp': high_temps[i], 'low_temp': low_temps[i],
                                 'precip_prob': precip_prob[i], 'wind_stats': wind_stats[i]}

forecast_dict[forecast_date] = forecast_detail

# Transform dict into a dataframe

weather_df = pd.DataFrame.from_dict(forecast_dict[forecast_date]).T

weather_df['forecast_date'] = forecast_date

# Convert the forecast date column to a datetime object
weather_df['forecast_date'] = pd.to_datetime(weather_df['forecast_date'])

weather_df['date'] = weather_df.index

weather_df['day'] = days
weather_df['month'] = months
weather_df['year'] = years

weather_df.set_index('forecast_date', inplace=True)

weather_df.reset_index(inplace=True)


weather_df.to_csv('./Data/barcelona.csv')

#as
