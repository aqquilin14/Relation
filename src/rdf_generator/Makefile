PYTHON_INTERPRETER = python3

requirements:
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	$(PYTHON_INTERPRETER) -m spacy download en_core_web_md

getRDF:
	$(PYTHON_INTERPRETER) main.py
