from transformers import pipeline
import underthesea

class zero_shot_classify:
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    candidate_labels = ["Chính Trị", "Kinh Tế", "Thể Thao", "Showbiz/Giải trí", "Thế Giới", "Khác"]
    
    def __init__(self, input_text):
        self.text = underthesea.text_normalize(input_text)

    def get_topic(self):
        output = self.classifier(self.text, self.candidate_labels, multi_label=False)
        #print(output)
        first_label = output['labels'][0]
        type_id = str(self.candidate_labels.index(first_label) + 1)
        #print(first_label)
        #print(type_id)
        return type_id


#classifier = zero_shot_classify("sampletext")
#classifier.get_topic()