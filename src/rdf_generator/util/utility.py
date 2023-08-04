from constants import NAMESPACE
from entity_linker.entity_linker import EntityLinker
from typing import Callable


class Entity:

    # Note that is_literal_class should be set to True iff all instances of the entity class would be literals
    def __init__(self, entity_text: str, entity_label: str,
                 entity_linker: Callable[[str, str], tuple[bool, bool]] = EntityLinker.rule_based_linker):
        self.namespace = NAMESPACE
        self.entity_label = entity_label
        self.entity_linker = entity_linker
        self.is_literal_class, self.is_canonical_item = self.entity_linker(entity_text, entity_label)
        if not self.is_literal_class:
            self.entity_text = entity_text.strip().replace("`", "").replace(" ", "_")
        else:
            self.entity_text = entity_text.strip()


class Relation:

    def __init__(self, relation_subject: int, relation_predicate: str, relation_object: int):
        self.namespace: str = NAMESPACE
        self.relation_subject: int = relation_subject
        self.relation_predicate: str = relation_predicate
        self.relation_object: int = relation_object
