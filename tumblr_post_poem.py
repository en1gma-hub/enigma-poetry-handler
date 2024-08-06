from requests_oauthlib import OAuth1Session
import os
from dotenv import load_dotenv
import pytumblr2 as pytumblr
import json 

# Load environment variables from .env file
load_dotenv('./.env')

# Set up your credentials
TUMBLR_CONSUMER_KEY = os.getenv('TUMBLR_CONSUMER_KEY')
TUMBLR_CONSUMER_SECRET = os.getenv('TUMBLR_CONSUMER_SECRET')
TUMBLR_OAUTH_TOKEN = os.getenv('TUMBLR_OAUTH_TOKEN')
TUMBLR_OAUTH_SECRET = os.getenv('TUMBLR_OAUTH_SECRET')

client = pytumblr.TumblrRestClient(
  TUMBLR_CONSUMER_KEY,
  TUMBLR_CONSUMER_SECRET,
  TUMBLR_OAUTH_TOKEN,
  TUMBLR_OAUTH_SECRET
)

# Make the request
client.info()




tumblr_max_len = 280
dir = 'tmp/'

with open(dir + 'output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    for key, value in data.items():
        print(f"Filename: {key}")
        filename = key
        media_path = dir + filename + '.png'
        text = value['text_content']
        hash_content = value['hash_content']
        
        # Initial length of the text content
        text_len = len(text)
        
        # Split the hash content into individual hashtags
        hashtags = hash_content.split('\n')
        
        # Split the hash content into individual tags and remove the '#' symbol
        hashtags = hash_content.replace('#', '').split()
        
        # Add hashtags while ensuring the total length doesn't exceed the limit
        if text_len > tumblr_max_len:
            final_text = text[:278]+'..'
        final_text = text
        
        print(f"Final Content:\n{final_text}\n")

        client.create_post(
            'enigmapoets',
             tags=hashtags,
            content=[
                {"type": "text", "text": final_text},
                {"type": "image", "media": [{"type": "image/png", "identifier": "my_media_identifier"}]}
            ],
            media_sources={"my_media_identifier": media_path}
        )


#Creating a text post
#client.create_post('enigmapoets', content=[{'type': 'text', 'text': "Posting Hello !from Python! 3"}])
