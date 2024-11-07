# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 09:34:12 2024

@author: jperezr
"""
import streamlit as st
import PyPDF2
import pandas as pd
import numpy as np
import re


# Estilo de fondo
page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background:
radial-gradient(black 15%, transparent 16%) 0 0,
radial-gradient(black 15%, transparent 16%) 8px 8px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 0 1px,
radial-gradient(rgba(255,255,255,.1) 15%, transparent 20%) 8px 9px;
background-color:#282828;
background-size:16px 16px;
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)


# Función para extraer texto de archivos PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page_num].extract_text()
    return text

# Función para evaluar el contenido de acuerdo con los criterios usando 're'
def evaluate_essay(text):
    # Evaluación de Contenido usando la longitud del texto (número de palabras)
    words = re.findall(r'\b\w+\b', text)  # Encuentra todas las palabras (sin puntuación)
    content_score = len(words)
    
    # Evaluación de Estructura (número de oraciones)
    sentences = re.split(r'[.!?]', text)  # Divide el texto en oraciones basadas en puntuación
    structure_score = len([sent for sent in sentences if sent.strip()])  # Oraciones no vacías
    
    # Evaluación de Estilo (diversidad de palabras)
    unique_words = len(set(words))  # Palabras únicas
    style_score = unique_words / len(words)  # Diversidad léxica
    
    # Evaluación de Originalidad (diversidad de frases)
    unique_sentences = len(set([sent.strip() for sent in sentences if sent.strip()]))  # Frases únicas
    original_score = unique_sentences / structure_score if structure_score > 0 else 0
    
    # Evaluación de Impacto (intensidad del sentimiento)
    # Usamos un enfoque simple: si hay más adjetivos o adverbios, el impacto es mayor
    sentiment_score = len(re.findall(r'\b(quick|slow|good|bad|interesting|important)\b', text, re.IGNORECASE))  # Palabras clave
    impact_score = sentiment_score * 2  # Escalar el impacto
    
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
