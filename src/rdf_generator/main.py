import json

from constants import INPUT_JSON_PATH, OUTPUT_RDFXML_PATH
from util.extractor import Extractor
from util.triple_depot import TripleDepot

if __name__ == '__main__':
    with open(INPUT_JSON_PATH, "r") as ip_file:
        dataset = json.loads(ip_file.read())

    extractor: Extractor = Extractor(dataset)

    triple_store: TripleDepot = TripleDepot(extractor)
    triple_store.dump(OUTPUT_RDFXML_PATH)
