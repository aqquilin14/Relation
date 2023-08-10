.PHONY: clean data lint requirements train-ner train-spancat get-repo predict-entity

#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = knowledge-graph-constructor
PYTHON_INTERPRETER = python3

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python Dependencies
requirements: test_environment
	$(PYTHON_INTERPRETER) -m pip install -U pip setuptools wheel
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt


## Make Dataset
data-ner: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset_ner.py data/ner/raw/train data/ner/processed/train
	$(PYTHON_INTERPRETER) src/data/make_dataset_ner.py data/ner/raw/test data/ner/processed/test

data-re: 
	$(PYTHON_INTERPRETER) src/data/make_dataset_re.py data/re/raw data/re/processed
## Delete all compiled Python files

## Parse Data
parseData :
	$(PYTHON_INTERPRETER) src/models/relation_extraction/parse_data.py data/re/processed/train/annotations_train.jsonl data/re/processed/dev/annotations_dev.jsonl data/re/processed/test/annotations_test.jsonl tmp/re/train.spacy tmp/re/dev.spacy tmp/re/test.spacy

## train model

train-ner :
	$(PYTHON_INTERPRETER) src/models/ner/train_model.py data/ner/processed tmp/ner
	$(PYTHON_INTERPRETER) -m spacy train models/ner/config.cfg --output models/ner/ --paths.train tmp/ner/train.spacy --paths.dev tmp/ner/test.spacy 

train-spancat :
	$(PYTHON_INTERPRETER) src/models/spancat/train_model.py data/ner/processed tmp/spancat
	$(PYTHON_INTERPRETER) -m spacy train models/spancat/config.cfg --output models/spancat/ --paths.train tmp/spancat/train.spacy --paths.dev tmp/spancat/test.spacy 

train-re-CPU :
	$(PYTHON_INTERPRETER) -m spacy train models/relation_extraction/configs/rel_tok2vec.cfg --output models/relation_extraction/ --paths.train tmp/re/train.spacy --paths.dev tmp/re/dev.spacy -c src/models/relation_extraction/custom_functions.py

## Train Model
train-re-GPU :
	$(PYTHON_INTERPRETER) -m spacy train models/relation_extraction/configs/rel_trf.cfg --output models/relation_extraction/ --paths.train tmp/re/train.spacy --paths.dev tmp/re/dev.spacy -c src/models/relation_extraction/custom_functions.py


get-repo-ner :
	cd data && cd ner && cd raw && git clone git@git.corp.adobe.com:AdobeDocs/experience-platform.en.git

get-repo-re :
	cd data && cd re && cd raw && git clone git@git.corp.adobe.com:AdobeDocs/experience-platform.en.git
	
predict-entity:
	$(PYTHON_INTERPRETER) src/models/predict_model_ner.py data/ner/processed

predict-relation:
	$(PYTHON_INTERPRETER) src/models/predict_model_re.py data/re/raw data/re/processed

##Evaluate model
evaluate-re: 
	$(PYTHON_INTERPRETER) src/models/relation_extraction/evaluate.py models/relation_extraction/model-best tmp/re/dev.spacy False

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py
