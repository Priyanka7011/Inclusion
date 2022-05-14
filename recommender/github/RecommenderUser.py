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



def orgs_recs_user(dictionary,tfidf,index,lsi,desc):
  new_doc=gensim.parsing.preprocessing.preprocess_string(desc)
  new_vec = dictionary.doc2bow(new_doc)
  vec_bow_tfidf = tfidf[new_vec]
  vec_lsi = lsi[vec_bow_tfidf]

  sims = index[vec_lsi]
  list_user=[]

  s=sorted(enumerate(sims), key=lambda item: -item[1])[:100]
  stop_words=['[',']',',',', ','[]','([','([])','])',', ']
  for i in range(0,100,10):
    tx=str(df["orgs"].iloc[s[i][0]])
    txt=tx.split("'")
    for k in txt:
        if k not in stop_words:
            list_user.append(k)

        

  list_user=np.array(list_user)
  list_user=np.unique(list_user)
  list_user

  return list_user
