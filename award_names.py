import json
import nltk
import re
from nltk import word_tokenize
from nltk.text import Text
from pprint import pprint

with open('gg2013.json') as f:
    data = json.load(f)

texts = []
for d in data:
    texts.append(d['text'])

# Remove duplicates
texts = list(set(texts))

texts[0:100]
# for each i in texts[0:3]:
#     texts[i]split(u)

matches = [re.search('award', text) for text in texts]

for match in matches:
    if match != None:
        print match.group()

# print matches
# matches[0].group()
