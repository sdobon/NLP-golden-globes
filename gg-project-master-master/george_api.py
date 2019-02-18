# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 16:02:40 2019

@author: georg
"""
# import re
import json
from pprint import pprint
from collections import Counter
from textblob import TextBlob
from google_images_download import google_images_download

import gg_api
import gg_black_box

print(gg_api.get_hosts('2013'))
print(gg_api.get_winner('2013'))

# years = ['2013', '2015']
#
# for year in years:
#     with open('gg_results_%s.json'%year, 'r') as f:
#         data = json.load(f)
#         pprint(data)



# OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
# OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']
# hosts = ["seth meyers", "Amy poehler"]
# awards = ["award1", 'award2', 'award3']
# year = 2013
# presenters = dict()
# presenters[OFFICIAL_AWARDS_1315[0]] = ['asd 1', 'tina fey']
# presenters[OFFICIAL_AWARDS_1315[1]] = ['asd 2', 'tina feye']
# presenters[OFFICIAL_AWARDS_1315[2]] = ['asd 1', 'tina feya']
# nominees = dict()
# nominees[OFFICIAL_AWARDS_1315[0]] = ['jodie foster', 'tina feys']
# nominees[OFFICIAL_AWARDS_1315[2]] = ['jodie fosters', 'tina feysa']
# nominees[OFFICIAL_AWARDS_1315[1]] = ['jodie fostera', 'tina feyss']
# winner = dict()
# winner[OFFICIAL_AWARDS_1315[0]] = 'jodie foster'
# winner[OFFICIAL_AWARDS_1315[1]] = 'jodie fostersa'
# winner[OFFICIAL_AWARDS_1315[2]] = 'jodie fosterdsa'
#
 # main takes in the year and prints the human readable format and stores the json format in an object called "ans_json"
def main(year):
     hosts = gg_api.get_hosts(year)
     awards = gg_api.get_awards(year)
     presenters = gg_api.get_presenters(year)
     winner = gg_api.get_winner(year)
     nominees = gg_api.get_nominees(year)
     if year == 2013:
         OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
     elif year == 2015:
         OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
     else:
         OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819


     def genre(award):
         if re.search('performance', award):
             return 'person'
         if re.search('director', award):
             return 'person'
         else:
             return 'non-person'
 #CREATE JSON w/ HOST
     json_i = dict()
     json_i['hosts'] = hosts
 #PRINT HOST
     hosts = [i.title() for i in hosts]
     if len(hosts) > 1:
         print("Hosts: ")
         print(*hosts, sep = ', ')
     else:
         print("Host: ")
         print(hosts[0].title())

     print('\n')
     print("Awards that we extracted: ")
     cnt = 1
     for i in awards:
         print(str(cnt) + ') ', i.title())
         cnt += 1

     print('\nBreakdowns by award:')
     print('---------------------------')

     json_i['award_data']= dict()
     for i in OFFICIAL_AWARDS:
         json_i['award_data'][i] = dict()
         json_i['award_data'][i]['nominees'] = nominees
         json_i['award_data'][i]['presenters'] = presenters
         json_i['award_data'][i]['winner'] = winner

         print('Award: ', i.title())
         print('Presenters: ', end='')
         presenters_i = [i.title() for i in presenters[i]]
         print(*presenters_i, sep = ', ')

         if genre(i) == 'non-person':
             print('Nominees: ', end='')
             nominees_i = ['\"' + i.title() + '\"' for i in nominees[i]]
             print(*nominees_i, sep = ', ')

             print('Winner: \"' + winner[i].title() + '\"')

             print('---------------------------\n')

         else:
             print('Nominees: ', end='')
             nominees_i = [i.title() for i in nominees[i]]
             print(*nominees_i, sep = ', ')

             print('Winner: ' + winner[i].title())

             print('---------------------------\n')

 #DUMP CONTENTS INTO DATA(YEAR).JSON
     with open('data' + str(year) + '.json', 'w') as outfile:
         json.dump(json_i, outfile)
 # BEGINNING OF EXTRAS -------------------------------------------------     
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


     rt = re.compile("rt")
     award_related_pat = re.compile("best")
     punctuation = re.compile(r'[^\w\s]')


     print('\nBEGINNING OF EXTRAS: \n')
     dress = re.compile("best dressed")
     dressed = []
     for t in tweets:
         low = t.lower()
         if not rt.match(low):
             if dress.search(low):
                #punctuation = re.compile(r'[^\w\s]')
                 dressed.append(t)

     np_count = []
     for i in dressed:
         blob = TextBlob(i)
         for np in blob.noun_phrases:
             np_count.append(np)

     best_dressed = []
     for i in Counter(np_count).most_common(3):
         best_dressed.append(i)

     def find_dressed(counter):
         surprises = []
         i = 3
         j = 0
         common = counter.most_common(20)
         while i > 0:
             if j == 20:
                 return surprises
             k = common[j][0]
             if not re.search('globe', k):
                 if len(k.split()) > 1:
                     surprises.append(k)
                     i -= 1
             j += 1
         return(surprises)

     keywords = ''
     returns = find_dressed(Counter(np_count))
     for i in range(3):
         keywords += returns[i] + ' golden globes ' + str(year) +','
     response = google_images_download.googleimagesdownload()
     arguments = {"keywords":keywords[:-1],"limit":1, "no_download":True}
     absolute_image_paths = response.download(arguments)




     # --------------------------------------------------------
     shock = re.compile("shock")
     surp = re.compile("surprise")
     shocks = []
     for t in tweets:
         low = t.lower()
         if not rt.match(low):
             if shock.search(low):
                 #punctuation = re.compile(r'[^\w\s]')
                 shocks.append(t)
             if surp.search(low):
                 shocks.append(t)

     np_count = []
     for i in shocks:
         blob = TextBlob(i)
         for np in blob.noun_phrases:
             np_count.append(np)


     def find_surprises(counter):
         surprises = []
         i = 3
         j = 0
         common = counter.most_common(20)
         while i > 0:
             if j == 20:
                 return surprises
             k = common[j][0]
             if not re.search('globe', k):
                 surprises.append(k)
                 i -= 1
             j += 1
         return(surprises)

     def find_first_appearance(np):
         count = 3
         ans = []
         for i in shocks:
             if count == 0:
                 return ans
             if re.search(np, i.lower()):
                 ans.append(i)
                 count -= 1

     surprises = find_surprises(Counter(np_count))
     first = find_first_appearance(surprises[0])
     second = find_first_appearance(surprises[1])
     third = find_first_appearance(surprises[2])
     first += second
     first += third
     print('Most surprising moments of the show: ')
     cnt = 1
     for i in first:
         print(str(cnt) + ') ' + i)
         cnt+=1


     # -------------------------------------------------------------
     win = []
     for t in tweets:
         low = t.lower()
         if not rt.match(low):
             if award_related_pat.search(low):
                 #punctuation = re.compile(r'[^\w\s]')
                 win.append(t)

     classified = []
     for i in win:
         classified.append(classify(i))

     class_dict = dict()

     for i in range(len(classified)):
         if classified[i]:
             if classified[i] not in class_dict.keys():
                 class_dict[classified[i]] = [win[i]]
             else:
                 class_dict[classified[i]].append(win[i])


     upset_score = dict()
     sentiment_scores = dict()
     for i in class_dict.keys():
         sentiment_scores[i] = list()
         upset_score[i] = 0
         for j in class_dict[i]:
             blob = TextBlob(j)
             sentiment_scores[i].append(blob.sentiment[0])
             upset_score[i] += blob.sentiment[0]
         upset_score[i] = upset_score[i] / len(class_dict[i])


     #for i in class_dict.keys():
     #    upset_score[i] = 0
     #    for j in class_dict[i]:
     #        blob = TextBlob(j)
     #        upset_score[i] += blob.sentiment[0]
     #    upset_score[i] = upset_score[i] / len(class_dict[i])


     def find_worst(category):
         worst_index = sentiment_scores[category].index(min(sentiment_scores[category]))
         return class_dict[category][worst_index]

     def find_best(category):
         worst_index = sentiment_scores[category].index(max(sentiment_scores[category]))
         return class_dict[category][worst_index]


     sorted_score =sorted(upset_score, key = upset_score.get)


     print("\nMost upset three categories are: ", sorted_score[0].title(),', ', sorted_score[1].title(),', ', sorted_score[2].title())
     print("\nAnd the most upset tweets in each category are: ")
     worsts = [find_worst(i) for i in sorted_score]
     for i in range(len(worsts)):
         print(sorted_score[i].title())
         print(worsts[i])
         print('-----------------------')
     print("Least upset three categories are: ", sorted_score[-1].title(),', ', sorted_score[-2].title(),', ', sorted_score[-3].title())
