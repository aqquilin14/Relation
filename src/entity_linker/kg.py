import requests


def get_select_query_string(label):
    return "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX aep: <https://www.adobe.com/aep/> PREFIX j.0: <aep:> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> SELECT ?x WHERE { { ?x rdfs:subClassOf j.0:"+label+" } UNION { ?x rdf:type aep:"+label+" } }"


def query_kg(query_string):
    response = requests.post(url='http://localhost:8080/kg/query', json={"queryString": query_string})

    if not response.ok:
        raise Exception
    
    response_json = response.json()
    return response_json


def get_fine_aliases(label):
    query_string = get_select_query_string(label)

    response_json = query_kg(query_string)
    
    if response_json['queryType'] != 'SELECT':
        raise Exception
    
    aliases = []
    for line in response_json['selectQueryResponse']['results']:
        alias = line['x']

        if alias.split(':')[0] != 'aep':
            continue

        aliases.append(alias.split(':')[1].replace('_', ' '))

    return aliases


def get_describe_query_string(alias):
    return "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX aep: <https://www.adobe.com/aep/> PREFIX j.0: <aep:> PREFIX owl: <http://www.w3.org/2002/07/owl#> PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> DESCRIBE aep:" + alias


def get_context(alias):
    query_string = get_describe_query_string(alias)

    response_json = query_kg(query_string)

    if response_json['queryType'] != 'DESCRIBE':
        raise Exception
    
    # Extracting only aep:relation triplets
    triples = response_json['describeQueryResponse']['statements']
    adj_nodes = []
    for triple in triples:
        if triple['predicate'].split('.')[1] == 'adobe':
            adj_nodes.append(triple['object'].split('^')[0].split('/')[-1].replace('_', ' '))
    
    return adj_nodes
    
    #get the label in case of full node, else the phrases in loteral