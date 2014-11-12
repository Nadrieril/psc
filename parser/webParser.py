import feedparser
import requests
import re
import json
from html import unescape
from localConfig import token


class webParser:
    """
    A simple class to parse articles from the web
    Use it with
    webParser.parse(uri)
    or
    webParser.getUrisFromRss(rssUri)
    """

    token = token

    def parse(self, url):
        """
        Parses the article at given url and returns it as plain text
        """
        article = self.readbilityGet(url)
        return self.parseText(article)

    def parseText(self, article):
        """
        Parses the given html text an returns it as plain text
        """
        # Remove all html tabs
        article = re.sub(r"<.*?>", "", article)
        # Remove special characters
        article = unescape(article)
        return article

    def readbilityGet(self, url):
        """
        Get the article at given url using the readability api
        to extract the content
        """
        # Get the article
        json_response = requests.get('https://www.readability.com/api/content'
                                     '/v1/parser?url=' + url + '&token=' +
                                     self.token)

        # Then extract content from json data :
        article = json.loads(json_response.text)['content']
        return article

    def getUrisFromRss(self, rssUri):
        """
        Get all the articles from the given RSS feed
        """
        rss = feedparser.parse(rssUri)
        return [item.link for item in rss.entries]
