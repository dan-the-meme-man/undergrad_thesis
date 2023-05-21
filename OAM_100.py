import os
import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

def affix_ly(w): # function to add -ly to a potential zero form
    if w == 'good':
        return 'well'
    elif w.endswith('y'): # special case: happy -> happily
        return w[:-1] + 'ily'
    elif w.endswith('le'): # special case: terrible -> terribly
        return w[:-1] + 'y'
    elif w.endswith('ic'): # special case: tragic -> tragically
        return w + 'ally'
    elif w.endswith('ue'): # special case: true -> truly
        return w[:-1] + 'ly'
    else:
        return w + 'ly' # general case: sad -> sadly

no_ly = pd.read_excel(os.path.join('regex_data', 'no_ly_only.xlsx'))#, nrows=400)
ly = pd.read_excel(os.path.join('regex_data', 'ly_only.xlsx'))#, nrows=400)

no_ly_adv = no_ly[no_ly['category'] != 'A']
ly_adv = ly[ly['category'] != 'A']

for i, row in no_ly_adv.iterrows():
    a = affix_ly(row['word'])
    if a in ly_adv['word'].values:
        ly_adv.drop(ly_adv[ly_adv['word'] == a].index, inplace=True)
        
ly_adv.sort_values(by=['total_freq'], ascending=False, inplace=True)

ly_adv.to_excel(os.path.join('regex_data', 'OAM_100_by_category.xlsx'), index=True) # save to spreadsheet

ly_adv = ly_adv.groupby(['word'], as_index=False).agg('sum')

ly_adv.drop(columns=['Unnamed: 0'], inplace=True)

ly_adv.sort_values(by=['total_freq'], ascending=False, inplace=True)

ly_adv.to_excel(os.path.join('regex_data', 'OAM_100.xlsx'), index=True) # save to spreadsheet