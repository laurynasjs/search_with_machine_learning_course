python week2/createContentTrainingData.py --output /workspace/datasets/fasttext/labeled_products.txt --sample_rate 0.1 --min_products 0

shuf /workspace/datasets/fasttext/labeled_products.txt > /workspace/datasets/fasttext/shuffled_labeled_products.txt

cat /workspace/datasets/fasttext/shuffled_labeled_products.txt | wc -l

head -n -3000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > training_data.txt 
tail -3000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > test_data.txt

# Train model v1
~/fastText-0.9.2/fasttext supervised -input training_data.txt  -output product_classifier
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt

# ~/fastText-0.9.2/fasttext predict product_classifier.bin -

# Train model v2
~/fastText-0.9.2/fasttext supervised -input training_data.txt -output product_classifier -lr 1.0 -epoch 25 -wordNgrams 2
~/fastText-0.9.2/fasttext test product_classifier.bin test_data.txt

# Train model v3
cat /workspace/datasets/fasttext/labeled_products.txt |sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]_]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_labeled_products.txt
shuf /workspace/datasets/fasttext/normalized_labeled_products.txt > /workspace/datasets/fasttext/normalized_shuffled_labeled_products.txt

head -n -3000 /workspace/datasets/fasttext/normalized_shuffled_labeled_products.txt > normalized_shuffled_training_data.txt 
tail -3000 /workspace/datasets/fasttext/normalized_shuffled_labeled_products.txt > normalized_shuffled_test_data.txt

~/fastText-0.9.2/fasttext supervised -input normalized_shuffled_training_data.txt -output product_classifier_normalized -lr 1.0 -epoch 25 -wordNgrams 2
~/fastText-0.9.2/fasttext test product_classifier_normalized.bin normalized_shuffled_test_data.txt

~/fastText-0.9.2/fasttext test product_classifier_normalized.bin normalized_shuffled_test_data.txt

# train after filtering
python week2/createContentTrainingData.py --output /workspace/datasets/fasttext/labeled_products.txt --sample_rate 1 --min_products 500
shuf /workspace/datasets/fasttext/labeled_products.txt > /workspace/datasets/fasttext/shuffled_labeled_products.txt

cat /workspace/datasets/fasttext/labeled_products.txt_filtered.txt | wc -l

shuf /workspace/datasets/fasttext/labeled_products.txt_filtered.txt > /workspace/datasets/fasttext/shufled_filtered_labeled_products.txt
cat /workspace/datasets/fasttext/shufled_filtered_labeled_products.txt | wc -l

head -n -10000 /workspace/datasets/fasttext/shufled_filtered_labeled_products.txt > shufled_filtered_labeled_products_training_data.txt 
tail -10000 /workspace/datasets/fasttext/shufled_filtered_labeled_products.txt > shufled_filtered_labeled_products_test_data.txt

~/fastText-0.9.2/fasttext supervised -input shufled_filtered_labeled_products_training_data.txt -output product_classifier_filtered -lr 1.0 -epoch 25 -wordNgrams 2
~/fastText-0.9.2/fasttext test product_classifier_filtered.bin shufled_filtered_labeled_products_test_data.txt

# step 2

cut -d' ' -f2- /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/titles.txt

~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/titles.txt -output /workspace/datasets/fasttext/title_model

cat /workspace/datasets/fasttext/titles.txt | sed -e "s/\([.\!?,'/()]\)/ \1 /g" | tr "[:upper:]" "[:lower:]" | sed "s/[^[:alnum:]]/ /g" | tr -s ' ' > /workspace/datasets/fasttext/normalized_titles.txt
~/fastText-0.9.2/fasttext skipgram -input /workspace/datasets/fasttext/normalized_titles.txt -output /workspace/datasets/fasttext/title_model -epoch 25 -minCount 20
~/fastText-0.9.2/fasttext nn /workspace/datasets/fasttext/title_model.bin

cat /workspace/datasets/fasttext/normalized_titles.txt | tr " " "\n" | grep "...." | sort | uniq -c | sort -nr | head -1000 | grep -oE '[^ ]+$' > /workspace/datasets/fasttext/top_words.txt

python week2/synonyms_model.py --threshold 0.75 

docker cp /workspace/datasets/fasttext/synonyms.csv opensearch-node1:/usr/share/opensearch/config/synonyms.csv
