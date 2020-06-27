# -*- coding: utf-8 -*-
"""
Created on Sat Jun 12 21:33:41 2020

@author: ARVIND KRISHNA
github: github.com/ArvindAROO
"""

import json
import re
with open('scraped_articles.json') as articles:
    data = json.load(articles)
    #this casts the json file into a dictionary with only one key 'newspapers'
    #print("Type:", type(data)) #dict 
    articles.close()

def manipulateData():
    newspapers = data["newspapers"]
    #this is a dictionary of newspapers
    #print("type:",type(newspapers)) #dict
    
    newspaperCompanies = list(newspapers.keys())
    #getting the keys for the dictionary
    print("The newspapers are {} ".format(newspaperCompanies))
    companyCount = 0
    for companyKey in newspaperCompanies:
        #print(newspapers[company])
        companyDict = newspapers[companyKey]
        #creating a dictionary containg all the aspects of the  company
        companyURL =  companyDict['link']
        print("Printing news from {} with website '{}'".format(companyKey,companyURL))
        articlesList = companyDict['articles']
        #print(type(articlesList)) #A list
        companyCount += 1
        for eachArticle in articlesList:
            #print(eachArticle.keys()) #['link', 'published', 'title', 'text']
            print("Article Name - \"{}\"\n\nsource URL - '{}' & published on {}\n ".format(eachArticle['title'], eachArticle['link'], eachArticle['published']))
            articleContent = eachArticle['text']
            #using regex to remove unwanted spaces and AD spaces
            articleContent = re.sub(r"AD", '', articleContent)
            articleContent = re.sub(r"\n\n", '', articleContent)
            print("\n{}\n\n\n".format(articleContent))
            del articleContent
            
if __name__ == '__main__':
    try:
        manipulateData()
    except Exception as E:
        print(E)