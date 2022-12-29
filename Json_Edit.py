import datetime
import json
import os


filename = datetime.date.today().strftime('%Y%m%d')+"HOLOGIC_PID_20210218-01_31 KOLs_InstagramProfiles_07Dec2021_V1"
path = os.getcwd()+'/'+datetime.date.today().strftime('%Y%m%d')+"HOLOGIC_PID_20210218-01_31 KOLs_InstagramProfiles_07Dec2021_V1/"
mkdir = os.mkdir(filename)
count = 0

with open('20211207_Abbott_Kols_Instagram.json') as df:
    for line in df:
        data = json.loads(line)
        name = data[u'GraphProfileInfo']['username']
        print(name)
        with open(path+name+'.json', 'w') as df:
            df.write(json.dumps(data,indent=4))

