from input_data import get_input_data
from entity_linker import entity_linker
from context_free_matcher import similarity_matcher
from context_based_matcher import context_based_matcher


if __name__ == '__main__':
    # doc = get_input_data()
    
    # new_spans = []
    # for span in doc.ents:
    #     new_span = entity_linker(doc, span, similarity_matcher)
    #     new_spans.append(new_span)

    # doc = get_input_data()
    # aliases = ['attribute_based_access_control', 'access_policy']
    # new_spans = []
    # for span in doc.ents:
    #     new_span = entity_linker(doc, span, context_based_matcher, aliases)
    #     new_spans.append(new_span)

    # doc.ents = new_spans
    
    doc, candidates = get_input_data()
    new_span = entity_linker(doc, doc.ents[0], context_based_matcher, candidates)

    doc.ents = [new_span]

    print(doc.text)
    for span in doc.ents:
        print('text:', span.text, '\tlabel:', span.label_)
    