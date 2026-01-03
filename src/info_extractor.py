# D:\ATS_project\src\info_extractor.py

import spacy
# from .utils import load_spacy_model # We no longer need to call load_spacy_model here globally

# REMOVE THIS LINE: nlp_keyword_matcher = load_spacy_model("en_core_web_sm")

def extract_entities(text, nlp_model): # ADD nlp_model as an argument
    """
    Extracts entities (e.g., SKILLS, QUALIFICATION) from text using the provided Spacy model.
    It processes the raw text directly as NER models are often trained on raw text.
    """
    if not isinstance(text, str) or not text.strip():
        return {} # Return empty dictionary for invalid or empty text

    # Process the text with the provided SpaCy model
    doc = nlp_model(text) # Use the passed nlp_model

    extracted_data = {}
    for ent in doc.ents:
        label = ent.label_
        entity_text = ent.text

        if label not in extracted_data:
            extracted_data[label] = []
        extracted_data[label].append(entity_text)

    for label, entities in extracted_data.items():
        extracted_data[label] = sorted(list(set(e.lower() for e in entities)))

    return extracted_data

# The __main__ block for testing would also need to be updated if you use it for standalone testing.
# For now, focus on the function signature.