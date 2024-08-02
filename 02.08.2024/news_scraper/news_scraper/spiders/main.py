from newspaper import Source, Config
from newspaper.mthreading import fetch_news
from collections import Counter
from transformers import pipeline
import underthesea
import string
import math
import threading
import json
import csv
from packages import keywords_LLM, zeroshot, get_keywords

class NewsCrawler:

    def __init__(self, source_urls, config=None):
        self.sources = [Source(url, config=config) for url in source_urls]
        self.articles = []

    def build_sources(self):
        threads = [threading.Thread(target=source.build) for source in self.sources]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def crawl_articles(self):
        self.articles = fetch_news(self.sources, threads=4)

    def extract_information(self):
        article_id = 1

        fields1 = ['id', 'catagory id', 'pub date', 'title', 'url']
        fields2 = ['id', 'keywords']
        savetofile1 = 'finalres_pt1.csv'
        savetofile2 = 'finalres_pt2.csv'


        for source in self.sources:
            print(f"Source {source.url}")
            for article in source.articles[:400]:
                try: 
                    article.parse()
                except Exception as e:
                    print("Error "+str(e))
                    continue
                if article.publish_date is not None and article.title is not None:
                    date_unprocessed = article.publish_date.strftime('%d-%m-%Y')
                    date = date_unprocessed[:11]
                else:
                    continue                
                classifier = zeroshot.zero_shot_classify(article.text)
                #raker = get_keywords.RAKE(article.text)
                LLM = keywords_LLM.extractor(article.text, article.title)
                
                res1 = {'id': str(article_id),'catagory id': classifier.get_topic(), 'pub date' : date, 'title' : article.title, 'url': article.url}
                with open(savetofile1, 'a', encoding= 'UTF-8', newline='') as savedata1:
                    writer1 = csv.DictWriter(savedata1, fieldnames=fields1)
                    writer1.writeheader
                    writer1.writerow(res1)

                res2 = {'id': str(article_id), 'keywords': f'{str(LLM.get_keywords())}' }
                with open(savetofile2, 'a', encoding= 'UTF-8', newline='') as savedata2:
                    writer2 = csv.DictWriter(savedata2, fieldnames=fields2)
                    writer2.writeheader
                    writer2.writerow(res2)
                article_id += 1


with open('news_urls.json', 'r') as input:
    inputs = json.load(input)
source_urls = inputs
config = Config()
config.memoize_articles = False
config.browser_user_agent = 'Mozilla/5.0 (Linux; Linux i551 x86_64) Gecko/20130401 Firefox/51.0'
config.request_timeout = 10
crawler = NewsCrawler(source_urls)
crawler.build_sources()
crawler.crawl_articles()
crawler.extract_information()