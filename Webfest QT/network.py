import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from sklearn.feature_extraction.text import TfidfTransformer


def sort_coo(coo_matrix):
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_topn_from_vector(feature_names, sorted_items, topn=10):
    # get the feature names and tf-idf score of top n items
    
    #use only topn items from vector
    sorted_items = sorted_items[:topn]

    score_vals = []
    feature_vals = []

    # word index and corresponding tf-idf score,
    for idx, score in sorted_items:

        #keep track of feature name and its corresponding score,
        score_vals.append(round(score, 3))
        feature_vals.append(feature_names[idx])

    #create a tuples of feature,score,
    #results = zip(feature_vals,score_vals),
    results= {}
    for idx in range(len(feature_vals)):
        results[feature_vals[idx]]=score_vals[idx]

    return results


def pre_process(text):

    # lowercase,
    text=str(text).lower()

    #text.translate(str.maketrans('', '', string.punctuation)),

    #remove tags,
    text=re.sub("<!--?.*?-->","",text)

    # remove special characters and digits,
    text=re.sub("(\\d|\\W)"," ",text)

    return text


def network_calculation(file):

    df = pd.read_csv(file, names=['Name', 'Event', 'title', 'description'], header=0)
    G = nx.Graph()

    # df.head()
    # df.size
    df['Name']=df['Name'].str.replace("{comma}",",")
    df['description_2']=df['title']+df['description']
    df['description'] = df['description_2'].apply(lambda x:pre_process(x))
    # get the text column
    docs=df['description'].tolist()

    # create a vocabulary of words
    # ignore words that appear in 10% of documents
    # eliminate stop words
    cv=CountVectorizer(max_df=0.05,stop_words='english')
    word_count_vector=cv.fit_transform(docs)
    tfidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)

    for name, group in df.groupby(['Name']):
        G.add_node(name,bipartite=0)
        tfidf_transformer.fit(word_count_vector)
        # you only needs to do this once, this is a mapping of index to
        feature_names=cv.get_feature_names()
        # generate tf-idf for the given document
        tf_idf_vector=tfidf_transformer.transform(cv.transform(group['description']))
        # sort the tf-idf vectors by descending order of scores
        sorted_items=sort_coo(tf_idf_vector.tocoo())

        # extract only the top n; n here is 100
        keywords=extract_topn_from_vector(feature_names,sorted_items,10)
        for k in keywords:
            # print(k,keywords[k])
            G.add_node(k,bipartite=1)
            G.add_edge(name,k,weight=keywords[k])
    print(nx.info(G))

    for n in G.neighbors(name):
        print(n)
        for i in G.neighbors(n):
            print("\t",i)

    nx.write_gexf(G, "test_all.gexf")
    #fig, ax = plt.subplots(1, 1, figsize=(8, 6));
    #nx.draw_networkx(G, ax=ax)"

    #fig, ax = plt.subplots(1, 1, figsize=(8, 6));
    #nx.draw_networkx(G, ax=ax, node_size=100)"

    #fig, ax = plt.subplots(1, 1, figsize=(8, 6));
    #nx.draw_spring(G, ax=ax)"

    #nx.number_connected_components(G)"

    #alist(cv.vocabulary_.keys())[:100]"

    G.neighbors(name)
    return name
