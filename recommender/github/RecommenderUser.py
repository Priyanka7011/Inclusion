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

def user_recs(dictionary,tfidf,index,lsi,desc):
  new_doc=gensim.parsing.preprocessing.preprocess_string(desc)
  new_vec = dictionary.doc2bow(new_doc)
  vec_bow_tfidf = tfidf[new_vec]
  vec_lsi = lsi[vec_bow_tfidf]
  
  sims = index[vec_lsi]
  
  
  user=[]
  s=sorted(enumerate(sims), key=lambda item: -item[1])[:100]
  user_repo=["a"]*10
  
  stop_words=['[',']',',',', ','[]','([','([])','])',', ', ' [',"'","['",'None, ']
  user_expert=[]

  for i in range(0,100,10):
    user_repo[i//10]=str(df['all_repos'].iloc[s[i][0]]).split("]")
    lang=["a"]*len(user_repo[i//10])
    for j in range(0,len(user_repo[i//10])):
      lang[j]=user_repo[0][j].split("'")
    main_word=[]
    for k in range(len(lang)):
      keywords=[]
      for l in range(len(lang[k])):
        if lang[k][l] not in stop_words:
          keywords.append(lang[k][l])
      main_word.append(keywords)
    lang_user=[]
    for m in range(len(main_word)):
      if(len(main_word[m])>3):
        if(main_word[m][2][0]!=','):
          lang_user.append(main_word[m][2])
    
    user_expert.append(lang_user)
  
  #print(user_expert)

          
  for i in range(len(user_expert)):
      user_expert[i]=np.array(user_expert[i])
      user_expert[i]=np.unique(user_expert[i])

  


  for i in range(0,100,10):
    
    user.append([df["login"].iloc[s[i][0]],df["avatar_url"].iloc[s[i][0]],df["git_url"].iloc[s[i][0]],
                     df["name"].iloc[s[i][0]],df["total_repos"].iloc[s[i][0]],df["orgs"].iloc[s[i][0]],user_expert[i//10]])
  
  

  return user,user_expert