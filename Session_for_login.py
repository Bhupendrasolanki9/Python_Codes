from selenium import webdriver
from bs4 import BeautifulSoup
import getpass
import requests
from selenium.webdriver.common.keys import Keys
import pprint
import time

userid = str(input("Enter email address or number with country code: "))
password = getpass.getpass('Enter your password:')


import pickle
driver_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
# option.add_argument("--incognito") OPTIONAL
# option.add_argument("--headless") OPTIONAL

# Create new Instance of Chrome
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)


driver.get("login_page_of_any_website")
driver.implicitly_wait(6)
driver.find_element_by_xpath("""//*[@name="username"]""").send_keys(userid)
driver.find_element_by_xpath("""//*[@name="password"]""").send_keys(password)
driver.find_element_by_xpath("""//*[@class="sqdOP  L3NKy   y3zKF     "]""").click()
pickle.dump( driver.get_cookies() , open("session.pkl","wb"))
time.sleep(5)
driver.find_element_by_xpath('//*[@class="sqdOP yWX7d    y3zKF     "]     ').click()
time.sleep(3)
driver.find_element_by_xpath('//*[@class="aOOlW   HoLwm "]     ').click()
time.sleep(2)
driver.get("https://www.instagram.com/") #Enter any of your connection profile Link

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
