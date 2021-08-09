#!/bin/python3

import json
from ntwewy_types import Pin

blobs = {'loc': {}}

for fname in ['BadgeLvUpType', 'Badge', 'PsychicInfo', 'Psychic', 'EnemyData', 'GroupData']:
    with open(f"data/{fname}.txt", "r") as infile:
        blobs[fname] = json.load(infile)

for lang in ['en']:
    blobs['loc'][lang] = {}
    for fname in ['ItemNameBDG']:
        with open(f'loc/{lang}/{fname}.txt', 'r') as infile:
            blobs['loc'][lang][fname] = json.load(infile)

pin_data = blobs['Badge']['mTarget']
pins = {}
for blob in pin_data:
    p = Pin(blob)
    pins[p.number] = p

# Create structured Python classes w/ constructors taking json blob as input
# map sort ID => GameID, mID => internalID
# map enemies => their pin drops
# map pins => their icon file
# map map enemies => the encounters they show up in via internal ID => days

# TODO: find the file for mapping noise name to ID
# TODO: command line arg for specifying locale code (default "en" bc i am lazy)
# TODO: find the glue for mapping itemNameBDG to badge mIDs / itemIDs 
