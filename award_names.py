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

# Remove retweets
texts = list(set(texts))


matches = [re.search(' host', text) for text in texts]
