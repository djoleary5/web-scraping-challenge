from splinter import Browser
from bs4 import BeautifulSoup
import requests
import os
import time
from selenium import webdriver
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/chromedriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    
    mars = {}

    ### NASA Mars News
    browser = init_browser()
    mars_url = 'https://mars.nasa.gov/news/'
    browser.visit(mars_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")   
    results = soup.find_all('div', class_="content_title")
    news_title = results[0].text
    results = soup.find_all('div', class_="article_teaser_body")
    news_p = results[0].text
    news = {"title": news_title,
       "text": news_p}

    ### JPL Mars Space Images - Featured Image
    browser = init_browser()
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('a', class_="button fancybox")
    fullimg_url = 'https://www.jpl.nasa.gov' + results[0]['data-link']
    browser = init_browser()
    browser.visit(fullimg_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('figure', class_="lede")
    featured_image_url = 'https://www.jpl.nasa.gov'+results[0].a['href']

    ### Mars Weather
    marstwit_url = 'https://twitter.com/marswxreport?lang=en'
    browser = init_browser()
    browser.visit(marstwit_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('div', class_="js-tweet-text-container")
    time.sleep(3)
    mars_weather = results[0].p.text

    ### Mars Facts
    res = requests.get("https://space-facts.com/mars/")
    soup = BeautifulSoup(res.content,'lxml')
    table = soup.find_all('table')[0] 
    marsfacts_df = pd.read_html(str(table))
    marsfacts_df = marsfacts_df[0]
    marsfacts_df.columns = ['Stats', 'Mars']
    marsfacts_df = marsfacts_df[['Stats', 'Mars']].set_index('Stats')
    marsfacts_url = marsfacts_df.to_html()

    ### Mars Hemispheres
    #cerberus
    img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'
    browser = init_browser()
    browser.visit(img_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('img', class_="wide-image")
    img_url1 = 'https://astrogeology.usgs.gov/'+results[0]['src']
    #schiaparelli
    img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'
    browser = init_browser()
    browser.visit(img_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('img', class_="wide-image")
    img_url2 = 'https://astrogeology.usgs.gov/'+results[0]['src']
    #syrtis_major
    img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'
    browser = init_browser()
    browser.visit(img_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('img', class_="wide-image")
    img_url3 = 'https://astrogeology.usgs.gov/'+results[0]['src']
    #valles_marineris
    img_url = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'
    browser = init_browser()
    browser.visit(img_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    results = soup.find_all('img', class_="wide-image")
    img_url4 = 'https://astrogeology.usgs.gov/'+results[0]['src']
    ### Mars Hemispheres
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": img_url4},
        {"title": "Cerberus Hemisphere", "img_url": img_url1},
        {"title": "Schiaparelli Hemisphere", "img_url": img_url2},
        {"title": "Syrtis Major Hemisphere", "img_url": img_url3},
    ]

    mars["news"] = news
    mars["Image"] = featured_image_url
    mars["Weather"] = mars_weather
    mars["Facts"] = marsfacts_url
    mars["Hemispheres"] = hemisphere_image_urls

    return mars