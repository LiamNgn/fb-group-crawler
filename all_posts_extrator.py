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
import my_logger

root_logger = logging.getLogger()
file_handler = logging.FileHandler('main_log.log')
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

my_logger.my_function()



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
# facebook_login(driver)
# sleep(4)

loadCookies(driver)

print('Cookies loaded. Login successfully.')

sleep(3)

logging.basicConfig(filename = 'crawl_log.log',filemode = 'w',level = logging.INFO)

# link = link_lst[4]

# link = 'https://www.facebook.com/groups/bumblevietnam/posts/2274733519385781/?__cft__[0]=AZWdy4syLwW-i-Tm5Xu5Fjmd-PljhkFQ9PG_Aiyw9dB08PspK--dwX8PjDKIxhmN2hyfPHoMZu0gu7IT8g1rMB0adD7dp8zsuw9vaZ6QeoY6olu26DUjVJCijho6rwMpltf8AKnSNTI-y50VQPqcPsRvHFd_azjvzEdxWsCxSsBcWbijazcxMwrdNeYuJEb1iI3jc6lmC9zNtjsLHPTeKGDnEfojAgiS5SkFa1fU-DQV0w&__tn__=%2CO%2CP-R./' # This link is obscured by a link to facebook homepage, which is weird -> TODO
# # link = "https://www.facebook.com/groups/bumblevietnam/posts/2381571642035301/"

# link = 'https://www.facebook.com/groups/bumblevietnam/posts/2382920688567063/'

# sleep(5)
# full_post = post_extrator(driver,link)

# with open("test_comment.pkl","wb") as f:
#     pickle.dump(full_post, f)

crawled_list = pickle.load(open("crawled_link_list.pkl", "rb"))
post_list = pickle.load(open("all_crawled_comments.pkl", "rb"))

i = 0
for link in link_lst:
    logging.info(f'Crawling {make_ordinal(i)} post.')
    print(f'Crawling {make_ordinal(i)} post.')
    if link in crawled_list:
        logging.info(f'Link already crawled. \n {link}')
        print(f'Link already crawled. \n {link}')
        continue
    else:
        pass
    try:
        logging.info(f'Crawling {link}')
        post = post_extrator(driver, link)
        post_list.append(post)
        crawled_list.append(link)
    except Exception as e:
        logging.error(e)
    i += 1

with open("crawled_link_list.pkl","wb") as f:
    pickle.dump(crawled_list, f)

with open("all_crawled_comments.pkl","wb") as f:
    pickle.dump(post_list, f)


