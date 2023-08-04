PYTHON_INTERPRETER = python3

requirements:
	$(PYTHON_INTERPRETER) -m pip install spacy==3.5.4
	$(PYTHON_INTERPRETER) -m spacy download en_core_web_lg

run_linker: 
	$(PYTHON_INTERPRETER) main.py