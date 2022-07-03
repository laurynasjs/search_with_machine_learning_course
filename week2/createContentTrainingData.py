import argparse
import multiprocessing
import glob
from tqdm import tqdm
import os
import random
import xml.etree.ElementTree as ET
from pathlib import Path
import pandas as pd
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer("english") 

def transform_name(product_name):
    return stemmer.stem(product_name)

# Directory for product data
directory = r'/workspace/datasets/product_data/products/'

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default=directory,  help="The directory containing product data")
general.add_argument("--output", default="/workspace/datasets/fasttext/output.fasttext", help="the file to output to")
general.add_argument("--label", default="id", help="id is default and needed for downsteam use, but name is helpful for debugging")


# Consuming all of the product data, even excluding music and movies,
# takes a few minutes. We can speed that up by taking a representative
# random sample.
general.add_argument("--sample_rate", default=1.0, type=float, help="The rate at which to sample input (default is 1.0)")

# IMPLEMENT: Setting min_products removes infrequent categories and makes the classifier's task easier.
general.add_argument("--min_products", default=0, type=int, help="The minimum number of products per category (default is 0).")

# filtering infrequents labels
# general.add_argument("--filter", default=0, type=int, help="filtering out infrequent labels")

args = parser.parse_args()
output_file = args.output
path = Path(output_file)
output_dir = path.parent

if os.path.isdir(output_dir) == False:
        os.mkdir(output_dir)

if args.input:
    directory = args.input
# IMPLEMENT:  Track the number of items in each category and only output if above the min
min_products = args.min_products
sample_rate = args.sample_rate
names_as_labels = False

if args.label == 'name':
    names_as_labels = True


def _label_filename(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    labels = []
    for child in root:
        if random.random() > sample_rate:
            continue
        # Check to make sure category name is valid and not in music or movies
        if (child.find('name') is not None and child.find('name').text is not None and
            child.find('categoryPath') is not None and len(child.find('categoryPath')) > 0 and
            child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text is not None and
            child.find('categoryPath')[0][0].text == 'cat00000' and
            child.find('categoryPath')[1][0].text != 'abcat0600000'):
              # Choose last element in categoryPath as the leaf categoryId or name
              if names_as_labels:
                  cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][1].text.replace(' ', '_')
              else:
                  cat = child.find('categoryPath')[len(child.find('categoryPath')) - 1][0].text
              # Replace newline chars with spaces so fastText doesn't complain
              name = child.find('name').text.replace('\n', ' ')
              labels.append((cat, transform_name(name)))
    return labels

if __name__ == '__main__':
    files = glob.glob(f'{directory}/*.xml')

    print("Writing results to %s" % output_file)
    if min_products > 0:
        print("Writing filtered results to %s" % (output_file + "_filtered.txt"))

    with multiprocessing.Pool() as p:
        all_labels = tqdm(p.imap_unordered(_label_filename, files), total=len(files))

        print()

        with open(output_file, 'w') as output:
            for label_list in all_labels:
                for (cat, name) in label_list:
                    
                    output.write(f'__label__{cat} {name}\n')

    if min_products > 0:
        df = pd.read_csv(output_file, sep='\t', header=None)
        df.rename(columns={df.columns[0]: "text"}, inplace=True)
        df[['label', 'data']] = df["text"].str.split(' ', 1, expand=True)

        counts = df['label'].value_counts()
        df = df.loc[df['label'].isin(counts[counts > min_products].index), :]

        filter_output_file = output_file + "_filtered.txt"
        with open(filter_output_file, 'w') as f:
            dfAsString = df[["text"]].to_string(header=False, index=False)
            f.writelines(dfAsString)


