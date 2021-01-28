#!/usr/bin/env python
# coding: utf-8

# In[1]:


from gensim import corpora, models, similarities
import jieba
import pickle
import numpy as np
import os

# In[9]:


class QABot(object):
    def __init__(self, corpus_path):
        with open(os.path.join(corpus_path, 'answers.pkl'), "rb") as f1,              open(os.path.join(corpus_path, 'corpus.pkl'), "rb") as f2,              open(os.path.join(corpus_path, 'dictionary.pkl'), "rb") as f3,              open(os.path.join(corpus_path, 'stopwords.txt')) as f4:

            self.answers = pickle.load(f1)
            self.corpus = pickle.load(f2)
            self.dictionary = pickle.load(f3)
            self.stopwords = set()
            for line in f4:
                self.stopwords.add(line.strip())
            self.tfidf = models.TfidfModel(self.corpus)
            self.corpus_tfidf = self.tfidf[self.corpus]
            self.index = similarities.MatrixSimilarity(self.corpus_tfidf)


    def reply(self, query):

        words = ' '.join(jieba.cut(query)).split(' ')
        new_vec = self.dictionary.doc2bow([word for word in words if word not in self.stopwords])

        new_vec_tfidf = self.tfidf[new_vec]
        sims = np.array(self.index[new_vec_tfidf])

        answer = self.answers[sims.argmax()][1]
        return answer

