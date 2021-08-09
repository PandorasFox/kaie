class Pin:
    def __init__(self, blob):
        self.__blob = blob
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

        self._pin_number = int(blob['mSortIndex']) # 'pin number' visible in game
        self._mId = int(blob['mId'])
        self._mItemId = int(blob['mItemId'])
        self._brand = blob['mBrand']
        self._sprite = blob['mBadgeSpriteName']
        # TODO: map to a brand enum
        # TODO: generate brand enum based on localization

        self._max_level = int(blob['mMaxLevel'])
        self._growth_rate = int(blob['mLevelUpRate'])
        # TODO: map to a growth rate Enum

        self._beat_drop_chance_name = blob['mNameChance']
        self._beat_drop_chance_info = blob['mInfoChance']

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
