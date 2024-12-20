from time import sleep
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException, MoveTargetOutOfBoundsException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from selenium.webdriver.remote.webelement import WebElement
import hashlib
import uuid
import logging
import my_logger

root_logger = logging.getLogger()
file_handler = logging.FileHandler('util_log.log',mode = 'w')
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)

my_logger.my_function()



#Util function
def make_ordinal(n):
    '''
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    '''
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

##Page manipulation function
def scroll_until_end(driver,pause_time = 4):
    #This function scroll infinitely until the web is no longer scrollable
    SCROLL_PAUSE_TIME = pause_time


    print('Start scrolling.')
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print(last_height)
    while True:
        # Scroll down to bottom


        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def post_expand(driver):
    #This function expand all post visible on a Facebook webpage 
    i = 1
    while True:
        sleep(4)

        try: 
            driver.find_element(By.XPATH,"//div[./div/div/span/div/div/div[text() = 'See more']]")
        except NoSuchElementException:
            break
        sleep(3)
        parent_element = driver.find_element(By.XPATH,"//div[./div/div/span/div/div/div[text() = 'See more']]")
        sleep(3)
        element = WebDriverWait(parent_element, 40).until(EC.element_to_be_clickable((By.XPATH, ".//div[text()='See more']")))
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", parent_element)
            sleep(3)
            ActionChains(driver).move_to_element(element).click().perform() 
        print(f"Click see more {make_ordinal(i)} time.")
        i += 1 
    print('Out of see more button.')


## Login and save cookies, an .env file is a must.

def facebook_login(driver):
    load_dotenv()
    email_elem = driver.find_element(By.ID, "email")  # Locate by ID
    email_elem.send_keys(os.environ.get("EMAIL"))

    password_elem = driver.find_element(By.ID, "pass")  # Locate by ID
    password_elem.send_keys(os.environ.get("PASSWORD"))

    password_elem.send_keys(Keys.RETURN)
    sleep(5)
    saveCookies(driver)

def saveCookies(driver):
# Get and store cookies after login
    cookies = driver.get_cookies()

    # Store cookies in a file
    pickle.dump( cookies, open("cookies.pkl","wb"))
    print('New Cookies saved successfully')


def loadCookies(driver):
    # Check if cookies file exists
    if 'cookies.pkl' in os.listdir():
        # Load cookies to a vaiable from a file
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        # Set stored cookies to maintain the session
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        print('No cookies file found')
    sleep(5)
    driver.refresh() # Refresh Browser after login


## Handling comments
## From this point onwards, a comment section is defined as the result of 
## the following XPATH: //div[./div/div[contains(@aria-label,'Comment by')  and @role = 'article']]

def comments_expand(driver):
    #This function expand all comments visible on a Facebook webpage 
    i = 1
    while True:
        sleep(3)
        try: 
            driver.find_element(By.XPATH,"//div[./span/span[contains(text(),'View more')]]")
        except NoSuchElementException:
            break
        sleep(3)
        element = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[./span/span[contains(text(),'View more')]]")))
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", element)
            sleep(3)
            ActionChains(driver).move_to_element(element).click().perform() 
        print(f"Click view more comments {make_ordinal(i)} time.")
        i += 1
    i = 1
    while True:
        sleep(3)

        try: 
            driver.find_element(By.XPATH,"//div[./span/span[contains(text(),'repl')]]")
        except NoSuchElementException:
            break
        sleep(3)
        element = WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[./span/span[contains(text(),'repl')]]")))
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", element)
            sleep(3)
            ActionChains(driver).move_to_element(element).click().perform() 
        print(f"Click view more replies {make_ordinal(i)} time.")
        i += 1 
    print('Out of view more replies button.')



def is_comment_single(comment):
    list_comments = comment.find_elements(By.XPATH,"./div[./*]")
    # print([i.get_attribute('outerHTML') for i in list_comments])
    # print(len(list_comments))
    if len(list_comments) == 1:
        return True
    else:
        return False
    
class CommentValueError(Exception):
    pass

@dataclass
class Comment:
    ID: str
    user_name: str
    user_group_link: str
    content: str
    media: str
    children: List['Comment'] = None
    ParentID: Optional[str] = None


    def __post_init__(self):
        self.children = self.children or []

    def to_dict(self) -> Dict:
        return {
            "ID": self.ID,
            "Username": self.user_name,
            "User_URL": self.user_group_link,
            "Content": self.content,
            "ParentID": self.ParentID,
        }

