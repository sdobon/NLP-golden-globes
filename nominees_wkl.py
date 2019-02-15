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

name_pattern = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
name_with_lower = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[a-z]*\b){1,2}(?:\s+[A-Z][a-z]*\b)+')
pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')

nominee_pat = re.compile("[Dd]idn't win|Did not win|didn't get|did not get|[Nn]ominee|[Nn]ominated|[Nn]omination")
# was\s[Nn]ominated|get[Nn]omin"
# for t in tweets:
#     print t
#     print("\n")

nominee = []

#append anything matching nominee_pat to nominee[]
for t in tweets:
    low = t.lower()
    if not rt.match(low):
        if (nominee_pat.search(low) or win_pat.search(low)):
            #punctuation = re.compile(r'[^\w\s]')
            nominee.append(t)


#create lists of all PN2s that show up in classified tweets, mapped to award names
all_nominee_pnouns = [[] for a in OFFICIAL_AWARDS]
#print all_nominee_pnouns

# Return array of names only!
def find_names_only(list_of_pronouns):
    names_array = []
    stringified_pronouns = [i.encode("utf-8") for i in list_of_pronouns]
    for pronoun in stringified_pronouns:
        if ((nltk.pos_tag(nltk.word_tokenize(pronoun))[0][1] == "NNP") and (nltk.pos_tag(nltk.word_tokenize(pronoun))[1][1] == "NNP")):
            names_array.append(pronoun)
    return list(set(names_array))

# test_pronouns = [u'Is Ben Affleck', u'Matt Damon', u'Affleck', u'Picture', u'Director', u'Matt Damon', u'Affleck just won Best Picture', u'Director while Matt Damon']
# print "CHECK (Matt Damon only): ", find_names_only(test_pronouns)


# Classify the nominee-related tweets by their awards, and
# infer the names in these same tweets
for t in nominee:
    award = classify(t)
    # Recall: classify function returns None if no award matches
    if award:
        # print "Tweet: ", t
        # print "Award label: ", award
        # if the award has to do with an actor...
        if act_pat.search(award):
            proper_nouns = pn2_pat.findall(t)
            # print ("no....")
            # print proper_nouns
            proper_nouns = find_names_only(proper_nouns)
        # if the award doesn't have to do with an actor...
        else:
            proper_nouns = name_pattern.findall(t)
            proper_nouns += name_with_lower.findall(t)
        # print "Pronouns found: ", proper_nouns

        # print "\n"
        for n in proper_nouns:
            all_nominee_pnouns[OFFICIAL_AWARDS.index(award)].append(n)

print ("******************************************")
correct = 0
for i in range(len(all_nominee_pnouns)):
    # print(OFFICIAL_AWARDS[i])
    # if Counter(all_nominee_pnouns[i]).most_common(3)[0][0].lower()==answers['award_data'][OFFICIAL_AWARDS[i]]['nominees']:
    #     correct += 1
    # else:
    print "Award: ", OFFICIAL_AWARDS[i]
    print "Our answer: ", (Counter(all_nominee_pnouns[i]).most_common(10))  #aggregate PN lists using Counter and show top 3
    print "Desired answer:", (answers['award_data'][OFFICIAL_AWARDS[i]]['nominees']) #pull from answer key
    print("------------------------------------------------")

# print("Correctly extracting " + str(correct) + " of " + str(len(OFFICIAL_AWARDS)) + " awards")
