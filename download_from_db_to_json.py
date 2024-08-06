#!/usr/bin/python3

######################################################################
# This downloads .txt from Dropbox to tmp/ folder
######################################################################
import dropbox
import os
import configparser
from datetime import datetime as dt
from dotenv import load_dotenv
import shutil
import json


# Load environment variables from .env file
load_dotenv('./.env')

# Set up your credentials
client_id = os.getenv

# Set up your credentials
refresh_token = os.getenv('DROPBOX_REFRESH_TOKEN')
app_key = os.getenv('DROPBOX_APP_TOKEN')
app_secret = os.getenv('DROPBOX_APP_TOKEN_SECRET')



def process_files(dbx, src_folder, dest_folder):
    """Process text files in the Dropbox folder."""
    counter = 0

    #dir = 'home/ph0s/code/enigma-poetry-handler/tmp/'
    dir = 'tmp/'

    shutil.rmtree(dir, ignore_errors=True)
    os.makedirs(dir, exist_ok=True)

    try:
        result = dbx.files_list_folder(src_folder)
        counter = 0
        data = {}

        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.path_lower.endswith('.txt'):
                counter += 1
                print('entry:', entry)
                file_metadata, response = dbx.files_download(entry.path_lower)
                print('path_lower:', entry.path_lower)
                text_content = response.content.decode('utf-8')
                text_content = text_content.replace('\r', '')  # removes invisible char that prints as unknown char
                
                # Split text_content into lines
                lines = text_content.split('\n')
                
                # Separate hash content from text content
                hash_content = []
                main_content = []
                hash_flag = False

                for line in lines:
                    if line.startswith('#'):
                        hash_flag = True
                    if hash_flag:
                        hash_content.append(line)
                    else:
                        main_content.append(line)

                text_content = '\n'.join(main_content)
                hash_content = '\n'.join(hash_content)
                hash_content = hash_content.replace('\n', '')  # removes invisible char that prints as unknown char
                
                fname = entry.name.split('.')[0]
                data[fname] = {
                    'text_content': text_content,
                    'hash_content': hash_content
                }

        # Save data to a JSON file with UTF-8 encoding
        with open('tmp/output.json', 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)

    except dropbox.exceptions.ApiError as err:
        print(f'Failed to process files in {src_folder}: {err}')

def main():
    """Main function."""
    # Read the credentials from the files
    
    # Initialize Dropbox SDK with refresh token
    dbx = dropbox.Dropbox(
        app_key=app_key,
        app_secret=app_secret,
        oauth2_refresh_token=refresh_token
    )
    
    #src_folder = '/app/new-poem'
    #dest_folder = '/app/archived-poems'
    src_folder = '/poem'
    dest_folder = '/archive'
    process_files(dbx, src_folder, dest_folder)

if __name__ == "__main__":
    main()


