Preprocess the training and dev sets in the distractor setting:
```
python main.py --mode prepro --data_file mixed_train.json --para_limit 2250 --data_split train
python main.py --mode prepro --data_file mixed_dev.json --para_limit 2250 --data_split dev
```
# hotpot 中 support / sent 比例：
4603011 215684
# 通过构图来提取support factor
graph processing code : process_graph.py missing rate 36%
word selection : missed 19 from 100
# ???
test for support_factor
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size12 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190512-005929 --prediction_file dev_distractor_pred.json
```
# mixed tricking input
50% unsupporting factor
```
best_dev_F1 61.769143905869505
```
20% unsupporting factor 
```
best_dev_F1 55.402730811662096
```
# use prediction traceback output
1. threshold = 0.4
```
-----------------------------------------------------------------------------------------
| eval     23 in epoch   3 | time: 1401.24s | dev loss    4.878 | EM 40.9572 | F1 54.7996
-----------------------------------------------------------------------------------------
best_dev_F1 55.05900759590962
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190512-005929 --prediction_file dev_distractor_pred.json
```
1. threshold = 0.3
```
-----------------------------------------------------------------------------------------
| eval     25 in epoch   3 | time: 851.63s | dev loss    4.805 | EM 41.7977 | F1 55.9168
-----------------------------------------------------------------------------------------
best_dev_F1 55.92223807984311
```
2. threshold = 0.2
```
-----------------------------------------------------------------------------------------
| eval     20 in epoch   2 | time: 865.81s | dev loss    4.876 | EM 40.3335 | F1 54.2117
-----------------------------------------------------------------------------------------
best_dev_F1 54.32020335808264
```
3. threshold = 0
```
| epoch   3 | step  27000 | lr 0.00020 | ms/batch 1121.13 | train loss    2.414
-----------------------------------------------------------------------------------------
| eval     27 in epoch   3 | time: 1383.11s | dev loss    4.808 | EM 42.4620 | F1 56.4316
-----------------------------------------------------------------------------------------
best_dev_F1 56.53792785703203
```
4. threshold = 0.01
```
-----------------------------------------------------------------------------------------
| eval     25 in epoch   3 | time: 897.66s | dev loss    4.910 | EM 40.9707 | F1 54.4158
-----------------------------------------------------------------------------------------
best_dev_F1 54.74794182228903
```
5. threshold = 0.001
```
-----------------------------------------------------------------------------------------
| eval     26 in epoch   3 | time: 860.75s | dev loss    4.898 | EM 41.1334 | F1 55.2774
-----------------------------------------------------------------------------------------
best_dev_F1 55.334311573506525
```
6. threshold = 0.005
```
 eval     20 in epoch   2 | time: 1335.69s | dev loss    4.875 | EM 41.0385 | F1 54.5506