class comment_tree:
    def __init__(self):
        self._comment_registry: Dict[str, Comment] = {}
        self._used_ids: Set[str] = set()

    def _comment_extraction_with_id_generator(self,driver, comment: WebElement, parent_id: Optional[str] = None) -> str:
        '''
        Generate ID for a comment based on its properties including name, link, comment, content, parentID.
        Args:
            comment: a selenium WebElement, in our case it is a single comment section as specified above
            parent_id: ID of the parent comment (if exists)
        '''
        # print("Extracting comment.")
        # print(comment.get_attribute('innerHTML'))
        # print(parent_id)
        logging.info(f'Extracting comment with parent_id {parent_id} and innerHTML')
        logging.info('+++++++')
        logging.info(comment.get_attribute('innerHTML'))
        logging.info('=======')
        if not is_comment_single(comment):
            raise CommentValueError("The comment must be single!")
        # comment_content = comment.find_elements(By.XPATH,"./div[./*]")
        comment_user = comment.find_element(By.XPATH,".//div[contains(@aria-label,'by')]//span/a[./span]")
        comment_user_link = "".join(["https://facebook.com",comment_user.get_attribute('href')])
        comment_user_name = comment_user.find_element(By.XPATH,"./span/span").get_attribute('innerHTML')
        # print(comment.get_attribute('innerHTML'))
        try:
            comment_content = comment.find_element(By.XPATH,".//div[@style = 'text-align: start;']").get_attribute('innerHTML')
        except NoSuchElementException:
            try:
                comment_content = comment.find_element(By.XPATH,".//a/img").get_attribute('src')
            except NoSuchElementException:
                try:
                    comment_content = comment.find_element(By.XPATH,".//video").get_attribute('src')
                except NoSuchElementException:
                    try:
                        comment_content = comment.find_element(By.XPATH,".//div[@role = 'button' and ./img]/img").get_attribute('src')
                    except NoSuchElementException:
                        try:
                            comment_content = comment.find_element(By.XPATH,".//div/img").get_attribute('src')
                        except Exception as e:
                            logging(e)
            

        # a = ActionChains(driver)

        try:
            # comment_image_element = comment.find_element(By.XPATH,".//a[./img]")
            # try:
            #     a.move_to_element(comment_image_element).perform()
            #     sleep(5)
            # except MoveTargetOutOfBoundsException:
            #     driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", comment_image_element)
            #     sleep(5)
            #     a.move_to_element(comment_image_element).perform()
            comment_media = comment.find_element(By.XPATH,".//a[./img]/img").get_attribute('src')
        except NoSuchElementException:
            try:
                comment_media = comment.find_element(By.XPATH,".//video").get_attribute('src')
            except NoSuchElementException:
                try:
                    comment_media = comment.find_element(By.XPATH,".//div[@role = 'button' and ./img]/img").get_attribute('src')           
                except NoSuchElementException:
                    try:
                        comment_media = comment.find_element(By.XPATH,".//div/img").get_attribute('src')
                    except NoSuchElementException:
                        comment_media = None
        #Create the unique string combining properties of the comments
        unique_string = f"{parent_id or ''}:{comment_user_name}:{comment_user_link}:{comment_content}:{uuid.uuid4()}"

        # Generate hash
        hash_object = hashlib.md5(unique_string.encode())
        base_id = hash_object.hexdigest()[:8]

        # Ensure ID is unique by adding suffix if necessary
        node_id = base_id
        counter = 1
        while node_id in self._used_ids:
            node_id = f"{base_id}_{counter}"
            counter += 1

        
        self._used_ids.add(node_id)
        return {'ID': node_id,'ParentID':parent_id,'Name':comment_user_name,'Group URL': comment_user_link,
                'Content':comment_content,'Media': comment_media}
    def build_comment_tree_section(self, driver, comment_section: WebElement, parent_id: Optional[str] = None) -> Optional[Comment]:
        '''
        
        '''
        try:
            comment_list = comment_section.find_elements(By.XPATH,"./div[./*]")
            parent_comment = comment_list[0]
            parent_comment_info = self._comment_extraction_with_id_generator(driver,parent_comment, parent_id)
        except CommentValueError:
            parent_comment = comment_section
            comment_list = [comment_section]
            # print('Checking removed comments')
            # print(parent_comment.get_attribute('innerHTML'))
            parent_comment_info = self._comment_extraction_with_id_generator(driver,parent_comment, parent_id)   
        # print(parent_comment_info)

        #Process children comments
        children = []
        removed_comment = []
        try:
            children_list = comment_list[1].find_elements(By.XPATH,"./div[./*]/div[./div/div[contains(@aria-label,' by ') and @role = 'article' and not(contains(text(),'has been deleted'))]]")
            if len(children_list) == 0:
                children_list = comment_list[1].find_elements(By.XPATH,"./div[./div/div[contains(@aria-label,' by ') and @role = 'article' and not(contains(text(),'has been deleted'))]]")
            if len(children_list) == 0:
                children_list = comment_list[1].find_elements(By.XPATH,"./div[./div[contains(@aria-label,' by ') and @role = 'article' and not(contains(text(),'has been deleted'))]]")
            # print(parent_comment_info['Name'])
            # print(parent_comment_info['ID'])
            for child in children_list:
                # print(parent_comment_info["Name"])
                # print('Printing child information')
                # print(child.get_attribute('innerHTML'))
                child_comment = self.build_comment_tree_section(driver, child, parent_comment_info['ID'])
                if child_comment:
                    children.append(child_comment)
        except (IndexError,CommentValueError) as e:
            pass
    
        
        try:
            logging.info(f'Handling removed comment')
            removed_comment = comment_list[1].find_elements(By.XPATH,"./div/div[./div/div[contains(text(),'has been deleted')]]")
            counter = 1
            for removed_comment_sections in removed_comment:
                logging.info('=======================')
                logging.info(removed_comment_sections.get_attribute('innerHTML'))
                logging.info('______________________')
                removed_comment_ID = parent_comment_info['ID'] + '_child_removed'
                node_id = removed_comment_ID
                while node_id in self._used_ids:
                    node_id = f"{removed_comment_ID}_{counter}"
                    counter += 1
                self._used_ids.add(node_id)
                children_list = removed_comment_sections.find_elements(By.XPATH,"./div[./*]")
                # print(len(children_list))                

                for child in children_list[1:]:
                    # print(child.get_attribute('innerHTML'))
                    # print('____________')
                    child_comment = self.build_comment_tree_section(driver, child, node_id)
                    if child_comment:
                        children.append(child_comment)
                removed_node = Comment(
                ID = removed_comment_ID,
                user_name = 'Removed',
                user_group_link = 'Removed',
                content = 'Removed',
                media = 'Removed',
                children = children,
                ParentID = parent_comment_info['ParentID'],
                )
                self._comment_registry[parent_comment_info['ID']] = removed_node
                # return removed_node
        except IndexError:
            pass
        # if len(removed_comment) == 0:
        
        parent_comment_node = Comment(
            ID = parent_comment_info['ID'],
            user_name = parent_comment_info['Name'],
            user_group_link = parent_comment_info['Group URL'],
            content = parent_comment_info['Content'],
            media = parent_comment_info['Media'],
            children = children,
            ParentID = parent_comment_info['ParentID'],
        )

        #Add to registry
        self._comment_registry[parent_comment_info['ID']] = parent_comment_node
        return parent_comment_node







