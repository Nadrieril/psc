import webParser
import tarfile
import os
import datetime
import shutil

resultPath = "result"
parser = webParser.webParser()
if not os.access(resultPath, os.R_OK):
    print("Folder " + resultPath + " does not exists,creating it")
    os.mkdir(resultPath)
with open("rssUrls.txt") as rssUris:
    for countRss, rss in enumerate(rssUris.readlines()):
        articles = parser.getTodayUrisFromRss(rss)

        folderName = (resultPath + "/"
                      + datetime.date.today().strftime("%Y_%m_%d")
                      + "/"
                      + str(countRss))
        os.makedirs(folderName)
        with open(folderName + "_url.txt", "w") as nameFile:
            nameFile.write(rss)

        for count, article in enumerate(articles):
            parsedArticle = parser.parse(article)
            with open(folderName + "/" + str(count), "w+") as f_out:
                f_out.write(parsedArticle)
            with open(folderName + "/" + str(count)
                      + "_url.txt", "w") as nameFile:
                nameFile.write(article)

        with tarfile.open(folderName + ".tar.gz", "w:gz") as tar_out:
            tar_out.add(folderName)

        shutil.rmtree(folderName)
