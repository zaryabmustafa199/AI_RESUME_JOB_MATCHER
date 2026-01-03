# D:\ATS_project\src\utils.py

import spacy
from sentence_transformers import SentenceTransformer
import streamlit as st # Keep this import for @st.cache_resource

@st.cache_resource
def load_spacy_model(model_name="en_core_web_sm"): # Ensure 'en_core_web_sm' is specified here
    """Loads a Spacy model. Let it raise exceptions if loading fails."""
    try:
        nlp = spacy.load(model_name)
        return nlp
    except Exception as e:
        # IMPORTANT: DO NOT call st.error() or st.stop() here.
        # Instead, raise a new exception so app.py can handle it gracefully.
        raise RuntimeError(f"Failed to load SpaCy model '{model_name}': {e}") from e

@st.cache_resource
def load_sentence_transformer_model(model_name='all-MiniLM-L6-v2'):
    """Loads a pre-trained Sentence Transformer model for embeddings."""
    try:
        model = SentenceTransformer(model_name)
        return model
    except Exception as e:
        # IMPORTANT: DO NOT call st.error() or st.stop() here.
        # Instead, raise a new exception so app.py can handle it gracefully.
        raise RuntimeError(f"Failed to load Sentence Transformer model '{model_name}': {e}") from e