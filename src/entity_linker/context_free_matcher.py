
def similarity_matcher(text, aliases, nlp, threshold=0.9):
    new_label = None

    text_lemma = ''
    for tok in nlp(text):
        text_lemma += tok.lemma_ + ' '
    span_doc = nlp(text_lemma)
    
    for alias in aliases:
        alias_lemma = ''
        for tok in nlp(alias):
            alias_lemma += tok.lemma_ + ' '
        alias_doc = nlp(alias_lemma)

        score = span_doc.similarity(alias_doc)
        if score > threshold:
            threshold = score
            new_label = alias

    return new_label
