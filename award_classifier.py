import json
import nltk
import re
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

texts = list(set(texts))
    

def index_return(array):
    listofindices = []
    for i in range(len(array)):
        if array[i] != None:
            listofindices.append(i)
    return listofindices

OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

award_words = set()
for i in OFFICIAL_AWARDS:
    for j in i.split():
        if len(j) <= 3:pass 
        else:
            award_words.add(j)
            
matches = [re.search('win|won', text) for text in texts]
win_texts = []
l = index_return(matches)
for i in l:
    win_texts.append(texts[i])
matches = [re.search('best',text) for text in win_texts]
l = index_return(matches)
best_texts = []
for i in l:
    best_texts.append(win_texts[i])
    
test = best_texts[5]

def categorize(text):
    award_words_in_test = []
    for i in text.split():
        if i in award_words:
            award_words_in_test.append(i)
    
    max_sim_count = 0    
    count = 0
    max_count = 0
    for i in OFFICIAL_AWARDS:
        sim_count = 0
        words = set(i.split())
        for i in award_words_in_test:
            if i in words:
                sim_count += 1
        count+=1
        if sim_count > max_sim_count:
            max_sim_count = sim_count
            max_count = count
    return max_count - 1

categories = [categorize(i) for i in best_texts]

indices = []
for i in range(len(categories)):
    if categories[i] == 0:
        indices.append(i)
    
for i in indices:
    print(best_texts[i])
        


