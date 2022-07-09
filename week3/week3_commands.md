python create_labeled_queries.py --output /workspace/datasets/fasttext/labeled_queries.txt  --min_queries 1000 

shuf /workspace/datasets/fasttext/labeled_queries.txt > /workspace/datasets/fasttext/shuffled_labeled_queries.txt

cat /workspace/datasets/fasttext/shuffled_labeled_products.txt | wc -l

head -5000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/training_data.txt 
tail -10000 /workspace/datasets/fasttext/shuffled_labeled_products.txt > /workspace/datasets/fasttext/test_data.txt

cat  /workspace/datasets/fasttext/training_data.txt | wc -l


~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data.txt  -output /workspace/datasets/fasttext/queries_classifier
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/queries_classifier.bin /workspace/datasets/fasttext/test_data.txt



~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data.txt -output /workspace/datasets/fasttext/queries_classifier -lr 1.0 -epoch 25 -wordNgrams 2
~/fastText-0.9.2/fasttext test product_classifier_normalized.bin normalized_shuffled_test_data.txt


Number of words:  27775
Number of labels: 1861
Progress: 100.0% words/sec/thread:     506 lr:  0.000000 avg.loss:  6.123954 ETA:   0h 0m 0s
(search_with_ml) gitpod /workspace/search_with_machine_learning_course/week3 (main) $ ~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/queries_classifier.bin /workspace/datasets/fasttext/test_data.txt


N       9969
P@1     0.488
R@1     0.488


shuf /workspace/datasets/fasttext/labeled_queries_1k.txt > /workspace/datasets/fasttext/shuffled_labeled_queries_1k.txt
cat /workspace/datasets/fasttext/labeled_queries_1k.txt | wc -l

head -50000 /workspace/datasets/fasttext/shuffled_labeled_queries_1k.txt > /workspace/datasets/fasttext/training_data_1k.txt 
tail -10000 /workspace/datasets/fasttext/shuffled_labeled_queries_1k.txt > /workspace/datasets/fasttext/test_data_1k.txt

~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data_1k.txt  -output /workspace/datasets/fasttext/queries_classifier_1k
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/queries_classifier_1k.bin /workspace/datasets/fasttext/test_data_1k.txt 

~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data_1k.txt  -output /workspace/datasets/fasttext/queries_classifier_1k -lr 0.5 -epoch 10 -wordNgrams 2
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/queries_classifier_1k.bin /workspace/datasets/fasttext/test_data_1k.txt 


shuf /workspace/datasets/fasttext/labeled_queries_10k.txt > /workspace/datasets/fasttext/shuffled_labeled_queries_10k.txt
cat /workspace/datasets/fasttext/shuffled_labeled_queries_10k.txt | wc -l

head -50000 /workspace/datasets/fasttext/shuffled_labeled_queries_10k.txt > /workspace/datasets/fasttext/training_data_10k.txt 
tail -10000 /workspace/datasets/fasttext/shuffled_labeled_queries_10k.txt > /workspace/datasets/fasttext/test_data_10k.txt

~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data_10k.txt  -output /workspace/datasets/fasttext/queries_classifier_10k 
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/queries_classifier_10k.bin /workspace/datasets/fasttext/test_data_10k.txt 

~/fastText-0.9.2/fasttext supervised -input /workspace/datasets/fasttext/training_data_10k.txt  -output /workspace/datasets/fasttext/queries_classifier_10k -lr 0.5 -epoch 10 -wordNgrams 2
~/fastText-0.9.2/fasttext test /workspace/datasets/fasttext/queries_classifier_10k.bin /workspace/datasets/fasttext/test_data_10k.txt 