import pandas as pd
import numpy as np
import sys
from tqdm import tqdm
import elasticsearch
from elasticsearch import Elasticsearch
import json
es=Elasticsearch('ELASTIC SEARCH URL:PORT here. something like http://localhost:9200', timeout=120)
from more_itertools import chunked
import json

def replace_punct_chars(term):
    # we replace these characters since Elastic Search tokenizes a-b as 'a b' thus not matching a-b
    term = term.replace('-','_')
    term = term.replace('.','_')
    term = term.replace(',','_')
    term = term.replace("'",'_')
    return term

def get_innovation_years(term, h, get_full_metadata=False):
    word1, word2 = term.split()
    total_hits=h['hits']['total']['value']
    if total_hits > 0:
       introduced_thesis_id = h['hits']['hits'][0]['_id']
       introduced_year = h['hits']['hits'][0]['_source']['year']
       all_metadata = []
       only_matched_metadata = []
       if get_full_metadata:
          for hit in h['hits']['hits']:
              docid = hit['_id']
              docyear = hit['_source']['year']
              toks = set(hit['_source']['body']['text'].split(' '))
              if (word1 in toks) and (word2 in toks):
                 only_matched_metadata.append((docid, docyear))
              all_metadata.append((docid, docyear))
          uptakes = len(only_matched_metadata) - 1
       else:
          uptakes = total_hits - 1
       return introduced_thesis_id, introduced_year, json.dumps(all_metadata), json.dumps(only_matched_metadata), uptakes 
    else:
       return None, None, None, None, None


def process_input_df_chunk(input_df, output_innovations_file):
    input_df=input_df.dropna()
    input_df["term"]=input_df["word1"] + ' ' + input_df["word2"]
    chunks=list(chunked(input_df.term.values, 50000))
    all_recs=[]
    for chunk in tqdm(chunks, total=len(chunks)):
        search_arr=[]
        for term in chunk:
            rterm = replace_punct_chars(term)
            search_arr.append({'index':'proquest_pnas_index_hyphen_removed_filtered'})
            search_arr.append({"query": {'query_string':{'query':rterm,'default_operator':'AND'}}, 'sort':'year', 'size': 1, 'track_total_hits':True})
        request = ''
        for each in search_arr:
            request += '%s \n' %json.dumps(each)
        resp = es.msearch(body = request)
        recs=[]
        for t,r in zip(chunk,resp['responses']):
            recs.append([t.split()[0], t.split()[1]] + list(get_innovation_years(t,r)))
        all_recs.extend(recs)
    odf = pd.DataFrame().from_records(all_recs, columns=['word1', 'word2','introduced_thesis_id','introduced_year','all_metadata', 'only_matched_metadata','uptakes'])
    odf.to_csv(output_innovations_file, sep='\t', encoding='utf-8', chunksize=1000000)

input_innovations_file=sys.argv[1] #Input file of dyads. 
output_innovations_file=sys.argv[2]
input_df_chunks=pd.read_csv(input_innovations_file, sep='\t', encoding='utf-8', index_col=0, chunksize=1000000)
for ix, input_df in enumerate(input_df_chunks):
    print("Processing chunk", ix)
    process_input_df_chunk(input_df, '{}_{}'.format(output_innovations_file, ix))
