import json
from pprint import pprint
import re, nltk, imdb, sys
from nominees_data_and_functions import *
from collections import Counter
from answers import answers

#first process everything
reload(sys)
sys.setdefaultencoding('utf8')

with open('gg2013.json') as f:
    data = json.load(f)

tweets = []
for d in data:
    tweets.append(d['text'])

tweets = list(set(tweets))

#-----------------------------------------------------------------------------------------------

sorted_awards = sorted(OFFICIAL_AWARDS, key=award_length)

# take the intersection of the tweet and each award, return the name with most matches. ties go to shortest award name (that's why it's sorted)
def classify(tweet):
    num_overlap = [len(tokenize(tweet).intersection(tokenize(a))) for a in sorted_awards]  #array that contains number of overlapping words, mapped to sorted_awards
    if max(num_overlap) > 1:  #if we're able to match more than one word
        return sorted_awards[num_overlap.index(max(num_overlap))]  #grab the first (and thus shortest) award name that matches max(num_overlap) times
    else:
        return None

nominee = []

#append anything matching nominee_pat or win_pat to nominee[]
for t in tweets:
    # print t
    low = t.lower()
    if not rt.match(low):
        if (nominee_pat.search(low) or win_pat.search(low)):
            #punctuation = re.compile(r'[^\w\s]')
            nominee.append(t)

#create lists of all PN2s that show up in classified tweets, mapped to award names
all_nominee_pnouns = [[] for a in OFFICIAL_AWARDS]
#print all_nominee_pnouns

# Classify the nominee-related tweets by their awards, and
# infer the names in these same tweets
# movie = imdb.IMBd()
for t in nominee:
    # print t
    # print "\n"
    award = classify(t)
    # Recall: classify function returns None if no award matches
    if award:
        # if (t == "Connie Britton should have won best actress #GoldenGlobes"):
        #     print "AWARD: ", award
        # print "AWARD_RELATED TWEET"
        # print t
        # print "\n"
        # print award
        # print "\n"
        # print "\n"
        # print "Tweet: ", t
        # print "Award label: ", award

        # if the award has to do with an actor / actress...
        if act_pat.search(award) or director_pat.search(award):
            proper_nouns = nominee_pat_1.findall(t)
            for n in proper_nouns:
                n = n[8:]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_2.findall(t)
            for n in proper_nouns:
                n = n[0:-14]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_3.findall(t)
            for n in proper_nouns:
                n = n[0:-11]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_4.findall(t)
            for n in proper_nouns:
                n = n[0:(n.find("did")-1)]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_5.findall(t)
            for n in proper_nouns:
                n = n[7:-7]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_6.findall(t)
            for n in proper_nouns:
                n = n[(n.find("been")+5):]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_7.findall(t)
            for n in proper_nouns:
                n = n[0:(n.find("should")-1)]
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            if (all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]):
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)] = list(set(all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]))

        # if the award doesn't have to do with an actor...
        else:
            proper_nouns = nominee_pat_8.findall(t)
            for n in proper_nouns:
                n = n[8:]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_9.findall(t)
            for n in proper_nouns:
                n = n[0:-14]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_10.findall(t)
            for n in proper_nouns:
                n = n[0:-11]
                if not unneeded_stuff.findall(n):
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_11.findall(t)
            for n in proper_nouns:
                n = n[0:(n.find("did")-1)]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_12.findall(t)
            for n in proper_nouns:
                n = n[7:-7]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_13.findall(t)
            for n in proper_nouns:
                n = n[(n.find("been")+5):]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            proper_nouns = nominee_pat_14.findall(t)
            for n in proper_nouns:
                n = n[0:(n.find("should")-1)]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            if (all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]):
                all_nominee_pnouns[OFFICIAL_AWARDS.index(award)] = list(set(all_nominee_pnouns[OFFICIAL_AWARDS.index(award)]))

print ("******************************************")
correct = 0
for i in range(1,len(all_nominee_pnouns)):
    # print(OFFICIAL_AWARDS[i])
    # if Counter(all_nominee_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['nominees']:
    #     correct += 1
    # else:
    print "Award: ", OFFICIAL_AWARDS[i]
    # print "Our answer: ", (Counter(all_nominee_pnouns[i]).most_common(5))  #aggregate PN lists using Counter and show top 3
    print "Our answer: ", all_nominee_pnouns[i][0:4]
    print "Desired answer:", (answers['award_data'][OFFICIAL_AWARDS[i]]['nominees']) #pull from answer key
    print "\n"

# print("Correctly extracting " + str(correct) + " of " + str(len(OFFICIAL_AWARDS)) + " awards")
