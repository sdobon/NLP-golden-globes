import json
from pprint import pprint
import re, nltk, sys
from presenters_data_and_functions import *
from collections import Counter
from answers import answers
answers = {"hosts": ["amy poehler", "tina fey"], "award_data": {"best screenplay - motion picture": {"nominees": ["zero dark thirty", "lincoln", "silver linings playbook", "argo"], "presenters": ["robert pattinson", "amanda seyfried"], "winner": "django unchained"}, "best director - motion picture": {"nominees": ["kathryn bigelow", "ang lee", "steven spielberg", "quentin tarantino"], "presenters": ["halle berry"], "winner": "ben affleck"}, "best performance by an actress in a television series - comedy or musical": {"nominees": ["zooey deschanel", "tina fey", "julia louis-dreyfus", "amy poehler"], "presenters": ["aziz ansari", "jason bateman"], "winner": "lena dunham"}, "best foreign language film": {"nominees": ["the intouchables", "kon tiki", "a royal affair", "rust and bone"], "presenters": ["arnold schwarzenegger", "sylvester stallone"], "winner": "amour"}, "best performance by an actor in a supporting role in a motion picture": {"nominees": ["alan arkin", "leonardo dicaprio", "philip seymour hoffman", "tommy lee jones"], "presenters": ["bradley cooper", "kate hudson"], "winner": "christoph waltz"}, "best performance by an actress in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["hayden panettiere", "archie panjabi", "sarah paulson", "sofia vergara"], "presenters": ["dennis quaid", "kerry washington"], "winner": "maggie smith"}, "best motion picture - comedy or musical": {"nominees": ["the best exotic marigold hotel", "moonrise kingdom", "salmon fishing in the yemen", "silver linings playbook"], "presenters": ["dustin hoffman"], "winner": "les miserables"}, "best performance by an actress in a motion picture - comedy or musical": {"nominees": ["emily blunt", "judi dench", "maggie smith", "meryl streep"], "presenters": ["will ferrell", "kristen wiig"], "winner": "jennifer lawrence"}, "best mini-series or motion picture made for television": {"nominees": ["the girl", "hatfields & mccoys", "the hour", "political animals"], "presenters": ["don cheadle", "eva longoria"], "winner": "game change"}, "best original score - motion picture": {"nominees": ["argo", "anna karenina", "cloud atlas", "lincoln"], "presenters": ["jennifer lopez", "jason statham"], "winner": "life of pi"}, "best performance by an actress in a television series - drama": {"nominees": ["connie britton", "glenn close", "michelle dockery", "julianna margulies"], "presenters": ["nathan fillion", "lea michele"], "winner": "claire danes"}, "best performance by an actress in a motion picture - drama": {"nominees": ["marion cotillard", "sally field", "helen mirren", "naomi watts", "rachel weisz"], "presenters": ["george clooney"], "winner": "jessica chastain"}, "cecil b. demille award": {"nominees": [], "presenters": ["robert downey, jr."], "winner": "jodie foster"}, "best performance by an actor in a motion picture - comedy or musical": {"nominees": ["jack black", "bradley cooper", "ewan mcgregor", "bill murray"], "presenters": ["jennifer garner"], "winner": "hugh jackman"}, "best motion picture - drama": {"nominees": ["django unchained", "life of pi", "lincoln", "zero dark thirty"], "presenters": ["julia roberts"], "winner": "argo"}, "best performance by an actor in a supporting role in a series, mini-series or motion picture made for television": {"nominees": ["max greenfield", "danny huston", "mandy patinkin", "eric stonestreet"], "presenters": ["kristen bell", "john krasinski"], "winner": "ed harris"}, "best performance by an actress in a supporting role in a motion picture": {"nominees": ["amy adams", "sally field", "helen hunt", "nicole kidman"], "presenters": ["megan fox", "jonah hill"], "winner": "anne hathaway"}, "best television series - drama": {"nominees": ["boardwalk empire", "breaking bad", "downton abbey (masterpiece)", "the newsroom"], "presenters": ["salma hayek", "paul rudd"], "winner": "homeland"}, "best performance by an actor in a mini-series or motion picture made for television": {"nominees": ["benedict cumberbatch", "woody harrelson", "toby jones", "clive owen"], "presenters": ["jessica alba", "kiefer sutherland"], "winner": "kevin costner"}, "best performance by an actress in a mini-series or motion picture made for television": {"nominees": ["nicole kidman", "jessica lange", "sienna miller", "sigourney weaver"], "presenters": ["don cheadle", "eva longoria"], "winner": "julianne moore"}, "best animated feature film": {"nominees": ["frankenweenie", "hotel transylvania", "rise of the guardians", "wreck-it ralph"], "presenters": ["sacha baron cohen"], "winner": "brave"}, "best original song - motion picture": {"nominees": ["act of valor", "stand up guys", "the hunger games", "les miserables"], "presenters": ["jennifer lopez", "jason statham"], "winner": "skyfall"}, "best performance by an actor in a motion picture - drama": {"nominees": ["richard gere", "john hawkes", "joaquin phoenix", "denzel washington"], "presenters": ["george clooney"], "winner": "daniel day-lewis"}, "best television series - comedy or musical": {"nominees": ["the big bang theory", "episodes", "modern family", "smash"], "presenters": ["jimmy fallon", "jay leno"], "winner": "girls"}, "best performance by an actor in a television series - drama": {"nominees": ["steve buscemi", "bryan cranston", "jeff daniels", "jon hamm"], "presenters": ["salma hayek", "paul rudd"], "winner": "damian lewis"}, "best performance by an actor in a television series - comedy or musical": {"nominees": ["alec baldwin", "louis c.k.", "matt leblanc", "jim parsons"], "presenters": ["lucy liu", "debra messing"], "winner": "don cheadle"}}}

#Adapted from nominees

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

presenter = []

for t in tweets: #append anything matching presenter_pat or win_pat to presenter[]
    low = t.lower()
    if not rt.match(low):
        if (presenter_pat.search(low)):
            presenter.append(t)

#create lists of all PN2s that show up in classified tweets, mapped to award names
all_presenter_pnouns = [[] for a in OFFICIAL_AWARDS]

# Classify the presenter-related tweets by their awards, and infer the names in these same tweets
for p in presenter:
    #print(p)
    award = classify(t) # Recall: classify function returns None if no award matches
    if award:
        if act_pat.search(award) or director_pat.search(award): #if the award has to do with an actor / actress...
            proper_nouns = presenter_pat_1.findall(p)
            for n in proper_nouns:
                n = n[10:]
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_2.findall(p)
            for n in proper_nouns:
                n = n[0:-10]
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_3.findall(p)
            for n in proper_nouns:
                n = n[0:(n.find("did")-1)]
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_4.findall(p)
            for n in proper_nouns:
                n = n[7:-11]
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_5.findall(p)
            for n in proper_nouns:
                n = n[(n.find("been")+5):]
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_6.findall(p)
            for n in proper_nouns:
                n = n[0:(n.find("should")-1)]
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            if (all_presenter_pnouns[OFFICIAL_AWARDS.index(award)]):
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)] = list(set(all_presenter_pnouns[OFFICIAL_AWARDS.index(award)]))
        else:         # if the award doesn't have to do with an actor...
            proper_nouns = presenter_pat_7.findall(p)
            for n in proper_nouns:
                n = n[10:]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_8.findall(p)
            for n in proper_nouns:
                n = n[7:-11]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_9.findall(p)
            for n in proper_nouns:
                n = n[(n.find("been")+5):]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            proper_nouns = presenter_pat_10.findall(p)
            for n in proper_nouns:
                n = n[0:(n.find("should")-1)]
                if not unneeded_stuff.findall(n) and n != "It" and n != "That":
                    all_presenter_pnouns[OFFICIAL_AWARDS.index(award)].insert(0,n)
            
            if (all_presenter_pnouns[OFFICIAL_AWARDS.index(award)]):
                all_presenter_pnouns[OFFICIAL_AWARDS.index(award)] = list(set(all_presenter_pnouns[OFFICIAL_AWARDS.index(award)]))

print ("******************************************")
correct = 0
for i in range(1,len(all_presenter_pnouns)):
    print "Award: ", OFFICIAL_AWARDS[i]
    print "Our answer: ", all_presenter_pnouns[i][0:2]
    print "Desired answer:", (answers['award_data'][OFFICIAL_AWARDS[i]]['presenters']) #pull from answer key
    print "\n"
