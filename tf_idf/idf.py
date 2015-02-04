'''
Created on Feb 1, 2015

@author: czx
'''
from __future__ import division, unicode_literals
import math
from textblob import TextBlob
from codecs import open
import glob
import time
def n_containing(word,bloblist):                    
    return sum(1 for blob in bloblist if word in blob)
def idf(word,bloblist):                             
    return math.log(len(bloblist)/(1+n_containing(word,bloblist)))

s=time.strftime("%x")
path=""
files=glob.glob("7/*")
bloblist=[]
word=[]
idf=[]
frequency=[]
f=open('word',encoding='utf-8')
contain=int(f.readline())
for line in f.readlines():
    if line.split()!=[]:
        word.append((line.split()[0]))
        frequency.append(int(line.split()[1]))
        idf.append(line.split()[2])
f.close;

for ff in files:
    print ff
    blob=open(ff,encoding='utf-8')
    article=""
    for line in blob.readlines():
        if line!="" and line!="\n":
            article=article+line
    bloblist.append(TextBlob(article))
    blob.close()
k=len(word)
bloblistlength=len(bloblist)+contain
wordoccur=[]             
for i,blob in enumerate(bloblist):
    for words in blob.words:
        if(wordoccur.count(words)==0):
            wordoccur.append(words)
            if word.count(words)==0:
                word.append(words)
                j=k
                k=k+1
                frequency.append(n_containing(words, bloblist))
                idf.append(math.log(bloblistlength/(1+frequency[k-1])))
            else:
                j=word.index(words)
                frequency[j]=frequency[j]+n_containing(words, bloblist)
                idf[j]=math.log(bloblistlength/(1+frequency[k-1]))
for i in range(len(word)):
    for j in range(i+1,len(word)):
        if idf[j]<idf[i]:
            temp=idf[j]
            idf[j]=idf[i]
            idf[i]=temp
            str1=word[i]
            word[i]=word[j]
            word[j]=str1
            temp=frequency[i]
            frequency[i]=frequency[j]
            frequency[j]=temp
writeword=open('word','w',encoding='utf-8')
writeword.write(str(bloblistlength)+"\n")
for i in range(len(word)):
    writeword.write(word[i]+' '+str(frequency[i])+' '+str(idf[i])+"\n")
writeword.close()
