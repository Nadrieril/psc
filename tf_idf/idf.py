'''
Created on Feb 1, 2015

@author: czx
update the word database which contain the idf index of all the word who have appeared
'''
from __future__ import division, unicode_literals
from abstracter.crawler.parse_crawler import download_and_parse_data,download_crawler_data,unify
import math
from textblob import TextBlob
from codecs import open
import glob
import datetime
import os
def n_containing(word,bloblist):                    
    return sum(1 for blob in bloblist if word in blob)


s=datetime.datetime.now()
s=str(s.year)+'_'+'%0*d'%(2,s.month)+'_'+'%0*d'%(2,s.day);
print s
download_crawler_data(s)
path="crawlerpsc/"+s+"/"
bloblist=[]
word=[]
wordexist=[]
f=open('word',encoding='utf-8')
contain=int(f.readline())
for line in f.readlines():
    if line.split()!=[]:
        temp=(float(line.split()[2]),int(line.split()[1]),line.split()[0])
        word.append(temp)
        wordexist.append(line.split()[0])
f.close;

i=0
j=0
while(os.path.exists(path+"%i/%i" % (i,j)) and i<10):
    while(os.path.exists(path+"%i/%i" % (i,j)) and j<100):
        blob=open(path+"%i/%i" % (i,j),encoding='utf-8')
        article=""
        for line in blob.readlines():
            if line!="" and line!="\n":
                article=article+line
        bloblist.append(TextBlob(article))
        blob.close()
        j+=1
        
    j=0
    i+=1
k=len(word)
print k
bloblistlength=len(bloblist)+contain
wordoccur=[]             
for i,blob in enumerate(bloblist):
    for words in blob.words:
        w=words.lower()
        if(wordoccur.count(words)==0):
            wordoccur.append(words)
            if wordexist.count(words)==0:
                frequency=n_containing(words, bloblist)
                temp=(math.log(bloblistlength/(1+frequency)),frequency,words)
                word.append(temp)
                k=k+1
            else:
                j=wordexist.index(words)
                frequency=word[j][1]+n_containing(words, bloblist)
                temp=(math.log(bloblistlength/(1+frequency)),frequency,words)
                word[j]=temp
                
word.sort()
writeword=open('word','w',encoding='utf-8')
writeword.write("number of words:"+str(k)+"\n")
writeword.write("word frequency idf\n")
for i in range(len(word)):
    writeword.write(word[i][2]+' '+str(word[i][1])+' '+str(word[i][0])+"\n")
writeword.close()
