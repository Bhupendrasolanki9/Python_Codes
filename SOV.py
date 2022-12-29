# # import tweepy
# # from textblob import TextBlob
# # # import pandas as pd
# # consumer_key = 'Zxm7FVOQPkNuFmXZDqqKjLsZZ'
# # consumer_secret = 'CExq5wFKuYRSyoLNIN11EEaEiPyeiOwIN8GpWITP4DiB2KUdIg'
# # access_token = '1370338600609488902-c0BZiUE8vwbasdcqSRI9kfdEA2MUUA'
# # access_token_secret ='NbiVEXgqOAYGuhTOaZQGcxYvJzGw1wtBpJkV8x2WO3WrL'
# # auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
# # auth.set_access_token(access_token,access_token_secret)
# # api = tweepy.API(auth)
# # # df = pd.read_csv('tweeter urls.csv')
# # # twitter_urls = df['URLs']
# # dr_tweet = api.search('@leomessi')
# # for tweets in dr_tweet:
# #     print(tweets.text) 


# import csv
# import tweepy
# import ssl
# import pandas as pd

# ssl._create_default_https_context = ssl._create_unverified_context

# # Oauth keys
# consumer_key = "1f2T81R2O4eLFIBbXDWX0lNuz"
# consumer_secret = "QPh9NBSmogeN0shO7hKPRKKys9UDg4V74N2KQMaXY6JtMllb4Q"
# access_token = "1370338600609488902-E3vqhEBnmBCK3Y3wfbdWyHSLE32qKw"
# access_token_secret = "9vH8eG0Ltvie7pbyrCon2vUhFmpcwrEIfdy4rjtlRUVaI"

# # Authentication with Twitter
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth)

# df = pd.read_csv('tweeter urls.csv')
# twitter_urls = df['URLs']
# for twitter_url in twitter_urls:
#     twitter_url = twitter_url.replace('https://twitter.com/','')
#     name = twitter_url
#     replies=[]
#     for tweet in api.mentions_timeline(max_id=1000).items(1000):
#         # if hasattr(tweet, 'in_reply_to_status_id_str'):
#             # if (tweet.in_reply_to_status_id_str==name):
#         replies.append(tweet)
#     print(replies)


import tweepy
from tweepy import OAuthHandler
import pandas as pd
class TwitterClient(object): 
    def __init__(self):
        # Access Credentials 
        consumer_key = "1f2T81R2O4eLFIBbXDWX0lNuz"
        consumer_secret = "QPh9NBSmogeN0shO7hKPRKKys9UDg4V74N2KQMaXY6JtMllb4Q"
        access_token = "1370338600609488902-E3vqhEBnmBCK3Y3wfbdWyHSLE32qKw"
        access_token_secret = "9vH8eG0Ltvie7pbyrCon2vUhFmpcwrEIfdy4rjtlRUVaI"
        try: 
            # OAuthHandler object 
            auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
            
        except tweepy.TweepError as e:
            print(f"Error: Twitter Authentication Failed - \n{str(e)}") 

    # Function to fetch tweets
    def get_tweets(self, query, maxTweets = 1000): 
        # empty list to store parsed tweets 
        tweets = [] 
        sinceId = None
        max_id = -1
        tweetCount = 0
        tweetsPerQry = 1000
        
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not sinceId):
                        new_tweets = self.api.search(q=query, count=tweetsPerQry)
                    else:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry,
                                                since_id=sinceId)
                else:
                    if (not sinceId):
                        new_tweets = self.api.search(q=query, count=tweetsPerQry,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = self.api.search(q=query, count=tweetsPerQry,
                                                max_id=str(max_id - 1),
                                                since_id=sinceId)
                if not new_tweets:
                    print("No more tweets found")
                    break
                    
                for tweet in new_tweets:
                    parsed_tweet = {} 
                    parsed_tweet['tweets'] = tweet.text 

                    # appending parsed tweet to tweets list 
                    if tweet.retweet_count > 0: 
                        # if tweet has retweets, ensure that it is appended only once 
                        if parsed_tweet not in tweets: 
                            tweets.append(parsed_tweet) 
                    else: 
                        tweets.append(parsed_tweet) 
                        
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets".format(tweetCount))
                max_id = new_tweets[-1].id

            except tweepy.TweepError as e:
                print("Tweepy error : " + str(e))
                break
        
        return pd.DataFrame(tweets)

