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
import logging
import my_logger
root_logger = logging.getLogger()
file_handler = logging.FileHandler('post_extractor.log')
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

my_logger.my_function()


##THis funtion is used to extract reactions and creation_time from the json_script
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


### Function to remove HTML tag
import re
# as per recommendation from @freylis, compile once only
CLEANR = re.compile('<.*?>') 

def clean_html(raw_html):
  cleantext = re.sub(CLEANR, '', raw_html)
  return cleantext




#This function is used to extract content of an individual post.
def post_extrator(driver,link):
        '''
        Given any link and a Selenium driver, this function will export post_url, post_username, post_user_url, image of the post(if available), creation_date, post_content, reactions_count (up to the level of each individual), and all comments
        '''
        driver.get(link)

        sleep(5)
        print(link)

        #Print all comments
        no_comment = False
        try:
            most_relevant = driver.find_element(By.XPATH,"//div[./span[contains(text(),'Most relevant')]]")
            sleep(2)
            most_relevant.click()
        except NoSuchElementException:
            no_comment = True

        sleep(2)

        view_all_comments = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, ".//div[./div/div/div/span[contains(text(),'All comments')]]")))
        view_all_comments.click()


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



        result = find_key(full_data, "creation_time")
        if result is None:
            print("Key not found")
        else:
            print("Creation Time:", result)

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

        post_list = []
        try:
            driver.find_element(By.XPATH,'//div[@data-ad-preview="message"]')
            post_data = driver.find_elements(By.XPATH,"//div[@data-ad-preview='message']//span/div/div")
            
            for post in post_data:
                try:
                    post.find_element(By.XPATH,".//a[contains(@href,'hashtag')]")
                    content = clean_html(post.get_attribute('innerHTML'))
                except NoSuchElementException:
                    content = post.get_attribute('innerHTML')
                post_list.append(content)
            image_in_post_list = driver.find_elements(By.XPATH,"//a[./div/div/div/div/img]")
            if len(image_in_post_list) == 2:
                image_in_post = image_in_post_list[1].find_element(By.XPATH,".//img").get_attribute('src')
            elif len(image_in_post_list) == 1:
                image_in_post = None
                

        except NoSuchElementException:
            full_post = driver.find_element(By.XPATH,"//div[@data-ad-rendering-role='story_message']/div/span")
            post_data = full_post.find_elements(By.XPATH,"./*")
            for section in post_data:
                try:
                    section.find_element(By.XPATH,".//a[contains(@href,'hashtag')]")
                    content = clean_html(section.get_attribute('innerHTML'))
                    post_list.append(content)
                except NoSuchElementException:
                    if section.tag_name == 'div':
                        try:
                            content = section.find_element(By.XPATH,'./div/span').get_attribute('innerHTML')
                        except NoSuchElementException:
                            try:
                                content = section.find_element(By.XPATH,'./div/div/span').get_attribute('innerHTML')
                            except NoSuchElementException:
                                content = section.find_element(By.XPATH,'.//span[not(span)]').get_attribute('innerHTML')
                        post_list.append(content)
                    elif section.tag_name =='ul':
                        content_list = section.find_elements(By.XPATH,'.//li/div/span')
                        bullet_points = ""
                        for content in content_list:
                            content = '- ' + content.get_attribute('innerHTML') + "\n"
                            bullet_points += content
                        
                        post_list.append(bullet_points)
            image_in_post_list = driver.find_elements(By.XPATH,"//a[./div/div/div/div/img]")
            if len(image_in_post_list) == 2:
                image_in_post = image_in_post_list[1].find_element(By.XPATH,".//img").get_attribute('src')
            elif len(image_in_post_list) == 1:
                image_in_post = None

        
        ##Find comments

        comment_builder = comment_tree()

        #Find all comment sections. A comment section is defined as a main comments and all of its children.
        if no_comment:
            df = None
        else:
            comment_sections = driver.find_elements(By.XPATH,"//div[./div/div[contains(@aria-label,'Comment by')  and @role = 'article']]")
            i = 0
            for comment in comment_sections:
                comment_builder.build_comment_tree_section(driver,comment)
                # sleep(3)
                df = pd.DataFrame.from_dict([i for i in comment_builder._comment_registry.values()])
                print(f'The {make_ordinal(i)} comment section will have cumulative {len(df)} comments')
                i += 1
            
        full_post = {'Post_url':link,"Post_username":profile_name,'Post_user_url':profile_link,
                    'creation_date':result,'Post_content':post_list,'Image_in_post':image_in_post,'reaction_count': reaction_result,"All comments":df}

        return full_post