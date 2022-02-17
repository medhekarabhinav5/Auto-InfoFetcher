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

import requests, re, os
logging.debug("Requests, re and os imported into program.")

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

def check_exists_by_xpath(xpath, xpathDriver): # Checking whether xpath is available
    try:

        xpathDriver.find_element_by_xpath(xpath)
        logging.debug(f"Checked Xpath : {xpath}")
    except:
        logging.debug(f"Checked path {xpath} does not exists")
        return False
    return True
    
link_info_list = []
link_info_list_used = []
model_variant_link_list = []
model_variant_link_list_used = []
users_list = []
logging.debug('News List generated.')
LinkCollectionStatus = True
falseLinkCount = 0
vehicleCount = 1
upcoming_link_response = True
logging.debug("Getting links from Web Pages")

currentDirectory = os.getcwd()
parentDir = "India/CarDekho"
currentWParent = os.path.join(currentDirectory, parentDir)
logging.debug(f"Got Current working Directory {currentDirectory}")
if os.path.isdir(currentWParent):
    print("Exists")
    logging.debug(f"Directory {currentWParent} exists")
else:
    os.makedirs(currentWParent)
    logging.debug(f"{currentWParent} does not exists, Creting one")
# # # # # # # # # # # # # # # # # # # # # #
# Getting Vehicle list from page
# # # # # # # # # # # # # # # # # # # # # # 
url = f"https://www.cardekho.com/filter/new-cars"
vehicleFileName = "vehicleList.txt"
os.chdir(currentWParent)
logging.debug(f"Changing current directory to {currentWParent}")
vehicleList = open(vehicleFileName, "w")
logging.debug(f"Creating file to write vehicle details, filename is {vehicleFileName}")
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
    totalCountXpath_response = check_exists_by_xpath(totalCountXpath, driver)
    if totalCountXpath_response:
        totalCountXpath_element = driver.find_element_by_xpath(totalCountXpath)
        totalCount = totalCountXpath_element.text
        logging.info(f'Number of Total Vehicles : {totalCount}')
               
    while upcoming_link_response: 
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
            link_response = check_exists_by_xpath(link_xpath, driver)
            if link_response == True:
                logging.debug("Responses to link returned True. Going Forward.")
                link_element = driver.find_element_by_xpath(link_xpath)
                link = link_element.get_attribute('href')
                logging.info(f'Link from elements : {link}')
                link_info_list.append(link) 
                vehicleList.write(link + "\n")   
                vehicleCount += 1
            else:
                logging.debug(f'Responses to Link is not True. Link Response : {link_response}')
                falseLinkCount += 1
                vehicleCount += 1
        else:
            logging.debug("False link count exceeds 10")
            upcoming_link_response = False

vehicleList.close()


# # # # # # # # # # # # # # # # # # # # # #
#Getting variants Link list
# # # # # # # # # # # # # # # # # # # # # #
logging.debug("Getting Variants link from link list")
logging.debug("Initializing driver for Variants")
driver.close()
modelDriver = webdriver.Chrome(
executable_path = CHROMEDRIVER_PATH,
    chrome_options = chrome_options
)
logging.debug("Initializing ChromeDriver")

for link in link_info_list:
    model_url = link
    link_info_list_used.append(model_url)
    logging.debug(f'Setting up url for Model: {model_url}.')
    logging.debug(f"setting up header for Model: {headers}")
    modelLinkRequest = requests.get(model_url, headers=headers)
    logging.debug('Getting url info.')
    logging.debug(f"checking whether url {model_url} exists")
    logging.debug(f"{modelLinkRequest.status_code}")
    if modelLinkRequest.status_code == 200: # if  status of url is 200 then it will proceed.
        logging.debug(f"Successfully get 200 status for link : {model_url}")
        modelDriver.get(model_url)
        vehicleName_Xpath = '//*[@id="overview"]/div/div/div[2]/h1'
        vehicleName_response = check_exists_by_xpath(vehicleName_Xpath, modelDriver)
        if vehicleName_response:
            vehicleName_element = modelDriver.find_element_by_xpath(vehicleName_Xpath)
            logging.debug(f"Checking Vehicle Xpath, got {vehicleName_element}")
            vehicleName = vehicleName_element.text
            logging.debug(f"Vehicle Name is {vehicleName}")
            splitz = model_url.split('/')
            logging.debug("Splitting URL to get Brand and Model")
            brand_name = splitz[-2].replace('_', ' ').replace('-', ' ').title()
            model_name = splitz[-1].replace('_', ' ').replace('-', ' ').title()
            logging.debug(f"Checking whether Model Name Consists Brand name, Remove if Exists")
            if re.search(brand_name, model_name):
                model_name = model_name.replace(brand_name, '').strip()
                logging.debug(f"Got Brand Name {brand_name} in Model {model_name}")
            logging.info(f'Vehicle Name : {brand_name} , {model_name}')

        for tabNum in range(15):
            modelXpath = f'//*[@id="rf01"]/div[1]/div/nav/div[2]/div/ul/li[{tabNum}]/a'
            logging.debug(f"Model Xpath : {modelXpath}")
            modelXpath_response = check_exists_by_xpath(modelXpath, modelDriver)
            logging.debug(f"Model Xpath response : {modelXpath_response}")
            if modelXpath_response:
                model_variantXpath_element = modelDriver.find_element_by_xpath(modelXpath)
                model_variant_link_text = model_variantXpath_element.text
                modelVariant_link = model_variantXpath_element.get_attribute("href")
                if model_variant_link_text == "VARIANTS":
                    logging.debug(f"checking link {modelVariant_link}'s status code")
                    variantLinkRequest = requests.get(modelVariant_link, headers=headers)
                    logging.debug(f"Status Code : {variantLinkRequest.status_code}")
                    if variantLinkRequest.status_code == 200:
                        vehicleInfoDict = {'brand' : brand_name, 'model' : model_name, 'variantlink' : modelVariant_link}
                        model_variant_link_list.append(vehicleInfoDict)
                        logging.debug(f'Model Variant Link : {modelVariant_link}')                    
                else:
                    continue
        else:
            continue
else:
    modelDriver.close()


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# Getting Internal List of variants for each Vehicle
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

logging.debug("Initializing Chromedriver for Variant list fetching")
variantDriver = webdriver.Chrome(
    executable_path = CHROMEDRIVER_PATH,
    chrome_options = chrome_options
)

for dict in model_variant_link_list:
    logging.debug("Looping through Model Variant Link List")
    print(dict['variantlink'])

