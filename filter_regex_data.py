import os
import pandas as pd
from scipy.stats import chi2_contingency, binomtest
import matplotlib.pyplot as plt
from numpy import arange

# fetch annotated data
in_data = pd.read_excel(os.path.join('regex_data', 'regex_search_output.xlsx'))#, nrows=400)

# get frequency counts based on word and category
try:
    counts = in_data.value_counts(subset=['word', 'category', 'count']).to_frame().reset_index()
except:
    print('No data found. The spreadsheet may be unannotated. A "category" column is required, as well as a "count" column for instances with multiple uses.')
    exit()
    
# rename column
counts.rename(columns={0: 'freq'}, inplace=True)

# easier to read
counts.sort_values(by=['word', 'category'], inplace=True)

# add up instances with multiple or single uses
counts['total_freq'] = counts['count'] * counts['freq']

# no longer need this separately
counts.drop(columns=['count', 'freq'], inplace=True)

# merge counts for instances with multiple or single uses
counts = counts.groupby(['word', 'category'], as_index=False).agg('sum')

# define percentage of total frequency
counts['percent'] = 100 * counts['total_freq'] / counts.groupby(['word'])['total_freq'].transform('sum')

#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)

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
))

filtered_counts = counts.where(
    #counts['percent'] != 100).where( # exclude words that are always the same category
    #counts['total_freq'] != 1).where( # exclude singletons optionally
    counts['category'] != 'N').where( # exclude words that weren't adj/adv
    counts['category'] != 'V').where(
    counts['category'] != 'E').where(
    counts['category'] != 'P').where(
    counts['category'] != '???').where(
    counts['category'] != '?').where(
    counts['category'] != 'C').where(
    counts['category'] != 'ASP').dropna()
    
filtered_counts = filtered_counts[~filtered_counts['word'].isin(skip_words)]
    
filtered_counts.to_excel(os.path.join('regex_data', 'all_results.xlsx'))

#mask = filtered_counts['word'].duplicated(keep=False) # deleting words that are used in one way only

#filtered_counts = filtered_counts.drop(filtered_counts[~mask].index)

mask = filtered_counts['word'].str.match(r'^.*ly$|^well$') # looking just at words that are not -ly forms (including well, which is grouped with -ly forms)

no_ly = filtered_counts[~mask]
no_ly.to_excel(os.path.join('regex_data', 'no_ly_only.xlsx'))
no_ly_cats = no_ly.drop('percent', axis=1).groupby('category').agg('sum')
no_ly_cats.to_excel(os.path.join('regex_data', 'no_ly_only_by_category.xlsx'))

no_ly_key = no_ly.where(counts['percent'] != 100).dropna()
no_ly_key.to_excel(os.path.join('regex_data', 'key_results.xlsx'))

ZAM = no_ly[no_ly['category'] != 'A'].dropna()
ZAM.to_excel(os.path.join('regex_data', 'ZAM_results.xlsx'))

ly = filtered_counts[mask]
ly.to_excel(os.path.join('regex_data', 'ly_only.xlsx'))
ly_cats = ly.drop('percent', axis=1).groupby('category').agg('sum')
ly_cats.to_excel(os.path.join('regex_data', 'ly_only_by_category.xlsx'))

ly_cat_counts = ly_cats['total_freq'].tolist()
no_ly_cat_counts = no_ly_cats['total_freq'].tolist()

data = [ly_cat_counts, no_ly_cat_counts]

with open(os.path.join('regex_data', 'significance.txt'), 'w') as f:
    stat, p, dof, exp = chi2_contingency(data)
    f.write('chi2 statistic: ' + str(stat) + '\n')
    f.write('p-value: ' + str(p) + '\n')
    f.write('degrees of freedom: ' + str(dof) + '\n')
    f.write('expected counts:\n')
    
    cats = ['A',    'NPAM',      'POSTJJ',  'POSTVB',    'PREJJ',     'PREVB']
    hyps = ['less', 'two-sided', 'greater', 'two-sided', 'two-sided', 'greater']
    # less = no-ly, greater = ly
    
    for i in range(len(cats)): # written as no-ly, ly
        f.write(cats[i] + '\t' + str(exp[1][i]) + '\t' + str(exp[0][i]) + '\n')
    f.write('\n')
    
    f.write('category\tstatistic\tp-value\tconfidence interval\n')
    
    plt.figure()
    
    for i in range(len(data[0])):
        result = binomtest(int(data[0][i]), int(data[0][i] + data[1][i]), alternative=hyps[i])
        stat = result.proportion_estimate
        p = result.pvalue
        ci = result.proportion_ci()
        f.write(cats[i] + '\t' + str(stat) + '\t' + str(p) + '\t' + str(ci) + '\n')
        plt.plot((ci.low, ci.high), (i,i), 'ko-', label=cats[i])
    
    plt.xticks(arange(0, 1.1, 0.1))
    plt.yticks(range(len(data[0])), cats)
    plt.grid()
    plt.title('Confidence intervals for proportion of adverbs in each environment')
    plt.xlabel('Expected preference for OAM')
    plt.ylabel('Syntactic environment')
    plt.savefig(os.path.join(os.getcwd(), 'figs', 'confidence_intervals.png'), dpi=450, bbox_inches='tight')