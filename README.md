# Custom Embeddings con Gensim

Proyecto de Procesamiento de Lenguaje Natural que entrena embeddings personalizados usando Gensim.

## 📝 Descripción

Este proyecto crea vectores de embeddings personalizados utilizando diferentes datasets de texto:
- Letras de canciones de diversos artistas (dataset principal)
- Evangelio de Juan de la Biblia de Jerusalén

El objetivo es explorar las relaciones semánticas entre palabras y visualizar similitudes en el espacio de embeddings.

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 📊 Uso

Abre y ejecuta el notebook principal:

```bash
jupyter notebook main.ipynb
```

El notebook incluye:
- Carga y preprocesamiento de datos
- Entrenamiento de modelos Word2Vec con diferentes parámetros
- Análisis de similitudes entre términos
- Visualizaciones de embeddings

## 📁 Estructura del Proyecto

- `main.ipynb` - Notebook principal con todo el análisis
- `songs_dataset/` - Letras de canciones de diversos artistas
- `evangelio_juan.txt` - Texto del Evangelio de Juan
- `scraper.py` - Script para descargar textos desde la web
- `vectors.tsv` y `labels.tsv` - Embeddings exportados para visualización

## 🛠️ Tecnologías

- Python
- Gensim (Word2Vec)
- NLTK (preprocesamiento)
- Matplotlib/Seaborn (visualización)
- BeautifulSoup (web scraping)

## 📌 Notas

El proyecto incluye experimentos comparando diferentes configuraciones de entrenamiento para evaluar la coherencia de los embeddings resultantes.
