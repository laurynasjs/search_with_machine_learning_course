import pandas as pd 
import argparse
import os
import fasttext

MODEL_FILE = "/workspace/datasets/fasttext/title_model.bin"
TOP_WORDS = "/workspace/datasets/fasttext/top_words.txt"
OUTPUT_FILE = "/workspace/datasets/fasttext/synonyms.csv"

parser = argparse.ArgumentParser(description='Process some integers.')
general = parser.add_argument_group("general")
general.add_argument("--threshold", default=0.75, type=float,  help="threshold")

args = parser.parse_args()
threshold = args.threshold

data = pd.read_csv(TOP_WORDS, header=None)
data.rename(columns={0: "input"}, inplace=True)

model = fasttext.load_model(MODEL_FILE)

model.get_nearest_neighbors('dog', k=100)

def get_synonyms(word, threshold):
    predictions = model.get_nearest_neighbors(word, k=10)
    filtered = filter(lambda x: x[0] > threshold, predictions)
    synonyms_list = [x[1] for x in filtered]
    synonyms_list = [word] + synonyms_list
    return ",".join(synonyms_list)

with open(OUTPUT_FILE, 'w') as f:
    for word in data["input"]:
        synonyms = get_synonyms(word, threshold)
        # if synonyms:
        f.write(f'{synonyms}\n')

