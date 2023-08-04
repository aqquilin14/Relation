from spacy import load as spacy_load
from spacy.tokens import Span
import constants

nlp = spacy_load(constants.SPACY_PIPELINE)


def get_input_data():
    # text = 'Attribute based access control enables administrators to control access to specific objects and/or capabilities based on attributes'
    # doc = nlp(text)
    # span = Span(doc, 0, 4, label='policy')
    # doc.ents = [span]

    # text = 'The administrator has previledged access rights, as against other roles like ordinary users.'
    # doc = nlp(text)
    # span1 = Span(doc, 1, 2, label='role')
    # span2 = Span(doc, 10, 11, label='role')
    # span3 = Span(doc, 13, 14, label='role')
    # doc.ents = [span1, span2, span3]

    # text = 'The attribute based access control API is used to access roles, products, permission categories, and permission sets within Adobe Experience Platform'
    # doc = nlp(text)
    # span = Span(doc, 1, 5, label='policy')
    # doc.ents = [span]

    candidates = ['CRM_connector', 'cloud_connector', 'streaming_connector']


    text = 'Let\'s use Azure Blob storage. To configure it, first select the desired source, and enter cloud authentication credentials. The data will be fetched from the Azure Blob Storage and will be mapped to XDM.'
    doc = nlp(text)
    span = Span(doc, 12, 13, label='connector')

    # text = 'The connector provides built in support for conversion of data stream ingested to XDM.'
    # doc = nlp(text)
    # span = Span(doc, 1, 2, label='connector')

    # text = 'Ingestion of association data past purchases, loyalty memberships, demography through the connector helps to stich a 360-degree view of the profile.'
    # doc = nlp(text)
    # span = Span(doc, 13, 14, label='connector')

    doc.ents = [span]
    return doc, candidates
