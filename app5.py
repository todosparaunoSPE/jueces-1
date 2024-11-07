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
    structure_score = len(re.findall(r'\.', text))  # Número de oraciones
    
    # Evaluación de Estilo (usando la diversidad de palabras)
    unique_words = len(set(text.split()))  # Número de palabras únicas
    style_score = unique_words / len(text.split())  # Diversidad léxica
    
    # Evaluación de Originalidad (diversidad de frases y complejidad)
    original_score = len(set([sent for sent in text.split('.')])) / structure_score
    
    # Evaluación de Impacto (intensidad del sentimiento, que es la polaridad del texto)
    impact_score = len(re.findall(r'\b(?:impact|important|crucial|critical)\b', text, re.IGNORECASE))  # Recuento de palabras de impacto
    
    return content_score, structure_score, style_score, original_score, impact_score

# Interfaz de Streamlit
st.title("Evaluación Automática de Ensayos: Selección de Candidatos para Ocupación de Vacantes Según la Nueva Reforma del Poder Judicial")

# Sección de Ayuda en el sidebar
with st.sidebar:
    st.header("Ayuda")
    st.write("""
    ### ¿Cómo funciona esta aplicación?
    Esta aplicación permite la evaluación automatizada de ensayos, útil para agilizar el proceso de selección de candidatos para ocupar vacantes en el Poder Judicial de la Federación.
    
    ### Criterios de Evaluación:
    1. **Contenido**: Se evalúa la cantidad de palabras en el texto.
    2. **Estructura**: Se mide el número de oraciones en el ensayo.
    3. **Estilo**: Se calcula la diversidad léxica, es decir, cuántas palabras diferentes se utilizan.
    4. **Originalidad**: Se evalúa la complejidad del texto y la diversidad de las frases.
    5. **Impacto**: Se analizan las palabras clave que denotan importancia y relevancia del ensayo.

    ### ¿Por qué es importante?
    Este sistema ayuda a reducir el tiempo necesario para evaluar los ensayos, permitiendo al comite evaluador puedan centrarse en aspectos más cualitativos y estratégicos de la selección de los candidatos.
    """)

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
