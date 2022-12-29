import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import re
import requests
import os
import datetime
# from apscheduler.schedulers.background import BackgroundScheduler

def facebook_page(driver):
    driver.get("https://www.facebook.com/login")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    driver.maximize_window()


def nameFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        wait = WebDriverWait(driver, 30)
        name = wait.until(EC.presence_of_element_located((By.XPATH,"//body/div/div/div/div/div[3]/div/div/div/div/div/div[2]/div/div/div/div[2]/div/div/div/h2/span/span")))
        item.append(name.text)
        complete_data={"Name":' '.join(map(str, item))}
        return complete_data  
    except:
        
        complete_data={"Name":' '.join(map(str, "NaN"))}
        return complete_data

def titleFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item =[]
        title = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div/div/div/div/div[2]/div/div/span/div/div/span/div/div').text
        item.append(title)
        complete_data={"Title":' '.join(map(str, item))}
        return complete_data  
    except:
        
        complete_data={"Title":' '.join(map(str, "NaN"))}
        return complete_data

def aboutFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        about = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div[2]/div/div/div/div/div[2]/div/div/span/div/div/span/div/div').text
        item.append(about)
        complete_data={"About":' '.join(map(str, item))}
        return complete_data  
    except:
        
        complete_data={"About":' '.join(map(str, "NaN"))}
        return complete_data

def followersFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        wait = WebDriverWait(driver, 30)
        num_followers = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div[5]/div/div/div/div[2]/div/div/span/span"))).text
        item.append(num_followers)
        complete_data={"Followers":' '.join(map(str, item))}
        return complete_data  
    except:
        print("Number of Followers Not Found")
        complete_data["Followers"] = "NaN"
        return complete_data["Followers"]

def emailFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        html = driver.page_source
        emails = re.findall(r'[\w\.-]+@[\w\.-]+',html)
        item.append(emails)
        complete_data={"Emails":' '.join(map(str, item))}
        return complete_data 
    except:
        print("Emails Not Found")
        complete_data["Emails"] = "NaN"
        return complete_data["Emails"]

def phoneNumbersFromPage(driver,complete_data):
    try:
        item = []
        time.sleep(3)
        html = driver.page_source
        numbers = re.findall(r'[(]?(\d{3})?[)]?(\d{3})(\s|-|\.)(\d{3})(\s|-|\.)(\d{4})',html)
        item.append(numbers)
        complete_data={"Phone":' '.join(map(str, item))}
        return complete_data 
    except:
        print("Numbers Not Found")
        complete_data["Phone"] = "NaN"
        return complete_data["Phone"]

def locationsFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        loc = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div[2]/div/div/div[2]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/span/a/span/span')
        item.append(loc.text)
        complete_data={"Location":' '.join(map(str, item))}
        return complete_data 
    except:
        print("Location Dates Not Found")
        complete_data["Location"] = "NaN"
        return complete_data["Location"]

def serviceFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        Service_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/a[2]/div/span'))).click()
        time.sleep(3)
        services = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/span')
        for service in services:
            item.append(service.text)
        complete_data={"Services":' '.join(map(str, item))}
        return complete_data 
    except:
        print("Services Not Found")
        complete_data["Services"] = "NaN"
        return complete_data["Services"]


