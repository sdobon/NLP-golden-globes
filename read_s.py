import json
from pprint import pprint
import re, nltk
# m = re.search("Your number is <b>(\d+)</b>",
#       "xxx Your number is <b>123</b>  fdjsk")
# if m:
#     print m.groups()[0]

with open('gg2013.json') as f:
    data = json.load(f)

tweets = []

for d in data[0:5000]:
    tweets.append(d['text'])

pat = re.compile(" [Hh]ost")

host = []

for t in tweets:
    if pat.search(t):
        host.append(t)

pprint(host)
print(len(host))
