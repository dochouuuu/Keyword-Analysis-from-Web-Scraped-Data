from openai import OpenAI

class extractor:
    edit1 = False
    edit2 = False
    def __init__(self, input_text:str, input_title:str):
        self.client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")
        self.text = input_text
        self.title = input_title

    def get_keywords_raw(self):
        completion = self.client.chat.completions.create(
            model="lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
            messages=[
                {"role": "system", "content": "You are a news article summarizer. You always provide well-reasoned answers that are both correct and helpful. Your answer must follow this syntax: [keyword_1, keyword_2, keyword_3, keyword_4, keyword_5] ."},
                {"role": "user", "content": f'''I will give you the text and title of an news article. Find the keyword of the article. Title: {self.title} Text: {self.text} '''}
            ],
        temperature=0.3,
        )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content

    def regex(self, string):
            if string.endswith('.'):
                self.edit1 = True
                
                
            if not (string.strip().startswith('[') and string.strip().endswith(']')):
                self.edit2 = True
                
            
            if string.find('_') != -1 :
                return False
    
            content = string[1:-1].strip()
            phrases = [phrase.strip() for phrase in content.split(',')]
            for phrase in phrases:
                if len(phrase.split()) > 3:
                    return False
            if len(phrases) > 6:
                return False
            return True
    

    def get_keywords(self):
        raw_res = self.get_keywords_raw()
        regex_res = self.regex(raw_res)
        while regex_res is False:
            raw_res = self.get_keywords_raw()
            regex_res = self.regex(raw_res)
        if self.edit1 == True:
            print("editted")
            raw_res = raw_res[:-1]
        if self.edit2 == True:
            raw_res = "[" + raw_res + "]"
            print("edited result:" + raw_res)            
            return raw_res
        else:
            print("final result:" + raw_res)
            return raw_res
    


'''text = "Tiếp bước Philippines, mới đây Indonesia thông báo có thể nhập khẩu đến 4,3 triệu tấn gạo trong năm nay, tăng 600.000 tấn so với kế hoạch ban đầu. Theo Reuters, trong cuộc họp trực tuyến ngày 22.7, ông Sarwo Edhy, Thư ký Cơ quan Lương thực Quốc gia Indonesia, cho biết: Sản lượng gạo mà quốc gia này sản xuất từ đầu năm đến tháng 8.2024 thấp hơn 9,52% so với cùng kỳ năm 2023. Trong tháng 6 vừa qua, giá gạo nội địa đã tăng khoảng 12% so với cùng kỳ năm trước do thời tiết nắng nóng. Trong 5 tháng đầu năm 2024, đất nước đông dân nhất Đông Nam Á với 270 triệu người đã phải nhập khẩu 2,2 triệu tấn gạo. Mục tiêu nhập khẩu năm nay là 3,6 triệu tấn, có thể tăng thêm khi cần thiết khi vụ thu hoạch bị ảnh hưởng vì thời tiết hoặc dịch bệnh. Mới đây, Cơ quan hậu cần quốc gia Indonesia (Bulog) thông báo mời thầu tháng 7 với số lượng nhập khẩu lên đến 320.000 tấn gạo trắng 5% tấm, tăng 20.000 tấn so với những tháng trước. Thời gian dự kiến nhận hàng từ tháng 8 - 9.2024. Đầu tháng này, nước nhập khẩu lớn nhất thế giới là Philippines cũng dự báo sản lượng gạo nhập khẩu lên tới 4,5 - 4,7 triệu tấn, tăng khoảng 500.000 tấn so với các dự báo trước đó. 6 tháng đầu năm 2024, tổng lượng gạo nhập khẩu của Philippines là 2,32 triệu tấn, tăng đến gần 25% so với cùng kỳ năm 2023. Cả Philippines và Indonesia đều là khách hàng truyền thống của hạt gạo Việt Nam vì thế, việc tăng nhập khẩu sẽ tác động mạnh đến giá gạo nội địa theo hướng tích cực."
title = "Gạo Việt gia tăng cơ hội khi Indonesia dự báo sẽ nhập đến 4,3 triệu tấn"
keyword = extractor(text,title)
keyword.get_keywords()'''