def reviewsFromPage(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        review_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/a[3]/div/span'))).click()
        time.sleep(3)
        reviews = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/span/h2/strong')
        for review in reviews:
            item.append(review.text)
        complete_data={"Reviews":' '.join(map(str, item))}
        return complete_data 
    except:
        print("reviews Not Found")
        complete_data["Reviews"] = "NaN"
        return complete_data["Reviews"]

def data_extraction_for_page(driver,facebook_url,complete_data,count,filename):
    # count +=1
    path = os.getcwd()+"/Json Data 25 Pedia-Gestro/"
    wait = WebDriverWait(driver, 30)
    aboutdata = [
    nameFromPage(driver,complete_data),
    titleFromPage(driver,complete_data),
    aboutFromPage(driver,complete_data),
    emailFromPage(driver,complete_data),
    phoneNumbersFromPage(driver,complete_data),
    locationsFromPage(driver,complete_data),
    followersFromPage(driver,complete_data)
    ]

    services= [
        serviceFromPage(driver,complete_data),
    
    ]

    review = [reviewsFromPage(driver,complete_data)]

    data={
        "aboutdata":aboutdata,
        "services":services,
        "reviews":review
    }

    if count == 0:
        with open(path+filename+str(count)+'.json', 'w') as df:
            df.write(json.dumps(data,indent=2))
    else:          
        with open(path+filename+str(count)+'.json', 'w') as df:
            df.write(json.dumps(data,indent=2))
    # with open('Facebook Data.json', 'r+') as df:
    #     if len(df.read()) == 0:
    #         df.write(json.dumps(complete_data))
    #     else:
    #         df.write(',\n' + json.dumps(complete_data))
      

def nameFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        name = driver.find_element_by_xpath("//body/div/div/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div/div/span/h1").text
        item.append(name)
        complete_data={"Name":' '.join(map(str, item))}
        return complete_data   
    except:
        print("Name Not Found")
        complete_data["Name"] = "NaN"
        return complete_data["Name"]

def titleFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        title = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/ul/div[2]/div[2]/div/div/span').text
        item.append(title)
        complete_data={"Title":' '.join(map(str, item))}
        return complete_data   
    except:
        print(" Title Not Found")
        complete_data["Title"] = "NaN"
        return complete_data["Title"]


def orgenizationFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        orgenization = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/ul/div[2]/div[2]/div/div/span/a/span/span').text
        item.append(orgenization)
        complete_data={"Orgenization":' '.join(map(str, item))}
        return complete_data   
    except:
        print(" Orgenization Not Found")
        complete_data["Orgenization"] = "NaN"
        return complete_data["Orgenization"]

def educationFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        education = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/ul/div[3]/div[2]/div/div/span').text
        item.append(education)
        complete_data={"Education":' '.join(map(str, item))}
        return complete_data
    except:
        print(" Education Not Found")
        complete_data["Education"] = "NaN"
        return complete_data["Education"]


def educationalInstituteFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item=[]
        Educational_institute = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/ul/div[3]/div[2]/div/div/span/a/span/span').text
        item.append(Educational_institute)
        complete_data={"Educational Institute":' '.join(map(str, item))}
        return complete_data
    except:
        print("Educational Institute Not Found")
        complete_data["Educational Institute"] = "NaN"
        return complete_data["Educational Institute"]


def friendsFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        num_followers = wait.until(EC.presence_of_element_located((By.XPATH, "//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[2]/div/div[3]/div/div/div/div/div/div/div/div/div[2]/span/span"))).text
        item.append(num_followers)
        complete_data={"Number of Friends":' '.join(map(str, item))}
        return complete_data
    except:
        print("Number of Friends Not Found")
        complete_data["Number of Friends"] = "NaN"
        return complete_data["Number of Friends"]

def emailFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        html = driver.page_source
        emails = re.findall(r'[\w\.-]+@[\w\.-]+',html)
        item.append(emails)
        complete_data={"Emails":' '.join(map(str, item))}
        return complete_data
    except:
        print("Emails Not Found")
        complete_data["Emails"] = "NaN"
        return complete_data["Emails"]

def phoneNumbersFromProfile(driver,complete_data):
    try:
        item = []
        time.sleep(3)
        html = driver.page_source
        numbers = re.findall(r'[(]?(\d{3})?[)]?(\d{3})(\s|-|\.)(\d{3})(\s|-|\.)(\d{4})',html)
        if numbers == True:
            item.append(numbers)
            complete_data={"Phone":' '.join(map(str, item))}
            return complete_data
        else:
            wait = WebDriverWait(driver, 30)
            number = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div[2]/div/div/div[2]/div/div/div/div/div/div/div[2]/div/div/ul/div[1]/div[2]/div/div/span/a/span/span')
            item.append(number.text)
            complete_data={"Phone":' '.join(map(str, item))}
            return complete_data
    except:
        print("Numbers Not Found")
        complete_data["Phone"] = "NaN"
        return complete_data["Phone"]

    # img_url = driver.find_element_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[1]/div[2]/div/div/div/div/div/a/div')

def reviewsFromProfile(driver,complete_data):
    try:
        time.sleep(2)
        item = []
        wait = WebDriverWait(driver, 30)
        review_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/div/div/div/div/div/div/div/div/div/div/a[3]/div/span'))).click()
        time.sleep(3)
        reviews = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div[4]/div/div/div[2]/div/div/div/div/div/div/div/div/div/div/div/div/div/div/div[2]/div/div[2]/div/div[2]/div/div/span/h2/strong')
        for review in reviews:
            item.append(review.text)
        complete_data={"Reviews":' '.join(map(str, item))}
        return complete_data
    except:
        print("reviews Not Found")
        complete_data["Reviews"] = "NaN"
        return complete_data["Reviews"]
    
    return driver.page_source
def university_group(driver,complete_data):
    try:
        elements = driver.find_element_by_link_text('Friends')
        elements.click()
        time.sleep(10)
        item = []
        wait = WebDriverWait(driver, 30)
        university_btns = wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/a[3]/div/span'))).click()
        time.sleep(3)
        name_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')
        for name_from_group in name_from_groups:
            item.append(name_from_group.text)
        complete_data={"Names":' '.join(map(str, item))}
        return complete_data        
        title_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div[2]/span/div/div')
        for title_from_group in title_from_groups:
            item.append(title_from_group.text)
        complete_data={"Titles":' , '.join(map(str, item))}
        return complete_data
    except:
        pass
# def university_group_title(driver,complete_data):
#     elements = driver.find_element_by_link_text('Friends')
#     elements.click()
#     time.sleep(10)
#     item = []
#     wait = WebDriverWait(driver, 30)
#     university_btns = wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[2]/div/div/div/div[2]/a[3]/div/span'))).click()
#     time.sleep(3)
#     title_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div[2]/span/div/div')
#     for title_from_group in title_from_groups:
#         item.append(title_from_group.text)
#     complete_data={"Titles":' , '.join(map(str, item))}
    # return complete_data
def work_group(driver,complete_data):
    try:
        wait = WebDriverWait(driver, 30)
        elements = driver.find_element_by_link_text('Friends')
        elements.click()
        item = []
        work_btn = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'Work'))).click()
        time.sleep(3)
        name_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')
        for name_from_group in name_from_groups:
            item.append(name_from_group.text)
        complete_data={"Names":' '.join(map(str, item))}
        return complete_data
        title_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div[2]/span/div/div')
        for title_from_group in title_from_groups:
            item.append(title_from_group.text)
        complete_data={"Titles":' , '.join(map(str, item))}
        return complete_data
    except:
        pass

