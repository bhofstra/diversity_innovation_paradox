import pandas as pd
import numpy as np
import swifter
import sys
import numpy as np
import scipy as sp
import math
from argparse import ArgumentParser
import glob
import json
import tqdm

def main(args):
    emb_df = pd.read_csv(args.innovation_atypicality_file, sep='\t', encoding='utf-8', usecols=['word1', 'word2', 'concept','emb_score'], index_col=0, nrows=10000000)
    print("Loaded atypicality file", args.innovation_atypicality_file)
    uptakes_df = pd.read_csv(args.innovation_uptakes_file, sep='\t', encoding='utf-8', index_col=0, dtype={'introduced_thesis_id':str})
    print("Loaded uptakes file", args.innovation_uptakes_file)
    uptakes_df['concept'] = uptakes_df["word1"]+'@'+uptakes_df["word2"]
    mdf = pd.merge(emb_df[["concept", "emb_score"]], uptakes_df[["concept","introduced_thesis_id","introduced_year","uptakes"]], on='concept')
    print("Merged")
    mdf.dropna(inplace=True)
    print("Dropped NA and dumping")
    mdf.to_csv(args.output_inno_level_file, sep='\t', encoding='utf-8', chunksize=1000000)
    agg_df = mdf.groupby('introduced_thesis_id').agg({'concept':len, 'introduced_year':lambda x: x.iloc[0], 'uptakes':np.sum, 'emb_score':np.mean})
    agg_df = agg_df.reset_index()
    agg_df.rename(columns={'concept':'num_inno'}, inplace=True)
    agg_df.to_csv(args.output_group_file, sep='\t', encoding='utf-8', chunksize=1000000)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--innovation_atypicality_file", dest="innovation_atypicality_file", help="List of innovations with atypicality")
    parser.add_argument("--innovation_uptakes_file", dest="innovation_uptakes_file", help="Output file")
    parser.add_argument("--output_group_file", dest="output_group_file", help="Output group file")
    parser.add_argument("--output_inno_level_file", dest="output_inno_level_file", help="Output innovation file with atypicality scores")
    args = parser.parse_args()
    main(args)
