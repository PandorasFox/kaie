class Noise:
    def __init__(self, data_blob, pins, report_blob=None, localization=None):
        self.__data_blob = data_blob
        self.__report_blob = report_blob
        if report_blob and localization:
            self._weakness = report_blob['mWeak']
            self._isBoss = report_blob['mIsBoss']
            self._noise_icon = report_blob['mSymbolType']
            self._sprite = report_blob['mNoiseImagePath']

            self._report_num = report_blob['mSortIndex'] + 1 # zero-indexed!
            self._name_key = report_blob['mName']
            self._info_key = report_blob['mInfo']
            self._name = {}
            self._info = {}
            for lang, lang_strs in localization.items():
                self._name[lang] = lang_strs[self._name_key].content
                self._info[lang] = lang_strs[self._info_key].content
        else:
            self._name = None
            self._info = None
            self._weakness = None
            self._isBoss = None
            self._noise_icon = None
            self._report_num = None
            self._name_key = None
            self._info_key = None

        self._mId = int(self.__data_blob['mBaseParam'])
        self._exp = int(self.__data_blob['mExp'])
        self._pinxp = int(self.__data_blob['mBp'])
        self._drops = {diff: (pins[pin_id], rate)
                for diff, pin_id, rate in zip(
                    ['easy', 'normal', 'hard', 'ultimate'], # TODO: loc?
                    self.__data_blob['mDrop'],
                    self.__data_blob['mDropRate']
                )
        }
        self._level = int(self.__data_blob['mLevel'])
        self._days = set()


    @property
    def ID(self):
        return self._mId

    @property
    def number(self):
        return self._report_num
    
    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return self._info
    
    def __drops(self, diff=None):
        if not diff:
            return self._drops
        else:
            return self._drops.get(diff, None)
    
    @property
    def drops(self):
        return self.__drops()

    @property
    def easy(self):
        return self.__drops('easy')

    @property
    def normal(self):
        return self.__drops('normal')

    @property
    def hard(self):
        return self.__drops('hard')

    @property
    def ultimate(self):
        return self.__drops('ultimate')

    @property
    def symbol_sprite(self):
        return f"UI_NoiseSymbol_{self._noise_icon:02}.png"

    @property
    def sprite(self):
        return self._sprite

    def addDay(self, day):
        # TODO: enum of days
        # based off the enemyGroups data file days
        self._days.add(day)