def college_group(driver,complete_data):
    try:
        wait = WebDriverWait(driver, 30)
        elements = driver.find_element_by_link_text('Friends')
        elements.click()
        item = []
        work_btn = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'College'))).click()
        time.sleep(3)
        name_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div/a/span')
        for name_from_group in name_from_groups:
            item.append(name_from_group)
        complete_data={"Names":' '.join(map(str, item))}
        return complete_data
        title_from_groups = driver.find_elements_by_xpath('//body/div/div/div/div/div[3]/div/div/div/div/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]/div/div[2]/div[2]/span/div/div')
        for title_from_group in title_from_groups:
            item.append(title_from_group.text)
        complete_data={"Titles":' , '.join(map(str, item))}
        return complete_data
    except:
        pass
# def booksData(driver,complete_data):
#     wait = WebDriverWait(driver, 30)

#     more_btn = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'More'))).click()
#     time.sleep(2)
#     book_btn = wait.until(EC.presence_of_element_located((By.LINK_TEXT,'Book'))).click()


def data_extraction_for_profile(driver,facebook_url,complete_data,count,filename):
   
    
    path = os.getcwd()+"/Json Data 97 Gynaecology/"

    aboutdata = [
        nameFromProfile(driver,complete_data),
        titleFromProfile(driver,complete_data),
        orgenizationFromProfile(driver,complete_data),
        emailFromPage(driver,complete_data),
        phoneNumbersFromPage(driver,complete_data),
        friendsFromProfile(driver,complete_data)
    ]
   
    reviews = [
        reviewsFromProfile(driver,complete_data)
    ]

    educations= [
        educationFromProfile(driver,complete_data),
        educationalInstituteFromProfile(driver,complete_data)
    ]
    
    
    
    university=[
        
        university_group(driver,complete_data)
    ]
    work_groups=[
        work_group(driver,complete_data)
    ]
    college_groups=[
        college_group(driver,complete_data)
    ]

    data={
        "aboutdata":aboutdata,
        "university groups":university,
        "work groups":work_groups,
        "college groups":college_groups,
        "reviews":reviews,
        "educations":educations
    }
    # directory = os.mkdir(os.getcwd()+"/Json Data")
    
    if count == 0:
        with open(path+filename+str(count)+'.json', 'w') as df:
            df.write(json.dumps(data,indent=2))
    else:          
        with open(path+filename+str(count)+'.json', 'w') as df:
            df.write(json.dumps(data,indent=2))


    

