#!/bin/python3
import json
from ntwewy_types import *

LOCALES = ['de', 'en', 'es', 'fr', 'it', 'ja']
DATA_FILES = ['AllItems', 'BadgeLvUpType', 'Badge', 'BattleCharacter',
        'Book', 'Costume', 'Department', 'EnemyData', 'EnemyReport', 'Food',
        'GoodsExchange', 'GroupData', 'Music', 'Psychic', 'SecretReport',
        'Shop', 'ShopGoods', 'Tips']
LOC_ITEMS = ['BDG', 'EQU', 'ETC', 'FOD']
LOC_ITEM_STEMS = ['ItemInfo', 'ItemName']
LOC_ITEM_NAMES = [f'{stem}{leaf}' for leaf in LOC_ITEMS for stem in LOC_ITEM_STEMS]
LOC_NOISE = [f'{stem}{leaf}'
        for stem in ['Ability', 'Chara', 'Enemy', 'Psychic']
        for leaf in ['Name', 'Info']]
LOC_IRREGULAR = ['BrandName', 'LocationName', 'MusicName', 'SReportText']
LOC_FILES = [f for lst in [LOC_ITEM_NAMES, LOC_NOISE, LOC_IRREGULAR] for f in lst]
class NTWEWYParser:
    def __init__(self):
        self.parsed = False

    def load_blobs(self):
        blobs = {'loc': {}, 'data': {}}

        for fname in DATA_FILES:
            with open(f'data/{fname}.txt', 'r') as infile:
                blobs['data'][fname] = json.load(infile)['mTarget']

        for lang in LOCALES:
            blobs['loc'][lang] = {}
            for fname in LOC_FILES:
                with open(f'loc/{lang}/{fname}.txt', 'r') as infile:
                    blobs['loc'][lang][fname] = json.load(infile)

        return blobs

    def _parse_locale(self, blobs):
        loc_data = {}
        self.localization = {} # {lang => {KEY: obj}}, where KEY is 'name' in blob
        for lang in LOCALES:
            loc_data[lang] = {}
            self.localization[lang] = {}
            for f in blobs['loc'][lang]:
                loc_data[lang][f] = blobs['loc'][lang][f]['columns']
                self.localization[lang]['Com_Blank'] = Locale(None, lang)
                for entry in loc_data[lang][f]:
                    self.localization[lang][entry['name']] = Locale(entry, lang)

    def parse_blobs(self, blobs):
        if self.parsed:
            return
        self._parse_locale(blobs)
        all_items_data = {itm['mId']:itm for itm in blobs['data']['AllItems']}
        noise_report_data = {itm['mEnemydata']:itm for itm in blobs['data']['EnemyReport']}


        book_data = blobs['data']['Book']
        tips = {blob['mId']: blob for blob in blobs['data']['Tips']}
        secrets = {blob['mId']: blob for blob in blobs['data']['SecretReport']}
        self.books = {'id': {}, 'num': {}}
        for blob in book_data:
            b_id = Item(blob, 1).itemID
            loc_info = all_items_data[b_id]
            b = Book(blob, tips, secrets, loc_info, self.localization)
            self.books['id'][b.ID] = b
            self.books['num'][b.number] = b

        cd_data = blobs['data']['Music']
        self.discs = {'id': {}, 'num': {}}
        for blob in cd_data:
            cd_id = Item(blob, 2).itemID
            loc_info = all_items_data[cd_id]
            cd = CD(blob, loc_info, self.localization)
            self.discs['id'][cd.ID] = cd
            self.discs['num'][cd.number] = cd

        pin_data = blobs['data']['Badge']
        self.pins = {'id': {}, 'num': {}}
        for blob in pin_data:
            pin_id = Item(blob, 3).itemID
            loc_info = all_items_data[pin_id]
            p = Pin(blob, loc_info, self.localization)
            self.pins['id'][p.ID] = p
            self.pins['num'][p.number] = p

        thread_data = blobs['data']['Costume']
        self.threads = {'id': {}, 'num': {}}
        for blob in thread_data:
            thread_id = Item(blob, 4).itemID
            loc_info = all_items_data[thread_id]
            t = Thread(blob, loc_info, self.localization)
            self.threads['id'][t.ID] = t
            self.threads['num'][t.number] = t

        food_data = blobs['data']['Food']
        self.noms = {'id': {}, 'num': {}}
        for blob in food_data:
            food_id = Item(blob, 5).itemID
            loc_info = all_items_data[food_id]
            f = Food(blob, loc_info, self.localization)
            self.noms['id'][f.ID] = f
            self.noms['num'][f.number] = f

        all_items = {v.itemID: v
                for table in [self.books, self.discs, self.pins, self.threads, self.noms]
                for v in table['num'].values()}

        shop_data = blobs['data']['Shop']
        self.shops = {}
        for blob in shop_data:
            shop = Shop(blob, self.localization)
            self.shops[shop.ID] = shop

        trade_data = blobs['data']['GoodsExchange']
        self.trades = {}
        for blob in trade_data:
            trade = Trade(blob, all_items)
            self.trades[trade.ID] = trade

        sale_data = blobs['data']['ShopGoods']
        self.items_for_sale = {}
        for blob in sale_data:
            sale = StoreItem(blob, all_items, self.trades, self.shops)
            if sale.item.itemID in self.items_for_sale:
                self.items_for_sale[sale.item.itemID].append(sale)
            else:
                self.items_for_sale[sale.item.itemID] = [sale]

        noise_data = blobs['data']['EnemyData']
        self.noise = {'id': {}, 'num': {}, 'no_num': {}}
        for blob in noise_data:
            try:
                report_blob = noise_report_data[blob['mId']]
            except KeyError:
                # there are a lot of noise EnemyData that are not in the report
                # presumably unkillable plague noise, w3d8 enemies, mr mews, etc.
                n = Noise(blob, self.pins['id'])
                self.noise['id'][n.ID] = n
                self.noise['no_num'][n.ID] = n
            else:
                n = Noise(blob, self.pins['id'], report_blob, self.localization)
                self.noise['id'][n.ID] = n
                self.noise['num'][n.number] = n
        self.parsed = True

# TODO: map enemies => the encounters they show up in via internal ID => days
# TODO: parse pin evolution data (already in badge.txt lol)
# -- probably add a method to Pin for remapping evolution ID to Pin obj after
# -- pin map is constructed (e.g. replace int ID with Pin obj)
# TODO: general pig noise stuff (need to add to repo)
ntwewy = NTWEWYParser()
blobs = ntwewy.load_blobs()
ntwewy.parse_blobs(blobs)

if __name__ == '__main__':
    print('Parsing files complete.\n'\
            'Available vars: blobs, ntwewy\n'\
            'Get started: poke at ntwewy.pins["num"][1] and ntwewy.noise["num"][1] :)\n'\
            'Dropping to an interpreter...')
    try:
        import code, readline, rlcompleter
        readline.parse_and_bind("tab: complete")
    except:
        # shitty interp with no tab complete, shrug
        print('  No tab complete available :(')
    interp = code.InteractiveConsole(locals=locals())
    interp.interact(banner='')
