import pandas as pd
import numpy as np

def get_contentRec(title):
    totalDF = pd.read_csv('./data/contentRec_3000_meta2.csv', memory_map=True)
    indices = pd.Series(totalDF.index, index=totalDF['title'])
    titles = totalDF['title']
    homepage = totalDF['homepage']
    poster = totalDF['poster_path']
    date = totalDF['release_date']
    totalDF = totalDF.drop(['title', 'homepage', 'poster_path', 'release_date'], axis=1)

    idx = indices[title]

    cosine_sim = totalDF.values
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    return titles.iloc[movie_indices].tolist(), homepage[movie_indices].tolist(), poster[movie_indices].tolist(), date[movie_indices].tolist()

#titles, homepage, poster, date = contentRec("Mad Max")