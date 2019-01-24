import json
import nltk
import re
from nltk import word_tokenize
from nltk.text import Text


from pprint import pprint

raw = "the project gutenberg ebook is available for free. the fork is in the raw chicken"

tokens = word_tokenize(raw)

#d = Text(raw)

with open('gg2013.json') as f:
    data = json.load(f)

texts = []
for d in data:
    texts.append(d['text'])

texts = list(set(texts))
    

matches = [re.search(' host', text) for text in texts]

def index_return(array):
    listofindices = []
    for i in range(len(array)):
        if array[i] != None:
            listofindices.append(i)
    return listofindices

processed = ''
l = index_return(matches)
for i in l:
    processed += texts[i]

sentences = nltk.sent_tokenize(processed) 
sentences = [nltk.word_tokenize(i) for i in sentences]
sentences = [nltk.pos_tag(i) for i in sentences]

name_grammar = 'Name: {<NNP><NNP>}'
cp = nltk.RegexpParser(name_grammar)

def get_names(tree):
    listofnames = []
    for subtree in tree:
        if type(subtree) is nltk.Tree:
            if subtree.label() == 'Name':        
                name = subtree[0] + subtree[1]
                listofnames.append(name)   
    
    for i in range(len(listofnames)):
        listofnames[i] = listofnames[i][0] + ' ' + listofnames[i][2]
        
    return listofnames
            
host_names = [get_names(cp.parse(sentence)) for sentence in sentences]

tina_fey_count = 0
amy_poehler_count = 0

def count(name_list, name):
    name_count = 0
    for i in name_list:
        for j in i:
            if j == name:
                name_count += 1
    return name_count

def highest_count(name_list):
    name_set = set()
    for i in name_list:
        for j in i:
            if j not in name_set:
                name_set.add(j)
    
    counts = dict()
    for name in name_set:
        counts[name] = count(name_list, name)
    
    return max(counts, key=counts.get)
        

#z = ""
#for t in texts:
#    z += t
#
#token = word_tokenize(z)
#
#text = Text(token)
#
#text.concordance("host")