```
7. threshold= 0.00023
```
-----------------------------------------------------------------------------------------
| eval     30 in epoch   4 | time: 1414.24s | dev loss    4.822 | EM 42.1773 | F1 56.0289
-----------------------------------------------------------------------------------------
best_dev_F1 56.41001179534331
```

# model by filter ing supporting factors in the middle stage before self-attention:
reminder: i have already change the overall util function to include the extra is_support_word data structure. 
model for testing using only supporting facts:
    [model_test2](/model_test2.py)//
    [run_test2](/run_test2.py)//
    [util](/util.py)//
    [sp_model_test2](/sp_model_test2.py)//
training code:
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode train --para_limit 2250 --batch_size 12 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
CUDA_VISIBLE_DEVICES=1 python main.py --mode train --para_limit 2250 --batch_size 12 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
```
```
output for training:
-----------------------------------------------------------------------------------------
| eval     21 in epoch   2 | time: 869.02s | dev loss    3.625 | EM 48.4409 | F1 63.1520
-----------------------------------------------------------------------------------------
best_dev_F1 63.37813440065209
```
# model using only supporting factors
```
-----------------------------------------------------------------------------------------
| eval     15 in epoch   3 | time: 172.94s | dev loss    3.183 | EM 49.7772 | F1 64.5559
-----------------------------------------------------------------------------------------
best_dev_F1 64.60608215105948
```
```
{'em': 0.4973666441593518, 'f1': 0.6460608215105955,'prec': 0.6743275068393223, 'recall': 0.6661522409243548, 'sp_em': 0.0, 'sp_f1': 0.14916748942406766, 'sp_prec': 0.09017627499446443,'sp_recall': 0.45199430886466524,'joint_f1': 0.09847809921520946, 'joint_prec': 0.06095010805013573,'joint_recall': 0.3034137242643319, 'joint_em': 0.0}
```
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190411-013304 --prediction_file dev_distractor_pred.json
```
```
python hotpot_evaluate_v1.py dev_distractor_pred.json hotpot_dev_distractor_v1.json
```
1. model for testing using only supporting facts:
    [model](/model_test1.py)
    [run](/run_test1.py)
# original file:
wordlength_csv file: [wordlength_csv](/length_vector.csv)
linux codes:
validation codes:
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190329-013728 --prediction_file dev_distractor_pred.json
```
validation outputs:
```
| epoch   4 | step  17600 | lr 0.00156 | ms/batch 1139.40 | train loss    2.398
| epoch   4 | step  17700 | lr 0.00156 | ms/batch 1121.55 | train loss    2.487
| epoch   4 | step  17800 | lr 0.00156 | ms/batch 1114.87 | train loss    2.408
| epoch   4 | step  17900 | lr 0.00156 | ms/batch 1152.25 | train loss    2.371
| epoch   4 | step  18000 | lr 0.00156 | ms/batch 1154.26 | train loss    2.343
-----------------------------------------------------------------------------------------
| eval     18 in epoch   4 | time: 1292.35s | dev loss    4.860 | EM 42.5705 | F1 56.6056
-----------------------------------------------------------------------------------------
best_dev_F1 56.64527711671228
```
test commands:
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20190329-013728 --prediction_file dev_distractor_pred.json
```
```
python hotpot_evaluate_v1.py dev_distractor_pred.json hotpot_dev_distractor_v1.json
```
```
missing answer 5a87ab905542996e4f3088c1
missing sp fact 5a87ab905542996e4f3088c1
missing answer 5ab56e32554299637185c594
missing sp fact 5ab56e32554299637185c594
missing answer 5a760ab65542994ccc918697
missing sp fact 5a760ab65542994ccc918697
missing answer 5ab7f97a5542991d322237ef
missing sp fact 5ab7f97a5542991d322237ef
missing answer 5ab266b5554299340b5254b4
missing sp fact 5ab266b5554299340b5254b4
missing answer 5ae7eb3c5542994a481bbe20
missing sp fact 5ae7eb3c5542994a481bbe20

