#taken from kanji-colorizer, and modified.

import os
from importlib.resources import open_text
class KanjiVG(object):

    def __init__(self, character, variant=''):
        self.character = character
        self.variant = variant
        data_path = os.path.join(os.path.dirname(__file__),'data')

        if self.variant is None:
            self.variant = ''
        try:
            with open(os.path.join(data_path,self.ascii_filename),'r',encoding="utf-8") as f:
                self.svg = f.read()
        except Exception as e:
            print(e)
            self.svg = 0

    @property
    def ascii_filename(self):
        '''
        An SVG filename in ASCII using the same format KanjiVG uses.
        >>> k = KanjiVG('漢')
        >>> k.ascii_filename
        '06f22.svg'
        May raise InvalidCharacterError for some kinds of invalid
        character/variant combinations; this should only happen during
        KanjiVG object initialization.
        '''
        try:
            code = '%05x' % ord(self.character)
        except TypeError as e:  # character not a character
            raise e
        if not self.variant:
            return code + '.svg'
        else:
            return '%s-%s.svg' % (code, self.variant)
