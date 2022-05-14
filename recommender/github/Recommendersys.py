import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import *
import gensim
from gensim.parsing.preprocessing import preprocess_documents

df=pd.DataFrame((list(GithubRepos.objects.all().values())))
def fit_repos(keywords):
  df['description'].fillna('').astype(str)
  df['content']=df['content'].map(str)

  print(df['content'])

  text_corpus = df['content'].values

  processed_corpus = preprocess_documents(text_corpus)
  dictionary = gensim.corpora.Dictionary(processed_corpus)
  bow_corpus = [dictionary.doc2bow(text) for text in processed_corpus]

  tfidf = gensim.models.TfidfModel(bow_corpus)
  corpus_tfidf = tfidf[bow_corpus]

  lsi = gensim.models.LsiModel(corpus_tfidf, num_topics=200)
  index = gensim.similarities.MatrixSimilarity(lsi[corpus_tfidf])
  #cv = CountVectorizer()

  #count_matrix = cv.fit_transform(keywords)

  # print(count_matrix.toarray())

  #cosine_sim = cosine_similarity(count_matrix) 
  #return cosine_sim
  return dictionary,tfidf,index,lsi

def get_name_from_index(index):
		return df[df['id'] == index]["full_name"].values[0]

def get_index_from_owner(project_desc):
  #print(project_desc)
  #print(df.head())
  #print(df.loc(0)['id'])
  #cv=CountVectorizer
  return df[df.topics == project_desc]['id'].values[0]