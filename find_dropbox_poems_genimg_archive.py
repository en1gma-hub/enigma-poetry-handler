import dropbox
from PIL import Image, ImageDraw, ImageFont
import os
import configparser
from datetime import datetime as dt
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv('./.env')

# Set up your credentials
client_id = os.getenv

# Set up your credentials
refresh_token = os.getenv('DROPBOX_REFRESH_TOKEN')
app_key = os.getenv('DROPBOX_APP_TOKEN')
app_secret = os.getenv('DROPBOX_APP_TOKEN_SECRET')

#print('r-token:', refresh_token,
#      '\na-key:', app_key, 
#      '\na-secret:', app_secret
#      )



def read_local_file(file):
    """Read local file."""
    with open(file, 'r') as file:
        return file.read().strip()

def create_image_from_text(text, image_path):
    size_increaser = 0
    size_decreaser = 0

    if len(text) > 1000:
        width, height = 1080, 1350  # Instagram resolution - portrait
        size_decreaser = round(len(text)/100)
    else:
        width, height = 1080, 1080  # Instagram resolution - square
        size_increaser = round(len(text)/100)
    image = Image.new('RGB', (width, height), color='white')

    # Initialize ImageDraw
    draw = ImageDraw.Draw(image)

    # Define the font and size
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"  # Use a TTF font
    font_size = 28 + (size_increaser) - (size_decreaser) # Increase font size
    print(font_size)

    font = ImageFont.truetype(font_path, font_size)

    # Calculate text size and position using textbbox
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2

    # Draw the text on the image
    draw.text((text_x, text_y), text, fill='black', font=font)

    # Save the image
    #image.save(image_path) # save in cur folder
    image.save(os.path.join('tmp', image_path))

    print("Image saved as", image_path)

def process_files(dbx, src_folder, dest_folder):
    """Process text files in the Dropbox folder."""
    counter = 0
    try:
        result = dbx.files_list_folder(src_folder)
        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata) and entry.path_lower.endswith('.txt'):
                counter += 1
                file_metadata, response = dbx.files_download(entry.path_lower)
                print('path_lower:',entry.path_lower)
                text_content = response.content.decode('utf-8')
                text_content = text_content.replace('\r', '') # removes invis char that prints as unknown char
                
                print(f'File Content of {entry.name}:\n{text_content}')
                
                image_path = f"{entry.name.replace('.txt', '.png')}"
                print('image_path:',image_path)
                create_image_from_text(text_content, image_path)
                
                # Move the file to the destination folder
                dest_path = f"{dest_folder}/{entry.name}"
                #dbx.files_move_v2(entry.path_lower, dest_path) # move it!
                print(f"Moved {entry.name} to {dest_folder}")
                
    except dropbox.exceptions.ApiError as err:
        print(f'Failed to process files in {src_folder}: {err}')

def main():
    """Main function."""
    # Read the credentials from the files
    #refresh_token = read_local_file('refresh_token.txt')
    #app_key = read_local_file('app_key.txt')
    #app_secret = read_local_file('app_secret.txt')

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
