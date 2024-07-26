import requests
from bs4 import BeautifulSoup

def get_news_site_urls():
    url = "https://vi.wikipedia.org/wiki/Danh_s%C3%A1ch_b%C3%A1o_%C4%91i%E1%BB%87n_t%E1%BB%AD_ti%E1%BA%BFng_Vi%E1%BB%87t"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    urls = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        if 'http' in href:
            urls.append(href)
    
    return urls

news_urls = get_news_site_urls()
for url in news_urls:
    print(url)

import json

with open('news_urls.json', 'w') as file:
    json.dump(news_urls, file)