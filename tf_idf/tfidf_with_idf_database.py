'''
Created on Feb 1, 2015

@author: czx
with the database word, calculate the index tfidf of all the word and the importance of all the sentences from a document and then make a summery by extract those sentences with a great importance
'''
from __future__ import division, unicode_literals
from textblob import TextBlob
from codecs import open
def tf(word,blob):                                  
    return blob.words.count(word)/len(blob.words)
def tfidf(w,article):
    if word.count(w)!=0:
        return tf(w,article)*idf[word.index(word)]
    else:
        return tf(w,article)
    
def tfphrase(sentence,blob):               
    s=0.0
    n=1
    for word in sentence.words:
        i=0
        while sorted_words[i][0]!=word:
            i=i+1
        s=s+sorted_words[i][1]
        n=n+1
    return (s/n)

word=[]
idf=[]
f=open('word',encoding='utf-8').read()
contain=f.readlines(1)
for line in f.readlines():
    word.append(line.split()[0])
    idf.append(line.split()[2])
f.close;
                    
name="test"
blob=open(name,encoding='utf-8').read()
article=""
for line in blob.readlines():
    if line!="":
        article=article+line
blob.close()
article=TextBlob(article)

resume=file('resume','w')                 
resume.write("Top words in document\n")
scores={word:tfidf(word,article) for word in blob.words}
sorted_words=sorted(scores.items(),key=lambda x:x[1],reverse=True)
for word,score in sorted_words[:5]:
    resume.write("Word:{},TF-IDF:{}\n".format(word,round(score,5)))
    resume.write("\n")

phrases={sentence:tfphrase(sentence, blob) for sentence in blob.sentences}
sorted_sentences=sorted(phrases.items(),key=lambda x:x[1],reverse=True)
k=int(len(blob.sentences)/10)+1
for sentence,phrase in sorted_sentences[:k]:
    resume.write(":{}\n".format(sentence))
    resume.write("\n")

resume.close()
