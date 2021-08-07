import json
with open('noise_report.json', 'r') as infile:
    noise_report = json.load(infile)

#print('|Noise#|Days Available|Easy|Normal|Hard|Ultimate|')
#print('| :--: | :----------: | :: | :--: | :: | :----: |')

print('|Noise#|Days Available|')
print('| :--: | :----------: |')

for num, noise in noise_report.items():
    print(f'|{num}|{noise["days"]}|', end="")
    #for difficulty in ['easy', 'normal', 'hard', 'ultimate']:
    #    if type(noise['pins']) == str:
    #        pin = noise['pins']
    #        rate = noise['odds']
    #    else:
    #        pin = noise['pins'][difficulty]
    #        rate = noise['odds'][difficulty]
    #    print(f'{pin} @ {rate}%', end='|')
    print('\n', end='')
