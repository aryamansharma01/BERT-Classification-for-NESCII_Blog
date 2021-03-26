import regex as re
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import random
import pandas as pd
import numpy as np
from urllib.request import urlopen
import requests
import os

options = webdriver.ChromeOptions()
options.add_argument("--incognito")
options.add_argument("headless")
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--ignore-ssl-errors')


# Creating driver object


def getRow(url):
    #url = "https://medium.com/curious-cult/advice-from-30-year-old-me-to-20-year-old-me-b9b035d39e2d"
    time.sleep(5)
    # sending a request to the page
    driver = webdriver.Chrome(
        executable_path=r"C:\Users\aryam\OneDrive\Desktop\ML for Blog\chromedriver.exe", options=options)
    driver.get(url)
    # Getting the page source
    html = driver.page_source

    driver.close()
    # print(driver.title) # Title of the page
    # print(driver.current_url)  # get the current url
    soup = BeautifulSoup(html, "html.parser")

    # There seems to be only 1 heading

    # Getting the title
    try:
        title = soup.find("h1").contents[0]
        print(title)
    except:
        title = 'N/A'
    try:
        # finding keywords
        # the script helps us to find the text as well as the keywords
        keywordScript = str(soup.find_all('script', type='application/ld+json')[0].contents)

        # we could improve the regex expression , though it seems to work correctly right now
        keyWordList = re.findall("Tag:[a-zA-Z0-9 ]*", keywordScript)

        keyWordList = ','.join([x[4:] for x in keyWordList])
        # for keyWord in keyWordList:
        #     print(keyWord)

        # Trying to get the text
        # If we look at the script of the page source which we have extracted above , we will find that
        # the text is availabel in parts in the script in the pattern __typename:paragragh,name:.....:text:"this is our text"
        # the following regex expressions extracts all such text and joins them
        #reExpression = '(?<="__typename":"Paragraph","name":"[a-zA-Z0-9]*","text":).*?(?=","type":)'
        regex = 'min read(.*)'
        textArray = re.findall(regex, soup.text)
        extractedText = ' '.join(textArray)

        # title = re.sub('[^0-9a-zA-Z]+','',title)
        # keyWordList = re.sub('[^0-9a-zA-Z]+',keyWordList)
        # text = re.sub('[^0-9a-zA-Z]+',text)

        titles.append(title)
        keywords.append(keyWordList)
        articleUrls.append(url)
        text.append(extractedText)
    except:
        pass


filepath = r"C:\Users\aryam\OneDrive\Desktop\ML for Blog\Links"
for file in os.listdir(filepath):
    dfArticles = pd.read_csv(filepath + "\\"+file)
    #dfArticles = pd.read_csv('dfArticles.csv')
    titles = []  # Stores all the titles
    keywords = []  # Stores KeyWord Corresponding to all the text
    articleUrls = []  # stores all the urls
    text = []  # stores the page text
    publication = []
    # we go through each url
    i = 0
    for row in dfArticles.iloc[:, :].values:
        i += 1
        if(i == len(dfArticles.iloc[:, ].values)):
            break
        # publication.append(row[1])
        print(i, row[0])
        getRow(row[0])

    titles = np.array(titles).reshape((-1, 1))
    keywords = np.array(keywords).reshape((-1, 1))
    articleUrls = np.array(articleUrls).reshape((-1, 1))
    text = np.array(text).reshape((-1, 1))
    #publication = np.array(publication).reshape((-1, 1))

    df = np.concatenate((titles, articleUrls, keywords, text), axis=1)  # publication,
    df = pd.DataFrame(df)
    df.columns = ['title', 'articleUrls', 'keywords', 'text']  # 'publication', ]
    df.to_csv('Scraped '+file, index=None, encoding='utf-8')
