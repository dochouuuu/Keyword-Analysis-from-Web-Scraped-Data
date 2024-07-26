import newspaper

article = newspaper.article('https://vov.vn/chinh-tri/tong-bi-thu-la-nguoi-tao-niem-tin-cho-nhan-dan-viet-nam-o-trong-va-ngoai-nuoc-post1109750.vov')
print(article.is_valid_url())
print(article.is_media_news())
print(article.is_valid_body())
