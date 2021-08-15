from .brand import Brand

class Shop:
    def __init__(self, data_blob, localization):
        self.__blob = data_blob
        self._ID = self.__blob['mId']
        self._brand = Brand(self.__blob['mBrand'])
        self._name = localization[self.__blob['mName']]
        self._category = localization[self.__blob['mShopCategory']]
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
