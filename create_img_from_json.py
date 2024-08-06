#!/usr/bin/python3
import dropbox
from PIL import Image, ImageDraw, ImageFont
import os
import configparser
from datetime import datetime as dt
from dotenv import load_dotenv
import json



def create_image_from_text(filename, text, image_save_path):
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
    #image.save(image_save_path) # save in cur folder
    image.save(image_save_path+filename+'.png')

    print("Image saved as", image_save_path)




dir = 'tmp/'

with open(dir + 'output.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    
    for key, value in data.items():
        print(f"Filename: {key}")
        filename=key
        print(f"Text Content: {value['text_content']}")
        text = value['text_content']
        print(f"Hash Content: {value['hash_content']}")
        hash = value['hash_content']
        print()

        create_image_from_text(filename=key,text=text, image_save_path=dir)