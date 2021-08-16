from enum import Enum
from .brand import Brand

class Item:
    class ItemType(Enum):
        UNDEF = 0
        BOOK  = 1
        CD = 2
        PIN   = 3
        THREAD = 4
        FOOD = 5

    def __init__(self, blob, t):
        self._item_type = t
        self._mId = blob['mId']
        self._item_id = blob['mItemId']
        self._number = blob['mSortIndex']
        try:
            self._sprite = blob['mBadgeSpriteName']
        except KeyError:
            self._sprite = blob['mUiSprite']

    def _bind_locale(self, loc_blob, loc_table):
        self._name_key = loc_blob['mName']
        self._info_key = loc_blob['mInfo']
        self._name = {}
        self._info = {}
        for lang, lang_strs in loc_table.items():
            self._name[lang] = lang_strs[self._name_key].content
            self._info[lang] = lang_strs[self._info_key].content

    @property
    def ID(self):
        return self._mId

    @property
    def item_type(self):
        return self._item_type.name

    @property
    def itemID(self):
        return self._item_id

    @property
    def number(self):
        return self._number

    def __lt__(self, other):
        return (self._item_type.value * 400 + self._number) < (other._number + other._item_type.value * 400)

    @property
    def sprite(self):
        return self._sprite

    @property
    def name(self):
        return self._name

    @property
    def info(self):
        return self._info

class Book(Item):
    def __init__(self, data_blob, tips_blobs, secrets_blobs, loc_blob, loc_table):
        super().__init__(data_blob, self.ItemType.BOOK)
        super()._bind_locale(loc_blob, loc_table)
        self.__data_blob = data_blob
        self._text = {lang: [loc_table[lang][key]
            for key in self.__data_blob['mText']] for lang in loc_table }
        try:
            sr_keys = secrets_blobs[self.__data_blob['mSecretId']]['mText']
        except KeyError:
            self._secret_report = False
        else:
            self._secret_report = {}
            for lang, lang_strs in loc_table.items():
                self._secret_report[lang] = [lang_strs[key] for key in sr_keys]

        try:
            tip = {k:v for k, v in tips_blobs[self.__data_blob['mTips']].items()
                    if k != 'mPageFileName' and type(v) == str}
        except KeyError:
            self._tips = False
        else:
            self._tips = {}
            self._tip_sprite = tips_blobs[self.__data_blob['mTips']]['mPageFileName']
            for lang, lang_strs in loc_table.items():
                # TODO: find loc file and add to parse?
                continue
                self._tips[lang] = {name: lang_strs[key] if key != '' else ''
                        for name, key in tip.items()}

class CD(Item):
    def __init__(self, data_blob, loc_blob, loc_table):
        super().__init__(data_blob, self.ItemType.BOOK)
        super()._bind_locale(loc_blob, loc_table)
        self.__data_blob = data_blob
        self._bgm = self.__data_blob['mBgm']

class Pin(Item):
    def __init__(self, data_blob, loc_blob, loc_table):
        super().__init__(data_blob, self.ItemType.PIN)
        super()._bind_locale(loc_blob, loc_table)
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

        self._brand = Brand(self.__data_blob['mBrand'])

        self._max_level = int(self.__data_blob['mMaxLevel'])
        self._growth_rate = int(self.__data_blob['mLevelUpRate'])
        # TODO: map to a growth rate Enum

        self._beat_drop_chance_name = self.__data_blob['mNameChance']
        self._beat_drop_chance_info = self.__data_blob['mInfoChance']

    @property
    def max_level(self):
        return self._max_level

    @property
    def brand(self):
        return self._brand

class Thread(Item):
    def __init__(self, data_blob, loc_blob, loc_table):
        super().__init__(data_blob, self.ItemType.THREAD)
        super()._bind_locale(loc_blob, loc_table)
        self.__data_blob = data_blob

        self._brand = Brand(self.__data_blob['mBrand'])
        self._hp = self.__data_blob['mHp']
        self._atk = self.__data_blob['mAttack']
        self._def = self.__data_blob['mDefence']
        self._req_style = self.__data_blob['mOpenSense']
        self._ability = self.__data_blob['mAbility'] # TODO: map to ability obj
        self._slot = self.__data_blob['mSlotType'] # TODO: map to enum

    @property
    def brand(self):
        return self._brand

    @property
    def hp(self):
        return self._hp

    @property
    def attack(self):
        return self._atk

    @property
    def defence(self):
        return self._def

    @property
    def style(self):
        return self._req_style

    @property
    def ability(self):
        return self._ability

    @property
    def slot(self):
        return self._slot

class Food(Item):
    def __init__(self, data_blob, loc_blob, loc_table):
        super().__init__(data_blob, self.ItemType.THREAD)
        super()._bind_locale(loc_blob, loc_table)
        self.__data_blob = data_blob

        self._hp = self.__data_blob['mHp']
        self._atk = self.__data_blob['mAttack']
        self._def = self.__data_blob['mDefence']
        self._style = self.__data_blob['mSense']

        self._calories = self.__data_blob['mStomach']
        self._taste = self.__data_blob['mTaste']
        # TODO: map to people (3 extra vals?)

    @property
    def hp(self):
        return self._hp

    @property
    def attack(self):
        return self._atk

    @property
    def defence(self):
        return self._def

    @property
    def style(self):
        return self._req_style

    @property
    def calories(self):
        return self._calories
