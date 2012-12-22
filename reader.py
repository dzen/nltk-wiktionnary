"""
    Convenient script to load the corpus
"""

from nltk.corpus.reader.tagged import TaggedCorpusReader
from nltk.tokenize import LineTokenizer
reader = TaggedCorpusReader('.', ['corpus'], word_tokenizer=LineTokenizer())
import ipdb ; ipdb.set_trace()
