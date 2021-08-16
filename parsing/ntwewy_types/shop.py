from .brand import Brand

class Shop:
    def __init__(self, data_blob, localization):
        self.__blob = data_blob
        self._ID = self.__blob['mId']
        self._brand = Brand(self.__blob['mBrand'])
        self._name_key = self.__blob['mName']
        self._name = {}
        self._category_key = self.__blob['mShopCategory']
        self._category = {}
        for lang, lang_strs in localization.items():
            self._name[lang] = lang_strs[self._name_key].content
            self._category[lang] = lang_strs[self._category_key].content
        self._type = self.__blob['mShopType'] # restaurant vs store?

        self.__items = []

    def add_item(self, item):
        self.__items.append(item)

    @property
    def ID(self):
        return self._ID

    @property
    def brand(self):
        return self._brand

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category