def main_funct():

driver_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/chromedriver.exe"
brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

option = webdriver.ChromeOptions()
option.binary_location = brave_path
# option.add_argument("--incognito") #OPTIONAL
# option.add_argument("--headless") # OPTIONAL
driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)
    wait = WebDriverWait(driver, 30)

    complete_data ={}
    df = pd.read_csv("facebook url.csv")
    facebook_urls = df["Facebook Url"]
    facebook_page(driver)
    count = 0
    filename = datetime.date.today().strftime('%Y%m%d')+"_Danone_97-Gynaecology_Facebook"
    directory = os.mkdir(os.getcwd()+"/Json Data 97 Gynaecology")



    for facebook_url in facebook_urls:
        driver.get(facebook_url)
        count =count+1
        try:
            liked_btn = wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div[3]/div/div/div/div[2]/div/div/div/div/div/div[2]/span/span')))
            if "Like" in liked_btn.text:
                print("************************")
                print("In Page")
                data_extraction_for_page(driver,facebook_url,complete_data,count,filename)
            else:
                continue
        except:
            add_frnd_btn  =  wait.until(EC.presence_of_element_located((By.XPATH,'//body/div/div/div/div/div[3]/div/div/div/div/div/div/div/div[2]/div/div/div/div[4]/div/div/div/div/div/div/div/div[2]/span[1]/span')))
            # add_frnd_btn  =  wait.until(EC.presence_of_element_located((By.LINK_TEXT,'Add Friend')))
            
            if "Add Friend" in add_frnd_btn.text:
                print("************************")
                print("In Profile")
                data_extraction_for_profile(driver,facebook_url,complete_data,count,filename)
            else:
                continue



if __name__ == '__main__':
    # main_funct()
    # now = datetime.now().time()
    t = time.localtime()
    current_time = time.strftime("%H", t)
    current_day_hours = 24  - int(current_time) 
    schedule_day_hours = int(current_time) + current_day_hours 

    today = datetime.date.today().strftime('%d')
    schedule_date = 30 - int(today) 
    one_day = schedule_day_hours * schedule_date
    # print(schedule_date)
    scheduler = BackgroundScheduler()
    if current_time == '24':

        scheduler.add_job(main_funct, 'interval',hours = one_day,minutes = 900)
        scheduler.start()
        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))
        
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            scheduler.shutdown()
    else:
        pass


