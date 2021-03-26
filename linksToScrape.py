import requests
from urllib.request import urlopen
import numpy as np
import pandas as pd
import random
from bs4 import BeautifulSoup
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import regex as re
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')

# Creating driver object
driver = webdriver.Chrome(
    executable_path=r"C:\Users\aryam\OneDrive\Desktop\ML for Blog\chromedriver.exe", options=options)
# archiveUrls -> store the archive name
# publication -> store the publication name
archiveUrls = []
publication = []


urls = {
    'Towards Data Science': 'https://towardsdatascience.com/archive/{0}/{1:02d}/{2:02d}',
    'UX Collective': 'https://uxdesign.cc/archive/{0}/{1:02d}/{2:02d}',
    'The Startup': 'https://medium.com/swlh/archive/{0}/{1:02d}/{2:02d}',
    'The Writing Cooperative': 'https://writingcooperative.com/archive/{0}/{1:02d}/{2:02d}',
    'Data Driven Investor': 'https://medium.com/datadriveninvestor/archive/{0}/{1:02d}/{2:02d}',
    'Better Humans': 'https://medium.com/better-humans/archive/{0}/{1:02d}/{2:02d}',
    'Better Marketing': 'https://medium.com/better-marketing/archive/{0}/{1:02d}/{2:02d}',
}


# Checks if a particular year is a leap year or not
def is_leap(year):
    if year % 4 != 0:
        return False
    elif year % 100 != 0:
        return True
    elif year % 400 != 0:
        return False
    else:
        return True

# Returns the month and the day of the month


def convert_day(day, year):
    month_days = [31, 29 if is_leap(year) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m = 0
    d = 0
    while day > 0:
        d = day
        day -= month_days[m]
        m += 1
    return (m, d)


# Randomly select some days from the year
numDays = 2
selected_days = random.sample([i for i in range(1, 366)], numDays)


# generating list of urls to scrap from
i = 0
n = len(selected_days)
for d in selected_days:
    i += 1
    year = 2019
    month, day = convert_day(d, year)
    date = '{0}-{1:02d}-{2:02d}'.format(year, month, day)
    print(f'{i} / {n} ; {date}')

    for publication_name, url in urls.items():

        currUrl = url.format(year, month, day)

        # The try and except method basically checks for the validity of the url

        try:
            response = requests.get(url.format(year, month, day), allow_redirects=True)
            if not response.url.startswith(url.format(year, month, day)):
                print("Invalid URL")
                continue
            # response = requests.get(currUrl, allow_redirects=True)
            # print(response.url)

            # if not response.url.startswith(currUrl):
            #     print("Invalid URL")
            #     continue
        except:

            print("Invalid URL")
            continue

        publication.append(publication_name)
        archiveUrls.append(currUrl)

# Once we have got the publication archive urls , all we have to do is visit those links
# and from there gather all the links


articleLinks = []

articlePublications = []
id = 0
i = 0
for url in archiveUrls:
    id += 1

    time.sleep(2)
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    # the below class if for redirecting to articles url so its href contains the article links
    links = soup.find_all("a", class_="button button--chromeless u-baseColor--buttonNormal")
    links = [x['href'] for x in links]
    for link in links:
        articleLinks.append(link)
        articlePublications.append(publication[i])
    i += 1
    print(f'{id}/{len(archiveUrls)}')


archiveUrls = np.array(archiveUrls).reshape((-1, 1))
publication = np.array(publication).reshape((-1, 1))
articleLinks = np.array(articleLinks).reshape((-1, 1))
articlePublications = np.array(articlePublications).reshape((-1, 1))

dfArchives = np.concatenate((archiveUrls, publication), axis=1)
dfArticles = np.concatenate((articleLinks, articlePublications), axis=1)

dfArchives = pd.DataFrame(dfArchives)
dfArticles = pd.DataFrame(dfArticles)

dfArchives.columns = ['url', 'publication']
dfArticles.columns = ['url', 'publication']

dfArchives.to_csv('dfArchives.csv')
dfArticles.to_csv('dfArticles.csv')
