# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 10:24:46 2020

@author: joel_dylan
"""
import praw
#import  urllib
import urllib.request
import feedparser

class Reddit:
    def __init__(self, client_id, client_secret, user_agent, search_query, limit):
        self.search_query = search_query
        self.limit = limit
        self.reddit = praw.Reddit(
            client_id = client_id,
            client_secret = client_secret,
            user_agent = user_agent
        )

    def getText(self):
        docs = []
        for post in self.reddit.subreddit(self.search_query).hot(limit=self.limit):
            txt = post.title+" " +post.selftext
            #txt = txt.replace("\n", " ")
            docs.append(txt)
        return docs

class Arxiv:
    def __init__(self, search_query, start, max_results, base_url):
        self.base_url = base_url
        # Search parameters
        self.search_query = search_query
        self.start = start                    # retreive the first 5 results
        self.max_results = max_results
        self.query = 'search_query=%s&start=%i&max_results=%i' % (search_query, start, max_results)
    def getText(self):
        feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
        feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'
        response = urllib.request.urlopen(self.base_url+self.query).read()
        feed = feedparser.parse(response)
        articles = []
        for entry in feed.entries:
            articles.append({
                'Published': entry.published,
                'Title': entry.title,
                'Abstract': entry.summary
            })
            #format de date de publication = 2015-01-20T18:48:22Z
        return articles
