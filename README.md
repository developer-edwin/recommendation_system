# recommendation_system
Sistema de recomendaciones de juegos basado en la información de la plataforma Steam

# Introducción al Proyecto de Machine Learning

Dentro del contexto de este proyecto de Machine Learning, nos enfrentamos a un desafío de gran envergadura en el ámbito de Steam, una plataforma internacional de videojuegos. Nuestra tarea principal consiste en desarrollar un sistema de recomendación de videojuegos para usuarios. Iniciaremos este proyecto desde cero, con el objetivo de crear un Producto Mínimo Viable (MVP) que cumpla con los requerimientos de Steam.

A pesar de los desafíos, como la falta de madurez en los datos y la ausencia de procesos automatizados, estamos comprometidos en llevar a cabo este proyecto, desde la etapa de ingeniería de datos hasta la implementación de una API accesible desde cualquier dispositivo en línea. Los invitamos a unirse a nosotros en este viaje, donde la satisfacción del jugador es nuestra prioridad.



# ETL

**Archivo 1: output_steam_games.json**

Este archivo contiene datos relacionados con juegos de Steam. El proceso de ETL se realiza de la siguiente manera:

**Extract (Extraer):**
- Se abre el archivo JSON utilizando la función `open` y se lee línea por línea.
- Cada línea se convierte de JSON a un diccionario utilizando `json.loads`.
- Los diccionarios resultantes se agregan a una lista `data`.

**Transform (Transformar):**
- Se crea un DataFrame llamado `df_games` a partir de la lista de diccionarios `data`.
- El DataFrame `df_games` contendrá información sobre los juegos de Steam.

**Load (Cargar):**
- Los datos transformados se almacenan en el DataFrame `df_games`.

---

**Archivo 2: australian_users_items.json**

Este archivo contiene datos relacionados con usuarios y elementos australianos. El proceso de ETL se realiza de la siguiente manera:

**Extract (Extraer):**
- Se abre el archivo JSON utilizando la función `open` y se lee línea por línea.
- Cada línea se evalúa utilizando `eval` para convertirla en un diccionario de Python.
- Los diccionarios resultantes se agregan a una lista `records`.

**Transform (Transformar):**
- Se crea un DataFrame llamado `df_items` a partir de la lista de diccionarios `records`.
- El DataFrame `df_items` contendrá información sobre usuarios y elementos australianos.

**Load (Cargar):**
- Los datos transformados se almacenan en el DataFrame `df_items`.

---

**Archivo 3: australian_user_reviews.json**

Este archivo contiene datos relacionados con revisiones de usuarios australianos. El proceso de ETL se realiza de la siguiente manera:

**Extract (Extraer):**
- Se abre el archivo JSON utilizando la función `open` y se lee línea por línea.
- Las líneas se concatenan en una cadena `fixed_data` después de eliminar las comas al final de las líneas y encerrar todo en corchetes para formar una lista de diccionarios válida.
- La cadena `fixed_data` se evalúa utilizando `eval` para convertirla en una lista de diccionarios de Python.

**Transform (Transformar):**
- Se crea un DataFrame llamado `reviews_df` a partir de la lista de diccionarios.
- El DataFrame `reviews_df` se crea combinando información de usuarios, elementos y revisiones.

**Load (Cargar):**
- Los datos transformados se almacenan en el DataFrame `reviews_df`.


# EDA

## Games

- El DataFrame contiene información sobre juegos de Steam.
- Se han eliminado las filas donde la columna 'genres' es nula.
- Se han realizado varias transformaciones en la columna 'release_date' para asegurarse de que esté en formato 'yyyy-mm-dd'.

## Valores Faltantes

- No existen registros con valores 'NaN' en las columnas 'title' o 'id'.

## Fecha de Lanzamiento (release_date)

- La columna 'release_date' ahora contiene fechas en formato 'yyyy-mm-dd'.
- Se han identificado y cambiado registros con fechas no válidas (por ejemplo, 'soon') por '0000-00-00'.
- Algunos registros pueden no cumplir con la estructura 'yyyy-mm-dd', y estos se han identificado.

## Géneros (genres)

- La columna 'genres' ha sido convertida en columnas binarias, donde cada columna representa un género y contiene valores 0 o 1 según la presencia del género en el juego.

