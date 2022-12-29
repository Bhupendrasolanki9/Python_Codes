import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pickle
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import datetime
import re
import json
from bs4 import BeautifulSoup

def Instagram_page(driver):
    driver.get("https://www.instagram.com/accounts/login/")
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
    # driver.find_element_by_xpath('//*[@class="aOOlW   HoLwm "]     ').click()
    driver.maximize_window()

def graphImages(driver,complete_data,edge_media,info,name,tags):
    data = driver.page_source    # a `bytes` object
    soup = BeautifulSoup(data)
    data = []
    count =0
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
# for i in range(len(shared_data)):
    json_data =json.loads(shared_data)
    for i in json_data['entry_data']['ProfilePage']:
        # print(i['graphql']['user']['edge_owner_to_timeline_media']['edges'])
        graph_images =i['graphql']['user']['edge_owner_to_timeline_media']['edges']
    for graph_image,i,j,k in zip(graph_images,edge_media,info,tags):
        type_Name = graph_image['node']['__typename']
        comment_Disabled = graph_image['node']['comments_disabled']
        dimention_height = graph_image['node']['dimensions']['height']
        dimention_width = graph_image['node']['dimensions']['width']
        display_urls = graph_image['node']['display_url']
        edge_media_preview_like_count = graph_image['node']['edge_media_preview_like']['count']
        edge_media_to_comment_count = graph_image['node']['edge_media_to_comment']['count']
        
        getting_info = graph_image['node']['gating_info']
        getting_info = getting_info
        id = graph_image['node']['id']
        is_video = graph_image['node']['is_video']
        media_preview = graph_image['node']['media_preview']
        owner = graph_image['node']['owner']['id']
        shortcode = graph_image['node']['shortcode']
        taken_at_timestamp = graph_image['node']['taken_at_timestamp']
        
        thumbnail_src = graph_image['node']['thumbnail_src']
        urls = []
        # username = graph_image['node']['username']
        complete_data= {
            "__typename":type_Name,
            "comments_disabled":comment_Disabled,
            "dimensions":{
                "height":dimention_height,
                "width":dimention_width
                },
            "display_url":display_urls,
            "edge_media_preview_like":{
                "count":edge_media_preview_like_count
                },
            "edge_media_to_caption":{
                "edges":[{
                    "node":{
                        "text":i,
                        }}]},
            "edge_media_to_comment":{
                "count":edge_media_to_comment_count},
            "gating_info":getting_info,
            "id":id,
            "is_video":is_video,
            "media_preview":media_preview,
            "owner":{
            "id":owner
            },
            "shortcode":shortcode,
            "tags":k,
            "taken_at_timestamp":taken_at_timestamp,
            "thumbnail_resources":
                j
                ,
            "thumbnail_src":thumbnail_src,
            "urls":urls,
            "username":name
            }
        data.append(complete_data)
    return data


def edgeMediaPreview(driver,complete_data):
    data = driver.page_source    # a `bytes` object
    soup = BeautifulSoup(data)
    info = []
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    json_data =json.loads(shared_data)
    print(json_data)
    for i in json_data['entry_data']['ProfilePage']:
        graph_images =i['graphql']['user']['edge_owner_to_timeline_media']['edges']
    for graph_image in graph_images:
        edge_media_preview_to_captions = graph_image['node']['edge_media_to_caption']['edges']
        for edge_media_preview_to_caption in edge_media_preview_to_captions:
            edge_media_preview_to_caption = edge_media_preview_to_caption['node']['text']
            info.append(edge_media_preview_to_caption)
    
    return info

def hashtags(driver,complete_data):
    data = driver.page_source    # a `bytes` object
    soup = BeautifulSoup(data)
    info = []
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    json_data =json.loads(shared_data)
    for i in json_data['entry_data']['ProfilePage']:
        # print(i['graphql']['user']['edge_owner_to_timeline_media']['edges'])
        graph_images =i['graphql']['user']['edge_owner_to_timeline_media']['edges']
    for graph_image in graph_images:
        edge_media_preview_to_captions = graph_image['node']['edge_media_to_caption']['edges']
        for edge_media_preview_to_caption in edge_media_preview_to_captions:
            edge_media_preview_to_caption = edge_media_preview_to_caption['node']['text']
            hashtags = re.findall(r"#(\w+)", edge_media_preview_to_caption)

            info.append(hashtags)
    
    return info


