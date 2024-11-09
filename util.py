from time import sleep
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import pickle
import os
from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
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
        sleep(10)
        parent_element = driver.find_element(By.XPATH,"//div[./div/div/span/div/div/div[text() = 'See more']]")
        sleep(3)
        element = WebDriverWait(parent_element, 40).until(EC.element_to_be_clickable((By.XPATH, ".//div[text()='See more']")))
        try:
            element.click()
        except ElementClickInterceptedException:
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", parent_element)
            sleep(5)
            ActionChains(driver).move_to_element(element).click().perform() 
        print(f"Click see more {i}th time.")
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
    
    driver.refresh() # Refresh Browser after login


## Handling comments
## From this point onwards, a comment section is defined as the result of 
## the following XPATH: //div[./div/div[contains(@aria-label,'Comment by')  and @role = 'article']]

def comments_expand(driver):
    #This function expand all comments visible on a Facebook webpage 
    i = 1
    while True:
        sleep(4)

        try: 
            driver.find_element(By.XPATH,"//div[./span/span[contains(text(),'repl')]]")
        except NoSuchElementException:
            break
        sleep(10)
        WebDriverWait(driver, 40).until(EC.element_to_be_clickable((By.XPATH, "//div[./span/span[contains(text(),'repl')]]"))).click()
        print(f"Click view more replies {i}th time.")
        i += 1 
    print('Out of view more replies button.')



def is_comment_single(comment):
    list_comments = comment.find_elements(By.XPATH,"./div[./*]")
    if len(list_comments) == 1:
        return True
    else:
        return False
    
class CommentValueError(Exception):
    pass


def single_comment_extractor(comment):
    comment_content = comment.find_elements(By.XPATH,"./div[./*]")
    if len(comment_content) != 1:
        raise CommentValueError("The comment must be single!")
    comment_user = comment.find_element(By.XPATH,".//div[contains(@aria-label,'Comment by')]//span/a[./span]")
    comment_user_link = "".join(["https://facebook.com",comment_user.get_attribute('href')])
    comment_user_name = comment_user.find_element(By.XPATH,"./span/span").get_attribute('innerHTML')
    comment_content = comment.find_element(By.XPATH,".//div[@style = 'text-align: start;']").get_attribute('innerHTML')
    return {'Name':comment_user_name,'Group URL': comment_user_link,'Content':comment_content}

def replied_comment_extractor(comment):
    comment_list = comment.find_elements(By.XPATH,"./div[./*]")
    if len(comment_list) == 1:
        raise CommentValueError("The comment must not be single!")
    for comment_section in comment_list:
        if is_comment_single(comment_section):
            return True

def comment_extractor(comment):
    #Given any div comments extracted in a Facebook page, this function will return name of poster, link to poster account (in the group atm)
    # but will be updated to profile later, and content of the poster.
    list_comments = comment.find_elements(By.XPATH,"./div[./*]")
    if len(list_comments) == 1:
        print('This is a single comment.')
        comment_user = comment.find_element(By.XPATH,".//div[contains(@aria-label,'Comment by')]//span/a[./span]")
        comment_user_link = "".join(["https://facebook.com",comment_user.get_attribute('href')])
        comment_user_name = comment_user.find_element(By.XPATH,"./span/span").get_attribute('innerHTML')
        print(comment_user_link)
        print(comment_user_name)
        comment_content = comment.find_element(By.XPATH,".//div[@style = 'text-align: start;']").get_attribute('innerHTML')
        print(comment_content)
        # try:
        #     top_contributor = comment_user.find_element(By.XPATH,'.//span[contains(text(),"Top contributor")]').get_attribute('innerHTML')
        # except NoSuchElementException:
        #     top_contributor = None
        # print(top_contributor)
        return {'Name':comment_user_name,'Group URL': comment_user_link,'Content':comment_content}
    else:
        print('This comment has replies.')
        