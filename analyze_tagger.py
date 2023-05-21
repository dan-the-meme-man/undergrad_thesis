import os
import pandas as pd

regex_data = pd.read_excel(os.path.join('regex_data', 'regex_search_output.xlsx'))#, nrows=100)
tagger_data = pd.read_csv(os.path.join('tagger_data', 'tagger_output.tsv'),
    sep='\t',
    header=None, names=('tokens', 'tags', 'confidence', 'raw'))#, nrows=100)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

all_data = pd.concat([regex_data, tagger_data], axis=1)

all_data = all_data.drop('raw', axis=1).drop('context', axis=1).drop('confidence', axis=1).drop(
    'Unnamed: 0', axis=1).drop('count', axis=1)

tp = 0 # human tagged adverb, tagger tagged adverb
fp = 0 # human tagged not adverb, tagger tagged adverb
tn = 0 # human tagged not adverb, tagger tagged not adverb
fn = 0 # human tagged adverb, tagger tagged not adverb

tp_rows = []
fp_rows = []
tn_rows = []
fn_rows = []

adv_tags = set(('POSTVB', 'PREJJ', 'PREVB', 'POSTJJ', 'NPAM'))

mistakes = 0

skip_words = set((
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
    #'well' # exclude this due to a possible disagreement with developers - is well an adverb, or an interjection here?
))

with open(os.path.join('tagger_data', 'agreements.tsv'), 'w') as agr:
    with open(os.path.join('tagger_data', 'disagreements.tsv'), 'w') as dis:
        
        agr.write('tokens\ttarget word\ttagger tag\thuman tag\ttp/tn\n')
        dis.write('tokens\ttarget word\ttagger tag\thuman tag\tfp/fn\n')

        for i, row in all_data.iterrows():
            
            target_word = row['word']
            
            if target_word in skip_words:
                continue
            
            tokens = str(row['tokens']) # get tokens
            
            tokens_list = tokens.split(' ') # get list of tokens
            
            try:
                target_word_idx = tokens_list.index(target_word) # get index of target word
            except:
                for j in range(len(tokens_list)):
                    if target_word in tokens_list[j]:
                        target_word_idx = j
                        break
            
            tags = str(row['tags']).split(' ') # get list of tags
            
            try:
                target_word_tag = tags[target_word_idx] # get tag of target word
            except:
                # a couple issues with proper nouns, fine to exclude anyway, not very interesting
                mistakes += 1
                continue
            
            human_tag = row['category'] # get human tag
            
            if human_tag in adv_tags: # human tagged adverb
                if target_word_tag == 'R': # tagger tagged adverb
                    tp += 1
                    agr.write(tokens + '\t' + target_word + '\t' + target_word_tag + '\t' + human_tag + '\ttp' + '\n')
                elif target_word_tag == 'A': # tagger tagged adjective
                    fn += 1
                    dis.write(tokens + '\t' + target_word + '\t' + target_word_tag + '\t' + human_tag + '\tfn' + '\n')
            elif human_tag == 'A': # human tagged adjective
                if target_word_tag == 'R': # tagger tagged adverb
                    fp += 1
                    dis.write(tokens + '\t' + target_word + '\t' + target_word_tag + '\t' + human_tag + '\tfp' + '\n')
                elif target_word_tag == 'A': # tagger tagged adjective
                    tn += 1
                    agr.write(tokens + '\t' + target_word + '\t' + target_word_tag + '\t' + human_tag + '\ttn' + '\n')

precision = tp / (tp + fp)
recall = tp / (tp + fn)
f1 = 2 * precision * recall / (precision + recall)

with open(os.path.join('tagger_data', 'stats.txt'), 'w') as f:
    f.write('tp: ' + str(tp) + '\n')
    f.write('fp: ' + str(fp) + '\n')
    f.write('tn: ' + str(tn) + '\n')
    f.write('fn: ' + str(fn) + '\n')
    f.write('precision: ' + str(precision) + '\n')
    f.write('recall: ' + str(recall) + '\n')
    f.write('f1: ' + str(f1) + '\n')
    f.write('mistakes: ' + str(mistakes) + '\n')
    
disagreements = pd.read_csv(os.path.join('tagger_data', 'disagreements.tsv'), sep='\t')
disagreements_by_word = disagreements.groupby(['target word','tagger tag'], as_index=False).count()
disagreements_by_word = disagreements_by_word.drop(['human tag', 'fp/fn'], axis=1)
disagreements_by_word['tokens'] = disagreements_by_word['tokens'].rename('count', inplace=True)
disagreements_by_word.to_csv(os.path.join('tagger_data', 'disagreements_by_word.tsv'), sep='\t', index=False)