# def single_comment_extractor(comment):
    
# def replied_comment_extractor(comment):
    
#     if len(comment_list) == 1:
#         raise CommentValueError("The comment must not be single!")
#     list_comment = []
#     parent_content = single_comment_extractor(parent_comment)
#     parent_content['ID'] = 1
#     parent_content['ParentID']
#     for comment_section in comment_list:
#         if is_comment_single(comment_section):
#             single_comment_extractor(comment)
#         else:
#             replied_comment_extractor(comment_section)
            
# def comment_extractor(comment):
#     if is_comment_single(comment):
#         single_comment_extractor(comment)
#     else:
        


# def comment_extractor(comment):
#     #Given any div comments extracted in a Facebook page, this function will return name of poster, link to poster account (in the group atm)
#     # but will be updated to profile later, and content of the poster.
#     list_comments = comment.find_elements(By.XPATH,"./div[./*]")
#     if len(list_comments) == 1:
#         print('This is a single comment.')
#         comment_user = comment.find_element(By.XPATH,".//div[contains(@aria-label,'Comment by')]//span/a[./span]")
#         comment_user_link = "".join(["https://facebook.com",comment_user.get_attribute('href')])
#         comment_user_name = comment_user.find_element(By.XPATH,"./span/span").get_attribute('innerHTML')
#         print(comment_user_link)
#         print(comment_user_name)
#         comment_content = comment.find_element(By.XPATH,".//div[@style = 'text-align: start;']").get_attribute('innerHTML')
#         print(comment_content)
#         # try:
#         #     top_contributor = comment_user.find_element(By.XPATH,'.//span[contains(text(),"Top contributor")]').get_attribute('innerHTML')
#         # except NoSuchElementException:
#         #     top_contributor = None
#         # print(top_contributor)
#         return {'Name':comment_user_name,'Group URL': comment_user_link,'Content':comment_content}
#     else:
#         print('This comment has replies.')
        