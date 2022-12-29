import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
import os
# from apscheduler.schedulers.background import BackgroundScheduler
def Instagram_page(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    # driver.find_element_by_xpath('//*[@class="aOOlW   HoLwm "]     ').click()
    driver.maximize_window()



def name(driver,complete_data):
    try:
        item = []
        time.sleep(2)
        name = driver.find_element_by_xpath("//body/div/section/main/div/header/section/div[2]/h1").text
        # item.append(name)
        # complete_data={"Name":' '.join(map(str, item))}
        name = str(name)
        return name
    except:
        print("Name Not Found")


def posts(driver,complete_data):
    try:
        item = []
        time.sleep(2)
        num_posts = driver.find_element_by_xpath('//body/div/section/main/div/header/section/ul/li[1]/a/span').text
        # item.append(num_connections)
        # complete_data={"Connection Numbers":' '.join(map(str, item))}
        posts = str(num_posts)
        return posts
    except:
        num_posts = driver.find_element_by_xpath('//body/div/section/main/div/header/section/ul/li[1]/span/span').text
        posts = str(num_posts)
        return posts
        print("Number of Connections Not Found")


def about(driver,complete_data):
    try:
        item = []
        time.sleep(2)
        about = driver.find_element_by_xpath('//body/div/section/main/div/header/section/div[2]/span').text
        about = about.encode("ascii", "ignore")
        about = about.decode()
        # item.append(about)
        # complete_data={"About":' '.join(map(str, item))}
        about = str(about)
        return about
    except:
        print("About Not Found")

def followers(driver,complete_data):
    try:
        item = []
        time.sleep(2)
        wait = WebDriverWait(driver, 30)
        num_followers = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div/section/main/div/header/section/ul/li[2]/span/span"))).text
        num_followers = str(num_followers)
        return num_followers
    except:
        wait = WebDriverWait(driver, 30)
        num_followers = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div/section/main/div/header/section/ul/li[2]/a/span"))).text
        num_followers = str(num_followers)        
        return num_followers


def followings(driver,complete_data):
    try:
        item = []
        time.sleep(2)
        wait = WebDriverWait(driver, 30)
        num_followings = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div/section/main/div/header/section/ul/li[3]/span/span"))).text
        # item.append(num_followers)
        # complete_data={"Followers":' '.join(map(str, item))}
        num_followings = str(num_followings)
        return num_followings
    except:

        wait = WebDriverWait(driver, 30)
        num_followers = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div/section/main/div/header/section/ul/li[3]/a/span"))).text
        num_followers = str(num_followers)        
        return num_followers

def imageUrls(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        image_urls = driver.find_elements_by_xpath('//body/div/section/main/div/div[2]/article/div/div/div/div/a/div/div/img')
        for image_url in image_urls:
            image_url = image_url.get_attribute("src")
            item.append(image_url)
        complete_data={"Urls":', '.join(map(str, item))}
        return complete_data
    except:
        print("Image Urls Not Found")


def data_extraction(driver,linkedin_url,complete_data,filename):
    driver.get(linkedin_url)


    profileAlternative = {
        "Name":name(driver,complete_data),
        "About":about(driver,complete_data),
        "Number of Posts":posts(driver,complete_data),
        "Followers":followers(driver,complete_data),
        "Followings":followings(driver,complete_data)
    }
    

    image_urls=[
        imageUrls(driver,complete_data)
    ]
    data={
        "profileAlternative":profileAlternative,
        "Image URls":image_urls

    }
    
    with open(filename, 'r+') as df:
        if len(df.read()) == 0:
            df.write(json.dumps(data))
        else:
            df.write('\n' + json.dumps(data))

        
# if __name__ == '__main__':
def main_funct():
    driver_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/chromedriver.exe"
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    # option.add_argument("--incognito") #OPTIONAL
    # option.add_argument("--headless") # OPTIONAL
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

    filename = datetime.date.today().strftime('%Y%m%d')+"_Danone_50-Dietcian_Instagram.json"

    complete_data ={}
    with open (filename,'w+') as data:
        print(filename+"Created")

    df = pd.read_csv("Instagram urls.csv")
    Instagram_urls = df["URLs"]
    Instagram_page(driver)
    for Instagram_url in Instagram_urls:
        data_extraction(driver,Instagram_url,complete_data,filename)


if __name__ == '__main__':
#     # now = datetime.now().time()
#     t = time.localtime()
#     current_time = time.strftime("%H", t)
#     current_day_hours = 24  - int(current_time) 
#     schedule_day_hours = int(current_time) + current_day_hours 

#     today = datetime.date.today().strftime('%d')
#     schedule_date = 30 - int(today) 
#     one_day = schedule_day_hours * schedule_date
#     # print(schedule_date)
#     scheduler = BackgroundScheduler()

#     if current_time == '24':

#         scheduler.add_job(main_funct, 'interval',hours = one_day, minutes = 900)
#         scheduler.start()
        main_funct()
#         try:
#             # This is here to simulate application activity (which keeps the main thread alive).
#             while True:
#                 time.sleep(2)
#         except (KeyboardInterrupt, SystemExit):
#             # Not strictly necessary if daemonic mode is enabled but should be done if possible
#             scheduler.shutdown()
#     else:
#         pass