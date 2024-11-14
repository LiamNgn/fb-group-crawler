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

link = link_lst[4]
driver.get(link)

sleep(5)
print(link)
#Get profile name
profile_div = driver.find_element(By.XPATH,'//div[@data-ad-rendering-role="profile_name"]')
try:
    profile_link = profile_div.find_element(By.XPATH,'.//a').get_attribute('href')
    profile_info = profile_div.find_element(By.XPATH,'.//strong/span')
    profile_name = profile_info.get_attribute('innerHTML')
except NoSuchElementException:
    profile_link = None
    profile_info = profile_div.find_element(By.XPATH,".//object/div")
    profile_name = profile_info.get_attribute('innerHTML')



#Get creation date
creation_date_element = driver.find_element(By.XPATH,'//script[contains(text(), "creation_time")]')
json_creation_date = creation_date_element.get_attribute('text')
full_data = json.loads(json_creation_date)


scroll_until_end(driver)
sleep(5)
comments_expand(driver)
sleep(5)
post_expand(driver)

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

def find_all_key_paths(data, target_key, path=None, paths=None):
    if path is None:
        path = []
    if paths is None:
        paths = []
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = path + [key]  
            if key == target_key:
                paths.append(new_path)  
            find_all_key_paths(value, target_key, new_path, paths)
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = path + [index]  # Use index for list path
            find_all_key_paths(item, target_key, new_path, paths)
    return paths
# with open('json_file_name', 'r') as file:
#     data = json.load(file)

reaction_count = find_all_key_paths(full_data, 'i18n_reaction_count')
reaction_type = find_all_key_paths(full_data, 'localized_name')



tempType = full_data
tempData = full_data
reaction_result = {}
interested_data = reaction_count[1:-1]  ## TODO: Check if it is possible to have the fixed value [1:-1] like this
for re_type, re_data in zip(reaction_type,interested_data):
    for i, j in zip(re_type, re_data):
        tempType = tempType[i]
        tempData = tempData[j]
    reaction_result[tempType['localized_name']] = tempData
    tempData = full_data
    tempType = full_data





## Get post data

post_data = driver.find_elements(By.XPATH,"//div[@data-ad-preview='message']//span/div/div")
post_list = []
for post in post_data:
    post_list.append(post.get_attribute('innerHTML'))

image_in_post_list = driver.find_elements(By.XPATH,"//a[./div/div/div/div/img]")
if len(image_in_post_list) == 2:
    image_in_post = image_in_post_list[1].find_element(By.XPATH,".//img").get_attribute('src')
elif len(image_in_post_list == 1):
    image_in_post = None


##Find comments

comment_builder = comment_tree()

#Find all comment sections. A comment section is defined as a main comments and all of its children.
comment_sections = driver.find_elements(By.XPATH,"//div[./div/div[contains(@aria-label,'Comment by')  and @role = 'article']]")
for comment in comment_sections:
    comment_builder.build_comment_tree_section(comment)
    df = pd.DataFrame.from_dict([i for i in comment_builder._comment_registry.values()])


full_post = {'Post_url':link,"Post_username":profile_name,'Post_user_url':profile_link,
             'creation_date':result,'Post_content':post_list,'Image_in_post':image_in_post,'reaction_count': reaction_result,"All comments":df}

pickle.dump(full_post, open("test_comment.pkl","wb"))

#Find number of separate reactions

