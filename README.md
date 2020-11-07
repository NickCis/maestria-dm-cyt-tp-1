# Clasificación de géneros musicales a partir de algoritmos de clustering

Links útiles:
 - [Enunciado](./DMCT_TP1_Clustering_Musica.pdf)
 - [Informe](https://www.overleaf.com/project/5fa1ef54dfa0a39e63bc8c8c)

Este trabajo implementa diferentes técnicas de clustering en piezas musicales de diversos géneros ('ambient', 'clásica','death metal','jazz','ópera', 'canta-autor','ska' y 'trance') con el fin de conocer si hay una agrupación natural entre sí. Con ese objetivo, se aplicaron diferentes modelos de clustering (Kmeans, Clustering jerárquico y DBSCAN). Todos los métodos utilizados presentaron dificultades para proveer, sobre los conjuntos de datos utilizados,  una clasificación distinguible entre los géneros

Este respositorio incluye el código utilizado para el [procesamiento del set de datos](./processing.py) y la [generación de los clusters](./clusters.py).

## Autores

 - Nicolas Cisco
 - Federico Scenna
 - Florencia Tadeo

## Requerimientos

Para poder correr el código e instalar las dependencias relacionado con el trabajo se requiere:
- Python 3
- pip 3

## Dependencias

Se requiere la instalación de las siguientes dependencias:

 - numpy
 - pandas
 - sklearn

```
pip install numpy pandas sklearn
```

## Descarga del dataset

Se debe descargar el dataset provisto por la catedra y colocarlo en la carpeta `dataset`.

```
wget 'https://www.dropbox.com/s/ms6260jqmsmz5qu/audio_features.pickle?dl=1' -O dataset/audio_features.pickle
wget 'https://www.dropbox.com/s/8d0y9bms80ly8ui/tracks.pickle?dl=1' -O dataset/tracks.pickle
wget 'https://www.dropbox.com/s/1cmb8e8zvv6hsfs/audio_analysis.pickle?dl=1' -O dataset/audio_analysis.pickle
```

## Procesamiento del set de datos

Inicialmente se obtuvieron tres conjuntos de datos:

 - **Tracks**: Dataset con metadatos de los tracks. De este dataset se extrajeron las variables: Album, Artista, Año, Género.
 - **Audio Features**: Dataset con atributos globales de alto nivel para cada track.
 - **Audio Analysis**: Dataset que cotiene variables continuas de bajo nivel, estimadas en ventanas temporales. En este dataset se realizó una reducción de variables por canción, tomando el promedio y el desviío estandar del timbre entre todas las ventanas.

El script `processing.py` es el encargado de procesar estos set de datos para generar uno.

```
python processing.py
```

Al finalizar, se generará un archivo llamado `datasets/dm-ct-tp1-dataset.csv`

## Agrupamiento en clusters

El script `clustering.py` realiza el agrupamiento utilizando tres algoritmos distintos:

 - KMeans
 - Agglomerative
 - DBSCAN

Al finalizar, se generará un archivo llamado `datasets/result.csv`.

## Ejecución vía Docker

Se incluye un _Dockerfile_ para hacer más sencilla la ejecución de los modelos en cualquier entorno:

Construcción de la imagen:

```
docker build -t dm-cyt-1 .
```

Ejecución del procesamiento del dataset:

```
docker run -ti --rm -v `pwd`/dataset:/opt/dm-cyt/dataset dm-cyt-1 python processing.py
```

Ejecución de los modelos de clustering:

```
docker run -ti --rm -v `pwd`/dataset:/opt/dm-cyt/dataset dm-cyt-1 python clustering.py
```

## Uso de formáto de marcado estandarizado

Se evaluó la utilización de [PMML](https://en.wikipedia.org/wiki/Predictive_Model_Markup_Language) _(Predictive Model Markup Language)_

Como primera limitante de la utilización de dicho lenguaje de marcado es que el mismo esta orientado a la descripción de modelos predictivos. Principalmente, el objetivo de PPML es la especificación de procesos de modelos predictivos para que sea más sencillo llevarlos a ambientes productivos. El objetivo de este trabajo no es la utilización de modelos predictivos, sino, modelos de agrupamiento, es decir, clustering, lo que inicialmente nos da una pauta de que no sería la herramienta adecuada.

Ya que se utilizó _sklearn_ como implementación de los modelos de clustering se tienen dos alternativas para generar dicho lenguaje de marcado:

 - [`sklearn-pmml`](https://github.com/alex-pirozhenko/sklearn-pmml)
 - [`sklearn2pmml`](https://github.com/jpmml/sklearn2pmml) (que una abstracción de [`JPMML-SkLearn`](https://github.com/jpmml/jpmml-sklearn))

Ninguna de ellas da soporte para los algoritmos utilizados. Por un lado `sklearn-pmml` no soporta ningún algoritmo de clustering, por el otro lado `JPMML-SkLearn` solo soporta kmeans de los tres algoritmos utilizados.

En base a esto, se decidió utilizar Docker como manera genérica para permitir una facilidad de ejecución de los modelos.


