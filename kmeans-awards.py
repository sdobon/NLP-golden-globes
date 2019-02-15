from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

import re, json
from pprint import pprint
from collections import Counter

#------------------------------------------------------------

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

#---------------------------------------------------------------------------------

win_pat = re.compile("[Ww]in|[Ww]on |[Tt]akes|[Nn]omin|[Pp]resent|[In]ntrodu|[Cc]ongrat|[Bb]est ")
rt = re.compile("rt")

win = []
for t in tweets:
    low = t.lower()
    if not rt.match(low):
        if win_pat.search(low):
            #punctuation = re.compile(r'[^\w\s]')
            win.append(t)

# # pre-processing, you can type in each of the list names to see exactly what's being pulled out
# best_split = []
# for i in tweets:
#     split = re.compile(r'wins best').split(i)
#     if len(split) > 1:
#         best_split.append(split[1])
#
# end_split = []
# for i in best_split:
#     split = punctuation.split(i)
#     end_split.append(split[0])
#
# es2 = []
# for i in end_split:
#     split = re.compile(r'for').split(i)
#     es2.append(split[0])
#
# no_space = []
# for i in es2:
#     if len(i.split()) == 1:
#         pass
#     else : no_space.append(i.strip())
# words = []
# for i in no_space:
#     for j in i.split():
#         words.append(j.lower())

#--------------------------------------------------------------

vectorizer = TfidfVectorizer(use_idf=False, ngram_range=(1,5), max_features=50000)#, sublinear_tf=True)#, stop_words='english')

freq_vects = vectorizer.fit_transform(win)  #win

# true_k is the k-means number
true_k = 50
model = KMeans(n_clusters=true_k, n_jobs=1, max_iter=100, n_init=1)
labels = model.fit_predict(freq_vects)


catch = [[] for i in range(true_k)]

for l, t in zip(labels, win):
    catch[l].append(t)

awards = []

for c in Counter(labels).most_common(true_k):
    print(c)
    res = Counter(list(map(classify, catch[c[0]]))).most_common(5)
    print(res)
    if res[0][0] == None and len(res) > 1:
        awards.append(res[1][0])
    else:
        awards.append(res[0][0])
    print("#-------------------------------")
print(len(set(awards)))

pprint(awards)

print(len(vectorizer.get_feature_names()))
#
# pprint(win[:300])




# # you can uncomment the prints to see whats going on
# #print("Top terms per cluster:")
# order_centroids = model.cluster_centers_.argsort()[:, ::-1]
# terms = vectorizer.get_feature_names()
# ans = []
# for i in range(true_k):
#     #print("Cluster %d:" % i),
#     s = ''
#     # you can change the number '15' to change how many of the top words in each cluster to include
#     for ind in order_centroids[i, :15]:
#         #print(' %s' % terms[ind])
#         s += ' ' + terms[ind]
#     ans.append(s)
#
# ans2 = []
# # this step is just processing out the non-award related words by filtering through things that appear in no_space
# for i in ans:
#     t = ''
#     for j in i.split():
#         if j.lower() in words:
#             t += ' ' + j
#     ans2.append(t)
#
# answers += [classify(i) for i in ans2]
#
# print(answers)
