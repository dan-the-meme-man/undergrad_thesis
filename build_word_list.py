"""
This script generates a list of adjectives and adverbs that are found in CORAAL.
It uses NLTK's implementation of WordNet as a source for potential words.
It reduces this list to adverbs ending in -ly, adjectives corresponding to those -ly forms, and adjectives ending in -y.
The last group contains words such as 'happy', which has a stem change in 'happy'->'happily'.
It also manually adds 'good' and 'well' to the list, because they are irregular, but behave like an -ly/non-ly pair.
It then further filters the list to only include words that are found in CORAAL.

Outputs adjectives.txt (list of all candidate adjectives), adverbs.txt (list of all candidate adverbs), and word_list.txt (filtered).
Runs in ~ 15 minutes on my machine.
"""

import os
import re
from nltk.corpus import wordnet as wn

# UNCOMMENT THIS IF YOU DON'T HAVE THE NLTK DATA
"""
import nltk
nltk.download('wordnet')
nltk.download('omw-1.4')
"""

def make_output_dir(output_dir: str): # make the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    return output_dir

input_dir = 'coraal_clean' # cleaned CORAAL files directory
output_dir = make_output_dir('data') # output directory

def affix_ly(w): # function to add -ly to a potential zero form
    if w.endswith('y'): # special case: happy -> happily
        return w[:-1] + 'ily'
    elif w.endswith('le'): # special case: terrible -> terribly
        return w[:-1] + 'y'
    elif w.endswith('ic'): # special case: tragic -> tragically
        return w + 'ally'
    elif w.endswith('ue'): # special case: true -> truly
        return w[:-1] + 'ly'
    else:
        return w + 'ly' # general case: sad -> sadly

adjectives = list(wn.all_lemma_names(pos=wn.ADJ, lang='eng')) # adj list from WordNet
adverbs = list(wn.all_lemma_names(pos=wn.ADV, lang='eng')) # adv list from WordNet

potential_set = set(('good', 'well')) # set which will contain all potential adverbs, including zero forms

for adj in adjectives: # for all potential zero forms
    adv = affix_ly(adj) # form potential -ly form
    if adv in adverbs: # if the overt form is in WordNet
        potential_set.add(adj) # add zero form to set of potential adverbs
        potential_set.add(adv) # add ly form to set of potential adverbs

final_set = set() # empty set to hold final set of adverbs after filtering process

try:
    files = os.listdir(input_dir)
except:
    print('Please run preprocess.py first.')
    exit()

for f in files: # clean garbage if needed
    if not f.endswith('.txt'):
        files.remove(f)
    
num_files = len(files)

for i in range(len(files)): # check each file of CORAAL, one at a time
    with open(os.path.join(input_dir, files[i]), 'r') as f:
        lines = ' ' + f.read() + ' ' # read whole file for efficiency, pad with spaces for regex
        
        for w in potential_set: # check each form that has not been found yet one at a time
            exp = re.compile(r'\W' + w + r'\W', re.IGNORECASE) # compile regex to look for word
            
            if exp.search(lines): # if we find the word in the file
                final_set.add(w) # add to final set
                
        potential_set -= final_set # remove forms that have been found from set of potential forms
        
        print(f'Processed file {i+1}/{num_files} with {len(final_set)} adverb forms found so far.') # print progress

to_remove = set((
    'atypical',
    'atypically',
    'fine',
    'finely',
    'elementary',
    'elementarily',
    'even',
    'evenly',
    'first',
    'firstly',
    'hard',
    'hardly',
    'high',
    'highly',
    'inaudible',
    'inaudibly',
    'just',
    'justly',
    'kind',
    'kindly',
    'late',
    'lately',
    'laughing',
    'laughingly',
    'like',
    'likely',
    'mocking',
    'mockingly',
    'most',
    'mostly',
    'only',
    'over',
    'overly',
    'poor',
    'poorly',
    'pretty',
    'prettily',
    'right',
    'rightly',
    'short',
    'shortly',
    'single',
    'singly',
    'unintelligible',
    'unintelligibly',
    'very',
    'verily'
))

with open(os.path.join(output_dir, 'word_list.txt'), 'w') as f: # write final list to file
    for w in sorted(list(final_set)):
        if len(w) > 2 and w not in to_remove: # filter out impossibly short words
            f.write(w + '\n')