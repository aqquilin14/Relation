from kg import get_context
from evaluator import evaluator as default_evaluator

# Get surrounding text, aliases
# Aliases must be contesting labels
def context_based_matcher(context_text, aliases, nlp, evaluator=default_evaluator):
    new_label = ''
    threshold = 0

    context_tok = [tok for tok in nlp(context_text) if tok.pos_ in ['PROPN', 'NOUN', 'VERB', 'ADJ']]

    for alias in aliases:
        alias_context = get_context(alias)
        weights = {}
        for elem in alias_context:
            doc = nlp(elem)

            for tok in doc:
                lemma = tok.lemma_
                pos = tok.pos_
                if pos in ['PROPN', 'NOUN']:
                    if lemma in weights:
                        weights[lemma] += 1
                    else:
                        weights[lemma] = 1
                elif pos in ['VERB', 'ADJ']:
                    if lemma in weights:
                        weights[lemma] += 0.5
                    else:
                        weights[lemma] = 0.5

        score = 0
        for lemma, weight in weights.items():
            tok = nlp(lemma)[0]
            for oth in context_tok:
                score += evaluator(oth, tok, weight)
        
        if score > threshold:
            new_label = alias
            threshold = score
    
    return new_label
