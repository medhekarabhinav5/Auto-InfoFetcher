#!/usr/bin/env python
# Getting Car news from web
# Decide website to be fetched from
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.debug("Start of Program.")

import pathlib
path_of_driver = pathlib.Path("chromedriver").parent.resolve()
logging.debug("Path of driver file is fetched.")

import smtplib, random
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
logging.debug('SMTP and Email Modules imported intp porgram.')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
logging.debug("Selenium modules imported into program.")

import requests
logging.debug("Requests imported into program.")

import time
from datetime import date, datetime, timedelta
from dateutil.parser import parse
logging.debug('Date related modules imported into program.')

CHROMEDRIVER_PATH = f"{path_of_driver}/chromedriver" # Chrome Driver Path
logging.debug(f"ChomeDriver Path : {CHROMEDRIVER_PATH}")

CHROME_PATH = ""
logging.debug(f"Chrome Path : {CHROME_PATH}")

WINDOW_SIZE = "1280,800" # Screen Size
logging.debug(f"Windows Size has been set to {WINDOW_SIZE}")

import pandas
logging.debug(f"Pandas module imported into program.")

chrome_options = Options()
chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)
chrome_options.add_argument("--headless")
chrome_options.binary_location = CHROME_PATH

prefs = {'profile.managed_default_content_settings.images' : 2}
chrome_options.add_experimental_option("prefs", prefs)
logging.debug("Disabling images on webpage for ChromeDriver, For faster loading")

driver = webdriver.Chrome(
executable_path = CHROMEDRIVER_PATH,
    chrome_options = chrome_options
)
logging.debug("Initializing ChromeDriver")

def check_exists_by_xpath(xpath): # Checking whether xpath is available
    try:

        driver.find_element_by_xpath(xpath)
        logging.debug(f"Checked Xpath : {xpath}")
    except:
        logging.debug(f"Checked path {xpath} does not exists")
        return False
    return True
    
link_info_list = []
users_list = []
logging.debug('News List generated.')
LinkCollectionStatus = True
falseLinkCount = 0
vehicleCount = 1
upcoming_link_respose = True
#current_date = str(date.today())
#yesterday_datetime = datetime.strptime((datetime.now() - timedelta(1)).strftime('%Y-%m-%d 19:00:00'), '%Y-%m-%d %H:%M:%S')
logging.debug("Getting links from Web Pages")

url = f"https://www.cardekho.com/filter/new-cars"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
logging.debug(f'Setting up url : {url}.')
logging.debug(f"setting up header : {headers}")
linkRequest = requests.get(url, headers=headers)
logging.debug('Getting url info.')
logging.debug(f"checking whether url {url} exists")
logging.debug(f"{linkRequest.status_code}")
if linkRequest.status_code == 200: # if  status of url is 200 then it will proceed.
    logging.debug(f"Successfully get 200 status for link : {url}")
    driver.get(url)
    totalCountXpath = '//*[@id="rf01"]/div[1]/div/main/div/div[1]/div[1]/div[1]/span'
    totalCountXpath_response = check_exists_by_xpath(totalCountXpath)
    if totalCountXpath_response:
        totalCountXpath_element = driver.find_element_by_xpath(totalCountXpath)
        totalCount = totalCountXpath_element.text
        logging.info(f'Number of Total Vehicles : {totalCount}')
               
    while upcoming_link_respose: 
        if falseLinkCount < 10:
            if vehicleCount % 10 == 0:
                falseLinkCount = 0 
                logging.debug('Program reached end on page, Scrolling down for more.')
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                time.sleep(4)
                logging.debug('letting Thread sleep for 4 seconds, for better loading of page.')
                """
                            //*[@id="rf01"]/div[1]/div/main/div/div[1]/div[2]/div[1]/div[2]/section/div[1]/div[2]/h3/a
                            //*[@id="rf01"]/div[1]/div/main/div/div[1]/div[2]/div[1]/div[3]/section/div[1]/div[2]/h3/a
                """
            link_xpath = f'//*[@id="rf01"]/div[1]/div/main/div/div[1]/div[2]/div[1]/div[{str(vehicleCount)}]/section/div[1]/div[2]/h3/a'
            logging.debug(f'link Xpath : {link_xpath}.')
            link_response = check_exists_by_xpath(link_xpath)
            if link_response == True:
                logging.debug("Responses to link returned True. Going Forward.")
                link_element = driver.find_element_by_xpath(link_xpath)
                link = link_element.get_attribute('href')
                logging.debug(f'Link from elements : {link}')
                link_info_list.append(link)    
                vehicleCount += 1
            else:
                logging.debug(f'Responses to Link is not True. Link Response : {link_response}')
                falseLinkCount += 1
                vehicleCount += 1
        else:
            logging.debug("False link count exceeds 10")
            upcoming_link_respose = False
print(link_info_list)
print(len(link_info_list))
                
