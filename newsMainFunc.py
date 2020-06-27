# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 1:23:10 2020

@author: ARVIND KRISHNA
github: github.com/ArvindAROO
"""

import json
import newspaper
import re

# Set the limit for number of articles to download per website
LIMIT = 2
def scrapeNews():    
    data = {}
    data['newspapers'] = {}
    
    # Loads the JSON files with news sites
    with open('NewsPapers.json') as companyList:
        companies = json.load(companyList)
        
    count = 1
    
    # Iterate through each news company
    for company, value in companies.items():            
        # It uses the python newspaper library to extract articles
        print("Building site for ", company)
        paper = newspaper.build(value['link'], memoize_articles=False)
        newsPaper = {
            "link": value['link'],
            "articles": []
        }
        #noneTypeCount = 0
        for content in paper.articles:
            if count > LIMIT:
                break
            try:
                content.download()
                content.parse()
            except Exception as e:
                # getting any kind of 404 error, should noy stop the program altogether
                print(e)
                continue
            
            if content.publish_date is None:
                print(count, " Article has date of type None...")
                continue
                #the program is made to loop over again because the fact that it doesnot have a 
                #publishing date means it can be any type of content like ads, video pages etc. but not news article
                #thats why such are skipped for good
            article = {}
            article['title'] = content.title
            article['text'] = content.text
            article['link'] = content.url
            article['published'] = content.publish_date.isoformat()
            newsPaper['articles'].append(article)
            del article
            ##print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
            count += 1
        count = 1
        data['newspapers'][company] = newsPaper
    
    # Finally it saves the articles as a JSON-file.
    try:
        with open('scraped_articles.json', 'w') as JSONfile:
            json.dump(data, JSONfile)
            JSONfile.close()
            del data
    except Exception as e: 
        print(e)


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
# dependencies - json, newpaper module
def newsMain():
    scrapeNews()
    print("News mined")
    manipulateData()
    
if __name__ == '__main__':
    try:
        newsMain()
    except ModuleNotFoundError as noModule:
        print("Some dependencies are not properly installed", noModule)
    except Exception as E:
        print(E)
    