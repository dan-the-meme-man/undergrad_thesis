import os
import pandas as pd

if not os.path.exists(os.path.join(os.getcwd(),'tagger_data')):
    os.mkdir('tagger_data')

in_data = pd.read_excel(os.path.join('regex_data', 'regex_search_output.xlsx'))

with open(os.path.join('tagger_data', 'tagger_raw_data.txt'), 'w') as f:
    for i in range(len(in_data)):
        f.write(f'{in_data["context"][i]}\n')