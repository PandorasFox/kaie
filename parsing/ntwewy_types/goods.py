class Trade:
    def __init__(self, blob, all_items):
        self.__blob = blob
        self._trade_id = self.__blob['mId']
        # self._items is a list of (itemID, quantity) needed for the trade ID
        self._items = zip([all_items[_id] for _id in self.__blob['mItem']], self.__blob['mItemCount'])

    @property
    def ID(self):
        return self._trade_id

    @property
    def items_needed(self):
        return self._items

class StoreItem:
    def __init__(self, blob, all_items, trades, shops):
        self.__blob = blob
        # mGoodsName and mReleaseParam are dead values (all empty string/0)
        self._ID = self.__blob['mId']
        self._item = all_items[self.__blob['mItem']]
        self._shop = shops[self.__blob['mShop']]
        self._price = self.__blob['mPrice']
        self._release_day = {
            'VIP': self.__blob['mReleaseVip'], # probably VIP level it is available at
            'Day': self.__blob['mReleaseDay'], # day 1-24 (0-23?), probably
            'Regular': self.__blob['mReleaseRegular'], # ??
            'Social Network': self.__blob['mReleaseSkill'] # food items via social network unlock
        }
        self._sort_num = self.__blob['mSortIndex']
        self._save_num = self.__blob['mSaveIndex']

        self._count = self.__blob['mItemCount'] # stock based on.... week?
        self._trade = self.__blob['mExchange']
        if self._trade == -1:
            self._trade = False
        else:
            self._trade = trades[self._trade]

        self._shop.add_item(self)

    @property
    def StoreItemID(self):
        return self._ID

    @property
    def PurchaseItemID(self):
        return self._item_id

    @property
    def item(self):
        return self._item

    @property
    def shop(self):
        return self._shop

    @property
    def price(self):
        return self._price

    @property
    def availability(self):
        return self._release_day

    @property
    def trade(self):
        return self._trade
