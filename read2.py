import json
import nltk
from nltk import word_tokenize
from nltk.text import Text

from pprint import pprint

raw = "the project gutenberg ebook is available for free. the fork is in the raw chicken"

tokens = word_tokenize(raw)

#d = Text(raw)

with open('gg2013.json') as f:
    data = json.load(f)

texts = []
for d in data:
    texts.append(d['text'])

z = ""
for t in texts:
    z += t
#
token = word_tokenize(z)

text = Text(token)

text.concordance("host")
