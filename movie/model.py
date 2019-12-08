import metapy
import os
# with open('description/tutorial.toml', 'w') as f:
#     f.write('type = "line-corpus"\n')
#     f.write('store-full-text = true\n')

# config = """prefix = "." # tells MeTA where to search for datasets

# dataset = "description" # a subfolder under the prefix directory
# corpus = "tutorial.toml" # a configuration file for the corpus specifying its format & additional args

# index = "idx" # subfolder of the current working directory to place index files

# stop-words = "lemur-stopwords.txt"

# [[analyzers]]
# method = "ngram-word"
# ngram = 1
# filter = "default-unigram-chain"

# """
# with open('description-config.toml', 'w') as f:
#     f.write(config)

print(os.getcwd())
inv_idx = metapy.index.make_inverted_index('description-config.toml')
import math
class BM25(metapy.index.RankingFunction):
    def __init__(self, k1 = 1.2, b = 0.2, k3 = 500, delta = 1.0):                                             
        self.k1 = k1
        self.b = b
        self.k3 = k3
        self.delta = 1.0
        # You *must* invoke the base class __init__() here!
        super(BM25, self).__init__()                                        
                                                                                 
    def score_one(self, sd):
        """
        sd.avg_dl: average document length of the collection
        sd.num_docs: total number of documents in the index
        sd.total_terms: total number of terms in the index
        sd.query_length: the total length of the current query (sum of all term weights)
        sd.query_term_weight: query term count (or weight in case of feedback)
        sd.doc_count: number of documents that a term t_id appears in
        sd.corpus_term_count: number of times a term t_id appears in the collection
        sd.doc_term_count: number of times the term appears in the current document
        sd.doc_size: total number of terms in the current document
        sd.doc_unique_terms: number of unique terms in the current document
        
        """
        k1 = self.k1
        b = self.b
        k3 = self.k3
        delta = self.delta
        N = sd.num_docs
        df = sd.doc_count
        ctd = sd.doc_term_count
        D = sd.doc_size
        avdl = sd.avg_dl
        ctq = sd.query_term_weight
        
        return math.log((N+1)/(df)) * ((k1+1)*ctd/(k1*(1-b+b*D/avdl)+ctd) + delta) * (k3+1)*ctq/(k3+ctq)

query_input = 'jack and rose'
ranker = BM25()
query_in = query_input
query = metapy.index.Document()
query.content(query_in)
top_docs = ranker.score(inv_idx, query, num_results=5)
for num, (d_id, _) in enumerate(top_docs):
    content = inv_idx.metadata(d_id).get('content')
    print("{}. {}\n".format(num + 1, content))