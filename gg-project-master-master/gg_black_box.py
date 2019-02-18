from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score

from pprint import pprint
import re, nltk, json, sys
from collections import Counter

from nominees_data_and_functions import *

from answers import answers

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


def voodoo_magic(year, OFFICIAL_AWARDS):
    # reload(sys)
    # sys.setdefaultencoding('utf8')

    with open('gg%s.json'%year) as f:
        data = json.load(f)

    tweets = []
    for d in data:
        tweets.append(d['text'])

    tweets = list(set(tweets))




    results = {}
    results['award_data'] = {}
    for a in OFFICIAL_AWARDS:
        results['award_data'][a] = {}

    #------ Helper Functions --------------------------------------------------------------------------------------
    punctuation = re.compile(r'[^\w\s]')

    def tokenize(str):
        str = str.lower()
        unpunctuated = re.sub(punctuation,'',str)
        tv_sub = re.sub('tv', "television", unpunctuated)

        return set([x for x in tv_sub.split() if not len(x)<4])



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

    #---------- Award Names Helper Functions -----------------

    def get_top_ngrams(corpus, n=None):

        vec = CountVectorizer(ngram_range=(2,5)).fit(corpus)
        raw_freq = vec.transform(corpus)
        sum_words = raw_freq.sum(axis=0)
        words_freq = [(word, sum_words[0, idx]) for word, idx in vec.vocabulary_.items()]
        words_freq =sorted(words_freq, key = lambda x: x[1], reverse=True)
        return words_freq[:n]

    # corp = ["i love to code in python", "everyone loves to code in python", "well, people who don't know how to code don't"]
    # print(get_top_ngrams(corp, 2))

    def merge_overlap(a, b):
        c = a.split()
        d = b.split()
        if set(c) == set(d):
            return None
        if c[-1] == d[0]:
            final = c + d[1:]
        elif d[-1] == c[0]:
            final = d + c[1:]
        else:
            return None
        s = ''
        for w in final:
            s += w + ' '
        return s[:-1]

    # print(merge_overlap("best actor", "actor tv"))
    # print(merge_overlap("actor tv", "best actor"))

    def construct_name(lst):
        if len(lst) == 0:
            return None
        s = lst.pop(0)
        for ng in lst:
            merge = merge_overlap(s, ng)
            if merge:
                lst.remove(ng)
                return construct_name( [merge] + lst)
        return s

    def  best_to_front(lst):
        for s in lst:
            if s.split()[0] == 'best':
                pop = lst.pop(lst.index(s))
                return [pop] + lst
        return []


    # print(construct_name(['best supporting', 'supporting actor','best supporting actor', 'actor in', 'supporting actor in', 'in drama']))



    #-----------------------------------------------------------------------------------------------



    #-------- Compiled Regex Patterns ----------------------------------------------------------

    host_pat = re.compile(" [Hh]ost")
    win_pat = re.compile("w[io]n|takes")
    pn2_pat= re.compile("[A-Z][a-z]+ [A-Z]\S+")
    rt = re.compile("rt")
    award_related_pat = re.compile("best.*actress.*television.*drama")
    act_pat = re.compile("act")
    gg_pat = re.compile("GoldenGlobes|[Gg]olden [Gg]lobe")

    present_pat = re.complile("[Pp]resent")
    name_pattern = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
    name_with_lower = re.compile(r'\b[A-Z][a-z]*\b(?:\s+[a-z]*\b){0,2}(?:\s+[A-Z][a-z]*\b)+')
    pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')

    # test_pat = re.compile("test|best|actor|", re.IGNORECASE)
    # print(tokenize(re.sub(test_pat, '', "the Best friggin actor on tv")))

    # ----- Award names helper Functions -------------

    end_pat = re.compile(r' for | at | goes |http|@|\.|:|#|!|"')
    wins_best = re.compile(r'wins [Bb]est|for [Bb]est')
    for_pat = re.compile(r'for')

    #--------Generate paterns to remove award names from classfied tweets--------------------

    removal_patterns = []

    for a in OFFICIAL_AWARDS:
        pat_str = ""
        for w in tokenize(a):
            pat_str += w + "|"
        rem_pat = re.compile(pat_str[:-1], re.IGNORECASE)
        removal_patterns.append(rem_pat)


    #-------- Filtering ---------------------------------------------------------------------------

    win = []

    host = []

    best_split = []

    nominee = []

    present = []

    #append anything matching filter pats to their catching arrays
    for t in tweets:
        t = re.sub(gg_pat, '', t)
        # ---- award names -------------
        split = wins_best.split(t)
        if len(split) > 1:
            # print(split)
            best_split.append("best" + split[1])

        low = t.lower()
        if not rt.match(low):
            #----- winners -------------------
            if win_pat.search(low):
                win.append(t)
            #----- hosts ---------------------
            if host_pat.search(t):
                host.append(t)
            #----- nominees ---------------------
            if (nominee_pat.search(low) or win_pat.search(low)):
                #punctuation = re.compile(r'[^\w\s]')
                nominee.append(t)
            #------presenters------------------
            if present_pat.search(low):
                present.append(t)

    #--- additional award names cleaning ----------
    end_split = []
    for i in best_split:
        split = end_pat.split(i)
        # print(split)
        end_split.append(split[0])

    #------------- End Filtering ---------------------------------------------------------

    #------------- Extracting Presenters -----------------------------------------

    # #create lists of all PN2s that show up in classified tweets, mapped to award names
    # all_present_pnouns = [[] for a in OFFICIAL_AWARDS]
    #
    # for t in win:
    #     award = classify(t)
    #     # if award == OFFICIAL_AWARDS[13]:
    #     #     print(t)
    #     #     print(name_pattern.findall(t))
    #     #     print(name_with_lower.findall(t))
    #     #     print('-------------')
    #     if award:
    #         name_removed_t = re.sub(removal_patterns[OFFICIAL_AWARDS.index(award)], '', t)
    #         if act_pat.search(award):
    #             proper_nouns = pn2_pat.findall(name_removed_t)
    #         else:
    #             proper_nouns = name_pattern.findall(name_removed_t)
    #             proper_nouns += name_with_lower.findall(name_removed_t)
    #         for n in proper_nouns:
    #             all_present_pnouns[OFFICIAL_AWARDS.index(award)].append(n)
    #
    # for i in range(len(all_present_pnouns)):
    #     print(OFFICIAL_AWARDS[i])
    #     results['award_data'][OFFICIAL_AWARDS[i]]['presenters'] = Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()
    #     try:
    #         results['award_data'][OFFICIAL_AWARDS[i]]['nominees'].append(Counter(all_win_pnouns[i]).most_common(3)[0][0].lower())
    #     except:
    #         results['award_data'][OFFICIAL_AWARDS[i]]['nominees'] = Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()
    #     if Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['winner']:
    #         correct += 1
    #     else:
    #         print(Counter(all_win_pnouns[i]).most_common(5))  #aggregate PN lists using Counter and show top 3
    #     print(answers['award_data'][OFFICIAL_AWARDS[i]]['winner']) #pull from answer key
    #     print("------------------------------------------------")

    #------------- End Ectracting Presenters ---------------------------------------------------------

    #------------- Extracting Award Names -----------------------------------------

    vectorizer = TfidfVectorizer(use_idf=False, ngram_range=(1,5), max_features=50000)#, sublinear_tf=True)#, stop_words='english')

    freq_vects = vectorizer.fit_transform(end_split)  #win

    # true_k is the k-means number
    true_k = 35
    model = KMeans(n_clusters=true_k, n_jobs=1, max_iter=100, n_init=1)
    labels = model.fit_predict(freq_vects)


    clusters = [[] for i in range(true_k)]

    for l, t in zip(labels, end_split):
        clusters[l].append(t)

    awards = []

    for c in clusters:
        name = construct_name( best_to_front( [ng[0] for ng in get_top_ngrams(c, 10) if ng[1]>5] ) )
        # print(get_top_ngrams(c, 10))
        if name:
            awards.append(name)
            print(get_top_ngrams(c, 10))
            print(name)
            print("-----------------------")

    #-------- Lengthening award names --------
    # lengthen_pats = []
    #
    # for a in awards:
    #     tokens = a.split()
    #     pat_s = tokens[0] + '.*' + tokens[-1]
    #     lengthen_pats.append(re.compile(pat_s))
    #
    # for p, c, a in zip(lengthen_pats, clusters, awards):
    #     print("------------------------------------")
    #     print(len(c))
    #     # if len(c) < 30:
    #     #     print(c)
    #     print(a)
    #     print("------------------------------------")
    #     for t in c:
    #         t = t.lower()
    #         longer = re.findall(p, t)
    #         # if longer:
    #         #     print(longer)

    pprint(awards)
    print(len(set(awards)))
    results['award_names'] = awards
    #---------- End Extracting Award Names --------------------------------------

    #--------- Extracting Hosts ------------------------------------------------
    all_proper_nouns = []

    for t in host:
        proper_nouns = pn2_pat.findall(t)
        for n in proper_nouns:
            all_proper_nouns.append(n)

    # print(Counter(all_proper_nouns).most_common(30))
    most_common = Counter(all_proper_nouns).most_common(2)
    results['hosts'] = [most_common[0][0], most_common[1][0]]


    #--------- End Extracting Hosts ------------------------------------------------

    #--------- Extracting Nominees ------------------------------------------------

    # #create lists of all PN2s that show up in classified tweets, mapped to award names
    # all_nominee_pnouns = [[] for a in OFFICIAL_AWARDS]
    #
    # # Classify the nominee-related tweets by their awards, and
    # # infer the names in these same tweets
    # # movie = imdb.IMBd()
    # for t in nominee:
    #     # print t
    #     # print "\n"
    #     award = classify(t)
    #     # Recall: classify function returns None if no award matches
    #     if award:
    #         # if (t == "Connie Britton should have won best actress #GoldenGlobes"):
    #         #     print "AWARD: ", award
    #         # print "AWARD_RELATED TWEET"
    #         # print t
    #         # print "\n"
    #         # print award
    #         # print "\n"
    #         # print "\n"
    #         # print "Tweet: ", t
    #         # print "Award label: ", award
    #
    #         # if the award has to do with an actor / actress...
    #         if act_pat.search(award) or director_pat.search(award):
    #             proper_nouns = nominee_pat_1.findall(t)
    #             for n in proper_nouns:
    #                 n = n[8:]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_2.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:-14]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_3.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:-11]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_4.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:(n.find("did")-1)]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_5.findall(t)
    #             for n in proper_nouns:
    #                 n = n[7:-7]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_6.findall(t)
    #             for n in proper_nouns:
    #                 n = n[(n.find("been")+5):]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_7.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:(n.find("should")-1)]
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             if (all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]):
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)] = list(set(all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]))
    #
    #         # if the award doesn't have to do with an actor...
    #         else:
    #             proper_nouns = nominee_pat_8.findall(t)
    #             for n in proper_nouns:
    #                 n = n[8:]
    #                 if not unneeded_stuff.findall(n) and n != "It" and n != "That":
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_9.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:-14]
    #                 if not unneeded_stuff.findall(n) and n != "It" and n != "That":
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_10.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:-11]
    #                 if not unneeded_stuff.findall(n):
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_11.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:(n.find("did")-1)]
    #                 if not unneeded_stuff.findall(n) and n != "It" and n != "That":
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_12.findall(t)
    #             for n in proper_nouns:
    #                 n = n[7:-7]
    #                 if not unneeded_stuff.findall(n) and n != "It" and n != "That":
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_13.findall(t)
    #             for n in proper_nouns:
    #                 n = n[(n.find("been")+5):]
    #                 if not unneeded_stuff.findall(n) and n != "It" and n != "That":
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             proper_nouns = nominee_pat_14.findall(t)
    #             for n in proper_nouns:
    #                 n = n[0:(n.find("should")-1)]
    #                 if not unneeded_stuff.findall(n) and n != "It" and n != "That":
    #                     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
    #             if (all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]):
    #                 all_nominee_pnouns[OFFICIAL_AWARDS.index(award)] = list(set(all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]))
    #
    # print ("******************************************")
    # correct = 0
    # for i in range(1,len(all_nominee_pnouns)):
    #     # print(OFFICIAL_AWARDS[i])
    #     # if Counter(all_nominee_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['nominees']:
    #     #     correct += 1
    #     # else:
    #     results['award_data'][OFFICIAL_AWARDS[i]]['nominees'] = all_nominee_pnouns[i][0:4]
    #     # print "Award: ", OFFICIAL_AWARDS[i]
    #     # # print "Our answer: ", (Counter(all_nominee_pnouns[i]).most_common(5))  #aggregate PN lists using Counter and show top 3
    #     # print "Our answer: ", all_nominee_pnouns[i][0:4]
    #     # print "Desired answer:", (answers['award_data'][OFFICIAL_AWARDS[i]]['nominees']) #pull from answer key
    #     # print "\n"
    #
    # # print("Correctly extracting " + str(correct) + " of " + str(len(OFFICIAL_AWARDS)) + " awards")


    #--------- End Extracting nominees ------------------------------------------------

    #--------- Extracting Winners --------------------------------------------------

    #create lists of all PN2s that show up in classified tweets, mapped to award names
    all_win_pnouns = [[] for a in OFFICIAL_AWARDS]

    for t in win:
        award = classify(t)
        # if award == OFFICIAL_AWARDS[13]:
        #     print(t)
        #     print(name_pattern.findall(t))
        #     print(name_with_lower.findall(t))
        #     print('-------------')
        if award:
            name_removed_t = re.sub(removal_patterns[OFFICIAL_AWARDS.index(award)], '', t)
            if act_pat.search(award):
                proper_nouns = pn2_pat.findall(name_removed_t)
            else:
                proper_nouns = name_pattern.findall(name_removed_t)
                proper_nouns += name_with_lower.findall(name_removed_t)
            for n in proper_nouns:
                all_win_pnouns[OFFICIAL_AWARDS.index(award)].append(n)

    correct = 0
    #print award name, top 3 predictions, then answer from answer key
    for i in range(len(all_win_pnouns)):
        print(OFFICIAL_AWARDS[i])
        results['award_data'][OFFICIAL_AWARDS[i]]['winner'] = Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()
        try:
            results['award_data'][OFFICIAL_AWARDS[i]]['nominees'].append(Counter(all_win_pnouns[i]).most_common(3)[0][0].lower())
        except:
            results['award_data'][OFFICIAL_AWARDS[i]]['nominees'] = Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()
        if Counter(all_win_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['winner']:
            correct += 1
        else:
            print(Counter(all_win_pnouns[i]).most_common(5))  #aggregate PN lists using Counter and show top 3
        print(answers['award_data'][OFFICIAL_AWARDS[i]]['winner']) #pull from answer key
        print("------------------------------------------------")


    print("Correctly extracting " + str(correct) + " of " + str(len(OFFICIAL_AWARDS)) + " awards winners")


    pprint(results)
    return results

# voodoo_magic('2013', OFFICIAL_AWARDS_13)
