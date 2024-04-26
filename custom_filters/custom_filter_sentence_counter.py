
import opusfilter
import spacy


class SentenceCounter(opusfilter.FilterABC):
    """
    This filter, is based on SpaCy. If the number of sentences
    in the source text is equal to the number of sentences in
    the target text, the filter will return True and the pair
    will be saved, otherwise the filter will return False and
    the pair will not be saved.
    """

    score_direction = opusfilter.CLEAN_LOW

    def __init__(self, spacy_model="xx_sent_ud_sm", **kwargs):
        """
        Initializes an object of the SentenceCounter.

        Args:
        - `spacy_model` (`str`): Name of the Spacy model for sentence processing.
        """

        self.nlp = spacy.load(spacy_model)
        super().__init__(**kwargs)

    def count_sentences(self, sentence: str) -> int:
        """
        Counts the number of sentences in a text.

        Args:
        - sentence (str): Text for counting sentences.
        Returns:
        - sentence_count (int): Number of sentences in the text.

        """
        if len(sentence) > 0:
            doc = self.nlp(sentence)
            sentences = list(doc.sents)
            sentence_count = len(sentences)
            return sentence_count
        return 0

    def score(self, pairs: iter) -> list:
        """
        Computes the score for each sentence pair.

        Args:
        - pairs (iter): Takes an iterator over tuples of parallel sentences.
        Yields:
        - score (list): Score object for each pair.

        """
        for pair in pairs:
            yield [self.count_sentences(sentence) for sentence in pair]

    def accept(self, score: list) -> bool:
        """
        Checks whether the number of sentences in the source
        and target texts are the same.

        Args:
        - score (list): score object for each pair.
        Returns:
        - accept (bool): Returns True if the number of sentences
        in the source and target text is the same, otherwise returns False
        """

        return True if score[0] == score[1] else False
