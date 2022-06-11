import pandas as pd
import os, glob

title2 = pd.read_csv('title.akas.tsv', sep='\t', low_memory=False, quoting=3)

# # title2 = title2.drop(['types','attributes','isOriginalTitle'], axis=1)

# # title2.to_csv('title.akas.csv',index = False)

# path = r'C:\Users\123456789\Desktop\new\new\chunkyakas'


# all_files = glob.glob(os.path.join(path, "chunk*.csv"))
# df_from_each_file  = (pd.read_csv(f, sep='\t') for f in all_files)
# df_merged   = pd.concat(df_from_each_file, ignore_index=True)
# df_merged.to_csv( "title.akas.csv")

title2['title'] = title2['title'].replace(',','', regex=True)
title2['title'] = title2['title'].replace('"','', regex=True)
title2['title'] = title2['title'].replace(';','', regex=True)

title2.to_csv('titles.akas.csv',sep=',', index = False)

# for f in all_files:


# path = r'C:\Users\123456789\Desktop\new\new\chunkyakas'

# all_files = glob.glob(os.path.join(path, "chunk*.csv"))

# all_df = []
# for f in all_files:
#     print(f)
#     df = pd.read_csv(f, sep='\t')
#     all_df.append(df)
    
# merged_df = pd.concat(all_df, ignore_index=True, sort=True)
# merged_df.to_csv( "title.akas.csv")
