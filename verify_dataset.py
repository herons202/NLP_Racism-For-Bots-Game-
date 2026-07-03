import pandas as pd

df = pd.read_csv('racism_dataset_additional.csv', encoding='utf-8')
print('=== Dataset Tambahan ===')
print('Total baris  :', len(df))
print('HS_Race = 1  :', (df['HS_Race']==1).sum())
print('HS_Race = 0  :', (df['HS_Race']==0).sum())
print()

df2 = pd.read_csv('re_dataset.csv', encoding='latin-1')
print('=== Dataset Utama ===')
print('Total baris  :', len(df2))
print('HS_Race = 1  :', (df2['HS_Race']==1).sum())
print('HS_Race = 0  :', (df2['HS_Race']==0).sum())
print()

keep = ['Tweet','HS','Abusive','HS_Individual','HS_Group','HS_Religion',
        'HS_Race','HS_Physical','HS_Gender','HS_Other','HS_Weak','HS_Moderate','HS_Strong']
df2['Source'] = 're_dataset'
df_all = pd.concat([df2[keep + ['Source']], df[keep + ['Source']]], ignore_index=True)
print('=== Dataset Gabungan ===')
print('Total baris  :', len(df_all))
print('HS_Race = 1  :', (df_all['HS_Race']==1).sum())
print('HS_Race = 0  :', (df_all['HS_Race']==0).sum())
ratio = (df_all['HS_Race']==0).sum() / (df_all['HS_Race']==1).sum()
print('Rasio imbalance:', round(ratio, 2))
print('Sukses! Dataset siap digunakan.')
