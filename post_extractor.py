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








# for link in link_lst:
#     driver.get(link)
#     sleep(5)
#     scroll_until_end(driver)
#     sleep(5)
#     elements = driver.find_elements(By.XPATH('//div[./span/span[contains(text(),"repl")]]'))

link = link_lst[1]
driver.get(link)

sleep(5)

#Get profile name
profile_name_div = driver.find_element(By.XPATH,'//div[@data-ad-rendering-role="profile_name"]//object/div')
profile_name = profile_name_div.get_attribute('innerHTML')


#Get creation date
creation_date_element = driver.find_element(By.XPATH,'//script[contains(text(), "creation_time")]')
json_creation_date = creation_date_element.get_attribute('text')
full_data = json.loads(json_creation_date)


scroll_until_end(driver)
sleep(5)
comments_expand(driver)
sleep(5)
post_expand(driver)

page = driver.page_source.encode('utf-8') 
# print(page) 
  
# open result.html 
file_ = open('result.html', 'wb') 
  
# Write the entire page content in result.html 
file_.write(page) 
  
# Closing the file 
file_.close() 


# a = ActionChains(driver)
# print('Actions initiated.')


def find_key(data, target_key):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == target_key:
                return value
            result = find_key(value, target_key)
            if result is not None:
                return result
    elif isinstance(data, list):
        for item in data:
            result = find_key(item, target_key)
            if result is not None:
                return result
    return None


result = find_key(full_data, "creation_time")
if result is None:
    print("Key not found")
else:
    print("Creation Time:", result)

## Get post data

post_data = driver.find_elements(By.XPATH,"//div[@data-ad-preview='message']//span/div/div")
post_list = []
for post in post_data:
    post_list.append(post.get_attribute('innerHTML'))

print('\n'.join(post_list))

##Find comments

comment_builder = comment_tree()

#Find all comment sections. A comment section is defined as a main comments and all of its children.
comment_sections = driver.find_elements(By.XPATH,"//div[./div/div[contains(@aria-label,'Comment by')  and @role = 'article']]")
for comment in comment_sections:
    comment_builder.build_comment_tree_section(comment)
    df = pd.DataFrame.from_dict([i for i in comment_builder._comment_registry.values()])
    print(df)

pickle.dump(df, open("test_comment.pkl","wb"))
#Find number of separate reactions
# react = driver.find_element(By.XPATH,"//div[./div[contains(text(),'All reactions')]]")
sleep(5)
# react.click()
sleep(5)
# dialog = driver.find_element(By.XPATH,"//div[@role = 'dialog']")
sleep(5)
# driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)


#Scroll reaction section

# element_list = driver.find_elements(By.XPATH,"//div[@role = 'dialog']//div[contains(@style,'padding-left')]")
# element = element_list[-1]

# while True:
#     sleep(5)
#     driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", element)
#     sleep(10)
#     new_element_list = driver.find_elements(By.XPATH,"//div[@role = 'dialog']//div[contains(@style,'padding-left')]")
#     sleep(10)
#     if element == new_element_list[-1]:
#         break
#     else:
#         element = new_element_list[-1]
