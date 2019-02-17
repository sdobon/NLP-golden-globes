import json
import re, nltk
from nltk.corpus import stopwords
from imdb import IMDb
from collections import Counter
from pprint import pprint
from answers import answers

#Initial Stuff
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

#Functions
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

def classify(tweet): #take the intersection of the tweet and each award, return the name with most matches. ties go to shortest award name (that's why it's sorted)
    num_overlap = [len(tokenize(tweet).intersection(tokenize(a))) for a in sorted_awards]  #array that contains number of overlapping words, mapped to sorted_awards
    if max(num_overlap) > 1:  #if we're able to match more than one word
        return sorted_awards[num_overlap.index(max(num_overlap))]  #grab the first (and thus shortest) award name that matches max(num_overlap) times
    else:
        return None

#Patterns
pn2_pat= re.compile("[A-Z][a-z]+ [A-Z]\S+")
rt = re.compile("rt")
presenter_pat = re.compile("[Pp]resent|[Pp]resents|[Pp]resenting|[Pp]resenter|[Pp]resented|[Pp]resenter")

#Finding presenters
all_presenter_pnouns = [[] for a in OFFICIAL_AWARDS] #create lists of all PN2s that show up in classified tweets, mapped to award names
names = []
presenter = []
movie_db = imdb.IMDb()
for t in tweets: #append anything matching presenter_pat to presenter[]
    low = t.lower()
    if not rt.match(low):
        if (presenter_pat.search(low)):
            presenter.append(t)

for p in presenter:
      award = classify(p) #Recall: classify function returns None if no award matches
      if award: 
            found = pn2_pat.findall(p)
            for f in found:
                  if (movie_db.search_person(f) != []):
                        names.append(f)
            for n in names:
                  all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].append(n)

correct = 0
for i in range(len(all_presenter_pnouns)):
    print "Award: ", OFFICIAL_AWARDS[i]
    print "Our answer: ", (Counter(all_presenter_pnouns[i]).most_common(2))  #aggregate PN lists using Counter and show top 2
    print "Desired answer:", (answers['award_data'][OFFICIAL_AWARDS[i]]['presenters']) #pull from answer key