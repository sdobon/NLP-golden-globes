import json
from pprint import pprint
import re, nltk
from collections import Counter

from answers import answers

# from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
# from sklearn.naive_bayes import GaussianNB, MultinomialNB, ComplementNB
# import numpy as np

with open('gg2013.json') as f:
    data = json.load(f)

tweets = []
for d in data:
    tweets.append(d['text'])

tweets = list(set(tweets))

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']




# name_map = {
# 'cecil b. demille award': 'cecil b demille',
# 'best motion picture - drama': 'best drama',
# 'best performance by an actress in a motion picture - drama': 'best actress drama',
# 'best performance by an actor in a motion picture - drama': 'best actor drama',
# 'best motion picture - comedy or musical': 'best comedy musical',
# 'best performance by an actress in a motion picture - comedy or musical': 'best actress comedy musical',
# 'best performance by an actor in a motion picture - comedy or musical': 'best actor comedy musical',
# 'best animated feature film': 'best animated',
# 'best foreign language film': 'best foreign',
# 'best performance by an actress in a supporting role in a motion picture': 'best supporting actress',
# 'best performance by an actor in a supporting role in a motion picture': 'best supporting actor',
# 'best director - motion picture': 'best director',
# 'best screenplay - motion picture': 'best screenplay',
# 'best original score - motion picture': 'best score',
# 'best original song - motion picture': 'best song',
# 'best television series - drama': 'best tv drama',
# 'best performance by an actress in a television series - drama': 'best actress tv drama',
# 'best performance by an actor in a television series - drama': 'best actor tv drama',
# 'best television series - comedy or musical': 'best tv comedy musical',
# 'best performance by an actress in a television series - comedy or musical': 'best actress tv comedy musical',
# 'best performance by an actor in a television series - comedy or musical': 'best actor tv comedy musical',
# 'best mini-series or motion picture made for television': 'best tv',
# 'best performance by an actress in a mini-series or motion picture made for television': 'best actress tv',
# 'best performance by an actor in a mini-series or motion picture made for television': 'best actor tv',
# 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television': 'best supporting acress tv',
# 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television': 'best supporting actor tv'}

# def generate_pat(award):
#     s = ""
#     for w in award.split():
#         s += w + ".*"
#     return s[:-2]

#-----------------------------------------------------------------------------------------------

def tokenize(str):
    punctuation = re.compile(r'[^\w\s]')
    unpunctuated = re.sub(punctuation,'',str)
    return set(re.sub("television", 'tv', unpunctuated).split())

def award_length(a):
    words = set()
    for w in tokenize(a):
        if len(w) <= 3:pass
        if w == "award": pass
        else:
            words.add(w)
    return len(words)

sorted_awards = sorted(OFFICIAL_AWARDS, key=award_length)

# print([len(tokenize(a)) for a in sorted_awards])


# take the intersection of the tweet and each award, return the name with most matches. ties go to shortest award name (that's why it's sorted)
def classify(tweet):
    num_overlap = [len(tokenize(tweet).intersection(tokenize(a))) for a in sorted_awards]  #array that contains number of overlapping words, mapped to sorted_awards
    if max(num_overlap) > 1:  #if we're able to match more than one word
        return sorted_awards[overlap.index(max(num_overlap))]  #grab the first (and thus shortest) award name that matches max(num_overlap) times
    else:
        return None

print(classify('best supporting actor tv'))


#-----------------------------------------------------------------------------------------------


# Make a set of all the words in OFFICIAL_AWARDS
award_words = set()
for a in OFFICIAL_AWARDS:
    for w in tokenize(a):
        if len(w) <= 3:pass
        if w == "award": pass
        else:
            award_words.add(w)


print(award_words)
print(len(award_words))


#-----------------------------------------------------------------------------------------------

host_pat = re.compile(" [Hh]ost")
win_pat = re.compile("w[io]n")
pn2_pat= re.compile("[A-Z][a-z]+ [A-Z][a-z]+")
rt = re.compile("rt")
award_related_pat = re.compile("best.*actress.*television.*drama")

win = []

#append anything matching win_pat to win[]
for t in tweets:
    low = t.lower()
    if not rt.match(low):
        if win_pat.search(low):
            win.append(t)


#create lists of all PN2s that show up in classified tweets, mapped to award names
all_win_pnouns = [[] for a in OFFICIAL_AWARDS]

for t in win:
    award = classify(t)
    if award:
        proper_nouns = pn2_pat.findall(t)
        for n in proper_nouns:
            all_win_pnouns[OFFICIAL_AWARDS.index(award)].append(n)


#print award name, top 3 predictions, then answer from answer key
for i in range(len(all_win_pnouns)):
    print(OFFICIAL_AWARDS[i])
    print(Counter(all_win_pnouns[i]).most_common(3))  #aggregate PN lists using Counter and show top 3
    print(answers['award_data'][OFFICIAL_AWARDS[i]]['winner']) #pull from answer key
    print("------------------------------------------------")




# BELOW: finding hosts------------------------------------
#
# all_proper_nouns = []
# host = []

#
# for t in tweets:
#     if not rt.match(t):
#         if host_pat.search(t):
#             host.append(t)
#             proper_nouns = pn2_pat.findall(t)
#         else:
#             proper_nouns = []
#         for n in proper_nouns:
#             all_proper_nouns.append(n)
#
#
# # print(all_proper_nouns)
# # print(Counter(all_proper_nouns).most_common(30))
