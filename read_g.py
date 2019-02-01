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
                   'best animated feature film', 'best foreign language film', 
                   'best performance by an actress in a supporting role in a motion picture', 
                   'best performance by an actor in a supporting role in a motion picture', 
                   'best director - motion picture', 'best screenplay - motion picture', 
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


#-----------------------------------------------------------------------------------------------

#first process everything
# unused
def tokenize2(str):
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
    
    #return set([x for x in re.sub("television", 'tv', unpunctuated).lower().split() if not len(x)<4])
def tokenize(str):
    str = str.lower()
    punctuation = re.compile(r'[^\w\s]')
    unpunctuated = re.sub(punctuation,'',str)

    return set([x for x in re.sub('tv', "television", unpunctuated).split() if not len(x)<4])

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

# print(classify('best supporting actor tv'))


#-----------------------------------------------------------------------------------------------


# # Make a set of all the words in OFFICIAL_AWARDS
# award_words = set()
# for a in OFFICIAL_AWARDS:
#     for w in tokenize(a):
#         if len(w) <= 3:pass
#         if w == "award": pass
#         else:
#             award_words.add(w)
#
#
# print(award_words)
# print(len(award_words))


#-----------------------------------------------------------------------------------------------

host_pat = re.compile(" [Hh]ost")
win_pat = re.compile("w[io]n|takes")
pn2_pat= re.compile("[A-Z][a-z]+ [A-Z]\S+")
rt = re.compile("rt")
award_related_pat = re.compile("best.*actress.*television.*drama")
act_pat = re.compile("act")

name_pattern = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
name_with_lower = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[a-z]*\b){1,2}(?:\s+[A-Z][a-z]*\b)+')
pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')

win = []

#append anything matching win_pat to win[]
for t in tweets:
    low = t.lower()
    if not rt.match(low):
        if win_pat.search(low):
            #punctuation = re.compile(r'[^\w\s]')
            win.append(t)


#create lists of all PN2s that show up in classified tweets, mapped to award names
all_win_pnouns = [[] for a in OFFICIAL_AWARDS]

for t in win:
    award = classify(t)
    if award:
        if act_pat.search(award):
            proper_nouns = pn2_pat.findall(t)
        else:
            proper_nouns = name_pattern.findall(t)
            proper_nouns += name_with_lower.findall(t)
        for n in proper_nouns:
            all_win_pnouns[OFFICIAL_AWARDS.index(award)].append(n)

correct = 0
for i in range(len(all_win_pnouns)):
    print(OFFICIAL_AWARDS[i])
    if Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['winner']:
        correct += 1
    else:
        print(Counter(all_win_pnouns[i]).most_common(5))  #aggregate PN lists using Counter and show top 3
    print(answers['award_data'][OFFICIAL_AWARDS[i]]['winner']) #pull from answer key
    print("------------------------------------------------")

#correct = 0
##print award name, top 3 predictions, then answer from answer key
#for i in range(len(all_win_pnouns)):
#    print(OFFICIAL_AWARDS[i])
#    print(Counter(all_win_pnouns[i]).most_common(3))  #aggregate PN lists using Counter and show top 3
#    print(answers['award_data'][OFFICIAL_AWARDS[i]]['winner']) #pull from answer key
#    print("------------------------------------------------")
#    if Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['winner']:
#        correct += 1
#
#print("Correctly extracting " + str(correct) + " of " + str(len(OFFICIAL_AWARDS)) + " awards")
#
#
#
#
## BELOW: finding hosts------------------------------------
##
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
