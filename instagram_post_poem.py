#!/usr/bin/python3

from instagrapi import Client
from dotenv import load_dotenv
import os
import json

# Load environment variables from .env file
load_dotenv('./.env')

# Set up your credentials
username = os.getenv('INSTAGRAM_USER_NAME')
password = os.getenv('INSTAGRAM_PASSWORD')

# Function to perform manual login and save session settings
def manual_login_and_save_session(client, username, password):
    client.login(username=username, password=password)
    settings = client.get_settings()
    with open('session_settings.json', 'w') as f:
        json.dump(settings, f)
    print("Logged in and session settings saved")

# Function to login using session settings
def login_with_session_settings(client):
    try:
        with open('session_settings.json', 'r') as f:
            settings = json.load(f)
        client.set_settings(settings)
        client.login(username=username, password=password)
        print("Logged in using session settings")
    except (FileNotFoundError, Exception) as e:
        print(str(e))
        manual_login_and_save_session(client, username, password)

# Initialize the client
cl = Client()

# Attempt to login using session settings
login_with_session_settings(cl)

instagram_max_len = 125
dir = 'tmp/'

with open(dir + 'output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

    for key, value in data.items():
        print(f"Filename: {key}")
        filename = key
        media_path = os.path.join(dir, filename + '.png')
        text = '\n' + value['text_content']
        hash_content = value['hash_content']
        
        # Initial length of the text content
        text_len = len(text)
        
        # Split the hash content into individual hashtags
        hashtags = hash_content.replace('#', '').split()
        
        final_text = text + '\n\n'  # newline to separate from hashtags
        
        for hashtag in hashtags:
            if text_len + len('#' + hashtag) + 1 <= instagram_max_len +125:  # +1 for the space or new line
                final_text += '#' + hashtag + ' '
                text_len += len('#' + hashtag) + 1
        
        print(f"Final Content:\n{final_text}\n")            
        cl.photo_upload(media_path, final_text)
        print("Instagram Post uploaded successfully.")
