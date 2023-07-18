# -*- coding: utf-8 -*-
import click
import logging
from dotenv import find_dotenv, load_dotenv
import os
import json
from pathlib import Path


def get_project_root() -> Path:
    return Path(__file__).parent.parent.parent


def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_data(file, data):
    with open(file, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def remove_overlap(entity_list):
    entity_list.sort()
    count = 1
    while count > 0:
        count = 0
        index = 0
        while index < len(entity_list) - 1:
            if entity_list[index][1] > entity_list[index+1][0]:
                count += 1
                entity_list.pop(index)
                index -= 1
            index += 1
    return entity_list


@click.command()
@click.argument('input_dir_path', type=click.Path(exists=True))
@click.argument('output_dir_path', type=click.Path())
def main(input_dir_path, output_dir_path):
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    path = get_project_root()
    input_dir_path = os.path.join(path, input_dir_path)
    output_dir_path = os.path.join(path, output_dir_path)
    data_for_spancat = []
    data_for_ner = []
    for file in os.listdir(input_dir_path):
        file_full_path = os.path.join(input_dir_path, file)
        with open(file_full_path) as f:
            for line in f:
                entities = []
                annotated_text = json.loads(line)
                for annotated_entity in annotated_text["entities"]:
                    entities.append([annotated_entity["start_offset"], annotated_entity["end_offset"],
                                     annotated_entity["label"]])
                data_for_spancat.append([annotated_text["text"], {"entities": entities}])
                data_for_ner.append([annotated_text["text"], {"entities": remove_overlap(entities)}])
    save_data(output_dir_path + "overlap.json", data_for_spancat)
    save_data(output_dir_path + "non-overlap.json", data_for_ner)

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
