import os
class KanjiVG(object):
    '''
    Class to create kanji objects containing KanjiVG data and some more
    basic qualities of the character
    '''
    def __init__(self, character, variant=''):
        '''
        Create a new KanjiVG object
        Either give just the character
        >>> k1 = KanjiVG('漢')
        >>> print(k1.character)
        漢
        >>> k1.variant
        ''
        Or if the character has a variant, give that as a second
        argument
        >>> k2 = KanjiVG('字', 'Kaisho')
        >>> print(k2.character)
        字
        >>> k2.variant
        'Kaisho'
        Raises InvalidCharacterError if the character and variant don't
        correspond to known data
        >>> k = KanjiVG('Л')
        Traceback (most recent call last):
            ...
        kanjicolorizer.colorizer.InvalidCharacterError: ('\\u041b', '')
        '''
        self.character = character
        self.variant = variant
        if self.variant is None:
            self.variant = ''
        try:
            with open(os.path.join("kanji", self.ascii_filename), 'r', encoding='utf-8') as f:
                self.svg = f.read()
        except Exception as e:
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
