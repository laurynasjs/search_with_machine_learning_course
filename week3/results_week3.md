# |train set| = 50k, |test set| = 10k

## best
### min_queries 10k:
| Model parameters | R@1 | R@3 | R@5 |
| --- | --- | --- | --- |
| epoch 20, lr=0.5, wordNgrams=2 |0.567|0.763|0.826|

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

## 2.a. improvements
### query = panasonic


['abcat0101001', 'abcat0900000']
"value": 342
 "Panasonic - 50\" Class / Plasma / 1080p / 600Hz / HDTV"
 "Panasonic - 50\" Plasma HDTV"

w/o filtering:

 "value": 1942
 "Panasonic - Lumix 7.2MP Digital Camera - Pink"
 "Panasonic - Wi-Fi Built-In Blu-ray Player"

### query = panasonic tv

['cat02015']
"value": 275,
"Magnavox - 15\" HD-Ready LCD TV w/HD Component Video Inputs"
"Panasonic - 50\" Class / Plasma / 1080p / 600Hz / HDTV"
"Panasonic - 11\" LCD Screen TV/DVD Combo"
"Panasonic 42\" Class Plasma TV & Blu-ray Home Theater System Package"

w/o filtering:

"value": 7421,
"Apple\u00ae - Apple TV\u00ae",
 "KCPI - Digital TV Converter Box"
"Monster Cable - TV Screen Cleaning Kit"
"Panasonic - Lumix 7.2MP Digital Camera - Pink"

## 2.a. doubts

nokia phone

['abcat0811002', 'abcat0801002', 'pcmcat209400050001']

"value": 2777,
"Nokia - Wireless Headset for Bluetooth-Enabled Phones"
"ZAGG - InvisibleSHIELD HD for Samsung Galaxy S III Mobile Phones"

w/o filterings
"value": 5341,
"Nokia - Shorty Pay-As-You-Go Cell Phone w/Voice Navigation (Virgin Mobile)"
 "MagicJack - PLUS USB Phone Jack"
 "Nokia - Wireless Headset for Bluetooth-Enabled Phones"