def thumbnailResourcesConfigHeight(driver,complete_data):
    data = driver.page_source    # a `bytes` object
    soup = BeautifulSoup(data)
    thumb_resource =[]
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    json_data =json.loads(shared_data)
    for i in json_data['entry_data']['ProfilePage']:
        # print(i['graphql']['user']['edge_owner_to_timeline_media']['edges'])
        graph_images =i['graphql']['user']['edge_owner_to_timeline_media']['edges']
        for graph_image in graph_images:
            thumbnail_resources_configs = graph_image['node']['thumbnail_resources']
            for thumbnail_resources_config in thumbnail_resources_configs:
        # print(thumbnail_resources_config)
                thumbnail_resources_config_height = thumbnail_resources_config['config_height']
                thumbnail_resources_config_width = thumbnail_resources_config['config_width']
                thumbnail_resources_config_src = thumbnail_resources_config['src']
                complete_data = {
                    "config_height":thumbnail_resources_config_height,
                    "config_width":thumbnail_resources_config_width,
                    "src":thumbnail_resources_config_src}
                thumb_resource.append(complete_data)

    return thumb_resource

def GraphProfileInfo(driver,complete_data):
    data = driver.page_source    # a `bytes` object
    soup = BeautifulSoup(data)
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    json_data =json.loads(shared_data)
    for i in json_data['entry_data']['ProfilePage']:
        # print(i['graphql']['user']['edge_owner_to_timeline_media']['edges'])
        biography =i['graphql']['user']['biography']
        followers_count = i['graphql']['user']['edge_followed_by']['count']
        following_count = i['graphql']['user']['edge_follow']['count']
        full_name = i['graphql']['user']['full_name']
        is_business_account = i['graphql']['user']['is_business_account']
        is_joined_recently = i['graphql']['user']['is_joined_recently']
        is_private = i['graphql']['user']['is_private']
        profile_pic_url = i['graphql']['user']['profile_pic_url']
        username = i['graphql']['user']['username']
        
        try:
            num_posts = driver.find_element_by_xpath('//body/div/section/main/div/header/section/ul/li[1]/span/span').text
            complete_data= {
                "info":{
                    "biography": biography,
                    "followers_count": followers_count,
                    "following_count": following_count,
                    "full_name": full_name,
                    "is_business_account": is_business_account,
                    "is_joined_recently": is_joined_recently,
                    "is_private": is_private,
                    "posts_count":int(num_posts),
                    "profile_pic_url":profile_pic_url},
                    "username":username
                    }
            return complete_data
        except:
            complete_data= {
                "info":{
                    "biography": biography,
                    "followers_count": followers_count,
                    "following_count": following_count,
                    "full_name": full_name,
                    "is_business_account": is_business_account,
                    "is_joined_recently": is_joined_recently,
                    "is_private": is_private,
                    "posts_count":0,
                    "profile_pic_url":profile_pic_url},
                    "username":username
                    }
            return complete_data

def username(driver,complete_data):
    data = driver.page_source    # a `bytes` object
    soup = BeautifulSoup(data)
    script_tag = soup.find('script', text=re.compile('window\._sharedData'))
    shared_data = script_tag.string.partition('=')[-1].strip(' ;')
    json_data =json.loads(shared_data)
    for i in json_data['entry_data']['ProfilePage']:
        username =i['graphql']['user']['username']
            
        return username


def dataExtraction(Instagram_url,filename,driver,complete_data):
    driver.get(Instagram_url)
    edge_media = edgeMediaPreview(driver,complete_data)
    info = thumbnailResourcesConfigHeight(driver,complete_data)
    tags = hashtags(driver,complete_data)
    name =username(driver,complete_data)
    data = {
        "GraphImages":graphImages(driver,complete_data,edge_media,info,name,tags),
        "GraphProfileInfo":GraphProfileInfo(driver,complete_data)
    }


    with open(filename, 'r+') as df:
        if len(df.read()) == 0:
            df.write(json.dumps(data))
        else:
            df.write('\n' + json.dumps(data))

if __name__ == '__main__':
    driver_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/chromedriver.exe"
    brave_path = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"

    option = webdriver.ChromeOptions()
    option.binary_location = brave_path
    # option.add_argument("--incognito") #OPTIONAL
    option.add_argument("--headless") # OPTIONAL
    driver = webdriver.Chrome(executable_path=driver_path, chrome_options=option)

    filename = datetime.date.today().strftime('%Y%m%d')+"_Abbott_Kols_Instagram.json"

    complete_data ={}
    with open (filename,'w+') as data:
        print(filename+"Created")

    df = pd.read_csv("Instagram urls.csv")
    Instagram_urls = df["URLs"]
    Instagram_page(driver)
    for Instagram_url in Instagram_urls:
        dataExtraction(Instagram_url,filename,driver,complete_data)




#main_funct()
