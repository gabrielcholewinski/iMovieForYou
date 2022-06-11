import pandas as pd

for i,chunk in enumerate(pd.read_csv('title.akas.tsv', sep="\t", chunksize=900000)):
    chunk.to_csv('chunk{}.tsv'.format(i), sep="\t", index=False)