import json
from pprint import pprint

with open('gg2015.json') as f:
    data = json.load(f)

for d in data[0:300]:
    pprint(d['text'])
