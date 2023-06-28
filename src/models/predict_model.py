import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import json
from pathlib import Path
import os
import spacy
import json

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data(file, data):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data,f,indent= 4)

def write_json(new_data, filename, str):
    with open(filename, 'r+', encoding="utf-8") as file:
        file_data = json.load(file)
        file_data[str].append(new_data)
        file.seek(0)
        json.dump(file_data, file, indent = 4)


@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())


def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        analyzed data (saved in ../processed).
    """
    path = get_project_root()
    input_filepath = str(path) + '/' + input_filepath
    output_filepath = str(path) + '/' + output_filepath + '/'

    output = { "output" : []}
    save_data(output_filepath + "output.json", output)
    cnt = 0

    for root,d_files, f_names in os.walk(path, topdown=False):
        for mdF in f_names:
            mdYes =  mdF.endswith(".md",len(mdF)-3,len(mdF))
            if(mdYes) :
                rootNew = root
                rootNew = rootNew.removeprefix(str(path))

                with open(root + "/" + mdF, "r") as f:
                    text = f.read()

                    trained_ner = spacy.load("models/ner/model-best")
                    trained_spancat = spacy.load("models/spancat/model-best")

                    doc1 = trained_ner(text)
                    doc2 = trained_spancat(text)
                    ent = []

                    for ents in doc1.ents :
                        ent.append([ents.text, ents.start_char, ents.end_char, ents.label_])

                    spans = doc2.spans["sc"]
                    try : 
                        for span, confidence in zip(spans, spans.attrs["scores"]):
                            if(round((100*confidence)) > 80):
                                ent.append([span.text, span.start_char, span.end_char, span.label_])
                    except KeyError:
                        print(root + '/' + mdF, "has key error")
                    y = {
                        "fileName" : root + "/" + mdF,
                        "text" : text,
                        "entities" : ent
                    }
                    write_json(y, output_filepath + "output.json", "output")
                    cnt += 1
                    print(cnt)

    logger = logging.getLogger(__name__)
    logger.info('making analyzed data set from raw data')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
