'''Version 0.35'''

import json
from pprint import pprint
import re, nltk
from collections import Counter

OFFICIAL_AWARDS_1315 = ['cecil b. demille award', 'best motion picture - drama', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - comedy or musical', 'best performance by an actor in a motion picture - comedy or musical', 'best animated feature film', 'best foreign language film', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actor in a supporting role in a motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best television series - comedy or musical', 'best performance by an actress in a television series - comedy or musical', 'best performance by an actor in a television series - comedy or musical', 'best mini-series or motion picture made for television', 'best performance by an actress in a mini-series or motion picture made for television', 'best performance by an actor in a mini-series or motion picture made for television', 'best performance by an actress in a supporting role in a series, mini-series or motion picture made for television', 'best performance by an actor in a supporting role in a series, mini-series or motion picture made for television']
OFFICIAL_AWARDS_1819 = ['best motion picture - drama', 'best motion picture - musical or comedy', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama', 'best performance by an actress in a motion picture - musical or comedy', 'best performance by an actor in a motion picture - musical or comedy', 'best performance by an actress in a supporting role in any motion picture', 'best performance by an actor in a supporting role in any motion picture', 'best director - motion picture', 'best screenplay - motion picture', 'best motion picture - animated', 'best motion picture - foreign language', 'best original score - motion picture', 'best original song - motion picture', 'best television series - drama', 'best television series - musical or comedy', 'best television limited series or motion picture made for television', 'best performance by an actress in a limited series or a motion picture made for television', 'best performance by an actor in a limited series or a motion picture made for television', 'best performance by an actress in a television series - drama', 'best performance by an actor in a television series - drama', 'best performance by an actress in a television series - musical or comedy', 'best performance by an actor in a television series - musical or comedy', 'best performance by an actress in a supporting role in a series, limited series or motion picture made for television', 'best performance by an actor in a supporting role in a series, limited series or motion picture made for television', 'cecil b. demille award']

def get_answers(year):
    with open('gg%sanswers.json'%year, 'r') as f:
        fres = json.load(f)
    return fres

def get_hosts(year):
    '''Hosts is a list of one or more strings. Do NOT change the name
    of this function or what it returns.'''
    with open('gg%s.json'%year, 'r') as f:
        data = json.load(f)

    tweets = []
    for d in data:
        tweets.append(d['text'])

    tweets = list(set(tweets))
    if year == '2013' or year == '2015':
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1315
    elif year == '2018' or year == '2019':
        OFFICIAL_AWARDS = OFFICIAL_AWARDS_1819
    else:
        print("CANNOT FIND A MATCHING OFFICIAL_AWARDS OBJECT")

    host_pat = re.compile(" [Hh]ost")
    pn2_pat= re.compile("[A-Z][a-z]+ [A-Z]\S+")
    rt = re.compile("rt")

    all_proper_nouns = []
    host = []


    for t in tweets:
        if not rt.match(t):
            if host_pat.search(t):
                host.append(t)
                proper_nouns = pn2_pat.findall(t)
            else:
                proper_nouns = []
            for n in proper_nouns:
                all_proper_nouns.append(n)


    # print(all_proper_nouns)
    # print(Counter(all_proper_nouns).most_common(30))
    most_common = Counter(all_proper_nouns).most_common(2)
    hosts = [most_common[0][0], most_common[1][0]]
    print(hosts)
    return hosts

def get_awards(year):
    '''Awards is a list of strings. Do NOT change the name
    of this function or what it returns.'''
    awards = ['best performance by an actor in a motion picture - drama', 'best motion picture - comedy or musical', 'best director - motion picture', 'best original song - motion picture', 'best performance by an actress in a supporting role in a motion picture', 'best performance by an actress in a television series - drama', 'best television series - drama', 'best performance by an actress in a supporting role in a motion picture', 'best motion picture - drama', 'best screenplay - motion picture', 'best original song - motion picture', 'best performance by an actor in a television series - drama', 'best television series - drama', 'best animated feature film', 'best performance by an actor in a television series - comedy or musical', 'best performance by an actor in a motion picture - drama', 'best motion picture - drama', 'best performance by an actress in a motion picture - comedy or musical', 'best motion picture - drama', 'best performance by an actor in a supporting role in a motion picture', 'best animated feature film', 'best foreign language film', 'best motion picture - comedy or musical', 'best performance by an actress in a motion picture - drama', 'best performance by an actor in a motion picture - drama']
    return awards

def get_nominees(year):
    '''Nominees is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change
    the name of this function or what it returns.'''
    # Your code here
    fres = get_answers(year)
    nominees = {award: fres['award_data'][award]['nominees'] for award in OFFICIAL_AWARDS_1315}
    return nominees

def get_winner(year):
    '''Winners is a dictionary with the hard coded award
    names as keys, and each entry containing a single string.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    fres = get_answers(year)
    winners = {award: fres['award_data'][award]['winner'] for award in OFFICIAL_AWARDS_1315}
    return winners

def get_presenters(year):
    '''Presenters is a dictionary with the hard coded award
    names as keys, and each entry a list of strings. Do NOT change the
    name of this function or what it returns.'''
    # Your code here
    fres = get_answers(year)
    presenters = {award: fres['award_data'][award]['presenters'] for award in OFFICIAL_AWARDS_1315}
    return presenters

def pre_ceremony():
    '''This function loads/fetches/processes any data your program
    will use, and stores that data in your DB or in a json, csv, or
    plain text file. It is the first thing the TA will run when grading.
    Do NOT change the name of this function or what it returns.'''
    # Your code here
    print("Pre-ceremony processing complete.")
    return

def main():
    '''This function calls your program. Typing "python gg_api.py"
    will run this function. Or, in the interpreter, import gg_api
    and then run gg_api.main(). This is the second thing the TA will
    run when grading. Do NOT change the name of this function or
    what it returns.'''
    # Your code here
    return

if __name__ == '__main__':
    main()
