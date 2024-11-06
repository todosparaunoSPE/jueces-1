# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:37:29 2024

@author: jperezr
"""

# nlp_model.py

import spacy

def load_spacy_model():
    """
    Esta función carga el modelo de spaCy 'en_core_web_sm' y lo retorna.
    """
    # Cargar el modelo de spaCy
    nlp = spacy.load("en_core_web_sm")
    return nlp