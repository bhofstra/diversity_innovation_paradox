# coding: utf-8
import gensim
import pandas as pd
from gensim.models import ldaseqmodel
from gensim.corpora import Dictionary, bleicorpus
import numpy
from gensim.matutils import hellinger
from gensim.parsing.preprocessing import remove_stopwords
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
from gensim.models.word2vec import Word2Vec
from argparse import ArgumentParser
from gensim.utils import ClippedCorpus

class PlainNGramsCorpus(object):
    def __init__(self, filename):
        self.file=filename
    def __iter__(self):
        f=open(self.file)
        for line in f:
            line=line.strip()
            line=line.replace('\n','')
            line=line.replace('\t','')
            line=line.replace('\r','')
            toks=line.split(' ')
            yield toks[:]



def main(args):
    input_file = args.input_file
    output_file = args.output_file
    min_count = args.min_count
    c=PlainNGramsCorpus(input_file)
    m=gensim.models.Word2Vec(sentences=c, sg=1, workers=16,iter=5, min_count=min_count, max_vocab_size=None)
    m.wv.save_word2vec_format(output_file)

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--input_file", dest="input_file", help="Input file")
    parser.add_argument("--output_file", dest="output_file", help="Output file")
    parser.add_argument("--min_count", dest="min_count", default=5, type=int, help="minimum count")
    args = parser.parse_args()
    main(args)
