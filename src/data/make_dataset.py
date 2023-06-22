# -*- coding: utf-8 -*-
import click
import logging
from pathlib import Path
from dotenv import find_dotenv, load_dotenv
import os,json
from pathlib import Path

def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def save_data(file, data):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data,f,indent= 4)

def remove_overlap(entity):
    entity.sort()
    cnt = 1
    while(cnt > 0):
        cnt = 0
        ind = 0
        while(ind < len(entity) - 1):
            if(entity[ind][1] > entity[ind+1][0]) :
                cnt += 1
                entity.pop(ind)
                ind -= 1
            ind += 1
    return entity

@click.command()
@click.argument('input_filepath', type=click.Path(exists=True))
@click.argument('output_filepath', type=click.Path())
def main(input_filepath, output_filepath):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    path = get_project_root()
    input_filepath = path + '/' + input_filepath
    output_filepath = path + '/' + input_filepath
    directory = os.fsencode(input_filepath)

    data_for_span = []
    data_for_ner = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        file_full_path=input_filepath+filename
        with open(file_full_path) as f1:
            for line in f1:
                entt = []
                j_line=json.loads(line)
                for ent in j_line["entities"] :
                    entt.append([ent["start_offset"], ent["end_offset"], ent["label"]])
                data_for_span.append([j_line["text"],{"entities" : entt}])
                data_for_ner.append([j_line["text"],{"entities" : remove_overlap(entt)}])
    save_data(output_filepath + "/overlap.json", data_for_span)
    save_data(output_filepath + "/non-overlap.json", data_for_ner)

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
