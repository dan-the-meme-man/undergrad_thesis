import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# fetch annotated data
in_data = pd.read_excel(os.path.join('regex_data', 'regex_search_output.xlsx'))#, nrows=400)

# create figure directory if it doesn't exist
figs = os.path.join(os.getcwd(), 'figs')    
if not os.path.exists(figs):
    os.mkdir(figs)

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

def affix_ly(w): # function to add -ly to a potential zero form
    if w == 'good':
        return 'well' # special case: good -> well
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

# Create the figure and axes objects for the subplots
fig, axs = plt.subplots(2, 3, figsize=(10, 5))

# Adjust the spacing between the subplots
plt.subplots_adjust(wspace=0.4, hspace=0.9)

fig_ly, axs_ly = plt.subplots(2, 3, figsize=(10, 5))

# Adjust the spacing between the subplots
plt.subplots_adjust(wspace=0.4, hspace=0.9)

contingency = counts.pivot(index='word', columns='category', values='total_freq').fillna(0)

loc = [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2)]

i = 0
for w in ('bad', 'good', 'real', 'different', 'quick', 'sure'):
    #print(contingency.loc[w].values.reshape(1, -1))
    
    # grab data
    word_ly = affix_ly(w)
    c = counts[counts['word'] == w]
    c_ly = counts[counts['word'] == word_ly]
    bins = ['A', 'PREVB', 'POSTVB', 'PREJJ', 'POSTJJ', 'NPAM']
    heights = []
    heights_ly = []
    for bin in bins:
        try:
            heights.append(c[c['category'] == bin]['total_freq'].values[0])
        except:
            heights.append(0)
        try:
            heights_ly.append(c_ly[c_ly['category'] == bin]['total_freq'].values[0])
        except:
            heights_ly.append(0)

    # Create the first subplot
    ax = sns.barplot(x=bins, y=heights, ax=axs[loc[i][0],loc[i][1]])
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    axs[loc[i][0],loc[i][1]].set_title(w)
    axs[loc[i][0],loc[i][1]].set_xlabel('Categories')
    axs[loc[i][0],loc[i][1]].set_ylabel('Counts')

    # Create the second subplot
    ax_ly = sns.barplot(x=bins, y=heights_ly, ax=axs_ly[loc[i][0],loc[i][1]])
    ax_ly.set_xticklabels(ax.get_xticklabels(), rotation=45, horizontalalignment='right')
    if (w == 'quick'):
        ax_ly.set_yticklabels((0,3,6,9,12))
    axs_ly[loc[i][0],loc[i][1]].set_title(word_ly)
    axs_ly[loc[i][0],loc[i][1]].set_xlabel('Categories')
    axs_ly[loc[i][0],loc[i][1]].set_ylabel('Counts')
    
    i += 1
    
fig.savefig(os.path.join(figs, 'ZAM.png'), dpi=450, bbox_inches='tight')
fig_ly.savefig(os.path.join(figs, 'OAM.png'), dpi=450, bbox_inches='tight')