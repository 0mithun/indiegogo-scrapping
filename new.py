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
        # url = url + "&q="+city+',%20US'
        count = 0
        browser = webdriver.Chrome(executable_path="E:\chromedriver_win32\chromedriver.exe", chrome_options=chrome_options)
        browser.get(url)
        while(True):
            count +=1
            print(count)
            # if(count> 425):
            #     break
            try:
                more = browser.find_element_by_xpath('//*[@class="i-cta-1 ng-binding ng-isolate-scope"]')
                time.sleep(3)
                more.click()
            except ElementNotVisibleException:
                break
        soup = BeautifulSoup(browser.page_source,'lxml')
        get_all_project_link(soup)
        # browser.close()


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
        print(link)
        html = requests.get(link).content
        soup = BeautifulSoup(html,'lxml')
        script = soup.find_all('script')[3].text
        data = script.replace('//<![CDATA[','').replace('//]]>','')
        try: 
            funding_data = data.split('gon.embedded_discoverable_card=')[1]
            funding_data = funding_data.split(';gon')[0]
            data = data.split('gon.trust_passport=')[1]
            data = data.split(';gon')[0]

            funding = 0
            location = ''
            try:
                funding_data = json.loads(funding_data)
                funding = funding_data['discoverable']['funds_raised_amount']
                print(funding)
            except JSONDecodeError:
                pass
            try:
                data = json.loads(data)
                location = data['project']['country']
                print(location)
            except JSONDecodeError:
                pass
            if (location == 'United States'):
                if funding > 9999:
                    print('ok')
                    filter_url.append(link)
        except IndexError:
            print('Error')

def write_csv(data, filename="file.csv"):
    with open(filename, 'w', newline='') as csvfile:
        f = csv.writer(csvfile)
        for line in data:
            f.writerow([line])

cities = ['Anniston']
url = "https://www.indiegogo.com/explore/audio?project_type=campaign&project_timing=all&sort=most_funded"


# get_all_project(url=url, cities=cities)

# filter_project(project_url)
# write_csv(filter_url, filename='filter_projects.csv')
# write_csv(project_url, filename='test.csv')

websites = [
'https://www.indiegogo.com/projects/the-molok/pica',
'https://www.indiegogo.com/projects/my-level-up/pica',
'https://www.indiegogo.com/projects/the-film-lab/pica',

]


filter_project(websites)
write_csv(filter_url, filename='filter_projects.csv')