missing answer 5a8b595855429949d91db563
missing sp fact 5a8b595855429949d91db563
missing answer 5a80762a5542996402f6a536
missing sp fact 5a80762a5542996402f6a536
missing answer 5adbe2c65542996e68525274
missing sp fact 5adbe2c65542996e68525274
missing answer 5ab8f33155429919ba4e237f
missing sp fact 5ab8f33155429919ba4e237f
missing answer 5a8f495c5542997ba9cb3220
missing sp fact 5a8f495c5542997ba9cb3220
missing answer 5a753c8c55429916b01642ab
missing sp fact 5a753c8c55429916b01642ab
missing answer 5ae5be02554299546bf82f3e
missing sp fact 5ae5be02554299546bf82f3e
missing answer 5a9042825542990a984935d6
missing sp fact 5a9042825542990a984935d6
missing answer 5adfff0755429925eb1afbce
missing sp fact 5adfff0755429925eb1afbce
missing answer 5adfa22655429942ec259ac4
missing sp fact 5adfa22655429942ec259ac4
missing answer 5a8f541e5542992414482a53
missing sp fact 5a8f541e5542992414482a53
missing answer 5a8bf0835542995d1e6f146b
missing sp fact 5a8bf0835542995d1e6f146b
missing answer 5ae69e6d5542996d980e7c62
missing sp fact 5ae69e6d5542996d980e7c62
missing answer 5a808f3f5542992097ad2ffd
missing sp fact 5a808f3f5542992097ad2ffd
missing answer 5a7b68a75542997c3ec97153
missing sp fact 5a7b68a75542997c3ec97153
missing answer 5a722a6855429971e9dc9320
missing sp fact 5a722a6855429971e9dc9320
missing answer 5a8f122955429918e830d17f
missing sp fact 5a8f122955429918e830d17f
missing answer 5ab2f6bd554299166977415e
missing sp fact 5ab2f6bd554299166977415e
missing answer 5a74629255429929fddd8402
missing sp fact 5a74629255429929fddd8402
missing answer 5a85a37d5542997175ce1fe5
missing sp fact 5a85a37d5542997175ce1fe5
missing answer 5a87bd4e5542996432c57279
missing sp fact 5a87bd4e5542996432c57279
missing answer 5ae67fba5542996d980e7b9a
missing sp fact 5ae67fba5542996d980e7b9a
missing answer 5ab29426554299545a2cf99f
missing sp fact 5ab29426554299545a2cf99f
{'em': 0.42336259284267386,'f1': 0.5642343875933413,'prec': 0.5861020489751079,  'recall': 0.5826240661559602,  'sp_f1': 0.6191265655344054,'joint_prec': 0.3994076045306619, 'joint_em': 0.09020931802835921, 'joint_recall': 0.4101608971320206,  'sp_em': 0.17933828494260634, 'sp_recall': 0.6615560592906983, 'joint_f1': 0.37115038958007174, 'sp_prec': 0.6493791878464388}
```

# HotpotQA: A Dataset for Diverse, Explainable Multi-hop Question Answering

This repository contains the baseline model code, as well as the entire pipeline of running experiments on the HotpotQA dataset,
including data download, data preprocessing, training, and evaluation.

## Requirements

Python 3, pytorch 0.3.0, spacy

To install pytorch 0.3.0, follow the instructions at https://pytorch.org/get-started/previous-versions/ . For example, with
CUDA8 and conda you can do
```
conda install pytorch=0.3.0 cuda80 -c pytorch
```

To install spacy, run
```
conda install spacy
```

## Data Download and Preprocessing

Run the script to download the data, including HotpotQA data and GloVe embeddings, as well as spacy packages.
```
./download.sh
```

There are three HotpotQA files:
- Training set http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_train_v1.1.json
- Dev set in the distractor setting http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_distractor_v1.json
- Dev set in the fullwiki setting http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_dev_fullwiki_v1.json This is just `hotpot_dev_distractor_v1.json` without the gold paragraphs, but instead with the top 10 paragraphs obtained using our
retrieval system. If you want to use your own IR system (which is encouraged!), you can replace the paragraphs in this json
with your own retrieval results. Please note that the gold paragraphs might or might not be in this json because our IR system
is pretty basic.
- Test set in the fullwiki setting http://curtis.ml.cmu.edu/datasets/hotpot/hotpot_test_fullwiki_v1.json Because in the fullwiki setting, you only need to submit your prediction to our evaluation server without the code, we publish the test set without the answers and supporting facts. The context in the file is paragraphs obtained using our retrieval system, which might or might not contain the gold paragraphs. Again you are encouraged to use your own IR system in this setting --- simply replace the paragraphs in this json with your own retrieval results.


## JSON Format

The top level structure of each JSON file is a list, where each entry represents a question-answer data point. Each data point is
a dict with the following keys:
- `_id`: a unique id for this question-answer data point. This is useful for evaluation.
- `question`: a string.
- `answer`: a string. The test set does not have this key.
- `supporting_facts`: a list. Each entry in the list is a list with two elements `[title, sent_id]`, where `title` denotes the title of the 
paragraph, and `sent_id` denotes the supporting fact's id (0-based) in this paragraph. The test set does not have this key.
- `context`: a list. Each entry is a paragraph, which is represented as a list with two elements `[title, sentences]` and `sentences` is a list
of strings.

There are other keys that are not used in our code, but might be used for other purposes (note that these keys are not present in the test sets, and your model should not rely on these two keys for making preditions on the test sets):
- `type`: either `comparison` or `bridge`, indicating the question type. (See our paper for more details).
- `level`: one of `easy`, `medium`, and `hard`. (See our paper for more details).

## Preprocessing

Preprocess the training and dev sets in the distractor setting:
```
python main.py --mode prepro --data_file hotpot_train_v1.1.json --para_limit 2250 --data_split train
python main.py --mode prepro --data_file hotpot_dev_distractor_v1.json --para_limit 2250 --data_split dev
```

Preprocess the dev set in the full wiki setting:
```
python main.py --mode prepro --data_file hotpot_dev_fullwiki_v1.json --data_split dev --fullwiki --para_limit 2250
```

Note that the training set has to be preprocessed before the dev sets because some vocabulary and embedding files are produced
when the training set is processed.

## Training

Train a model
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode train --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
```

