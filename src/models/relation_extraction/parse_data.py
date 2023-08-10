# print("I'm in parse.py")
import json
import typer
from pathlib import Path
from wasabi import Printer
import traceback
import re
import spacy
from spacy.vocab import Vocab
from spacy.lang.en import English
from spacy.tokenizer import Tokenizer
from spacy.tokens import Span, DocBin, Doc
from spacy.util import compile_infix_regex

nlp = spacy.blank("en")
# Create a blank Tokenizer with just the English vocab

msg = Printer()

MAP_LABELS = {
  "has_title": "has_title",
  "has_description": "has_description",
  "has_function": "has_function",
  "has_feature": "has_feature",
  "has_path": "has_path",
  "refers_self": "refers_self",
  "field_for": "field_for",
  "has_field": "has_field",
  "accessibility_aid": "accessibility_aid",
  "has_procedure": "has_procedure",
  "subTypeOf": "subTypeOf",
  "has_prereq": "has_prereq"
}


def main(json_loc_train: Path, json_loc_dev: Path, json_loc_test: Path, train_file: Path, dev_file: Path,
         test_file: Path):
    """Creating the corpus from the Prodigy annotations."""
    Doc.set_extension("rel", default={})
    vocab = Vocab()

    docs = {"train": [], "dev": [], "test": []}
    ids = {"train": set(), "dev": set(), "test": set()}
    count_all = {"train": 0, "dev": 0, "test": 0}
    count_pos = {"train": 0, "dev": 0, "test": 0}
    file_paths = {"train": train_file, "dev": dev_file, "test": test_file}

    for set_type, json_loc in zip(['train', 'dev', 'test'], [json_loc_train, json_loc_dev, json_loc_test]):
        # with json_loc.open("r", encoding="utf8") as jsonfile:
        with open(json_loc, 'r', encoding='utf8') as jsonfile:
            for line in jsonfile:
                example = json.loads(line)
                span_starts = set()
                if example["answer"] == "accept":
                    neg = 0
                    pos = 0
                    try:
                        doc = nlp(example["text"])
                        
                        # Parse the entities
                        spans = example["entities"]
                        entities = []
                        span_end_to_start = {}
                        for span in spans:
                            entity = doc.char_span(span["start_offset"], span["end_offset"], label=span["label"])
                            
                            if entity is not None and not any(entity.start < ent.end for ent in entities):
                                entities.append(entity)
                                span_starts.add(span["token_start"])
                                span_end_to_start[span["token_end"]] = span["token_start"]
                        doc.ents = entities
                        


                        # Parse the relations
                        rels = {}
                        for x1 in span_starts:
                            for x2 in span_starts:
                                rels[(x1, x2)] = {}
                        relations = example["relations"]
                        for relation in relations:
                            # the 'head' and 'child' annotations refer to the end token in the span
                            # but we want the first token
                            
                            start = span_end_to_start.get(relation["head"])
                            if start is not None: 
                                end = span_end_to_start.get(relation["child"])
                                if end is not None :
                                    label = relation["type"]
                                    label = MAP_LABELS[label]
                                    if label not in rels[(start, end)]:
                                        rels[(start, end)][label] = 1.0
                                        pos += 1

                        # The annotation is complete, so fill in zero's where the data is missing
                        for x1 in span_starts:
                            for x2 in span_starts:
                                for label in MAP_LABELS.values():
                                    if label not in rels[(x1, x2)]:
                                        neg += 1
                                        rels[(x1, x2)][label] = 0.0
                        doc._.rel = rels

                        # only keeping documents with at least 1 positive case
                        if pos > 0:
                            ids[set_type].add(doc)
                            docs[set_type].append(doc)
                            count_pos[set_type] += pos
                            count_all[set_type] += pos + neg
                    except KeyError as e:
                        print('relation_Child: ', relation["child"])
                        print(traceback.format_exc())
                        msg.fail("skipping doc due to error")
                        # msg.fail(f"Skipping doc because of key error: {e} in {example['meta']['source']}")

        docbin = DocBin(docs=docs[set_type], store_user_data=True)
        docbin.to_disk(file_paths[set_type])
        msg.info(
            f"{len(docs[set_type])} training sentences from {len(ids[set_type])} articles, "
            f"{count_pos[set_type]}/{count_all[set_type]} pos instances."
        )


if __name__ == "__main__":
    typer.run(main)

