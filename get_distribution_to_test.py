import os

coraal = os.path.join(os.getcwd(), 'coraal')

d = dict.fromkeys(['ATL', 'DCA', 'DCB', 'DCA', 'LES', 'PRV', 'ROC', 'VLD'], 0)

for file in os.listdir(coraal):
    
    if not file.endswith('.txt'):
        continue
    
    loc = os.path.join('coraal', file)
    
    key = file[:3]
    d[key] += os.path.getsize(loc)
    
total = sum(d.values())
    
total_to_read = total / 10 # read 10%

for k in d:
    d[k] /= total # proportions
    print (k, d[k]*100)
    d[k] *= (total_to_read/1024) # 10% of total in KB
    #print (k, d[k])
    
"""
ATL 147.03544921875002
-> ATL_se0_ag2_f_02_1, ATL_se0_ag1_m_04_1
-> 98 + 50 = 148

DCA 593.816796875
-> DCA_se1_ag4_m_02_1, DCA_se1_ag1_f_04_1, DCA_se2_ag3_m_03_1, DCA_se2_ag1_f_03_1, DCA_se1_ag1_m_08_1, DCA_se3_ag1_f_02_1
-> 126 + 124 + 117 + 117 + 57 + 55 = 596

DCB 879.7040039062501
-> DCB_se3_ag3_m_02_1, DCB_se2_ag2_f_02_1, DCB_se3_ag3_f_01_1, DCB_se1_ag1_m_02_1
-> 232 + 231 + 209 + 208 = 880

LES 159.11875
-> LES_se0_ag3_m_01_1, LES_se0_ag4_f_01_1
-> 126 + 42 = 168

PRV 260.75078125
-> PRV_se0_ag1_m_01_1, PRV_se0_ag1_f_02_1
-> 133 + 131 = 264

ROC 252.18349609375002
-> ROC_se0_ag3_f_01_1, ROC_se0_ag2_m_01_3, ROC_se0_ag2_m_01_1, ROC_se0_ag2_m_01_4
-> 131 + 64 + 40 + 29 = 264

VLD 207.58916015625002
-> VLD_se0_ag3_m_02_1, VLD_se0_ag3_f_01_1
-> 128 + 126 = 254

"""