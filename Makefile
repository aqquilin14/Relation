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
data: requirements
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw/train data/processed/train
	$(PYTHON_INTERPRETER) src/data/make_dataset.py data/raw/test data/processed/test
## Delete all compiled Python files


## train model

train-ner :
	$(PYTHON_INTERPRETER) src/models/ner/train_model.py data/processed tmp/ner
	$(PYTHON_INTERPRETER) -m spacy train models/ner/config.cfg --output models/ner/ --paths.train tmp/ner/train.spacy --paths.dev tmp/ner/test.spacy 

train-spancat :
	$(PYTHON_INTERPRETER) src/models/spancat/train_model.py data/processed tmp/spancat
	$(PYTHON_INTERPRETER) -m spacy train models/spancat/config.cfg --output models/spancat/ --paths.train tmp/spancat/train.spacy --paths.dev tmp/spancat/test.spacy 

get-repo :
	cd data && cd raw && git clone git@git.corp.adobe.com:AdobeDocs/experience-platform.en.git
	
predict-entity:
	$(PYTHON_INTERPRETER) src/models/predict_model.py data/processed

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using flake8
lint:
	flake8 src

## Test python environment is setup correctly
test_environment:
	$(PYTHON_INTERPRETER) test_environment.py
