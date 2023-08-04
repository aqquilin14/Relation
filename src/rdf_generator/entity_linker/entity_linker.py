from constants import CANONICAL_ENTITIES, LITERAL_INSTANCED_ENTITIES, SPACY_PIPELINE
from difflib import SequenceMatcher
from spacy import load as spacy_load, Language as SpacyLanguage
from spacy.tokens import Doc as SpacyDoc


nlp: SpacyLanguage = spacy_load(SPACY_PIPELINE)

class EntityLinker:

    @staticmethod
    def rule_based_linker(entity_text: str, entity_label: str, threshold: float = 0.8) -> tuple[bool, bool]:
        '''
        :param entity_text: the physical text in the span of the instance
        :param entity_label: the assigned label
        :param threshold: the minimum score to assume similarity
        :return: a tuple (is_literal_class, is_canonical_item)
        '''
        if entity_label in CANONICAL_ENTITIES:
            return False, True
        elif entity_label in LITERAL_INSTANCED_ENTITIES:
            return True, False
        else:
            # Checking for distance
            similarity: float = SequenceMatcher(None, entity_label, entity_text).ratio()
            if similarity > threshold:
                return False, True
            else:
                return False, False

    @staticmethod
    def lemmatizing_linker(entity_text: str, entity_label: str) -> tuple[bool, bool]:
        text_doc: SpacyDoc = nlp(entity_text)
        label_doc: SpacyDoc = nlp(entity_label)

        text_lemma = text_doc[0].lemma_
        label_lemma = label_doc[0].lemma_

        if entity_label in LITERAL_INSTANCED_ENTITIES:
            return True, False
        elif text_lemma == label_lemma:
            return False, True
        else:
            return False, False

    @staticmethod
    def embedding_based_linker(entity_text: str, entity_label: str, threshold: float = 0.8) -> tuple[bool, bool]:
        text_doc: SpacyDoc = nlp(entity_text)
        label_doc: SpacyDoc = nlp(entity_label)

        if entity_label in LITERAL_INSTANCED_ENTITIES:
            return True, False
        elif text_doc.similarity(label_doc) > threshold:
            return False, True
        else:
            return False, False
