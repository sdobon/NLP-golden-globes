import json
from pprint import pprint

with open('gg2015.json') as f:
    data = json.load(f)

pprint(data[0:5])
