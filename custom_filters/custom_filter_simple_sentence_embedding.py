"""Sentence embeddings"""

import opusfilter
from laserembeddings import Laser
from scipy.spatial.distance import cosine


class SimpleSentenceEmbeddingFilter(opusfilter.FilterABC):
    """Filtering based on multilingual sentence embeddings"""

    score_direction = opusfilter.CLEAN_HIGH
    accept_threshold = 0
    reject_threshold = 1 + 10**-6

    def __init__(self, source_lang='en', target_lang='ru', threshold=0.5, **kwargs):
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.threshold = threshold
        self.embedding_model = Laser()
        super().__init__(**kwargs)

    def _cosine_similarities(self, pair):
        """Calculate cosine similarities for the text"""
        source_text = pair[0]
        target_text = pair[1]
        source_text_embedding = self.embedding_model.embed_sentences(
            [source_text], lang=self.source_lang)[0]
        target_text_embedding = self.embedding_model.embed_sentences(
            [target_text], lang=self.target_lang)[0]
        similarity = 1 - cosine(source_text_embedding, target_text_embedding)
        return similarity

    def score(self, pairs):
        for pair in pairs:
            yield self._cosine_similarities(pair)

    def accept(self, score):        
        return True if score >= self.threshold else False
