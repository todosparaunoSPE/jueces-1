# -*- coding: utf-8 -*-
"""
Created on Tue Nov  5 12:19:27 2024

@author: jperezr
"""



import streamlit as st
from PyPDF2 import PdfReader
import pandas as pd
import spacy
import random

# Cargar el modelo de spaCy
nlp = spacy.load("en_core_web_sm")

def evaluar_contenido(texto):
    # Lógica para evaluar el contenido
    keywords = ["justicia", "derecho", "tribunal", "juicio", "prueba"]
    puntuacion = sum(1 for word in keywords if word in texto.lower())
    return random.randint(3, 5) + puntuacion  # Calificación base más algún extra

def evaluar_estructura(texto):
    # Lógica para evaluar la estructura
    doc = nlp(texto)  # Usamos spaCy para procesar el texto
    num_parrafos = texto.count('\n\n') + 1
    num_oraciones = len([sent for sent in doc.sents if sent.text.strip() != ''])  # Número de oraciones en el texto
    return random.randint(3, 5) + (num_oraciones // 2)  # Calificación base más número de oraciones

def evaluar_estilo(texto):
    # Lógica para evaluar el estilo
    doc = nlp(texto)  # Usamos spaCy para procesar el texto
    oraciones = list(doc.sents)  # Convertir el generador de oraciones en una lista
    long_media = sum(len(sent) for sent in oraciones) / len(oraciones) if len(oraciones) > 0 else 0
    
    if long_media < 15:
        return random.randint(4, 5)  # Mejores estilos tienen oraciones más cortas
    else:
        return random.randint(2, 4)  # Estilo menos atractivo si oraciones son largas

def evaluar_originalidad(texto):
    # Lógica para evaluar la originalidad
    frases_cliches = ["en conclusión", "es importante destacar", "finalmente"]
    return random.randint(2, 4) if any(frase in texto for frase in frases_cliches) else random.randint(4, 5)

def evaluar_impacto(texto):
    # Lógica para evaluar el impacto
    if "debería" in texto or "es crucial" in texto:
        return random.randint(4, 5)
    return random.randint(2, 4)

def evaluar_ensayo(texto):
    # Evaluar contenido, estructura, estilo, originalidad e impacto
    contenido = evaluar_contenido(texto)
    estructura = evaluar_estructura(texto)
    estilo = evaluar_estilo(texto)
    originalidad = evaluar_originalidad(texto)
    impacto = evaluar_impacto(texto)

    # Calificación final como promedio
    calificacion_final = (contenido + estructura + estilo + originalidad + impacto) / 5
    
    return contenido, estructura, estilo, originalidad, impacto, calificacion_final

def main():
    st.title("Evaluación de Ensayos Judiciales")

    # Sidebar con sección de ayuda
    st.sidebar.markdown("## Ayuda")
    st.sidebar.markdown("""
    ### Evaluación de Ensayos Judiciales
    Esta aplicación permite evaluar ensayos judiciales en formato PDF mediante un sistema de calificación basado en cinco criterios: Contenido, Estructura, Estilo, Originalidad e Impacto. Los ensayos son analizados utilizando técnicas de procesamiento de lenguaje natural (NLP) para generar calificaciones y seleccionar los mejores candidatos.

    #### ¿Cómo Funciona?
    1. **Carga de Archivos PDF**: Los usuarios pueden cargar uno o varios archivos PDF que contienen los ensayos que desean evaluar.
    2. **Extracción de Texto**: El texto se extrae de cada archivo PDF utilizando la biblioteca `PyPDF2`.
    3. **Evaluación del Ensayo**: Cada ensayo se evalúa según cinco criterios:
        - **Contenido**: Evaluación de palabras clave relevantes.
        - **Estructura**: Análisis de la cohesión del texto.
        - **Estilo**: Longitud media de las oraciones y diversidad léxica.
        - **Originalidad**: Identificación de frases clichés.
        - **Impacto**: Presencia de elementos persuasivos.
    4. **Cálculo de Calificaciones**: Se suman las calificaciones de cada criterio para obtener una calificación total y un promedio.
    5. **Resultados**: Los resultados se muestran en una tabla con calificaciones.
    6. **Guardar Resultados**: Puedes guardar los resultados en un archivo Excel.

    #### Requisitos
    - Python 3.x
    - Bibliotecas: `streamlit`, `PyPDF2`, `pandas`, `spacy`
    - Asegúrate de tener el modelo de spaCy (`en_core_web_sm`) instalado.
    """)

    # Resto de tu código para carga y evaluación de ensayos
    uploaded_files = st.file_uploader("Cargar archivos PDF", accept_multiple_files=True)
    
    # Procesar archivos y evaluar ensayos
    if uploaded_files:
        results = []
        for uploaded_file in uploaded_files:
            # Leer el PDF
            reader = PdfReader(uploaded_file)
            texto = ''
            for page in reader.pages:
                texto += page.extract_text() + ' '

            # Evaluar el ensayo
            calificaciones = evaluar_ensayo(texto)
            results.append([uploaded_file.name] + list(calificaciones))

        # Crear un DataFrame y mostrar los resultados
        df_resultados = pd.DataFrame(results, columns=['Archivo', 'Contenido', 'Estructura', 'Estilo', 'Originalidad', 'Impacto', 'Calificación Final'])
        st.write(df_resultados)

        # Obtener los mejores 5 candidatos
        mejores_candidatos = df_resultados.nlargest(5, 'Calificación Final')
        st.write("### Mejores 5 Candidatos")
        st.write(mejores_candidatos)

        # Guardar resultados en un archivo Excel
        if st.button("Guardar Resultados"):
            df_resultados.to_excel("resultados_evaluacion.xlsx", index=False)
            st.success("Resultados guardados en 'resultados_evaluacion.xlsx'")

if __name__ == "__main__":
    main()
