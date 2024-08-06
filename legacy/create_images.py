import dropbox
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime as dt

dir = 'tmp/'


files = os.listdir(dir)
files

for file in files:
    # Only parse .txt files
    if file.endswith('.txt'):
        fname = file
        print('file:', file)
        name_part = fname.rsplit('.', 1)[0]
        ifpath = os.path.join(dir, fname)

        ofpath = os.path.join(dir, name_part+'.png')
        print(fname,'-', name_part, 'file will be saved as:', ofpath)

        with open(ifpath, 'r') as file:
            text = file.read()
        
        
            

def create_image_from_text(text, ofpath):
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
    #image.save(ofpath) # save in cur folder
    image.save(ofpath)

    print("Image saved as", ofpath)


create_image_from_text(text, ofpath=ofpath)