import pandas as pd
import numpy as np
from ast import literal_eval
'''
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet

'''

'''  "anger": 1.0570484E-08,
      "contempt": 1.52679547E-09,
      "disgust": 1.60232943E-07,
      "fear": 6.00660363E-12,
      "happiness": 0.9999998,
      "neutral": 9.449728E-09,
      "sadness": 1.23025981E-08,
      "surprise": 9.91396E-10
      '''

emotionToGenre = {'anger' : 'War',
                  'contempt' : 'Horror',
                  'disgust' : 'Horror',
                  'fear' : 'Horror',
                  'happiness' : 'Animation',
                  'neutral' : 'Adventure',
                  'sadness' : 'Romance',
                  'surprise' : 'Thriller'}

def build_chart(emotion, percentile=0.85):
    genre = emotionToGenre[emotion]
    md = pd.read_csv('./data/top5Genre.csv')
    md = md[md['Genre'] == genre]

    print "chart built"
    print md['title'].tolist()
    print md['year'].tolist()
    return md['title'].tolist(), md['year'].tolist(), md['poster_path'].tolist(), md['homepage'].tolist()


#title, year, poster, homepage = build_chart("anger")
#print title