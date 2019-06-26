#Search Engine

#import redis
import re
import math
import sys
import PythonGui 
import Tkinter as tk


#index = redis.Redis(host = 'localhost', port = 6379, db = 0)
all_tokens = list() # All tokens from each document
df_dict = dict() # Document frequency of each token


# Creates dictionary of {token: term frequency} per document
def count_tok_dict(tok_list):
    tok_dict = dict()
    for tok in tok_list:
        if tok in tok_dict:
            tok_dict[tok] += 1
        else:
            tok_dict[tok] = 1
    return tok_dict


# String of indices per token separated by periods
def find_indices(tok_list, term):
    indices = ''
    for i in range(len(tok_list)):
        if tok_list[i] == term:
            indices += str(i) + '.'
    return indices


# Calculates TF*IDF of each token
def calculate_tfidf(tok_list, tok_dict, term):
    doc_count = 0
    tf = float(tok_dict[term])/len(tok_list)
    values = df_dict[term].split()
    doc_count = int(values[0])
    idf = math.log(37497.0/doc_count) #37497
    return tf * idf


# Creates dictionary of {token: document frequency}
def create_df_dict():
    doc = 0
    for doc_list in all_tokens:
        for tok in doc_list:
            if tok not in df_dict:
                df_dict[tok] = str(1) + ' ' + str(doc)
            else:
                values = df_dict[tok].split()
                if int(values[1]) != doc:
                    df_dict[tok] = str(int(values[0]) + 1) + ' ' + str(doc)
        doc += 1


# Creates list of tokens per document
def create_tok_list():
    for folder in range(75):
        for doc in range(500):
            pathname = '/Users/ben/Desktop/WEBPAGES_RAW/'+str(folder)+'/'+str(doc)
            tok_list = list()
            try:
                with open(pathname, 'r') as html_file:
                    for line in html_file:
                        new_text = re.sub('<[^<>]+>|[^ a-zA-Z]', ' ', line.lower())
                        tok_list.extend(new_text.split())
            except:
                pass
            all_tokens.append(tok_list)


# Creates index using token and metadata (doc name, term frequency, indices, tfidf)
def create_index():
    global index
    folder = 0
    doc = 0
    index.flushdb()
    create_tok_list()
    create_df_dict()
    for list_doc in all_tokens:
        tok_dict = count_tok_dict(list_doc)
        for term in tok_dict:
            metadata = ''
            document = str(folder) + '/' + str(doc)
            freq = str(tok_dict[term])
            indices = str(find_indices(list_doc, term))
            tfidf = str(calculate_tfidf(list_doc, tok_dict, term))
            metadata += document+','+freq+','+indices+','+tfidf+';'
            index.append(term, metadata)
        doc += 1
        if doc > 499:
            doc = 0
            folder += 1


# Sort by cosine similarity
def sort_cossim(x):
    return x[1]


# Gets the TF-IDF of the query
def query_tfidf(query_list):
    tfidf_list = list()
    for query in query_list:
        tf = float(query_list.count(query))/len(query_list)    
        postings = index.get(query)
        doc_count = len(postings.split(';')[:-1])
        idf = math.log(37497.0/doc_count)
        tfidf_list.append(tf*idf)
    return tfidf_list


# Combines all postings of the query and returns a list of TF-IDF
def combine_postings(query_list):
    query_postings = list()
    query_docs = list()
    doc_tfidf = dict()
    for query in query_list:
        postings = index.get(query)
        metadata = [r.split(',') for r in postings.split(';')][:-1]
        query_postings.append(metadata)
        docs = [docs[0] for docs in metadata]
        query_docs.append(docs)
    and_docs = set(query_docs[0])
    for i in range(len(query_docs)-1):
        and_docs = and_docs & set(query_docs[i+1])
    and_docs = list(and_docs)    
    for query in query_postings:
        for docs in query:
            if docs[0] in and_docs:
                if docs[0] not in doc_tfidf:
                    doc_tfidf[docs[0]] = [float(docs[-1])]
                else:
                    doc_tfidf[docs[0]].append(float(docs[-1]))
    return doc_tfidf


# Calculates cosine similarity of the query and a document
def cosine_similarity(query, doc):
    dot_product = 0
    query_mag = 0
    doc_mag = 0
    for i in range(len(query)):
        dot_product += query[i] * doc[i]
        query_mag += query[i]**2
        doc_mag += doc[i]**2
    query_magnitude = math.sqrt(query_mag)
    doc_magnitude = math.sqrt(doc_mag)
    return dot_product/(query_magnitude*doc_magnitude)


# Retrieves top 20 search results
def retrieve_query():
    results = list()
    gui_query = PythonGui.entry_box.get().split()
    query_list = [x.lower() for x in gui_query]
    sub_query = list()
    for q in query_list:
        q = re.sub('[^a-z]', '', q)
        if q != '':
            sub_query.append(q)
    try:
        query = query_tfidf(sub_query)
        doc_tfidf = combine_postings(sub_query)
        for doc in doc_tfidf:
            cos_sim = cosine_similarity(query, doc_tfidf[doc])
            results.append((doc, cos_sim))
        top_results = sorted(results, key=sort_cossim, reverse=True)[:20]
        top_url = list()
        for result in top_results:
            with open('/Users/ben/Desktop/WEBPAGES_RAW/bookkeeping.tsv', 'r') as bookkeeping:
                for line in bookkeeping:
                    line = line.split()
                    if result[0] == line[0]:
                        top_url.append(line[1])
    except:
        return ['NO RESULTS FOUND']
    return top_url


