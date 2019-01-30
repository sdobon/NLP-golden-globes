import json
import nltk
import re
from nltk import word_tokenize
from nltk.text import Text
from pprint import pprint

name_pattern = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')


with open('gg2013.json') as f:
    data = json.load(f)

# Call our corpus of tweets as texts
texts = []
for d in data:
    texts.append(d['text'])

texts = list(set(texts))

# Remove punctuation from our corpus
punctuation = re.compile(r'[^\w\s]')
unpunctuated = [re.sub(punctuation,'',i) for i in texts]
    
# Helper function: input -> some array; output -> list of indices for array where entries are NOT None
def index_return(array):
    listofindices = []
    for i in range(len(array)):
        if array[i] != None:
            listofindices.append(i)
    return listofindices

# List of hard coded awards
OFFICIAL_AWARDS = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']

# Make a set of all the words in OFFICIAL_AWARDS
award_words = set()
for i in OFFICIAL_AWARDS:
    for j in i.split():
        if len(j) <= 3:pass 
        if j == "award": pass
        else:
            award_words.add(j)
            
# COMMENTED OUT - finds all the tweets that mention ("win" OR "won") AND "best"
#matches = [re.search('win|won', text) for text in texts]
#win_texts = []
#l = index_return(matches)
#for i in l:
#    win_texts.append(texts[i])
#matches = [re.search('best',text) for text in win_texts]
#l = index_return(matches)
#best_texts = []
#for i in l:
#    best_texts.append(win_texts[i])
    
# Categorize: input -> a line of text (tweet)
#             output -> a number which corresponds to the index of OFFICIAL_AWARDS
#                       for example, 1 corresponds to OFFICIAL_AWARDS[1] or "best motion picture - drama"
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
        for j in award_words_in_test:
            if j in words:
                sim_count += 1
        count+=1
        if sim_count > max_sim_count:
            max_sim_count = sim_count
            max_count = count
    return max_count - 1

categories = []
for i in unpunctuated:
    categories.append(categorize(i.lower()))
        
