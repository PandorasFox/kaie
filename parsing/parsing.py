#!/bin/python3

import json
from ntwewy_types import Pin, Noise

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
pins = {'id': {}, 'num': {}}
for blob in pin_data:
    p = Pin(blob)
    pins['id'][p.ID] = p
    pins['num'][p.number] = p

noise_data = blobs['EnemyData']['mTarget']
noise_report = {}
for noise in noise_data:
    n = Noise(noise, pins['id'])
    noise_report[n.ID] = n

# map map enemies => the encounters they show up in via internal ID => days

# TODO: find the file for mapping noise name to ID
# TODO: find the file for mapping noise report num to ID
# TODO: find the glue for mapping itemNameBDG to badge mIDs / itemIDs 
# TODO: command line arg for specifying locale code (default "en" bc i am lazy)
# TODO: grab all loc files once all necessary ones in en are all in use
