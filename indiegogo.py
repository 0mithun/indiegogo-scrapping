from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import ElementNotVisibleException
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import time
import csv
import json

from json import JSONDecodeError

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--start-maximized")



project_url = []
filter_url = []

def get_all_project(url, cities):
    for city in cities:
        url = url + "&q="+city+',%20US'
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get(url)
        while(True):
            try:
                more = browser.find_element_by_xpath('//*[@class="i-cta-1 ng-binding ng-isolate-scope"]')
                time.sleep(3)
                more.click()
            except ElementNotVisibleException:
                break
        soup = BeautifulSoup(browser.page_source,'lxml')
        get_all_project_link(soup)
        browser.close()


def get_all_project_link(soup):
    all_item = soup.find('div', class_="exploreDetail-campaigns")
    items = all_item.find_all('div', class_="discoverableCard")
    for single_item in items:
        link = single_item.find('a')['href']
        link = link.replace('/pies','#/')
        link = 'https://www.indiegogo.com'+ link
        if link not in project_url:
            project_url.append(link)

def filter_project(url):
    for link in url:
        html = requests.get(link).content
        soup = BeautifulSoup(html,'lxml')
        script = soup.find_all('script')[16].text
        data = script.replace('//<![CDATA[','').replace('//]]>','')
        data =data.split(';')
        data = data[17]
        data = data.replace('gon.trust_passport=','')
        try:
            data = json.loads(data)
            location = data['project']['country']
            if (location == 'United States'):
                filter_url.append(link)
        except JSONDecodeError:
            pass

def write_csv(data, filename="file.csv"):
    with open(filename, 'w', newline='') as csvfile:
        f = csv.writer(csvfile)
        for line in data:
            f.writerow([line])

cities = ['Anniston']
url = "https://www.indiegogo.com/explore/home?project_type=campaign&project_timing=all&sort=trending"


get_all_project(url=url, cities=cities)

filter_project(project_url)
write_csv(filter_url, filename='test.csv')




