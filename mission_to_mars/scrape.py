from bs4 import BeautifulSoup as bs 
import requests 
from splinter import Browser
import pymongo
import pandas as pd

def scrape():
    final_dict = {}

    # Finding Most recent title and summary 

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    # list_text = soup.find('div', class_='list_text')
    # news_title = list_text.find('div', class_='content_title')
    # final_dict['title'] = news_title
    # final_dict['text'] = list_text 

    news_title = soup.find('div', class_='content_title').text
    news_title.replace("\n","")
    final_dict['news_title'] = news_title

    list_text = soup.find('div', class_='rollover_description').text
    list_text.replace("\n","")
    final_dict['list_text'] = list_text
    # Find the spaceimage using splinter 

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'html.parser')
    soup

    feat_img = soup.find("div", class_='carousel_items').find("article", class_='carousel_item').find("a")['data-fancybox-href']
    full_url = f'https://www.jpl.nasa.gov{feat_img}'
    final_dict['feat_img'] = full_url
    # close browser 
    browser.quit()

    # Scraping twitter

    url = 'https://twitter.com/marswxreport?lang=en'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    tweet = soup.find('p', class_ = "TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    final_dict['tweet'] = tweet

    # Scraping Mars Facts using pandas 
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts = tables[0]
    mars_facts.to_html('mars_facts.html')
    final_dict['mars_fact'] = mars_facts.to_html()

    # Scraping Mars Hemispheres
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response = requests.get(url)
    soup = bs(response.text, 'lxml')

    title = []
    hemi = soup.find_all('div', class_ = 'description')
    hemi = soup.find_all('h3')
    hemi[0].text.replace('Enhanced','')
    for i in hemi:
        title.append(i.text.replace('Enhanced',''))
    
    new_url = []
    for a in soup.find_all('a', class_ = 'itemLink product-item', href=True):
        new_url.append(a['href'])

    hemi_url = 'https://astrogeology.usgs.gov/'
    imgs = []
    for i in new_url:
        response = requests.get(f'{hemi_url}{i}')
        soup = bs(response.text, 'lxml')
        finder =  soup.find('img', class_ = 'wide-image')
        full_url_img = f'{hemi_url}{finder["src"]}'
        imgs.append(full_url_img)

    hemi_list = []
    hemi_dict = {}
    y = 0
    for i in title:
        hemi_dict = {'title':i , 'images_url': imgs[y]}
        hemi_list.append(hemi_dict)
        y += 1

    final_dict['hemi_list'] = hemi_list

    return final_dict
