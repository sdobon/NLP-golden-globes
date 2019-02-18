import re

#Adapted from nominees

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

#Data
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

#REGEX STUFF
unneeded_stuff = re.compile("(?:[a-z][A-Z][a-z0-9]+)+|@|#")

pn2_pat= re.compile("(?!Best)(?!Golden)(?!Globes)(?!Supporting)(?!Actor)(?!Actress)(?!Cecil)[A-Z][a-z]+ [A-Z]\S+")
rt = re.compile("rt")
award_related_pat = re.compile("best.*actress.*television.*drama")
act_pat = re.compile("act")
director_pat = re.compile("direct")
name_pattern = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
name_with_lower = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[a-z]*\b){1,2}(?:\s+[A-Z][a-z]*\b)+')
pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')
presenter_pat = re.compile("[Pp]resent|[Pp]resents|[Pp]resenting|[Pp]resenter|[Pp]resented|[Pp]resenter")

# Common presenter patterns for actors / actresses
# Nominee ____
presenter_pat_1 = re.compile("[Pp]resenter [A-Z][a-z]+ [A-Z][a-z]+")
presenter_pat_2 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ presented")
presenter_pat_3 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ did not present|[A-Z][a-z]+ [A-Z][a-z]+ didn[']*t present")
presenter_pat_4 = re.compile("wanted [A-Z][a-z]+ [A-Z][a-z]+ to present")
presenter_pat_5 = re.compile("should have been [A-Z][a-z]+ [A-Z][a-z]+|should[']*ve been [A-Z][a-z]+ [A-Z][a-z]+")
presenter_pat_6 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ should have presented|[A-Z][a-z]+ [A-Z][a-z]+ should[']*ve presented")
presenter_pat_7 = re.compile("[Pp]resenter [A-Z][a-z]+|[Pp]resenter [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|[Pp]resenter [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|[Pp]resenter [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|[Pp]resenter [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+")
presenter_pat_8 = re.compile("wanted [A-Z][a-z]+ to present|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to present|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to present|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to present|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to present")
presenter_pat_9 = re.compile("should have been [A-Z][a-z]+|should[']*ve been [A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+")
presenter_pat_10 = re.compile("[A-Z][a-z]+ should have presented|[A-Z][a-z]+ should[']*ve presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have presented|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve presented")