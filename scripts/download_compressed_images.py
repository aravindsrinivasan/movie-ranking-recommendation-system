import os
import requests
import numpy as np
import pandas as pd
from PIL import Image
from StringIO import StringIO

#Get paths of image file and data
ROOT_DIR = os.path.dirname(os.path.realpath('__file__'))
IMG_DIR_PATH = os.path.join(ROOT_DIR, '..', 'images')
DATA_PATH = os.path.join(ROOT_DIR, '..', 'data')

if not os.path.exists(IMG_DIR_PATH):
    os.makedirs(IMG_DIR_PATH)

#Filter by movie_id and url extension to poster
script_path = os.path.join(DATA_PATH, 'movies_metadata.csv')
df = pd.read_csv(script_path)
df = df[['id', 'poster_path']]
print ('Total: {0} images'.format(df.shape[0]))

#Size images will be compressed to
size = 125, 190

#Iterate through every record, obtain the poster, compress it and store in the image repo
for index, row in df.iterrows():
    try:
        video_id = str(row[0])
        link = "https://image.tmdb.org/t/p/w500" +  str(row[1])
        file_name = os.path.join(IMG_DIR_PATH, '{}.jpg'.format(video_id))
        url = requests.get(link)
        img = Image.open(StringIO(url.content))
        img.thumbnail(size, Image.ANTIALIAS)
        print '{} of {} in progress'.format(index + 1, df.shape[0])
        print video_id
        print link
    except:
        continue
    if not os.path.isfile(file_name):
        img.save(file_name)
        

