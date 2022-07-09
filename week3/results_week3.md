# |train set| = 50k, |test set| = 10k

## best

## min_queries 1k:

| Model parameters | R@1 | R@3 | R@5 |
| --- | --- | --- | --- |
| default | 0.469 | 0.635 | 0.697 |
| epoch 10, lr=0.5, wordNgrams=2 | 0.517 | 0.705 | 0.773 |

## min_queries 10k:

| Model parameters | R@1 | R@3 | R@5 |
| --- | --- | --- | --- |
| default |0.565|0.754|0.818|
| epoch 10, lr=0.5, wordNgrams=2 |0.57| 0.764|0.827|
| epoch 20, lr=0.7, wordNgrams=2 |0.567|0.76|0.823|
| epoch 20, lr=0.3, wordNgrams=2 |0.569|0.762|0.827|
| epoch 20, lr=0.5, wordNgrams=2 |0.567|0.763|0.826|