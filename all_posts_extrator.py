from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import FirefoxOptions,FirefoxService
import os
from selenium.webdriver.common.alert import Alert
from time import sleep
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, MoveTargetOutOfBoundsException
from util import *  
from selenium.webdriver.firefox.options import Options
import pickle
from io import StringIO
import lxml.etree
from selenium.webdriver.common.action_chains import ActionChains
import json
from post_extractor import post_extrator
import logging

with open('link_list.pkl', 'rb') as f:
    link_lst = pickle.load(f)

firefoxOptions = FirefoxOptions(); 
firefoxOptions.set_preference("dom.webnotifications.enabled",False); 
driver = webdriver.Firefox(firefoxOptions)

driver.get("https://www.facebook.com/")

sleep(3)
decline_cookie = driver.find_element(By.CSS_SELECTOR,'div.x1i10hfl:nth-child(2)')
decline_cookie.click()

sleep(4)
facebook_login(driver)
sleep(4)

loadCookies(driver)

print('Cookies loaded. Login successfully.')

sleep(3)

logging.basicConfig(filename = 'crawl_log.log',filemode = 'w',level = logging.INFO)

# link = link_lst[4]

# link = 'https://www.facebook.com/groups/bumblevietnam/posts/2381987825327016/' // This link is obscured by a link to facebook homepage, which is weird -> TODO
link = "https://www.facebook.com/groups/bumblevietnam/posts/2381571642035301/"



sleep(5)
full_post = post_extrator(driver,link)


# post_2023 = []
# for link in link_lst:
#     post = post_extrator(driver, link)
#     post_2023.append(link)

with open("test_comment.pkl","wb") as f:
    pickle.dump(full_post, f)

#Find number of separate reactions

