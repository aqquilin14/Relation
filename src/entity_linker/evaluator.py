
def evaluator(tok1, tok2, weight):
    return ( tok1.similarity(tok2)**2 )* weight
