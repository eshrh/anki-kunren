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

    @classmethod
    def _create_from_filename(cls, filename):
        '''
        Alternate constructor that uses a KanjiVG filename; used by
        get_all().
        >>> k = KanjiVG._create_from_filename('00061.svg')
        >>> k.character
        'a'
        '''
        m = re.match('^([0-9a-f]*)-?(.*?).svg$', filename)
        return cls(chr(int(m.group(1), 16)), m.group(2))

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

    @property
    def character_filename(self):
        '''
        An SVG filename that uses the unicode character
        >>> k = KanjiVG('漢')
        >>> print(k.character_filename)
        漢.svg
        '''
        if not self.variant:
            return '%s.svg' % self.character
        else:
            return '%s-%s.svg' % (self.character, self.variant)

    @classmethod
    def get_all(cls):
        '''
        Returns a complete list of KanjiVG objects; everything there is
        data for
        >>> kanji_list = KanjiVG.get_all()
        >>> kanji_list[0].__class__.__name__
        'KanjiVG'
        '''
        kanji = []
        for file in os.listdir(source_directory):
            kanji.append(cls._create_from_filename(file))
        return kanji

