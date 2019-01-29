import json
from pprint import pprint
import re, nltk
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB
import numpy as np

with open('gg2013.json') as f:
    data = json.load(f)

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

name_map = {
'cecil b. demille award': 'cecil b demille',
'best motion picture - drama': 'best drama',
'best performance by an actress in a motion picture - drama': 'best actress drama',
'best performance by an actor in a motion picture - drama': 'best actor drama',
'best motion picture - comedy or musical': 'best comedy musical',
'best performance by an actress in a motion picture - comedy or musical': 'best actress comedy musical',
'best performance by an actor in a motion picture - comedy or musical': 'best actor comedy musical',
'best animated feature film': 'best animated',
'best foreign language film': 'best foreign',
'best performance by an actress in a supporting role in a motion picture': 'best supporting actress',
'best performance by an actor in a supporting role in a motion picture': 'best supporting actor',
'best director - motion picture': 'best director',
'best screenplay - motion picture': 'best screenplay',
'best original score - motion picture': 'best score',
'best original song - motion picture': 'best song',
'best television series - drama': 'best tv drama',
'best performance by an actress in a television series - drama': 'best actress tv drama',
'best performance by an actor in a television series - drama': 'best actor tv drama',
'best television series - comedy or musical': 'best tv comedy musical',
'best performance by an actress in a television series - comedy or musical': 'best actress tv comedy musical',
'best performance by an actor in a television series - comedy or musical': 'best actor tv comedy musical',
'best mini-series or motion picture made for television': 'best tv',
'best performance by an actress in a mini-series or motion picture made for television': 'best actress tv',
'best performance by an actor in a mini-series or motion picture made for television': 'best actor tv',
'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'best supporting acress tv',
'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'best supporting actor tv'}

#-----------------------------------------------------------------------------------------------

def generate_pat(award):
    s = ""
    for w in award.split():
        s += w + ".*"
    return s[:-2]

host_pat = re.compile(" [Hh]ost")
pn2_pat= re.compile("[A-Z][a-z]+ [A-Z][a-z]+")
rt = re.compile("RT")
award_related_pat = re.compile("best.*actress.*drama.*tv")

host = []
award_related = []
all_proper_nouns = []


for d in data:
    t = d['text'].lower()
    if not rt.match(t):
        if award_related_pat.search(t):
            award_related.append(t)
        if host_pat.search(t):
            host.append(t)
            proper_nouns = pn2_pat.findall(t)
        else:
            proper_nouns = []
        for n in proper_nouns:
            all_proper_nouns.append(n)

pprint(award_related)
print(len(award_related))


# print(all_proper_nouns)
# print(Counter(all_proper_nouns).most_common(30))
# pprint(present)
# print(len(present))
