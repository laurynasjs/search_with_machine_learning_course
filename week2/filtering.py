import pandas as pd
import argparse
import os

from pathlib import Path

# Directory for product data

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--input", default="/workspace/datasets/fasttext/labeled_products.txt",  help="The file containing input data")
general.add_argument("--output", default="/workspace/datasets/fasttext/labeled_product_filtered.txt", help="the file to output to")

# filtering infrequents labels
general.add_argument("--filter", default=0, type=int, help="filtering out infrequent labels")

args = parser.parse_args()
output_file = args.output
input_file = args.input
threshold = int(args.filter)

if __name__ == '__main__':

    if threshold > 0:
        # df = pd.read_csv('/workspace/datasets/fasttext/labeled_products.txt', sep='\t', header=None)
        df = pd.read_csv(input_file, sep='\t', header=None)
        df.rename(columns={df.columns[0]: "text"}, inplace=True)
        df[['label', 'data']] = df["text"].str.split(' ', 1, expand=True)

        counts = df['label'].value_counts()
        df = df.loc[df['label'].isin(counts[counts > threshold].index), :]

        with open(output_file, 'w') as f:
            dfAsString = df[["text"]].to_string(header=False, index=False)
            f.writelines(dfAsString)
