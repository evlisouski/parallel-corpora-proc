import opusfilter
import requests


class LanguageToolAPI(opusfilter.FilterABC):
    """
    The `LanguageToolAPI` filter is designed to check grammar,
    spelling, and syntax using the LanguageTool API.

    Attributes:
    - `score_direction`: Indicates the filtering direction, where a low level
    is considered "clean". Default value: `opusfilter.CLEAN_LOW`.

    Methods:
        - `__init__(self, url='<http://127.0.0.1:8010/v2/check>', **kwargs)`:
    Class constructor, accepts the following arguments:
        - `url`: URL address to access the LanguageTool API. Default value:
        `'<http://127.0.0.1:8010/v2/check'`>.
        - `**kwargs`: Additional arguments passed to the parent class
    constructor `opusfilter.FilterABC`.
        - `check_text(self, text)`: Checks a text for errors using
    the LanguageTool API. Accepts the argument `text`, the text to be
    checked. Returns `True` if the text contains no errors,
    and `False` otherwise.
        - `score(self, pairs)`: Computes a score for each text-error pair
    in the `pairs` list. Accepts the argument `pairs`, a list of text-error
    pairs. Returns a generator that yields the score for each pair in the form
    `[0, check_text(pair[1])]`, where `pair[1]` is the text
    with an error.
        - `accept(self, score)`: Determines whether to accept or reject the
    pair.
    """

    score_direction = opusfilter.CLEAN_LOW

    def __init__(self, url='http://127.0.0.1:8010/v2/check', **kwargs):
        """
        Args:
            `url` (str): URL to the API of the LanguageTool server.
        Defaults to 'http://127.0.0.1:8010/v2/check'.
        """
        
        self.url = url
        super().__init__(**kwargs)

    def check_text(self, text: str) -> bool:
        """
        Checks the text for errors using the LanguageTool API.

        Args:
        - `text`: The text to be checked.

        Returns: 
        - `True` if the text contains no errors, otherwise `False`.
       
        """
        url = self.url
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'text': f'{text}',
            'language': 'ru-RU',
            'enabledOnly': 'false'
        }
        response = requests.post(url, headers=headers, data=data)
        result = response.json()
        return False if result['matches'] else True

    def score(self, pairs) -> list:
        for pair in pairs:
            yield [0, self.check_text(pair[1])]

    def accept(self, score) -> bool:
        return score[1]
