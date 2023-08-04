INPUT_JSON_PATH: str = "./resources/input.json"
OUTPUT_RDFXML_PATH: str = "./resources/dataset.rdf"

NAMESPACE_URL: str = "https://www.adobe.com/aep/"
NAMESPACE: str = "aep"

DEFAULT_AEP_PREAMBLE: str = " \n\
    xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\" \n\
    xmlns:owl=\"http://www.w3.org/2002/07/owl#\" \n\
    xmlns:rdfs=\"http://www.w3.org/2000/01/rdf-schema#\" \n\
    xmlns:aep=\"https://www.adobe.com/aep/\" \n\
    xmlns:xsd=\"http://www.w3.org/2001/XMLSchema#\" "

LITERAL_INSTANCED_ENTITIES: list[str] = ["description", "title", "procedure", "path", "self_reference"]

CANONICAL_ENTITIES: list[str] = ["api", "attribute_based_access_control", "attributes", "role_based_access_control_environment",
                      "policy", "api_call"]

SPACY_PIPELINE: str = 'en_core_web_md'
