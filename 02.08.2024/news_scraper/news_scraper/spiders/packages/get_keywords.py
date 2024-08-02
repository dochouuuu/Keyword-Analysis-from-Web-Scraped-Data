from collections import Counter
import underthesea
import string
import math

class RAKE:


    def __init__(self, input_text):
        with open("vietnamese-stopwords.txt", 'r', encoding='utf-8') as file:
            stopwords = [line.strip() for line in file if line.strip()]
        self.stopwords = set(stopwords)
        self.text = input_text
        
    def _is_stopword(self, word):
        return word.lower() in self.stopwords or word in string.punctuation

    def _split_text(self, text):
        text = underthesea.text_normalize(text)
        text = underthesea.word_tokenize(text)
        return text

    def _extract_phrases(self, words):
        phrases = []
        current_phrase = []
        for word in words:
            if self._is_stopword(word):
                if current_phrase:
                    phrases.append(' '.join(current_phrase))
                    current_phrase = []
            else:
                current_phrase.append(word)
        if current_phrase:
            phrases.append(' '.join(current_phrase))
        return phrases

    def _score_phrases(self, phrases):
        word_freq = Counter()
        phrase_freq = Counter()

        for phrase in phrases:
            words = phrase.split()
            phrase_freq[phrase] += 1
            word_freq.update(words)
        
        scores = {}
        for phrase in phrase_freq:
            words = phrase.split()
            score = 0
            for word in words:
                score += word_freq[word]
            score /= len(words)  
            scores[phrase] = score * phrase_freq[phrase]  
        return scores

    def extract_keywords_from_text(self, text):
        words = self._split_text(text)
        phrases = self._extract_phrases(words)
        return self._score_phrases(phrases)
    
    def top_keywords(self):
        keywords = self.extract_keywords_from_text(self.text)
        ranked_keywords = sorted(keywords.items(), key=lambda item: item[1], reverse=True)
        main_words = []
        keyword_counts = math.floor(sum(not c.isspace() for c in self.text) / 180)
        for word_tuple in ranked_keywords[:keyword_counts]:
            main_words.append(word_tuple[0])
        return main_words

#rake = RAKE("""Tiếp bước Philippines, mới đây Indonesia thông báo có thể nhập khẩu đến 4,3 triệu tấn gạo trong năm nay, tăng 600.000 tấn so với kế hoạch ban đầu. Theo Reuters, trong cuộc họp trực tuyến ngày 22.7, ông Sarwo Edhy, Thư ký Cơ quan Lương thực Quốc gia Indonesia, cho biết: Sản lượng gạo mà quốc gia này sản xuất từ đầu năm đến tháng 8.2024 thấp hơn 9,52% so với cùng kỳ năm 2023. Trong tháng 6 vừa qua, giá gạo nội địa đã tăng khoảng 12% so với cùng kỳ năm trước do thời tiết nắng nóng. Trong 5 tháng đầu năm 2024, đất nước đông dân nhất Đông Nam Á với 270 triệu người đã phải nhập khẩu 2,2 triệu tấn gạo. Mục tiêu nhập khẩu năm nay là 3,6 triệu tấn, có thể tăng thêm khi cần thiết khi vụ thu hoạch bị ảnh hưởng vì thời tiết hoặc dịch bệnh. Mới đây, Cơ quan hậu cần quốc gia Indonesia (Bulog) thông báo mời thầu tháng 7 với số lượng nhập khẩu lên đến 320.000 tấn gạo trắng 5% tấm, tăng 20.000 tấn so với những tháng trước. Thời gian dự kiến nhận hàng từ tháng 8 - 9.2024. Đầu tháng này, nước nhập khẩu lớn nhất thế giới là Philippines cũng dự báo sản lượng gạo nhập khẩu lên tới 4,5 - 4,7 triệu tấn, tăng khoảng 500.000 tấn so với các dự báo trước đó. 6 tháng đầu năm 2024, tổng lượng gạo nhập khẩu của Philippines là 2,32 triệu tấn, tăng đến gần 25% so với cùng kỳ năm 2023. Cả Philippines và Indonesia đều là khách hàng truyền thống của hạt gạo Việt Nam vì thế, việc tăng nhập khẩu sẽ tác động mạnh đến giá gạo nội địa theo hướng tích cực.""")
#guh = rake.top_keywords




