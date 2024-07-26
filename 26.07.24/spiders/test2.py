from newspaper import Source, Config
from newspaper.mthreading import fetch_news
import threading
import json
#import csv

class NewsCrawler:

    def __init__(self, source_urls, config=None):
        self.sources = [Source(url, config=config) for url in source_urls]
        self.articles = []

    def build_sources(self):
        # Multithreaded source building
        threads = [threading.Thread(target=source.build) for source in self.sources]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

    def crawl_articles(self):
        # Multithreaded article downloading
        self.articles = fetch_news(self.sources, threads=4)

    def extract_information(self):
        fields1 = ['catagory id', 'pub date', 'title', 'url']
        fields2 = ['id', 'keywords']
        savetofile1 = 'finalres_pt1.csv'
        savetofile2 = 'finalres_pt2.csv'

        for source in self.sources:
            print(f"Source {source.url}")
            for article in source.articles[:20]:
                article.parse()
                if article.publish_date is not None:
                    date_unprocessed = article.publish_date.strftime('%d-%m-%Y')
                    date = date_unprocessed[:11]
                else:
                    date = article.publish_date

                #with open('article_urls.txt', 'a', encoding= "UTF-8", newline='') as debug_file:
                #    debug_file.write(f"Date: {date}\n"+f"Title: {article.title}...\n"+ f"url: {article.url}...\n" +"-------------------------------\n")
                #print(f"Title: {article.title}")

                #res1 = {'catagory id': str(1), 'pub date' : date, 'title' : article.title, 'url': article.url}
                #with open(savetofile1, 'a', encoding= 'UTF-8', newline='') as savedata1:
                #    writer1 = csv.DictWriter(savedata1, fieldnames=fields1)
                #    writer1.writeheader
                #    writer1.writerow(res1)

                #res2 = {'id': str(1), 'keywords': 'test' }
                #with open(savetofile2, 'a', encoding= 'UTF-8', newline='') as savedata2:
                #    writer2 = csv.DictWriter(savedata2, fieldnames=fields2)
                #    writer2.writeheader
                #    writer2.writerow(res2)
                print(date)
                print(article.title)
                print(article.url)
                return [date, article.title, article.url, article.text]
                
                
if __name__ == "__main__":
    with open('urls_maintest.json', 'r') as input:
        inputs = json.load(input)
    source_urls = ["https://doanhnghiepvn.vn", "https://doanhnghiephoinhap.vn"]
    config = Config()
    config.memoize_articles = False
    crawler = NewsCrawler(source_urls)
    crawler.build_sources()
    crawler.crawl_articles()
    crawler.extract_information()