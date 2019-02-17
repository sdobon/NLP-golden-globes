import json
from pprint import pprint
import re, nltk, imdb, sys
from collections import Counter

from answers import answers

reload(sys)
sys.setdefaultencoding('utf8')

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


host_pat = re.compile(" [Hh]ost")
win_pat = re.compile("w[io]n|takes")
pn2_pat= re.compile("(?!Best)(?!Golden)(?!Globes)(?!Supporting)(?!Actor)(?!Actress)(?!Cecil)[A-Z][a-z]+ [A-Z]\S+")
rt = re.compile("rt")
award_related_pat = re.compile("best.*actress.*television.*drama")
act_pat = re.compile("act")
director_pat = re.compile("direct")

# Common nominee patterns for actors / actresses
# Nominee ____
nominee_pat_1 = re.compile("[Nn]ominee [[A-Z][a-z]+ [A-Z][a-z]+")
# n = n[8:]
# _____ was nominated
nominee_pat_2 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ was nominated")
# n = n[0:-14]
# ___ was robbed
nominee_pat_3 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ was robbed")
# n = n[0:-11]
# ____ didn't win
nominee_pat_4 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ did not win|[A-Z][a-z]+ [A-Z][a-z]+ didn[']*t win")
# I wanted ____
nominee_pat_5 = re.compile("wanted [A-Z][a-z]+ [A-Z][a-z]+")
# should have been ___
nominee_pat_6 = re.compile("should have been [A-Z][a-z]+ [A-Z][a-z]+|should[']*ve been [A-Z][a-z]+ [A-Z][a-z]+")
# ____ should have won
nominee_pat_7 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ should have won|[A-Z][a-z]+ [A-Z][a-z]+ should[']*ve won")

# Common nominee patterns for movie titles
nominee_pat_8 = re.compile("[Nn]ominee [[A-Z][a-z]+ [A-Z][a-z]+|[Nn]ominee [A-Z][a-z]+.[a-z]{1,3}.[A-Z][a-z]+")
# n = n[8:]
# _____ was nominated
nominee_pat_9 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ was nominated|[Nn]ominee [A-Z][a-z]+.[a-z]{1,3}.[A-Z][a-z]+")
# n = n[0:-14]
# ___ was robbed
nominee_pat_10 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ was robbed")
# n = n[0:-11]
# ____ didn't win
nominee_pat_11 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ did not win|[A-Z][a-z]+ [A-Z][a-z]+ didn[']*t win")
# I wanted ____
nominee_pat_12 = re.compile("wanted [A-Z][a-z]+ [A-Z][a-z]+")
# should have been ___
nominee_pat_13 = re.compile("should have been [A-Z][a-z]+ [A-Z][a-z]+|should[']*ve been [A-Z][a-z]+ [A-Z][a-z]+")
# ____ should have won
nominee_pat_14 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ should have won|[A-Z][a-z]+ [A-Z][a-z]+ should[']*ve won")


name_pattern = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
name_with_lower = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[a-z]*\b){1,2}(?:\s+[A-Z][a-z]*\b)+')
pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')

nominee_pat = re.compile("[Dd]idn't win|Did not win|didn't get|did not get|[Nn]ominee|[Nn]ominated|[Nn]omination|robbed|wanted [A-Z][a-z]+|should have been|should've been|should've won|should have won")

nominee = []

#append anything matching nominee_pat to nominee[]
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

# Return array of actor / actress names only!
def find_names_only(list_of_pronouns):
    # print ("Entering find_names_only")
    actor = imdb.IMDb()
    names_array = []
    stringified_pronouns = [i.encode("utf-8") for i in list_of_pronouns]
    for pronoun in stringified_pronouns:
        # if ((nltk.pos_tag(nltk.word_tokenize(pronoun))[0][1] == "NNP") and (nltk.pos_tag(nltk.word_tokenize(pronoun))[1][1] == "NNP")):
        #     names_array.append(pronoun)
        try:
            if (actor.search_movie(pronoun)[0]['name'] == pronoun):
                names_array.append(pronoun)
        except:
            pass
    # print "Returned list of names: ", names_array
    return list(set(names_array))

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
                n = n[7:]
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
                n = n[7:]
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

        # print "Pronouns found: ", proper_nouns

        # print "\n"
        # for n in proper_nouns:
        #     all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].append(n)

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
