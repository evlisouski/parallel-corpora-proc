
import opusfilter
import spacy
import re


class CustomSpellingFilter(opusfilter.FilterABC):

    score_direction = opusfilter.CLEAN_LOW

    def __init__(self, **kwargs):        
        self.nlp = spacy.load("ru_core_news_md")
        super().__init__(**kwargs)

    def check_spelling(self, sentence):
        if len(sentence) > 0:
            words_with_mistakes = []
            doc = self.nlp(sentence.lower())            
            for token in doc:
                if bool(re.match(r'^[а-яА-Яa-zA-Z]+$', token.text)):
                    if token.is_oov:                    
                        words_with_mistakes.append(token.text)
            return len(words_with_mistakes)
        return -1

    def score(self, pairs):
        for pair in pairs:
            yield [0, self.check_spelling(pair[1])]

    def accept(self, score):        
        return True if score[1] == 0 else False



from deeppavlov import build_model, configs

class CustomDeeppavlovSpellingFilter(opusfilter.FilterABC):

    score_direction = opusfilter.CLEAN_LOW

    def __init__(self, **kwargs):
        self.model = build_model('levenshtein_corrector_ru', download=True)
        self.nlp = spacy.load("ru_core_news_sm")
        super().__init__(**kwargs)

    def check_spelling(self, sentence):
        if len(sentence) > 0:
            words_with_mistakes = []
            doc = self.nlp(sentence.lower())          
            pavlov_result = self.model([sentence.lower()])[0]
            pavlov_doc = self.nlp(pavlov_result.lower())
            pavlov_doc_list_of_tokens_text = [token.text for token in pavlov_doc]
            for token in doc:
                if bool(re.match(r'^[а-яА-Яa-zA-Z]+$', token.text)):
                    if token.text not in pavlov_doc_list_of_tokens_text:             
                        words_with_mistakes.append(token.text)
            return len(words_with_mistakes)
        return -1

    def score(self, pairs):
        for pair in pairs:
            yield [0, self.check_spelling(pair[1])]

    def accept(self, score):        
        return True if score[1] == 0 else False