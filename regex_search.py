import os
import re
import pandas as pd

input_dir = 'coraal_clean' # cleaned CORAAL files directory
output_dir = 'regex_data' # data directory

try:
    files = os.listdir(input_dir) # list of files
except:
    print('Please run preprocess.py first.')
    exit()

try:
    word_list = open(os.path.join(output_dir, 'word_list.txt'), 'r').read().splitlines() # word list
except:
    print('Please run build_word_list.py first.')
    exit()

num_files = len(files) # number of files

df = pd.DataFrame(columns=('file', 'word', 'context')) # empty dataframe

for i in range(len(files)): # loop over all files
    
    with open(os.path.join(input_dir, files[i]), 'r') as f: # open a file
        
        lines = ' ' + f.read() + ' ' # read the whole file into memory for efficiency, pad with spaces for regex
        
        for word in word_list: # look for word and capture context as well
            exp = re.compile(r'[\s\S]{,30}[\W]' + word + r'[\W][\s\S]{,30}', re.IGNORECASE)
            match = re.findall(exp, lines)
            for m in match:
                df.loc[len(df.index)] = [files[i], word, m.replace('\n', ' ')] # save examples to dataframe
                
    print(f'Processed file {i+1}/{num_files} with {len(df.index)} words found so far.') # print progress
        
df = df.drop_duplicates(subset='context', keep='first') # drop duplicates

df.sort_values(by=['word'], inplace=True) # sort by word

df.to_excel(os.path.join(output_dir, 'regex_search_output.xlsx'), index=True) # save to spreadsheet