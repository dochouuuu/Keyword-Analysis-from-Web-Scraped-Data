import newspaper
from packages import get_keywords, zeroshot

article = newspaper.article('https://thanhnien.vn/cac-tap-doan-dau-khi-cong-nghe-hang-dau-an-do-muon-dau-tu-vao-viet-nam-185240731182957907.htm')
print(article.title)
print(article.text)
classifier = zeroshot.zero_shot_classify(article.text)
raker = get_keywords.RAKE(article.text)
print(classifier.get_topic())
print({'keywords': f'{str(raker.top_keywords())}'})