# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 15:30:11 2019

@author: georg
"""

# -*- coding: utf-8 -*-
import json
from pprint import pprint
import re, nltk
from collections import Counter

from answers import answers


with open('gg2013.json') as f:
    data = json.load(f)

tweets = []
for d in data:
    tweets.append(d['text'])

tweets = list(set(tweets))

OFFICIAL_AWARDS = ['cecil b. demille award', 
                   'best motion picture - drama', 
                   'best performance by an actress in a motion picture - drama', 
                   'best performance by an actor in a motion picture - drama', 
                   'best motion picture - comedy or musical', 
                   'best performance by an actress in a motion picture - comedy or musical', 
                   'best performance by an actor in a motion picture - comedy or musical', 
                   'best animated feature film', 
                   'best foreign language film', 
                   'best performance by an actress in a supporting role in a motion picture', 
                   'best performance by an actor in a supporting role in a motion picture', 
                   'best director - motion picture', 
                   'best screenplay - motion picture', 
                   'best original score - motion picture', 
                   'best original song - motion picture', 
                   'best television series - drama', 
                   'best performance by an actress in a television series - drama', 
                   'best performance by an actor in a television series - drama', 
                   'best television series - comedy or musical', 
                   'best performance by an actress in a television series - comedy or musical', 
                   'best performance by an actor in a television series - comedy or musical', 
                   'best mini-series or motion picture made for television', 
                   'best performance by an actress in a mini-series or motion picture made for television', 
                   'best performance by an actor in a mini-series or motion picture made for television', 
                   'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 
                   'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

host_pat = re.compile(" [Hh]ost")
win_pat = re.compile("w[io]n|takes")
pn2_pat= re.compile("[A-Z][a-z]+ [A-Z]\S+")
rt = re.compile("rt")
award_related_pat = re.compile("best")
act_pat = re.compile("act")
punctuation = re.compile(r'[^\w\s]')
name_pattern = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
name_with_lower = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[a-z]*\b){1,2}(?:\s+[A-Z][a-z]*\b)+')
pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')

# pre-processing, you can type in each of the list names to see exactly what's being pulled out
best_split = []
for i in tweets:
    split = re.compile(r'wins best').split(i)
    if len(split) > 1:
        best_split.append(split[1])

end_split = []
for i in best_split:
    split = punctuation.split(i)
    end_split.append(split[0])

es2 = []
for i in end_split:
    split = re.compile(r'for').split(i)
    es2.append(split[0])

no_space = []
for i in es2:
    if len(i.split()) == 1:
        pass
    else : no_space.append(i.strip())

important_words = []
for i in set(no_space):
    words = []
    for j in i.split():
        if len(j) > 3:
            words.append(j)
    important_words.append(words)
    
answers = []

# same functions from our other file
def tokenize(str):
    punctuation = re.compile(r'[^\w\s]')
    unpunctuated = re.sub(punctuation,'',str)
    processed = []
    for i in unpunctuated.lower().split():
        if len(i) < 4: pass
        else:
            processed.append(i)
            if i == "television": processed.append("tv")
            if i == "tv": processed.append("television")
            if i == "motion picture": processed.append("movie")
            if i == "movie": processed.append("motion picture")
    return set(processed)

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
        return sorted_awards[num_overlap.index(max(num_overlap))]  #grab the first (and thus shortest) award name that matches max(num_overlap) times
    else:
        return None
    
    
answers = [classify(i) for i in best_split]
print(len(set(answers)))    
