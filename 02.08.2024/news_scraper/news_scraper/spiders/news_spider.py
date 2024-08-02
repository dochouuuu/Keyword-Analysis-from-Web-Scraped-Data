import scrapy
import newspaper

class NewsSpider(scrapy.Spider):
    name = 'news'
    start_urls = ['https://abcnews.go.com/elections']  # Replace with your target URLs

    def parse(self, response):
        # Extract URLs from the response and yield Scrapy Requests
        for href in response.css('a::attr(href)'):
            yield response.follow(href, self.parse_article)

    def parse_article(self, response):
        # Use Newspaper4k to parse the article
        article = newspaper.article(response.url, language='en', input_html=response.text)
        article.parse()
        article.nlp()

        # Extracted informationll
        yield {
            'url': response.url,
            'title': article.title,
        }


