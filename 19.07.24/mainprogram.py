from openai import OpenAI
import requests
from bs4 import BeautifulSoup
import json

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        soup = BeautifulSoup(response.content, 'html.parser')

        element = soup.find(itemprop='articleBody')

        if not element:
            return "unreadable - skipping"

        scraped_text = element.get_text(strip=True)

        # Write the result and URL to a text file for debugging
        '''with open('scraped_data.txt', 'w', encoding='utf-8') as f:
            f.write(f"URL: {url}\n")
            f.write(scraped_text)'''

        return scraped_text

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return "unreadable - skipping"


with open('urls.json', 'r') as file:
    data = json.load(file)
    urls = data['urls']

# Ensure you have your OpenAI API key and correct base URL
api_key = 'your-api-key'
base_url = 'http://localhost:1234/v1'

client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

for url in urls:
    scraped_content = scrape_website(url)

    if scraped_content == "unreadable - skipping":
        print(f"Skipping {url} due to unreadable content")
        continue    

    response = client.chat.completions.create(
            model= "TheBloke/NexusRaven-V2-13B-GGUF",
            messages =[ {"role": "system", "content": "Bạn là trợ lí ảo tóm tắt văn bản. Bạn sẽ tóm tắt văn bản một cách chích xác nhất có thể. Câu trả lời phải theo cấu hình [Ngày đăng: (DD/MM/YY);Tiêu đề: (Tiêu đề);Từ khóa: (từ khóa)]. Từ khóa không dài hơn 2 chữ cái. Tiêu đề không dài hơn 1 câu."},
                        {"role": "user", "content": "Tôi sẽ cho bạn 1 dây kí tự. Nó được thu thập từ 1 trang báo mạng. Tìm tiêu đề của bài báo, ngày đăng tin và từ khóa chính không dài hơn 16 kí tự. Bỏ qua những văn bản không liên quan.  văn bản: " + scraped_content}],
            temperature=0.3
        )
response_message = response.choices[0].message.content
print(response_message )

with open('finalres.txt', 'w', encoding='utf-8') as f:
    f.write(f"URL: {url}\n")
    f.write(response_message)
