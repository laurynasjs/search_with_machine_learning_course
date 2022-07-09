import os
import argparse
import xml.etree.ElementTree as ET
import pandas as pd
import numpy as np
import csv
import string
import re

# Useful if you want to perform stemming.
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('stopwords')
nltk_stop_words = set(stopwords.words("english"))

stemmer = nltk.stem.PorterStemmer()

categories_file_name = r'/workspace/datasets/product_data/categories/categories_0001_abcat0010000_to_pcmcat99300050000.xml'

queries_file_name = r'/workspace/datasets/train.csv'
output_file_name = r'/workspace/datasets/labeled_query_data.txt'

parser = argparse.ArgumentParser(description='Process arguments.')
general = parser.add_argument_group("general")
general.add_argument("--min_queries", default=1,  help="The minimum number of queries per category label (default is 1)")
general.add_argument("--output", default=output_file_name, help="the file to output to")

args = parser.parse_args()
output_file_name = args.output

if args.min_queries:
    min_queries = int(args.min_queries)

# The root category, named Best Buy with id cat00000, doesn't have a parent.
root_category_id = 'cat00000'

tree = ET.parse(categories_file_name)
root = tree.getroot()

# Parse the category XML file to map each category id to its parent category id in a dataframe.
categories = []
parents = []
for child in root:
    id = child.find('id').text
    cat_path = child.find('path')
    cat_path_ids = [cat.find('id').text for cat in cat_path]
    leaf_id = cat_path_ids[-1]
    if leaf_id != root_category_id:
        categories.append(leaf_id)
        parents.append(cat_path_ids[-2])
parents_df = pd.DataFrame(list(zip(categories, parents)), columns =['category', 'parent'])

# Read the training data into pandas, only keeping queries with non-root categories in our category tree.
df = pd.read_csv(queries_file_name)[['category', 'query']]
df = df[df['category'].isin(categories)]

# IMPLEMENT ME: Convert queries to lowercase, and optionally implement other normalization, like stemming.
new_string = [query.translate(str.maketrans('', '', string.punctuation)) for query in df["query"]]
df["query"] = new_string

removeSpaces = [re.sub('\\s+', ' ', msg) for msg in df["query"]]
df["query"] = removeSpaces

lowering = [query.lower() for query in df["query"]]
df["query"] = lowering
df["query"] = df["query"].apply(lambda x: x.strip())

queries = []
for query in df["query"]:
    words = []
    for w in query.split():
        if w not in nltk_stop_words:
            words.append(w)
    queries.append(" ".join(words))

df["query"] = queries

stemmed_queries = []
for query in df["query"]:
    # tokens = word_tokenize(query)
    tokens = query.split()
    porter_eu = [stemmer.stem(word) for word in tokens]
    stemmed_queries.append(' '.join(porter_eu))

df["query"] = stemmed_queries

# IMPLEMENT ME: Roll up categories to ancestors to satisfy the minimum number of queries per category.

ind = (df["category"].value_counts() >= min_queries)
ind_true = ind[ind == True].index.to_numpy()
ind_false = ind[ind == False].index.to_numpy()

mappings = parents_df.set_index("category").to_dict()["parent"]
mappings["cat00000"] = "cat00000"
df["parent"] = df["category"].map(mappings)

if len(ind_false) > 0:

    qualified = dict((x, y) for x, y in zip(ind_true, ind_true))
    mask = np.where(df["category"].isin(ind_false))
    temp_df = df.iloc[mask]

    while True:

        ind_temp = (temp_df["parent"].value_counts() >= min_queries)
        ind_tmp_true = ind_temp[ind_temp == True].index.to_numpy()
        ind_tmp_false = ind_temp[ind_temp == False].index.to_numpy()

        mask_true = np.where(temp_df["parent"].isin(ind_tmp_true))[0]

        qualified_temp = dict((x, y) for x, y in zip(temp_df.iloc[mask_true]["category"], temp_df.iloc[mask_true]["parent"]))
        qualified.update(qualified_temp)

        if len(ind_tmp_false) == 0:
            break

        mask = np.where(temp_df["parent"].isin(ind_tmp_false))
        temp_df = temp_df.iloc[mask]
        temp_df["parent"] = temp_df["parent"].map(mappings)

        temp_df[temp_df["parent"].isna()]

else:
    qualified = dict((x, y) for x, y in zip(ind_true, ind_true))

print(len(np.unique(np.array(list(qualified.values())))))
df["parent"] = df["category"].map(qualified)

# Create labels in fastText format.
df['label'] = '__label__' + df['parent']

# Output labeled query data as a space-separated file, making sure that every category is in the taxonomy.
df = df[df['category'].isin(categories)]
df['output'] = df['label'] + ' ' + df['query']
df[['output']].to_csv(output_file_name, header=False, sep='|', escapechar='\\', quoting=csv.QUOTE_NONE, index=False)