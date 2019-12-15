# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 20:41:10 2019

@author: TechM User
"""
import tweepy

auth = tweepy.OAuthHandler("xLkZXvpPfdt312O4AWhJZ7nDO", "98aKw4N5rt965hGfkVPqtb6rIBt2P7AE8lNOqKqI2VrNMvi0iX")

auth.set_access_token("1199489241337741312-rudgr2a1BxwbVNOgwTbDLjmjx3aHRo", "oF54MFDdp6CsTSF7Yv1KpautaV8PDm1t1sI7JngNGXFv6")

api = tweepy.API(auth)

Number_of_tweets = 100
 
file = open('TrendingNews.log', 'w+', encoding="utf-8")
file1 = open('Health.log', 'w+', encoding="utf-8")
file2 = open('Sports.log', 'w+', encoding="utf-8")
file3 = open('Beauty.log', 'w+', encoding="utf-8")
file4 = open('Technology.log', 'w+', encoding="utf-8")


 
                    
i = 1000000 
for tweet in tweepy.Cursor(api.search, q="technology", lang="en").items(Number_of_tweets):
     file4.write(str(i) + "  " + f"{tweet.text.strip()}\n")
     i = i + 1

i = 1000000 
for tweet in tweepy.Cursor(api.search, q="beauty", lang="en").items(Number_of_tweets):
     file3.write(str(i) + "  " + f"{tweet.text.strip()}\n")
     i = i + 1

i = 1000000 
for tweet in tweepy.Cursor(api.search, q="sports", lang="en").items(Number_of_tweets):
     file2.write(str(i) + "  " + f"{tweet.text.strip()}\n")
     i = i + 1

i = 1000000 
for tweet in tweepy.Cursor(api.search, q="health", lang="en").items(Number_of_tweets):
     file1.write(str(i) + "  " + f"{tweet.text.strip()}\n")
     i = i + 1

i = 1000000 
for tweet in tweepy.Cursor(api.search, q="news", lang="en").items(Number_of_tweets):
     file.write(str(i) + "  " + f"{tweet.text.strip()}\n")
     i = i + 1



file4.close()
file3.close()
file2.close()
file1.close()
file.close()
       