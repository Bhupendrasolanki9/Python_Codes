import tweepy 
from tweepy import OAuthHandler
from tweepy import API
import pandas as pd
from python_sql_connection import connection
import mysql.connector
import json
import re


def twitterScrapper(name):
    API_Key='UpGPUvvYbKaxuh07Iv1o2u7si'
    API_Secret_Key='KR9Vg3Jig5sBvFcsTDL7j3m19yfC8vWIOzLVyPAFKGvRKjbUOX'
    Access_Token='1370338600609488902-4O2HZDNbTEe8cR70TjF7nAeZmLkb5Q'
    Access_Token_Secret='i05hJ7V8RyuJeFskYpEmirx9cCNok1T1vcYbBDq2vls7N' 
    auth = OAuthHandler(API_Key, API_Secret_Key)
    auth.set_access_token(Access_Token, Access_Token_Secret)
    api = API(auth)
    api

    # Main code
    # name = "dalbrightmd OR aujeromd OR karendrkbarbosa OR beitsch OR pwbmdpeter OR patriciaclarkmd OR  kirandevisetty OR dr_lars_grimm OR drjayharness OR drholmesla OR minciardi OR bonniejoemd OR dr_sadiakhan OR MdCamelia OR anthonylucci1 OR drlizmorris OR amykpatel OR MayoClinicCIM OR annepeledmd"
    
    since_date = input('Start date :- ' )
    until_date = input('End Date :- ' )
    # since_date = '2021-07-23'
    # until_date = '2021-07-23'
    for tweet in tweepy.Cursor(api.search,q='to:'+name,lang="en").items(1000): #item iterators
        my_itr = [tweet.text,tweet.user.screen_name]
        
    # data frame created
        T_df = pd.DataFrame(data = my_itr)
        pd.set_option('max_colwidth',800)
        T_df.to_csv('twitter_data.csv',index = True,header=False,mode='a')

    return since_date,until_date

def userFinder(name):
    # names = ['dalbrightmd' , 'aujeromd' , 'karendrkbarbosa' , 'beitsch' , 'pwbmdpeter' , 'patriciaclarkmd' ,'kirandevisetty' , 'dr_lars_grimm' , 'drjayharness' , 'drholmesla' , 'minciardi' , 'bonniejoemd' ,'dr_sadiakhan' , 'MdCamelia' , 'anthonylucci1',  'drlizmorris','amykpatel', 'MayoClinicCIM', 'annepeledmd']
    filters = name.replace(' OR ',',')
    li = list(filters.split(" "))
    count_list = []
    name_list = []
    with open('twitter_data.csv', 'r+',encoding='utf-8') as f:
        lines = f.readlines()
        for i in li:
            count_list.append(len('@'+i))
            name_list.append('@'+i)
        
    return count_list,name_list


def dataStore(data,info,date):
    sum_count = sum(data[0])
    for i,j in zip(data[0],data[1]):
        sov = i/sum_count*100
        final_data = {
            "KOl ID":info[0],
            "CRM ID":info[1],
            "Name of Kol":j,
            "Count of Kol":i,
            "SOV of KOL":sov,
            "Since_date":date[0],
            "Until_date":date[1],
            "CreatedBy":info[3]
        }
        df = pd.DataFrame([final_data])
        df.to_csv('SOV_Data.csv',index=False,header=False,mode='a')
    
def connection ():
    con = mysql.connector.connect(
    host="testinstancedb.cjngfiuidw88.ap-south-1.rds.amazonaws.com", user="testmaster",
    password="Aq-?t?,z)SBD", database="version1")
    # create cursor object
    cursor = con.cursor()
    created_by = input('Input the Created_by Id for selecting the company :- ')
    query1 = "select id,crmid ,twitterusername FROM  tbldoctorspersonalinfo WHERE createdby ="+ created_by +" AND twitterusername IS NOT NULL AND twitterusername <> '' "

    cursor.execute(query1)

    table = cursor.fetchall()

    usernames = []
    user_ids =[]
    crm_ids = []
    for tup in table:
        tup = '{}: {}: {}'.format(*tup)
        user_id = tup.split(':')[0]
        crm_id = tup.split(':')[1]
        username = tup.split(':')[2]
        usernames.append(username)
        crm_ids.append(crm_id)
        user_ids.append(user_id)
    # print(usernames,crm_ids,user_ids)
    return user_ids,crm_ids,usernames,created_by

if __name__ == '__main__':

    # name = "dalbrightmd OR aujeromd OR karendrkbarbosa OR beitsch OR pwbmdpeter OR patriciaclarkmd OR  kirandevisetty OR dr_lars_grimm OR drjayharness OR drholmesla OR minciardi OR bonniejoemd OR dr_sadiakhan OR MdCamelia OR anthonylucci1 OR drlizmorris OR amykpatel OR MayoClinicCIM OR annepeledmd"
    info = connection()
    username=''.join(info[2])
    
    #regular expression for find numbers in string
    pattern = r'[0-9]'
    # Match all digits in the string and replace them by empty string
    mod_string = re.sub(pattern, '', username)

    df = pd.DataFrame(columns=['text'])
    df.to_csv('twitter_data.csv',index = True,header=True)

    df1 = pd.DataFrame(columns=['Kol_ID','CRM_ID','Name_of_Kol','Count_of_Kol','SOV_of_KOL','Start_Date','End_Date','CreatedBy'])
    df1.to_csv('SOV_Data.csv',index=False,header=True)
    
    username = mod_string.replace('/status/','')
    name = username.replace(' ', ' OR ')

    date =twitterScrapper(name)
    data = userFinder(name)
    dataStore(data,info,date)
        

