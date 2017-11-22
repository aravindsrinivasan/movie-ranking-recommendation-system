import os
import requests # pip install requests

import numpy as np
import pandas as pd


ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
IMG_DIR_PATH = os.path.join(ROOT_DIR, '..', 'images')
DATA_PATH = os.path.join(ROOT_DIR, '..', 'data')

if not os.path.exists(IMG_DIR_PATH):
    os.makedirs(IMG_DIR_PATH)


script_path = os.path.join(DATA_PATH, 'movies_metadata.csv')


df = pd.read_csv(script_path)
df = df[['id', 'poster_path']]


print ('Total: {0} images'.format(df.shape[0]))


for index, row in df.iterrows():
    try:
        video_id = str(row[0])
        #@ Aravind, change the movie poster width from w500 to w180 if you want smaller resolution files
        link = "https://image.tmdb.org/t/p/w500" +  str(row[1])
        file_name = os.path.join(IMG_DIR_PATH, '{0}.jpg'.format(video_id))
        print video_id
        print link
    except:
        continue
    if not os.path.isfile(file_name):
        f = open(file_name, 'wb')
        f.write(requests.get(link).content)
        f.close()


