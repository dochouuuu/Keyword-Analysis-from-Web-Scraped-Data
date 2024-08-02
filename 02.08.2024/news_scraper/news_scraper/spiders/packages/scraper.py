from newspaper import Source
from newspaper.mthreading import fetch_news
import threading

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

        for source in self.sources:
            print(f"Source {source.url}")
            for article in source.articles[:20]:
                article.parse()
                if article.publish_date is not None:
                    date_unprocessed = article.publish_date.strftime('%d-%m-%Y')
                    date = date_unprocessed[:11]
                else:
                    date = article.publish_date

                return [date, article.title, article.url, article.text]
                
                
#if __name__ == "__main__":
#    with open('urls_maintest.json', 'r') as input:
#        inputs = json.load(input)
#    source_urls = inputs
#    config = Config()
#    config.memoize_articles = False
#    crawler = NewsCrawler(source_urls)
#    crawler.build_sources()
#    crawler.crawl_articles()
#    crawler.extract_information()