Twitter Sentiment Analysis and Search
Definitions
Document– a single line of text in the text data file derived from the twitter data.
query - a search query which can have multiple words / terms;
term – a single word in a query.
Goal
Given a set of data about 5 different products/services,  implement a tf*idf index in memory which does the following:
Read English text data into the index;
For a given query, output the top 10 results ranked by their tf*idf scores.
Data
cranfield.dat – This file contains public reviews on 5 topic including Health, beauty, technology, news and sports. Each line in the document represents one review.
Code
The solution is written in python using the modules metapy,tweepy, tkinter,and tkhyperlinkmanager. TKinter is used to design the front end of the application, which receives the input query from the user. The Metapy module is used for the index creation and scoring the documents. 
Contents:
lsearchgui.py: Module containing search implementation
cranfield/cranfield.dat- contaIns the data set derived from twitter.
Running the application
$ searchgui.py
Comments
The current implementation proposes a general framework for indexing and ranking documents. 
The query is input into the application via the user screen. The relevant documents are scored and ranked and the output is the top 10 documents, displayed in the text area. Once the documents are retrieved, it is also possible to pull one particular document based on the index to view the complete document content. 
