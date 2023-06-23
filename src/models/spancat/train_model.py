import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os,json
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent.parent


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data(file, data):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data,f,indent= 4)

import spacy
from spacy.tokens import DocBin
import srsly
from pathlib import Path


## some of the entities will be skipped as they dont align with token boundaries
def convert(lang: str, input_path: Path, output_path: Path, spans_key: str = "sc"):
    nlp = spacy.blank(lang)
    doc_bin = DocBin()
    for text, annot in srsly.read_json(input_path):
        doc = nlp(text)
        spans = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label, alignment_mode="contract")
            if span != None :
                spans.append(span)
        doc.spans[spans_key] = spans
        doc_bin.add(doc)
    doc_bin.to_disk(output_path)

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn processed data from (../processed) into
        cleaned data ready to be analyzed (saved in ../tmp).
    """
    path = get_project_root()
    input_filepath = str(path) + '/' + input_filepath + '/'
    output_filepath = str(path) + '/' + output_filepath + '/'

    convert("en", input_filepath + "train/overlap.json", output_filepath + "train.spacy")
    convert("en", input_filepath + "test/overlap.json", output_filepath + "test.spacy")

    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
