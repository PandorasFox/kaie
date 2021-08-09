#!/bin/python3

import json

blobs = {}

for fname in ['BadgeLvUpType', 'Badge', 'PsychicInfo', 'Psychic', 'EnemyData', 'GroupData']:
    with open(f"data/{fname}.txt", "r") as infile:
        blobs[fname] = json.load(infile)['mTarget']


# Create structured Python classes w/ constructors taking json blob as input
# map sort ID => GameID, mID => internalID
# map enemies => their pin drops
# map pins => their icon file
# map map enemies => the encounters they show up in via internal ID => days


