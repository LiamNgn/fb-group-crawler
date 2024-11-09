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
from util import scroll_until_end, post_expand, saveCookies, loadCookies, facebook_login
from selenium.webdriver.firefox.options import Options
import pickle
from io import StringIO
import lxml.etree
from selenium.webdriver.common.action_chains import ActionChains

# from selenium.webdriver.firefox.webdriver import add_cookie,delete_cookie,refresh
# opts = FirefoxOptions()
# opts.add_argument("--headless")
# install_dir = "/snap/firefox/current/usr/lib/firefox"
# driver_loc = "/home/omniverse/Projects/fb-crawler/driver/geckodriver"
# binary_loc = "/usr/bin/firefox"
# service = FirefoxService(driver_loc)
# opts = FirefoxOptions()
# opts.binary_location = binary_loc
# driver = webdriver.Firefox(service=service, options=opts)

firefoxOptions = FirefoxOptions(); 
firefoxOptions.set_preference("dom.webnotifications.enabled",False); 
driver = webdriver.Firefox(firefoxOptions)
# driver = webdriver.Firefox()
driver.get("https://www.facebook.com/")

sleep(5)

decline_cookie = driver.find_element(By.CSS_SELECTOR,'div.x1i10hfl:nth-child(2)')
decline_cookie.click()

sleep(5)

facebook_login(driver)