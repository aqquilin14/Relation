from util.utility import Entity, Relation


class Extractor:

    TEXT_KEY: str = "text"
    ENTITIES_KEY: str = "entities"
    RELATIONS_KEY: str = "relations"

    ENTITY_ID: str = "id"
    ENTITY_START_OFFSET: str = "start_offset"
    ENTITY_END_OFFSET: str = "end_offset"
    ENTITY_LABEL: str = "label"

    RELATION_ID: str = "id"
    RELATION_SUBJECT: str = "from_id"
    RELATION_OBJECT: str = "to_id"
    RELATION_LABEL: str = "type"

    def __init__(self, dataset):
        self.dataset = dataset
        self.text = dataset[Extractor.TEXT_KEY]
        self.entities = dataset[Extractor.ENTITIES_KEY]
        if Extractor.RELATIONS_KEY in dataset:
            self.relations = dataset[Extractor.RELATIONS_KEY]
        else:
            self.relations = []

        self.num_entity = len(self.entities)
        self.num_relation = len(self.relations)
        self.extracted_entity = int(0)
        self.extracted_relation = int(0)
        self.counter = int(0)   # Counter to produce dummy id's for when entity object in json doesn't have "id" field

    # Returns True if more entities could be extracted
    def has_entity(self) -> bool:
        if self.extracted_entity < self.num_entity:
            return True
        else:
            return False

    # Returns True if more relations could be extracted
    def has_relation(self) -> bool:
        if self.extracted_relation < self.num_relation:
            return True
        else:
            return False

    # Returns the object for the next entity
    def next_entity(self) -> tuple[int, Entity]:
        curr_entity = self.entities[self.extracted_entity]
        entity_text = self.get_span(curr_entity[Extractor.ENTITY_START_OFFSET],
                                    curr_entity[Extractor.ENTITY_END_OFFSET])
        entity_label = curr_entity[Extractor.ENTITY_LABEL]
        if Extractor.ENTITY_ID in curr_entity:
            entity_id = curr_entity[Extractor.ENTITY_ID]
        else:
            entity_id = self.counter
            self.counter += 1

        extracted = Entity(entity_text, entity_label)

        self.extracted_entity += 1

        return entity_id, extracted

    # Returns the object for the next relation
    def next_relation(self) -> Relation:
        curr_relation = self.relations[self.extracted_relation]
        relation_subject_id: int = curr_relation[Extractor.RELATION_SUBJECT]
        relation_predicate: str = curr_relation[Extractor.RELATION_LABEL]
        relation_object: int = curr_relation[Extractor.RELATION_OBJECT]

        self.extracted_relation += 1

        return Relation(relation_subject_id, relation_predicate, relation_object)

    # Returns the text span associated with an offset
    def get_span(self, start_offset: int, end_offset: int) -> str:
        return self.text[start_offset: end_offset]
