import constants
from spacy import load as spacy_load
from spacy.tokens import Span
from kg import get_fine_aliases


nlp = spacy_load(constants.SPACY_PIPELINE)


# returns span with new label
def entity_linker(doc, span, matcher):
    # For similarity based matcher
    aliases = get_fine_aliases(span.label_)
    aliases.append(span.label_)

    span_text = span.text.strip().replace("`", "")

    new_label = matcher(span_text, aliases, nlp)

    if new_label is None:
        new_label = span.label_
        return span
    else:
        return Span(doc, span.start, span.end, label=new_label)


def entity_linker(doc, span, matcher, aliases):
    # For context based alises
    start_idx = max(0, span.start - 10)
    end_idx = min(span.end + 20, len(doc))
    context_text = doc[start_idx: end_idx].text
    new_label = matcher(context_text, aliases, nlp)

    return Span(doc, span.start, span.end, label=new_label)