## DataFrame Final

- El DataFrame final, `df_games_final`, incluye las columnas 'id', 'title', 'genres' y 'release_date'.

## Guardado de Datos

- El DataFrame final se ha guardado como un archivo CSV en la ruta '/content/drive/MyDrive/pf_henry/datasets/games.csv'.

## Items

- Número total de filas: [Número de filas]
- Número total de columnas: [Número de columnas]

## Columnas importantes

- `user_id`: Identificación única del usuario.
- `items_count`: Cantidad de elementos relacionados con el usuario.
- `steam_id`: Identificación de Steam del usuario.
- `user_url`: URL del usuario.

## Estadísticas descriptivas para las columnas numéricas

- `items_count`:
  - Número total de elementos: [Número total de elementos]
  - Valor medio: [Valor medio]
  - Valor mínimo: [Valor mínimo]
  - Valor máximo: [Valor máximo]
  - Desviación estándar: [Desviación estándar]

- `playtime_forever`:
  - Número total de elementos: [Número total de elementos]
  - Valor medio: [Valor medio]
  - Valor mínimo: [Valor mínimo]
  - Valor máximo: [Valor máximo]
  - Desviación estándar: [Desviación estándar]

## Visualización de datos

- Histograma de `items_count` y `playtime_forever` para ver su distribución.
- Gráfico de barras para contar cuántas veces aparecen valores únicos en `steam_id`.
- Diagrama de caja (boxplot) para `items_count` y `playtime_forever` para identificar valores atípicos.

## Filtrado de datos

El DataFrame `df_items` se ha filtrado para incluir solo las filas donde `playtime_forever` es mayor a 1200. Puedes verificar cuántas filas cumplen con este criterio y examinar sus estadísticas descriptivas.

## DataFrame `df_items_info`

El DataFrame `df_items_info` contiene información desglosada de los elementos y tiene las siguientes columnas:

- `user_id`: Identificación única del usuario.
- `item_id`: Identificación única del elemento.
- `playtime_forever`: Tiempo de juego acumulado para el elemento.

## Almacenamiento de datos

Los datos del DataFrame `df_items_info` se han guardado en un archivo CSV en la siguiente ubicación: `/content/drive/MyDrive/pf_henry/datasets/items.csv`.


## Reviews

El DataFrame `reviews_df` contiene datos de revisiones de usuarios, con información sobre el usuario, el artículo, la fecha de publicación, la recomendación y el análisis de sentimiento de cada revisión. A continuación, se presenta un análisis detallado de los datos:

### Tamaño del DataFrame

El DataFrame contiene un total de [N] registros y [M] columnas.

### Columnas

1. **user_id**: Identificación única del usuario que realizó la revisión.
2. **item_id**: Identificación única del artículo asociado a la revisión.
3. **recommend**: Variable que indica si el usuario recomendó o no el artículo.
4. **posted**: Fecha de publicación de la revisión.
5. **sentiment_analysis**: Análisis de sentimiento de la revisión (0: negativo, 1: neutral, 2: positivo).

## Estadísticas Resumidas

A continuación, se presentan estadísticas resumidas para las columnas numéricas y categóricas relevantes del DataFrame:

### Variable 'recommend'

- Recuento de registros recomendados: [count_recommended]
- Recuento de registros no recomendados: [count_not_recommended]

### Variable 'sentiment_analysis'

- Recuento de revisiones negativas: [count_negative_sentiments]
- Recuento de revisiones neutrales: [count_neutral_sentiments]
- Recuento de revisiones positivas: [count_positive_sentiments]

### Fecha de Publicación ('posted')

- Fecha mínima de publicación: [min_posted_date]
- Fecha máxima de publicación: [max_posted_date]

## Distribución de Sentimientos

El análisis de sentimiento se distribuye de la siguiente manera:

- Negativo: [percentage_negative_sentiments]%
- Neutral: [percentage_neutral_sentiments]%
- Positivo: [percentage_positive_sentiments]%

## Visualización de Datos

A continuación, se pueden encontrar gráficos y visualizaciones que ayudan a comprender mejor los datos:

### Histograma de Sentimientos

El histograma muestra la distribución de sentimientos en las revisiones.

### Gráfico de Recomendaciones

