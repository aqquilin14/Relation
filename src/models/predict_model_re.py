# print("I'm in predict_model.py")
import spacy
from relation_extraction.rel_pipe import make_relation_extractor, score_relations
from relation_extraction.rel_model import create_relation_model, create_classification_layer, create_instances, create_tensors
import click
import logging
from pathlib import Path
# from dotenv import find_dotenv, load_dotenv
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
                    
class RelationExtractor:

    def __init__(self):
        self.__model = spacy.load('models/ner/model-best')
        self.__re = spacy.load('models/relation_extraction/model-last')
        self.__model.add_pipe("tok2vec", name="re_tok2vec", source=self.__re)
        self.__model.add_pipe("relation_extractor", source=self.__re, last=True)
        
    def get_predictions(self, text: str, threshold: float = 0.5):
        doc = self.__model(text)
        ent = []
        count = 0
        for e in doc.ents :
            ent.append({"id":count, "start_offset": e.start, "text":e.text, "label": e.label_})
            count += 1
        rels = []
        rel_id = 0
        for value, rel_dict in doc._.rel.items():    
            for e in ent:
                for b in ent:
                    if e["start_offset"] == value[0] and b["start_offset"] == value[1]:
                        for key in rel_dict:    
                            threshold = 1.751218e-04
                            
                            if rel_dict[key]>=threshold:
                                rel_json = {
                                    "id":rel_id,
                                    "from_id": e["id"],
                                    "to_id": b["id"],
                                    "type":key
                                }
                                rel_id += 1
                                rels.append(rel_json)
        return ent, rels



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
                with open(root + "/" + mdF, "r") as f:
                    print(root+"/"+mdF)
                    text = f.read()
                    extractor = RelationExtractor()
                    ent, rels = extractor.get_predictions(text)
                    y = {
                        "fileName" : root + "/" + mdF,
                        "text" : text,
                        "entities" : ent,
                        "relations" : rels
                    }
                    write_json(y, output_filepath + "output.json", "output")
                    cnt += 1
                    print(cnt)

if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    
    main()

    
