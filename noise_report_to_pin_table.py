from collections import defaultdict
import json
import sys

TIERS=['easy', 'normal', 'hard', 'ultimate']

with open('noise_report.json', 'r') as infile:
    noise_report = {int(k):v for k, v in json.load(infile).items()}

pins = { k:{diff:{} for diff in TIERS} for k in range(1,334)}

for num, noise in noise_report.items():
    if 48 <= num and num <= 57:
        continue
    for difficulty in TIERS:
        pin = noise['pins'][difficulty]
        pins[pin][difficulty][num] = noise['odds'][difficulty]

outfile_name = f'reports/pins.md'
with open(outfile_name, 'w') as outfile:
    outfile.write('|Pin #| Dropped By |\n')
    outfile.write('| :-: | :--------: |\n')
    for pin, pin_data in pins.items():
        # pin_data is {difficulty: {noise_num: percent_chance, ..}}
        outfile.write(f'|{pin}|')
        for diff in TIERS:
            entries = []
            for noise, chance in pin_data[diff].items():
                entries.append(f'{noise}: {chance:.2f}%')
            if len(entries) > 0:
                outfile.write(f'{diff}: ')
                outfile.write(', '.join(entries))
                outfile.write('<br />')
    outfile.write('|\n')
