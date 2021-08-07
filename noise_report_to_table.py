import json
import sys

with open('noise_report.json', 'r') as infile:
    noise_report = json.load(infile)

try:
    days_mode = (sys.argv[1] == 'days')
except IndexError:
    days_mode = False

outfile_name = f'reports/noise_report{"_days" if days_mode else ""}.md'
with open(outfile_name, 'w') as outfile:
    if days_mode:
        outfile.write('|Noise#|Days Available|\n')
        outfile.write('| :--: | :----------: |\n')
    else:
        outfile.write('|Noise#|Days Available|Easy|Normal|Hard|Ultimate|\n')
        outfile.write('| :--: | :----------: |:--:| :--: |:--:| :----: |\n')


    for num, noise in noise_report.items():
        outfile.write(f'|{num}|{noise["days"]}|')
        if not days_mode:
            for difficulty in ['easy', 'normal', 'hard', 'ultimate']:
                if type(noise['pins']) == str:
                    pin = noise['pins']
                    rate = noise['odds']
                else:
                    pin = noise['pins'][difficulty]
                    rate = noise['odds'][difficulty]
                outfile.write(f'{pin} @ {rate}%|')
        outfile.write('\n')
