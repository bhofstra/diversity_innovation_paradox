from elasticsearch import Elasticsearch
import pandas as pd
import more_itertools
import tqdm
import os
import sys
import pickle
import csv
import re
from collections import Counter
import time
from io import open
from elasticsearch.helpers import bulk, streaming_bulk, parallel_bulk

## NOTE: You need to ensure you have an Elastic Search server instance running.
es = Elasticsearch('http://localhost:9200') 
es.cluster.health(wait_for_status='yellow', request_timeout=60)
es.indices.delete(index='proquest_pnas_index_hyphen_removed_filtered', ignore=[400, 404])
full_df=pd.read_csv('Properly filtered and tokenized file of ProQuest theses data in Tab seperated format here', sep='\t', usecols=['ProQuest Thesis ID','ThesisYear','filtered_abstract'], dtype={'ProQuest Thesis ID':str,}, encoding='utf-8')
full_df.rename(columns={'ProQuest Thesis ID':'thesis_id'}, inplace=True)
print(Counter(full_df.ThesisYear.values))
print("Loaded data frames")
def gen_data():
    for row in tqdm.tqdm(full_df.itertuples(), total=len(full_df)):
        doc_id = row.thesis_id
        content = row.filtered_abstract.replace('-','_')
        content = content.replace(',','_')
        content = content.replace('.','_')
        content = content.replace("'",'_')
        year = row.ThesisYear
        yield {"_index":'proquest_pnas_index_hyphen_removed_filtered', "_id":doc_id, "body":{'text':content},'year':year}   

from collections import deque
for chunk in more_itertools.chunked(gen_data(), 100000):
    deque(parallel_bulk(es, chunk, thread_count=10, request_timeout=600), maxlen=0)
