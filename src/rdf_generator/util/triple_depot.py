from util.extractor import Extractor
from util.utility import Entity, Relation
import constants
# from constants import NAMESPACE, DEFAULT_AEP_PREAMBLE


class TripleDepot:

    def __init__(self, extractor: Extractor):
        self.entities: dict[int, Entity] = {}
        self.declared_entities: dict[int, bool] = {}
        self.relations: dict[int, list[Relation]] = {}

        self.extract_entities(extractor)
        self.extract_relation(extractor)

    def extract_entities(self, extractor: Extractor) -> None:
        while extractor.has_entity():
            entity_id, entity = extractor.next_entity()
            self.entities[entity_id] = entity
            self.declared_entities[entity_id] = False

    def extract_relation(self, extractor: Extractor) -> None:
        while extractor.has_relation():
            relation: Relation = extractor.next_relation()
            if relation.relation_subject in self.relations:
                self.relations[relation.relation_subject].append(relation)
            else:
                self.relations[relation.relation_subject] = [relation]

    # Dumps the stored entity and relations into the specified file as RDF/XML
    def dump(self, filename: str, preamble: str = constants.DEFAULT_AEP_PREAMBLE,
             namespace: str = constants.NAMESPACE, namespace_url: str = constants.NAMESPACE_URL) -> None:
        with open(filename, "w") as f:
            # Write preamble
            f.write("<rdf:RDF")
            f.write(preamble)
            f.write(">\n")

            # Dumping self-classes entities using owl:sameAs
            for entity_id, entity in self.entities.items():
                if entity.is_canonical_item:
                    f.write("<owl:Class rdf:about=\"")
                    f.write(entity.entity_text)
                    f.write("\">\n")

                    f.write("<owl:sameAs rdf:resource=\"" + namespace + ":")
                    f.write(entity.entity_label)
                    f.write("\"/>\n")

                    f.write("</owl:Class>\n")

            # Dumping relations and instance entities
            for subject_id, relation_subject in self.entities.items():

                if subject_id not in self.relations:
                    continue

                # Opening subject scope
                f.write("<" + namespace + ":")
                f.write(relation_subject.entity_label)
                # f.write(" rdf:about=\"" + NAMESPACE + ":")
                f.write(" rdf:about=\"")
                f.write(relation_subject.entity_text)
                f.write("\">")

                # Writing individual relations
                for relation in self.relations[subject_id]:
                    relation_object: Entity = self.entities[relation.relation_object]

                    if relation_object.is_literal_class:
                        f.write("<" + namespace + ":")
                        f.write(relation.relation_predicate)
                        f.write(" rdf:parseType=\"Literal\">")
                        f.write(relation_object.entity_text)

                        f.write("</" + namespace + ":")
                        f.write(relation.relation_predicate)
                        f.write(">\n")
                        continue

                    else:
                        # Non-literal class
                        # Opening relation scope
                        f.write("<" + namespace + ":")
                        f.write(relation.relation_predicate)
                        f.write(">")

                        # Object
                        f.write("<" + namespace + ":")
                        f.write(relation_object.entity_label)
                        f.write(" rdf:about=\"")
                        f.write(relation_object.entity_text)
                        f.write("\"/>")

                        # Closing relation scope
                        f.write("</" + namespace + ":")
                        f.write(relation.relation_predicate)
                        f.write(">")

                # Closing subject scope
                f.write("</" + namespace + ":")
                f.write(relation_subject.entity_label)
                f.write(">\n")

            # Closing the preamble
            f.write("</rdf:RDF>")
