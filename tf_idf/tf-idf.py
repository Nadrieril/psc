'''
Created on Jan 17, 2015

@author: czx
'''
from __future__ import division, unicode_literals
import math
from textblob import TextBlob
def tf(word,blob):                                  #calculer la fréquence d'un mot dans un texte
     return blob.words.count(word)/len(blob.words)
def n_containing(word,bloblist):                    #calculer la fréquence d'apparition d'un mot sur le corpus
    return sum(1 for blob in bloblist if word in blob)
def idf(word,bloblist):                             #l'inverse de la fréquence d'apparition
    return math.log(len(bloblist)/(1+n_containing(word,bloblist)))
def tfidf(word,blob,bloblist):                      #calculer l'incide de tfidf
    return tf(word,blob)*idf(word,bloblist)
def tfphrase(sentence,blob,bloblist):               #calculer les poids des phrases dans un texte
    s=0.0
    n=0
    for word in sentence.words:
        s=s+tfidf(word, blob, bloblist)
        ++n
    return (s/n)
                                    #initialiser le bloblist(ici on a choisit un corpus de 1500 textes)
bloblist=[]
for i in range(1500):
    blob=file(str(i))
    article=""
    for line in blob.readlines():
        if line!="":
            article=article+line
    bloblist.append(TextBlob(article))
    blob.close()
resume=file('resume','w')
for i in range(10):                 #résumer les dix premiers textes
    blob=bloblist.pop()
    resume.write("Top words in document {}\n".format(i+1))
    scores={word:tfidf(word, blob, bloblist) for word in blob.words}
    sorted_words=sorted(scores.items(),key=lambda x:x[1],reverse=True)
    for word,score in sorted_words[:5]:
        resume.write("Word:{},TF-IDF:{}\n".format(word,round(score,5)))
        resume.write("\n")
    phrases={sentence:tfphrase(sentence, blob, bloblist) for sentence in blob.sentences}
    sorted_sentences=sorted(phrases.items(),key=lambda x:x[1],reverse=True)
    k=int(len(blob.sentences)/10)+1
    for sentence,phrase in sorted_sentences[:k]:
        resume.write(":{}\n".format(sentence))
    resume.write("\n")
resume.close()