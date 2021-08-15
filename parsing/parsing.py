#!/bin/python3
import code, json
from ntwewy_types import Pin, Noise, Locale, LocaleError

LOCALES = ['de', 'en', 'es', 'fr', 'it', 'ja']
DATA_FILES = ['BadgeLvUpType', 'Badge',  'Psychic', 'EnemyData', 'GroupData', 'EnemyReport', 'AllItems']
LOC_ITEMS = ['BDG', 'EQU', 'ETC', 'FOD']
LOC_ITEM_STEMS = ['ItemInfo', 'ItemName']
LOC_ITEM_NAMES = [f'{stem}{leaf}' for leaf in LOC_ITEMS for stem in LOC_ITEM_STEMS]
LOC_NOISE = [f'{stem}{leaf}' for stem in ['Ability', 'Chara', 'Enemy', 'Psychic'] for leaf in ['Name', 'Info']]
LOC_IRREGULAR = ['BrandName', 'LocationName', 'MusicName', 'SReportText']
LOC_FILES = [f for lst in [LOC_ITEM_NAMES, LOC_NOISE, LOC_IRREGULAR] for f in lst]

def read_blobs():
    blobs = {'loc': {}, 'data': {}}

    for fname in DATA_FILES:
        with open(f'data/{fname}.txt', 'r') as infile:
            blobs['data'][fname] = json.load(infile)

    for lang in LOCALES:
        blobs['loc'][lang] = {}
        for fname in LOC_FILES:
            with open(f'loc/{lang}/{fname}.txt', 'r') as infile:
                blobs['loc'][lang][fname] = json.load(infile)

    return blobs

def parse_locale(blobs):
    loc_data = {}
    localization = {} # {lang => {KEY: obj}}, where KEY is 'name' in blob
    for lang in LOCALES:
        loc_data[lang] = {}
        localization[lang] = {}
        for f in blobs['loc'][lang]:
            loc_data[lang][f] = blobs['loc'][lang][f]['columns']
            localization[lang]
            for entry in loc_data[lang][f]:
                localization[lang][entry['name']] = Locale(entry, lang)
    return localization

def parse_blobs(blobs):
    localization = parse_locale(blobs)
    all_items_data = {itm['mId']:itm for itm in blobs['data']['AllItems']['mTarget']}
    noise_report_data = {itm['mEnemydata']:itm for itm in blobs['data']['EnemyReport']['mTarget']}

    pin_data = blobs['data']['Badge']['mTarget']
    pins = {'id': {}, 'num': {}}
    for blob in pin_data:
        pin_id = blob['mItemId']
        loc_info = all_items_data[pin_id]
        p = Pin(blob, loc_info, localization)
        pins['id'][p.ID] = p
        pins['num'][p.number] = p

    noise_data = blobs['data']['EnemyData']['mTarget']
    noise = {'id': {}, 'num': {}, 'no_num': {}}
    for blob in noise_data:
        try:
            report_blob = noise_report_data[blob['mId']]
            n = Noise(blob, pins['id'], report_blob, localization)
            noise['id'][n.ID] = n
            noise['num'][n.number] = n
        except:
            # there are a lot of noise EnemyData that are not in the report
            # presumably unkillable plague noise, w3d8 enemies, mr mews, etc.
            n = Noise(blob, pins['id'])
            noise['id'][n.ID] = n
            noise['no_num'][n.ID] = n


    return pins, noise, localization

# TODO: map enemies => the encounters they show up in via internal ID => days
# TODO: parse pin evolution data (already in badge.txt lol)
# -- probably add a method to Pin for remapping evolution ID to Pin obj after
# -- pin map is constructed (e.g. replace int ID with Pin obj)
# TODO: parse shop data, match up to localization data
# TODO: parse the trade data (after shop data)
# TODO: enum of brands using brand locale
# TODO: general pig noise stuff (need to add to repo)
blobs = read_blobs()
pins, noise, localization = parse_blobs(blobs)

if __name__ == '__main__':
    print('Parsing files complete.\n'\
            'Available vars: blobs, pins, noise, localization\n'\
            'Get started: poke at pins["num"][1] and noise["num"][1] :)\n'\
            'Dropping to an interpreter...')
    try:
        import readline, rlcompleter
        readline.parse_and_bind("tab: complete")
    except:
        # shitty interp with no tab complete, shrug
        print('  No tab complete available :(')
    interp = code.InteractiveConsole(locals=locals())
    interp.interact(banner='')
