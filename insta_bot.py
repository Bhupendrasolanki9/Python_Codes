from instabot import Bot
import json
import pandas as pd
bot = Bot()
bot.login(username="bhupendra_singh_solanki9", password="9929188471vk")

######  upload a picture #######
# bot.upload_photo("yoda.jpg", caption="biscuit eating baby")

######  follow someone #######
# bot.follow("elonrmuskk")

######  send a message #######
# bot.send_message("Hello from Dhaval", ['user1','user2'])

######  get follower info #######
my_followers = bot.get_user_followers("bhupendra_singh_solanki9")

with open('Insta Info.json','w+'):
    for follower in my_followers:
        data = bot.get_user_info(follower)
        with open ('Insta Info.json','r+') as df:
            if len(df.read()) == 0:
                df.write(json.dumps(data))
            else:
                df.write('\n' + json.dumps(data))

bot.unfollow_everyone()