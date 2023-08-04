from graph import Graph, Node, Predicate

from rdflib import Graph as RDFGraph


class ExtractGraph:

    def __init__(self, input_file: str):
        self.rdf_graph = RDFGraph()
        self.rdf_graph.parse(input_file)

    def get_graph(self) -> Graph:
        graph = Graph()

        for subject in self.rdf_graph.subjects(unique=True):
            graph.nodes.append(Node(str(subject)))

        for relation_subject, relation_predicate, relation_object in self.rdf_graph.triples((None, None, None)):
            graph.edges.append(
                (Node(str(relation_subject)), Predicate(str(relation_predicate)), Node(str(relation_object)))
            )

        return graph
