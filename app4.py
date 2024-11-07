# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 14:03:16 2024

@author: jperezr
"""

import streamlit as st
import PyPDF2
import pandas as pd
import spacy
import numpy as np
import spacy.cli

# Descargar el modelo en caso de que no esté disponible
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Función para extraer texto de archivos PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Función para evaluar el contenido de acuerdo con los criterios
def evaluate_essay(text):
    # Evaluación de Contenido usando la longitud del texto
    content_score = len(text.split())  # Número de palabras
    
    # Evaluación de Estructura (Número de oraciones y uso adecuado de puntuación)
    doc = nlp(text)
    structure_score = len([sent for sent in doc.sents])  # Número de oraciones
    
    # Evaluación de Estilo (usando la diversidad de palabras)
    unique_words = len(set(text.split()))  # Número de palabras únicas
    style_score = unique_words / len(text.split())  # Diversidad léxica
    
    # Evaluación de Originalidad (diversidad de frases y complejidad)
    original_score = len(set([sent.text for sent in doc.sents])) / structure_score
    
    # Evaluación de Impacto (intensidad del sentimiento, que es la polaridad del texto)
    sentiment = doc.sentiment if hasattr(doc, 'sentiment') else 0
    impact_score = abs(sentiment) * 10  # Escalar el sentimiento
    
    return content_score, structure_score, style_score, original_score, impact_score

# Interfaz de Streamlit
st.title("Evaluación Automática de Ensayos: Selección de Candidatos para Ocupación de Vacantes Según la Nueva Reforma del Poder Judicial")

# Cargar archivos PDF
uploaded_files = st.file_uploader("Sube tus archivos PDF", type="pdf", accept_multiple_files=True)

if uploaded_files:
    results = []
    
    # Procesar cada archivo cargado
    for uploaded_file in uploaded_files:
        # Extraer texto del PDF
        text = extract_text_from_pdf(uploaded_file)
        
        # Mostrar el texto (para referencia)
        st.subheader(f"Texto extraído de {uploaded_file.name}:")
        st.write(text[:1000])  # Muestra solo los primeros 1000 caracteres

        # Evaluación automatizada del ensayo
        content_score, structure_score, style_score, original_score, impact_score = evaluate_essay(text)
        
        # Calificación final (promedio de los puntajes)
        final_score = np.mean([content_score, structure_score, style_score, original_score, impact_score])
        
        # Almacenar resultados
        results.append({
            "Archivo": uploaded_file.name,
            "Contenido": round(content_score, 2),
            "Estructura": round(structure_score, 2),
            "Estilo": round(style_score, 2),
            "Originalidad": round(original_score, 2),
            "Impacto": round(impact_score, 2),
            "Calificación Final": round(final_score, 2)
        })
    
    # Mostrar resultados en una tabla
    st.subheader("Resultados de la evaluación automática:")
    df = pd.DataFrame(results)
    st.write(df)

    # Obtener los 5 mejores candidatos ordenados por Calificación Final
    top_5 = df.sort_values(by="Calificación Final", ascending=False).head(5)
    
    st.subheader("Top 5 mejores ensayos:")
    st.write(top_5)