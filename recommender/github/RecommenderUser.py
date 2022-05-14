import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import *
import gensim
from gensim.parsing.preprocessing import preprocess_documents

df=pd.DataFrame((list(GithubUsers.objects.all().values())))

def fit(keywords):
  
  df['all_repos']=df['all_repos'].map(str)

  text_corpus = df['all_repos'].values

  processed_corpus = preprocess_documents(text_corpus)
  dictionary = gensim.corpora.Dictionary(processed_corpus)
  bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]

  tfidf = gensim.models.TfidfModel(bow_corpus)
  corpus_tfidf = tfidf[bow_corpus]

  lsi = gensim.models.LsiModel(corpus_tfidf, num_topics=200)
  index = gensim.similarities.MatrixSimilarity(lsi[corpus_tfidf])
  
  return dictionary,tfidf,index,lsi
