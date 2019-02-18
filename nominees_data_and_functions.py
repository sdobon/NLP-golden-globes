import re

# Funcions

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

# Data
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

# REGEX STUFF

unneeded_stuff = re.compile("(?:[a-z][A-Z][a-z0-9]+)+|@|#")

win_pat = re.compile("w[io]n|takes")
pn2_pat= re.compile("(?!Best)(?!Golden)(?!Globes)(?!Supporting)(?!Actor)(?!Actress)(?!Cecil)[A-Z][a-z]+ [A-Z]\S+")
rt = re.compile("rt")
award_related_pat = re.compile("best.*actress.*television.*drama")
act_pat = re.compile("act")
director_pat = re.compile("direct")
name_pattern = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[A-Z][a-z]*\b)*')
name_with_lower = re.compile(r'\b(?!Best)[A-Z][a-z]*\b(?:\s+[a-z]*\b){1,2}(?:\s+[A-Z][a-z]*\b)+')
pnx_pat= re.compile(r'\b[A-Z]\S+\b(?:\s+[A-Z]\S*\b)*')
nominee_pat = re.compile("[Dd]idn't win|Did not win|didn't get|did not get|[Nn]ominee|[Nn]ominated|[Nn]omination|robbed|wanted [A-Z][a-z]+|should have been|should've been|should've won|should have won")

# Common nominee patterns for actors / actresses
# Nominee ____
nominee_pat_1 = re.compile("[Nn]ominee [A-Z][a-z]+ [A-Z][a-z]+")
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
nominee_pat_5 = re.compile("wanted [A-Z][a-z]+ [A-Z][a-z]+ to win")
# should have been ___
nominee_pat_6 = re.compile("should have been [A-Z][a-z]+ [A-Z][a-z]+|should[']*ve been [A-Z][a-z]+ [A-Z][a-z]+")
# ____ should have won
nominee_pat_7 = re.compile("[A-Z][a-z]+ [A-Z][a-z]+ should have won|[A-Z][a-z]+ [A-Z][a-z]+ should[']*ve won")

# Common nominee patterns for movie titles: 1 word titles, 2 word titles, 3 word titles, 4 word titles, 5 word titles

# Nominee _____
nominee_pat_8 = re.compile("[Nn]ominee [A-Z][a-z]+|[Nn]ominee [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|[Nn]ominee [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|[Nn]ominee [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|[Nn]ominee [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+")
# n = n[8:]
# _____ was nominated
nominee_pat_9 = re.compile("[A-Z][a-z]+ was nominated|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was nominated|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was nominated|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was nominated|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was nominated")
# n = n[0:-14]
# ___ was robbed
nominee_pat_10 = re.compile("[A-Z][a-z]+ was robbed|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was robbed|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was robbed|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was robbed|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ was robbed")
# n = n[0:-11]
# ____ didn't win
nominee_pat_11 = re.compile("[A-Z][a-z]+ did not win|[A-Z][a-z]+ didn[']*t win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ did not win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ didn[']*t win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ did not win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ didn[']*t win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ did not win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ didn[']*t win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ did not win|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ didn[']*t win")
# I wanted ____
nominee_pat_12 = re.compile("wanted [A-Z][a-z]+ to win|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to win|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to win|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to win|wanted [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ to win")
# should have been ___
nominee_pat_13 = re.compile("should have been [A-Z][a-z]+|should[']*ve been [A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should have been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+|should[']*ve been [A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+")
# ____ should have won
nominee_pat_14 = re.compile("[A-Z][a-z]+ should have won|[A-Z][a-z]+ should[']*ve won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should have won|[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+\s*[a-z]{0,3}\s*[a-z]{0,3}\s[A-Z][a-z]+ should[']*ve won")
