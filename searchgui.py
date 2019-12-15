import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
#import searchModel
import tkHyperlinkManager 
import webbrowser
import math
import sys
import time
from textblob import TextBlob
import metapy
import pytoml



class InL2Ranker(metapy.index.RankingFunction):
    """
    Create a new ranking function in Python that can be used in MeTA.
    """
    def __init__(self, some_param=1.0):
        self.c = some_param
        # You *must* call the base class constructor here!
        super(InL2Ranker, self).__init__()

    def score_one(self, sd):
        """
        You need to override this function to return a score for a single term.
        For fields available in the score_data sd object,
        @see https://meta-toolkit.org/doxygen/structmeta_1_1index_1_1score__data.html
        """
       

        
        tfn = sd.doc_term_count * math.log2(1.0 + (sd.avg_dl/sd.doc_size))
        r1 = sd.query_term_weight * (tfn/(tfn+self.c))
        r2 = math.log2((sd.num_docs+1)/(sd.corpus_term_count + 0.5))
        return r1*r2


class SearchGUI(tk.Tk):
            
	
    def popupmsg(self):
        self.popup = tk.Toplevel()
        self.popup.rowconfigure(0, weight = 1)
        self.content=StringVar()
        #self.label1 = ttk.Label(self.popup, text="Search Document by Term", font=self.NORM_FONT).grid(row=0,column=0)
        self.B1 = tk.Button(self.popup, text="Search By Term",command=self.btnClicked).grid(row=0,column=0)
        self.B2 = tk.Button(self.popup, text="Search by ID",command=self.btnClicked1).grid(row=1,column=0)
        #self.label2 = ttk.Label(self.popup, text="Search Document by ID", font=self.NORM_FONT).grid(row=1,column=0)
        self.e= Entry(self.popup)
        self.e.grid(column=1, row=0)
        self.e.width=30
        self.e.focus_set()
        self.e1= Entry(self.popup)
        self.e1.grid(column=1, row=1)
        self.e1.width=30
        self.e1.focus_set()
        self.txt = scrolledtext.ScrolledText(self.popup,width=40,height=10)
        self.txt.grid(column=0,row=2)
        self.txt.insert(INSERT,"")
        self.txt.insert(END, "")
        #self.txt.config(state=DISABLED)
        
        
        self.B3 = tk.Button(self.popup, text="Exit window",command=self.popup.destroy).grid(row=3,column=0)
        self.B4 = tk.Button(self.popup, text="Clear All",command=self.clearAll).grid(row=3,column=1)
       


    def sentiment(self):
        self.popup = tk.Toplevel()
        self.popup.rowconfigure(0, weight = 1)
        self.content=StringVar()
        #self.label1 = ttk.Label(self.popup, text=" Enter Document ID", font=self.NORM_FONT).grid(row=0,column=0)
        self.sentB2 = tk.Button(self.popup, text="Search by ID",command=self.btnSentiment).grid(row=1,column=0)
        self.e1= Entry(self.popup)
        self.e1.grid(column=1, row=1)
        self.e1.width=30
        self.e1.focus_set()
        self.txt = scrolledtext.ScrolledText(self.popup,width=40,height=10)
        self.txt.grid(column=0,row=2)
        self.txt.insert(INSERT,"")
        
        #self.txt.config(state=DISABLED)
        #self.B1 = tk.Button(self.popup, text="Search",command=self.btnSentiment).grid(row=1,column=1)
        self.B2 = tk.Button(self.popup, text="Last 10 Search Results",command=self.btnLast10).grid(row=3,column=1)
        self.B3 = tk.Button(self.popup, text="Exit window",command=self.popup.destroy).grid(row=3,column=0)
            
        
    def btnSentiment(self):
        print("run Sentiment...")
        idx = metapy.index.make_inverted_index('config.toml')
        try:
            
            idVal=int(self.e1.get().strip())
            messagebox.showinfo("Document",idx.metadata(idVal).get('content'))
        except:
            messagebox.showerror("Error", "Invalid Value")

    def btnLast10(self):
        print("get sentiment of last 10 results")
        
        self.hyperlink = tkHyperlinkManager.HyperlinkManager(self.txt)
        self.contents={}
        sentiment = ''
        for num, (d_id, _) in enumerate(self.top10):
            
            content = self.idx.metadata(d_id).get('content')
            self.id = d_id
            self.txt.insert(INSERT, 'ID')
            self.txt.insert(INSERT, d_id,self.hyperlink.add(self.clickLink))
            self.txt.insert(INSERT, ':- ')            
                        
            fb1 = content[0:150]
            b1 = TextBlob(fb1)

            if b1.sentiment.polarity > 0.0:
                sentiment = " :Positive"
            else:
                sentiment = " :Negative"                
            
            self.txt.insert(INSERT,content[0:150].encode('UTF-8'))
            self.txt.insert(INSERT, sentiment, self.hyperlink.add(self.clickLink))            
            self.txt.insert(INSERT,'\n')
                        
            self.contents[num]= content

    def load_ranker(self,cfg_file):
        return InL2Ranker(1.2)
        
    def clearAll(self):
        #print("I am here")
        self.txt.config(state=NORMAL)
        self.txt.delete('1.0',END)
        self.e.delete('0',END)
        self.e1.delete('0',END)
            
    def clickLink(self):
        
        print(self.hyperlink.text.tag_names(CURRENT))
        

    def btnClicked1(self):
        idx = metapy.index.make_inverted_index('config.toml')
        try:
            
            idVal=int(self.e1.get().strip())
            messagebox.showinfo("Document",idx.metadata(idVal).get('content'))
        except:
            messagebox.showerror("Error", "Invalid Value")
        
        
        
        
   
    def btnClicked(self):
        cfg = 'config.toml'
        print('Building or loading index...')
        self.idx = metapy.index.make_inverted_index(cfg)
        ranker = self.load_ranker(cfg)
        ev = metapy.index.IREval(cfg)

        with open(cfg, 'r') as fin:
             cfg_d = pytoml.load(fin)

        query_cfg = cfg_d['query-runner']
        if query_cfg is None:
            
            print("query-runner table needed in {}".format(cfg))
            sys.exit(1)

        start_time = time.time()
        top_k = 10
        query_path = query_cfg.get('query-path', 'queries.txt')
        query_start = query_cfg.get('query-id-start', 0)

        query = metapy.index.Document()
        print('Running queries')
        
        query.content(self.e.get().strip())
        #print(query.content())
        results = ranker.score(self.idx, query, top_k)
        self.top10 = results
        self.hyperlink = tkHyperlinkManager.HyperlinkManager(self.txt)
        self.contents={}
        
		
        for num, (d_id, _) in enumerate(results):
            
            content = self.idx.metadata(d_id).get('content')
            self.sentiment_content = content
            self.txt.insert(INSERT, 'ID')
            self.txt.insert(INSERT, d_id,self.hyperlink.add(self.clickLink))
            self.txt.insert(INSERT, ':- ')
            
            
            self.txt.insert(INSERT,content[0:150].encode('UTF-8'))
            
            self.txt.insert(INSERT,'\n')
            
            #print("{}. {}...\n".format(num + 1, content[0:250]))
            self.contents[num]= content
        
            
        self.txt.config(state=DISABLED)  


    def popupmsgDoc(self,d_id,idx):    
        self.popup1 = tk.Toplevel()
        self.popup1.rowconfigure(0, weight = 1)
        self.txtDoc = scrolledtext.ScrolledText(self.popup,width=40,height=10)
        self.txtDoc.grid(column=0,row=1)
        #self.txtDoc.insert(INSERT,self.idx.metadata(d_id).get('content'))
        print(self.idx.metadata(d_id).get('content'))
	
    def clicked1(self):
        self.popupmsg() 
        
        print("Search Document")

    def clicked2(self):
        self.sentiment()
        print("Sentiment Analysis")

    def clicked3(self):
         print("Topic Search")

    def clicked4(self):
        print("Exit")
        app.destroy()    
   
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.LARGE_FONT= ("Verdana", 12)
        self.NORM_FONT= ("Verdana", 10)
        self.SMALL_FONT= ("Verdana", 8)
        
        	
        # Create Labels
        self.wm_grid(1000,1000,5,5)
        self.label=tk.Label(self,text=" Title: Text Retrieval Options")
        self.button1= tk.Button(self, text='Search Document',command=self.clicked1)
        self.button2= tk.Button(self, text='Sentiment Analysis',command=self.clicked2)
        #self.button3= tk.Button(self, text='Topic Search',command=self.clicked3)
        self.button4= tk.Button(self, text='Exit',command=self.clicked4)
        self.label.grid(row=1,column=1)
        self.button1.grid(row = 3, column =1)
        self.button2.grid(row = 5, column =1)
        #self.button3.grid(row = 7, column =1)
        self.button4.grid(row = 9, column =1)
        self.top10 = None
        self.sentiment_content = None
        self.idx = None
       
     
  
app = SearchGUI()

app.mainloop()


        