El gráfico muestra la proporción de revisiones recomendadas y no recomendadas.

### Serie Temporal de Publicaciones

La serie temporal muestra cómo las revisiones se distribuyen en el tiempo.

## Conclusiones

- El DataFrame `reviews_df` contiene datos de revisiones de usuarios con información sobre usuarios, artículos, fechas de publicación y análisis de sentimientos.
- La mayoría de las revisiones son [positivas/neutrales/negativas], según el análisis de sentimiento.
- La mayoría de los registros son [recomendados/no recomendados].
- Las revisiones se distribuyen en un rango de fechas desde [min_posted_date] hasta [max_posted_date].


# Diccionario de datos

| DataFrame          | Columna              | Descripción                                               | Tipo de Datos     |
|--------------------|----------------------|-----------------------------------------------------------|-------------------|
| df_reviews          | user_id              | ID de usuario                                             | object            |
|                    | item_id              | ID de juego                                               | int64             |
|                    | recommend            | Booleano que indica si el usuario recomienda el juego    | bool              |
|                    | posted               | Fecha en la que realizó la review                        | datetime64[ns]   |
|                    | sentiment_analysis   | Categoría de análisis de sentimiento (0 = Negativa, 1 = Neutra, 2 = Positiva) | int64 |
| df_items            | user_id              | ID de usuario                                             | object            |
|                    | item_id              | ID de juego                                               | int64             |
|                    | playtime_forever     | Tiempo total que el usuario ha jugado por cada juego    | int64             |
| df_games            | id                   | ID de juego                                               | int64             |
|                    | title                | Nombre del juego                                          | object            |
|                    | release_date         | Fecha de lanzamiento del juego                            | datetime64[ns]   |
|                    | Action               | Categoría: Acción (1 si el juego pertenece, 0 si no)     | int64             |
|                    | Casual               | Categoría: Casual (1 si el juego pertenece, 0 si no)     | int64             |
|                    | Indie                | Categoría: Indie (1 si el juego pertenece, 0 si no)      | int64             |
|                    | Simulation           | Categoría: Simulación (1 si el juego pertenece, 0 si no)  | int64             |
|                    | Strategy             | Categoría: Estrategia (1 si el juego pertenece, 0 si no) | int64             |
|                    | Free_to_Play         | Categoría: Free-to-Play (1 si el juego pertenece, 0 si no) | int64             |
|                    | RPG                  | Categoría: RPG (1 si el juego pertenece, 0 si no)        | int64             |
|                    | Sports               | Categoría: Deportes (1 si el juego pertenece, 0 si no)   | int64             |
|                    | Adventure            | Categoría: Aventura (1 si el juego pertenece, 0 si no)   | int64             |
|                    | Racing               | Categoría: Carreras (1 si el juego pertenece, 0 si no)   | int64             |
|                    | Early_Access         | Categoría: Acceso Anticipado (1 si el juego pertenece, 0 si no) | int64       |
|                    | Massively_Multiplayer| Categoría: Multijugador Masivo (1 si el juego pertenece, 0 si no) | int64       |
|                    | Animation__Modeling  | Categoría: Animación y Modelado (1 si el juego pertenece, 0 si no) | int64     |
|                    | Video_Production     | Categoría: Producción de Video (1 si el juego pertenece, 0 si no) | int64     |
|                    | Utilities            | Categoría: Utilidades (1 si el juego pertenece, 0 si no) | int64             |
|                    | Web_Publishing       | Categoría: Publicación Web (1 si el juego pertenece, 0 si no) | int64          |
|                    | Education            | Categoría: Educación (1 si el juego pertenece, 0 si no)  | int64             |
|                    | Software_Training    | Categoría: Entrenamiento de Software (1 si el juego pertenece, 0 si no) | int64 |
|                    | Design__Illustration | Categoría: Diseño e Ilustración (1 si el juego pertenece, 0 si no) | int64    |
|                    | Audio_Production     | Categoría: Producción de Audio (1 si el juego pertenece, 0 si no) | int64     |
|                    | Photo_Editing        | Categoría: Edición de Fotos (1 si el juego pertenece, 0 si no) | int64        |
|                    | Accounting           | Categoría: Contabilidad (1 si el juego pertenece, 0 si no) | int64             |
