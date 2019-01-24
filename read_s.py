import json
from pprint import pprint
import re, nltk
from collections import Counter
# m = re.search("Your number is <b>(\d+)</b>",
#       "xxx Your number is <b>123</b>  fdjsk")
# if m:
#     print m.groups()[0]

with open('gg2013.json') as f:
    data = json.load(f)

tweets = []

for d in data:
    tweets.append(d['text'])

host_pat = re.compile(" [Hh]ost")
pn2_pat= re.compile("[A-Z][a-z]+ [A-Z][a-z]+")
wf = re.compile("Will Ferrell")
rt = re.compile("RT")

# print(pn2_pat.findall("asdfasdfsd   ina Fey"))

host = []
all_proper_nouns = []

for t in tweets:
    if host_pat.search(t):
        host.append(t)
        # if wf.search(t):
        #     try:
        #         print(t)
        #     except:
        #         pass
        if not rt.match(t):
            try:
                print(t)
            except:
                pass
            proper_nouns = pn2_pat.findall(t)
        for n in proper_nouns:
            all_proper_nouns.append(n)



# print(all_proper_nouns)
print(Counter(all_proper_nouns).most_common(10))
# pprint(host)
print(len(host))
