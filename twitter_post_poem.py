import tweepy
from tweepy import API
import os
import configparser
from datetime import datetime as dt
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv('./.env')

# Set up your credentials
client_id = os.getenv

# Set up your credentials
consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_KEY_SECRET')
beaerer_token = os.getenv('TWITTER_BEARER_TOKEN')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
print('c-key:', consumer_key, 
      '\nc-secret:', consumer_secret,
      '\nbearer:', beaerer_token, 
      '\na-token:', access_token, 
      '\na-secret:', access_token_secret
      )



def get_twitter_conn_v1(api_key, api_secret, access_token, access_token_secret) -> tweepy.API:
    """Get twitter conn 1.1"""

    auth = tweepy.OAuth1UserHandler(api_key, api_secret)a
    auth.set_access_token(
        access_token,
        access_token_secret,
    )
    return tweepy.API(auth)

def get_twitter_conn_v2(api_key, api_secret, access_token, access_token_secret) -> tweepy.Client:
    """Get twitter conn 2.0"""

    client = tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret,
    )

    return client

client_v1 = get_twitter_conn_v1(consumer_key, consumer_secret, access_token, access_token_secret)
client_v2 = get_twitter_conn_v2(consumer_key, consumer_secret, access_token, access_token_secret)




twitter_max_len = 280
dir = 'tmp/'

with open(dir + 'output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    for key, value in data.items():
        print(f"Filename: {key}")
        filename = key
        media_path = dir+filename+'.png'
        text = value['text_content']
        hash_content = value['hash_content']
        
        # Initial length of the text content
        text_len = len(text)
        
        # Split the hash content into individual hashtags
        hashtags = hash_content.split('\n')
        
        # Add hashtags while ensuring the total length doesn't exceed the limit
        if text_len >= twitter_max_len:
            final_text = text[:278]+'..'
        else:
            final_text = text
            for hashtag in hashtags:
                if text_len + len(hashtag) + 1 <= twitter_max_len:  # +1 for the space or new line
                    final_text += '\n' + hashtag
                    text_len += len(hashtag) + 1
            
            print(f"Final Content:\n{final_text}\n")

        media = client_v1.media_upload(filename=media_path)
        media_id = media.media_id

        client_v2.create_tweet(text=final_text, media_ids=[media_id])





#media_path = "C:\\YourPath"

#media = client_v1.media_upload(filename=media_path)
#media_id = media.media_id

#client_v2.create_tweet(text="This is a test", media_ids=[media_id])
