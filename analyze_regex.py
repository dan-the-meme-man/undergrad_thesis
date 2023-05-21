import os
import pandas as pd
from scipy.stats import chi2_contingency

# fetch annotated data
in_data = pd.read_excel(os.path.join('regex_data', 'key_results.xlsx'))#, nrows=400)

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

adv = in_data.where(in_data['category'] != 'A')

allowed = adv.where(in_data['category'] != 'POSTJJ').where(in_data['category'] != 'PREVB').dropna()
disallowed = adv.where(in_data['category'] != 'POSTVB').where(in_data['category'] != 'PREJJ').where(in_data['category'] != 'NPAM').dropna()

allowed = allowed.groupby(['word'], as_index=False).agg('sum')
disallowed = disallowed.groupby(['word'], as_index=False).agg('sum')

allowed.drop(columns=['Unnamed: 0'], inplace=True)
disallowed.drop(columns=['Unnamed: 0'], inplace=True)

words = sorted(list(set(allowed['word']).union(set(disallowed['word']))))

a_dict = dict.fromkeys(words, 0)
b_dict = dict.fromkeys(words, 0)

for word in words:
    if word in list(allowed['word']):
        a_dict[word] = allowed.loc[allowed['word'] == word, 'total_freq'].iloc[0]
    else:
        b_dict[word] = disallowed.loc[disallowed['word'] == word, 'total_freq'].iloc[0]