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
        with open(os.path.join(corpus_path, 'answers.pkl'), "rb") as f:
            self.answers = pickle.load(f)
        with open(os.path.join(corpus_path, 'corpus.pkl'), "rb") as f:
            self.corpus = pickle.load(f)
        with open(os.path.join(corpus_path, 'dictionary.pkl'), "rb") as f:
            self.dictionary = pickle.load(f)
        self.stopwords = set()
        with open(os.path.join(corpus_path, 'stopwords.txt'), "rb") as f:
            for line in f:
                self.stopwords.add(line.strip())
        self.tfidf = models.TfidfModel(self.corpus)
        self.corpus_tfidf = self.tfidf[self.corpus]
        self.index = similarities.MatrixSimilarity(self.corpus_tfidf)

    def reply(self, query):

        words = ' '.join(jieba.cut(query)).split(' ')
        new_vec = self.dictionary.doc2bow([word for word in words if word not in self.stopwords])

        new_vec_tfidf = self.tfidf[new_vec]
        sims = np.array(self.index[new_vec_tfidf])

        answer = self.answers[sims.argmax()]
        return answer

