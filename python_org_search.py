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
from util import scroll_until_end, post_expand, saveCookies, loadCookies
from selenium.webdriver.firefox.options import Options
import pickle
from io import StringIO
import lxml.etree
from selenium.webdriver.common.action_chains import ActionChains



firefoxOptions = FirefoxOptions(); 
firefoxOptions.set_preference("dom.webnotifications.enabled",False); 
driver = webdriver.Firefox(firefoxOptions)
# driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

sleep(3)
decline_cookie = driver.find_element(By.CSS_SELECTOR,'div.x1i10hfl:nth-child(2)')
decline_cookie.click()

sleep(4)

print('Login successfully.')


# sleep(
loadCookies(driver)

print('cookies loaded.')

sleep(3)

# hashtag timny year 2023
# link = "https://www.facebook.com/groups/1615892121936594/search?q=%23timny&filters=eyJycF9jcmVhdGlvbl90aW1lOjAiOiJ7XCJuYW1lXCI6XCJjcmVhdGlvbl90aW1lXCIsXCJhcmdzXCI6XCJ7XFxcInN0YXJ0X3llYXJcXFwiOlxcXCIyMDIzXFxcIixcXFwic3RhcnRfbW9udGhcXFwiOlxcXCIyMDIzLTFcXFwiLFxcXCJlbmRfeWVhclxcXCI6XFxcIjIwMjNcXFwiLFxcXCJlbmRfbW9udGhcXFwiOlxcXCIyMDIzLTEyXFxcIixcXFwic3RhcnRfZGF5XFxcIjpcXFwiMjAyMy0xLTFcXFwiLFxcXCJlbmRfZGF5XFxcIjpcXFwiMjAyMy0xMi0zMVxcXCJ9XCJ9In0%3D"

# hashtag timny year 2024
# link = "https://www.facebook.com/groups/1615892121936594/search?q=%23timny&filters=eyJycF9jcmVhdGlvbl90aW1lOjAiOiJ7XCJuYW1lXCI6XCJjcmVhdGlvbl90aW1lXCIsXCJhcmdzXCI6XCJ7XFxcInN0YXJ0X3llYXJcXFwiOlxcXCIyMDI0XFxcIixcXFwic3RhcnRfbW9udGhcXFwiOlxcXCIyMDI0LTFcXFwiLFxcXCJlbmRfeWVhclxcXCI6XFxcIjIwMjRcXFwiLFxcXCJlbmRfbW9udGhcXFwiOlxcXCIyMDI0LTEyXFxcIixcXFwic3RhcnRfZGF5XFxcIjpcXFwiMjAyNC0xLTFcXFwiLFxcXCJlbmRfZGF5XFxcIjpcXFwiMjAyNC0xMi0zMVxcXCJ9XCJ9In0%3D"

#hashtag timngiu

# link = "https://www.facebook.com/groups/1615892121936594/search/?q=%23timngiu"
# driver.get(link)

#hashtag timnguoiyeu

link = "https://www.facebook.com/groups/1615892121936594/search/?q=%23timnguoiyeu"
driver.get(link)

# sleep(10)
# js_code = "return document.getElementsByTagName('html').innerHTML"
# your_elements = driver.execute_script(js_code)
# # parser = lxml.etree.HTMLParser()
# # tree = lxml.etree.parse(StringIO(your_elements), parser)

# print('Scripts executed')
# sleep(10)

# # open result.html 
# file_ = open('result.html', 'wb') 
  
# # Write the entire page content in result.html 
# file_.write(tree) 
  
# # Closing the file 
# file_.close() 
# print('File saved.')

# elem = driver.find_element(By.XPATH,"//*[contains(@href,'https://facebook.com/groups/bumblevietnam/posts')]")
# elems = driver.find_elements(By.XPATH,"//a")
# for elem in elems:
#     print(elem.get_attribute('href'))
#     sleep(3)
# print('Did we find the link?')
# sleep(3)







# element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[starts-with(@aria-label, "Like:")]')))
# element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"comments")]')))

# element.click()

scroll_until_end(driver)
print("scroll done")
sleep(4)

a = ActionChains(driver)
print('Actions initiated.')

elems = driver.find_elements(By.XPATH,"//a")
i = 0
for elem in elems:
    if 'group' in elem.get_attribute('href'):
        i += 1
        print(f'The {i} link')

keywordToCheck = ['photo','hashtag','tab']

for elem in elems:
    print(elem.get_attribute('href'))
    if any(ext in elem.get_attribute('href') for ext in keywordToCheck):
        print('This link does not neet hovering.')
        continue
    try:
        a.move_to_element(elem).perform()
        sleep(5)
        a.move_by_offset(100,0)
        sleep(10)
        print('Hover first time succeeded.')
    except MoveTargetOutOfBoundsException:
        try:
            driver.execute_script("arguments[0].scrollIntoView(true);window.scrollBy(0,-100);", elem)
            sleep(5)
            a.move_to_element(elem).perform()
            sleep(5)
            a.move_by_offset(100,0)
            sleep(10)
            print('Hover second time succeeded.')
        except MoveTargetOutOfBoundsException:
            # element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, f"//a[@class = '{elem.get_attribute('class')}']")))
            # sleep(5)
            # a.move_to_element(element).perform()
            # sleep(5)
            # print('Hover third time succeeded.')
            # elems1 = driver.find_elements(By.XPATH,"//a")
            # for elem1 in elems1:
            #     print(elem1.get_attribute('href'))
            print('Link is duplicated')
            sleep(5)


# sleep(5)
# SCROLL_PAUSE_TIME = 5

# link_list_hovered = []
# print('Start scrolling.')
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
# print(last_height)
# while True:
#     # Scroll down to bottom
#     elems = driver.find_elements(By.XPATH,"//a")
#     for elem in elems:
#         print(elem.get_attribute('href'))
#         if elem.get_attribute('href') in link_list_hovered:
#             print('Link hovered.')
#             continue
#         else:
#             print(elem.get_attribute('href'))
#             link_list_hovered.append(elem.get_attribute('href'))
#             try:
#                 a.move_to_element(elem).perform()
#             except MoveTargetOutOfBoundsException:
#                 driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
#                 a.move_to_element(elem).perform()
#         sleep(3)

#     sleep(5)
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")

#     # Wait to load page
#     sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height





print('Did we find the link?')
sleep(3)

elems = driver.find_elements(By.XPATH,"//a[contains(@href,'facebook.com/groups/bumblevietnam/posts')]")

sleep(10)

list_link = []
for elem in elems:
    list_link.append(elem.get_attribute("href"))
    print(elem.get_attribute('href'))

with open('link_list.pkl', 'wb') as f:
    pickle.dump(list_link, f)

print(len(list_link))
print(list_link[0])
print(list_link[1])

# for i in list_link:
#     driver.get(i)

# post_expand(driver)



# # print('Out of see more button.')
# page = driver.page_source.encode('utf-8') 
# # print(page) 
  
# # open result.html 
# file_ = open('result.html', 'wb') 
  
# # Write the entire page content in result.html 
# file_.write(page) 
  
# # Closing the file 
# file_.close() 

# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()
driver.close()
