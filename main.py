#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  5 19:21:31 2021

@author: adonis
"""
import get_source as dsource
import string
from collections import Counter
from operator import itemgetter
import heapq
import collections

class CorpusAnalysis:
    def __init__(self):
        obj_reddit = dsource.Reddit('53EBbuUEDKupuA', '8ydTUoUUckRKSqOBcuPBoLtsq1Y', 'joel dylan', 'dylan', 10)
        self.reddit_text = obj_reddit.getText()
        obj_arxiv = dsource.Arxiv('all:electron',0, 5, 'http://export.arxiv.org/api/query?')
        self.arxiv_text = obj_arxiv.getText()
    def termineTreat(self):
        print('\n\n')
        print("Enter Yes to return to the home page or anything to else!!!")
        val = input("return to the home page?")
        if val.upper() == "YES":
            self.mainFunction()
        else:
            print("############################################")
            print("####                                    ####")
            print("####            GOOD BYE                ####")
            print("####                                    ####")
            print("############################################")
            exit()
    def least_common_values(self, array):
        counter = collections.Counter(array)
        return sorted(counter.items(), key=itemgetter(1), reverse=False)
    def analysisRedditArxivArticle(self, redditConf, arxivConf):
        """
        this function will analyse one reddit and one arxiv articles
        """
        redditTopic = input("Enter your Reddit Topic: ")
        loops = True
        while loops == True:
            redditLimit = input("Enter your Reddit Limit: ")
            try:
                limit = int(redditLimit)
                loops = False
            except ValueError:
                print("Limit of reddit results must be integer!!!")
        arxivTopic = input("Enter your Arxiv Topic: ")
        obj_reddit = dsource.Reddit(
            redditConf['client_id'],
            redditConf['client_secret'],
            redditConf['user_agent'], redditTopic, limit)
        reddit_list = obj_reddit.getText()
        reddit_text = []
        reddit_words = []
        for reddit in reddit_list:
            reddit_text.append(reddit.split('\n'))
            for reddit_phrase in reddit.split('\n'):
                reddit_phrase = reddit_phrase.translate(str.maketrans('', '', string.punctuation))
                for word in reddit_phrase.split():
                    reddit_words.append(word)
        obj_arxiv = dsource.Arxiv(arxivTopic, arxivConf['start'], 1, arxivConf['base_url'])
        arxiv_list = obj_arxiv.getText()
        arxiv_fulltext = []
        arxiv_text = []
        arxiv_words = []
        for arxiv_article in arxiv_list:
            arxiv_fulltext.append(arxiv_article['Title'] + ' ' + arxiv_article['Abstract'])
        for arxiv_t in arxiv_fulltext:
            arxiv_text.append(arxiv_t.split('\n'))
            for arxiv_phrase in arxiv_t.split('\n'):
                arxiv_phrase = arxiv_phrase.translate(str.maketrans('', '', string.punctuation))
                for word in arxiv_phrase.split():
                    arxiv_words.append(word)
        print("Reddit Text to analyse")
        print('\n')
        print(reddit_list)
        print('\n')
        print("Reddit Words to treat")
        print('\n')
        print(reddit_words)
        print('\n')
        print("Arxiv Text to analyse")
        print('\n')
        print(arxiv_list)
        print("Arxiv Words to treat")
        print('\n')
        print(arxiv_words)
        print('\n')
        #analyse des mots Reddit dans Arxiv
        result = []
        for reddit_word in list(set(reddit_words)): #j'enlève les doublons dans la liste avant tout
            reddit_apparition = arxiv_words.count(reddit_word)
            arxiv_apparition = reddit_words.count(reddit_word)
            result.append({
                'reddit_apparition': reddit_apparition,
                'arxiv_apparition': arxiv_apparition,
                'word': reddit_word
            })
        #Le mot qui apparait le plus dans le corpus Reddit qui apparait le moins dans le corpus Arxiv
        #je considère le 1er résultat comme correspondant a la recherche
        maxReddit_apparition = result[0]['reddit_apparition']
        maxArxiv_apparition = result[0]['arxiv_apparition']
        word = result[0]['word']
        for res in result:
            if res['reddit_apparition'] > maxReddit_apparition and res['arxiv_apparition'] < maxArxiv_apparition:
                maxReddit_apparition = res['reddit_apparition']
                maxArxiv_apparition = res['arxiv_apparition']
                word = res['word']
        print(("Le mot qui apparait le plus dans le corpus Reddit et qui apparait le moins dans le corpus Arxiv est %s") % word)
        print('\n')
        #analyse des mots Arxiv dans Reddit 
        result = []
        reddit_words
        for arxiv_word in list(set(arxiv_words)): #j'enlève les doublons dans la liste avant tout
            arxiv_apparition = arxiv_words.count(arxiv_word)
            reddit_apparition = reddit_words.count(arxiv_word)
            result.append({
                'reddit_apparition': reddit_apparition,
                'arxiv_apparition': arxiv_apparition,
                'word': reddit_word
            })
        #Le mot qui apparait le plus dans le corpus Arxiv qui apparait le moins dans le corpus Reddit
        #je considère le 1er résultat comme correspondant a la recherche
        maxReddit_apparition = result[0]['reddit_apparition']
        maxArxiv_apparition = result[0]['arxiv_apparition']
        word = result[0]['word']
        for res in result:
            if res['reddit_apparition'] < maxReddit_apparition and res['arxiv_apparition'] > maxArxiv_apparition:
                maxReddit_apparition = res['reddit_apparition']
                maxArxiv_apparition = res['arxiv_apparition']
                word = res['word']
        print(("Le mot qui apparait le plus dans le corpus Arxiv qui apparait le moins dans le corpus Reddit est %s") % word)
        print('\n')
        #Le mot qui apparait le plus dans le corpus Reddit
        val = Counter(reddit_words).most_common(1)
        for v in val:
            mot, taille = v
            print(("Le mot apparaissant le plus dans le corpus Reddit est '%s'") % mot)
            print('\n')
        #Le mot qui apparait le plus dans le corpus Arxiv
        val = Counter(arxiv_words).most_common(1)
        for v in val:
            mot, taille = v
            print(("Le mot apparaissant le plus dans le corpus Arxiv est '%s'") % mot)
            print('\n')
        self.termineTreat()
        
    def mainFunction(self):
        """
        main function of our program
        """
        print("############################################")
        print("####                                    ####")
        print("####   WELCOME TO OUR CORPUS ANALYSER   ####")
        print("####                                    ####")
        print("############################################")
        print("\n")
        print("#### To analyse one reddit and one arxiv article, type 1####")
        print("#### To analyse arxiv's articles about one subject in the time, type 2####")
        print("#### To close the program, type anything else ####")
        choice = input("Enter your choice please!")
        #Reddit api configuration
        redditConf = {
            'client_id': '53EBbuUEDKupuA',
            'client_secret':  '8ydTUoUUckRKSqOBcuPBoLtsq1Y',
            'user_agent': 'joel dylan'
        }
        #Arxiv api configuration
        arxivConf = {
            'base_url': 'http://export.arxiv.org/api/query?',
            'start':  0
        }
        if choice == '1':
            self.analysisRedditArxivArticle(redditConf, arxivConf)
        elif choice == '2':
            #self.analysisRedditArxivArticle()
            pass
        else:
            print("############################################")
            print("####                                    ####")
            print("####            GOOD BYE                ####")
            print("####                                    ####")
            print("############################################")
            exit()

val = CorpusAnalysis()
val.mainFunction()