Our implementation supports running on multiple GPUs. Remove the `CUDA_VISIBLE_DEVICES` variable to run on all GPUs you have
```
python main.py --mode train --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0
```

You will be able to see the perf reach over 58 F1 on the dev set. Record the file name (something like `HOTPOT-20180924-160521`)
which will be used during evaluation.

## Local Evaluation

First, make predictions and save the predictions into a file (replace `--save` with your own file name).
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20180924-160521 --prediction_file dev_distractor_pred.json
```

Then, call the evaluation script:
```
python hotpot_evaluate_v1.py dev_distractor_pred.json hotpot_dev_distractor_v1.json
```

The same procedure can be repeated to evaluate the dev set in the fullwiki setting.
```
CUDA_VISIBLE_DEVICES=0 python main.py --mode test --data_split dev --para_limit 2250 --batch_size 24 --init_lr 0.1 --keep_prob 1.0 --sp_lambda 1.0 --save HOTPOT-20180924-160521 --prediction_file dev_fullwiki_pred.json --fullwiki python hotpot_evaluate_v1.py dev_fullwiki_pred.json hotpot_dev_fullwiki_v1.json
```

## Prediction File Format

The prediction files `dev_distractor_pred.json` and `dev_fullwiki_pred.json` should be JSON files with the following keys:
- `answer`: a dict. Each key of the dict is a QA pair id, corresponding to the field `_id` in data JSON files. Each value of the dict is a string representing the predicted answer.
- `sp`: a dict. Each key of the dict is a QA pair id, corresponding to the field `_id` in data JSON files. Each value of the dict is a list representing the predicted supporting facts. Each entry of the list is a list with two elements `[title, sent_id]`, where `title` denotes the title of the paragraph, and `sent_id` denotes the supporting fact's id (0-based) in this paragraph.

## Model Submission and Test Set Evaluation

We use Codalab for test set evaluation. In the distractor setting, you must submit your code and provide a Docker environment. Your code will run on the test set. In the fullwiki setting, you only need to submit your prediction file. See https://worksheets.codalab.org/worksheets/0xa8718c1a5e9e470e84a7d5fb3ab1dde2/ for detailed instructions.

## License
The HotpotQA dataset is distribued under the [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/legalcode) license.
The code is distribued under the Apache 2.0 license.

## References

The preprocessing part and the data loader are adapted from https://github.com/HKUST-KnowComp/R-Net . The evaluation script is
adapted from https://rajpurkar.github.io/SQuAD-explorer/ .



