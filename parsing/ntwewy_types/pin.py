class Pin:
    def __init__(self, data_blob, loc_info, localization):
        self.__data_blob = data_blob
        # values not exposed, but useful to add in the future when roping in more data:
        # * psychic, pyschic key (attack type?)
        # * attack, attack per level
        # * charge time, reboot time, boot time, changes per level to each (!)
        # * auto recover stuff
        # * sell price formula based on current level
        # * evolution info (need to research)
        # * "sort psychic" psych type/category?
        # * "rarity" uberpin/godpin?
        # * notably missing: affinity? is that PyschicKey??
        self._name_key = loc_info['mName']
        self._info_key = loc_info['mInfo']
        self._name = {}
        self._info = {}
        for lang, lang_strs in localization.items():
            self._name[lang] = lang_strs[self._name_key].content
            self._info[lang] = lang_strs[self._info_key].content
        
        # 'pin number' visible in game; may need adjusting +-1 
        # (or possibly more, if sortIndex is for the items page in general)
        self._pin_number = int(self.__data_blob['mSortIndex'])
        self._mId = int(self.__data_blob['mId'])
        self._mItemId = int(self.__data_blob['mItemId'])
        self._brand = self.__data_blob['mBrand']
        self._sprite = self.__data_blob['mBadgeSpriteName']
        # TODO: map to a brand enum
        # TODO: generate brand enum based on localization

        self._max_level = int(self.__data_blob['mMaxLevel'])
        self._growth_rate = int(self.__data_blob['mLevelUpRate'])
        # TODO: map to a growth rate Enum

        self._beat_drop_chance_name = self.__data_blob['mNameChance']
        self._beat_drop_chance_info = self.__data_blob['mInfoChance']

        # pass in interface for looking up pin name once available?
        # give pin name lookup the generator for generating these?

    def __lt__(self, other):
        return self._pin_number < other._pin_number

    @property
    def number(self):
        return self._pin_number

    @property
    def ID(self):
        return self._mId

    @property
    def itemID(self):
        return self._mItemId

    @property
    def max_level(self):
        return self._max_level
    
    @property
    def sprite(self):
        return self._sprite

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return self._info
