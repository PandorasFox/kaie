from collections import defaultdict

class LocaleError(Exception):
    """Exception raised when trying to access a field not available in locale"""
    def __init__(self, lang, needed_lang):
        # TODO: dict of {lang => error message}
        # The locale error should probably be localized itself :)
        super().__init__(
                f"This field is only available in {needed_lang} locale, but "\
                f"blob is of locale {lang}.")

class Locale:
    def __init__(self, blob, lang):
        self._lang = lang
        if blob is None:
            # make the 'no string' locale entry
            blob = defaultdict(str)
            blob['name'] = 'Com_Blank'

        self.__blob = blob
        self._name = blob['name']
        self._content = blob['content']
        # presumably only used in voice cutscene blobs
        self._listener = blob['listener']
        self._speaker = blob['speaker']
        # only in ja loc files (as far as I know)
        if self._lang == 'ja':
            self._extra = blob['extra']
            self._annotation = blob['annotation']

    @property
    def lang(self):
        return self._lang

    @property
    def name(self):
        return self._name

    @property
    def content(self):
        return self._content

    @property
    def listener(self):
        return self._listener

    @property
    def speaker(self):
        return self._speaker

    @property
    def extra(self):
        if self._lang == 'ja':
            return self._extra
        raise LocaleError(self._lang, 'ja')
    
    @property
    def annotation(self):
        if self._lang == 'ja':
            return self._annotation
        raise LocaleError(self._lang, 'ja')
