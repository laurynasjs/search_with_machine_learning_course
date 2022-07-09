python create_labeled_queries.py --output /workspace/datasets/fasttext/labeled_queries.txt  --min_queries 1000 

shuf /workspace/datasets/fasttext/labeled_queries.txt > /workspace/datasets/fasttext/shuffled_labeled_queries.txt

cat /workspace/datasets/fasttext/shuffled_labeled_products.txt | wc -l

head -n -3000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > training_data.txt 
tail -3000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > test_data.txt

~/fastText-0.9.2/fasttext supervised -input training_data.txt  -output product_classifier