import pandas as pd



def size():
    df_games = pd.read_csv('datasets/games.csv')
    df_items = pd.read_csv('datasets/items.csv')
    df_reviews = pd.read_csv('datasets/reviews.csv')
    return {
        'games':df_games.shape[0],
        'items':df_items.shape[0],
        'reviews':df_reviews.shape[0],
            }


# Lista de nombres de las columnas de categorias
categories = [
    'Action', 'Casual', 'Indie', 'Simulation', 'Strategy', 'Free_to_Play',
    'RPG', 'Sports', 'Adventure', 'Racing', 'Early_Access', 'Massively_Multiplayer',
    'Animation__Modeling', 'Video_Production', 'Utilities', 'Web_Publishing',
    'Education', 'Software_Training', 'Design__Illustration', 'Audio_Production',
    'Photo_Editing', 'Accounting'
]

def custom_title_case(s):
    # Palabras comunes en minúsculas (excepto "and" y "or").
    lowercase_words = ["to"]

    # Eliminamos los &
    s.replace('&', '__')

    # Eliminamos los " "
    s.replace(' ', '_')

    # Divide la cadena en palabras.
    words = s.split('_')

    # Aplica capitalización personalizada.
    title_case_words = [word.capitalize() if word.lower() not in lowercase_words else word.lower() for word in words]

    # Capitaliza la primera letra de la cadena.
    title_case_words[0] = title_case_words[0].capitalize()

    # Une las palabras con espacios.
    return "_".join(title_case_words)\

def year_with_most_playtime_for_genre(genre):
    # Validar si el género ingresado está en la lista de categorías y capitalizarlo.
    genre_title = custom_title_case(genre)
    if genre_title in categories:
        # Cargar los datos necesarios
        df_games = pd.read_csv('datasets/games.csv')
        df_items = pd.read_csv('datasets/items.csv')
        
        # Filtrar df_games para obtener solo los juegos del género deseado.
        df_genre = df_games[df_games[genre_title] == 1]

        # Fusionar df_genre con df_items en función del 'item_id'.
        df_merged = pd.merge(df_items, df_genre, left_on='item_id', right_on='id', how='inner')

        # Eliminar filas con valores no válidos en la columna 'release_date'.
        df_merged = df_merged[df_merged['release_date'].notnull()]

        # Convertir la columna 'release_date' a tipo datetime.
        df_merged['release_date'] = pd.to_datetime(df_merged['release_date'], errors='coerce')

        # Eliminar filas con fechas inválidas (NaT).
        df_merged = df_merged.dropna(subset=['release_date'])

        # Agrupar por el año de lanzamiento y calcular la suma de las horas jugadas.
        aggregated = df_merged.groupby(df_merged['release_date'].dt.year)['playtime_forever'].sum()

        # Encontrar el año con más horas jugadas.
        year_most_playtime = aggregated.idxmax()

        # Convertir el resultado a tipo int nativo en lugar de numpy.int32
        year_most_playtime = int(year_most_playtime)

        return {"Año de lanzamiento con más horas jugadas para Género {}".format(genre_title): year_most_playtime}
    else:
        # Generar una lista de géneros válidos basados en 'categories'.
        valid_genres = [custom_title_case(category.replace('__', ' & ').replace('_', ' ')) for category in categories]
        return {"Error": "Genero erroneo o invalido", "Generos validos": valid_genres}

def user_with_most_playtime_for_genre(genre):
    # Validar si el género ingresado está en la lista de categorías y capitalizarlo.
    genre_title = custom_title_case(genre)
    if genre_title in categories:
        # Cargar los datos necesarios
        df_games = pd.read_csv('datasets/games.csv')
        df_items = pd.read_csv('datasets/items.csv')
        
        # Filtrar df_games para obtener solo los juegos del género deseado.
        df_genre = df_games[df_games[genre_title] == 1]

        # Fusionar df_genre con df_items en función del 'item_id'.
        df_merged = pd.merge(df_items, df_genre, left_on='item_id', right_on='id', how='inner')

        # Eliminar filas con valores no válidos en la columna 'user_id'.
        df_merged = df_merged[df_merged['user_id'].notnull()]

        # Convertir la columna 'release_date' a tipo datetime.
        df_merged['release_date'] = pd.to_datetime(df_merged['release_date'], errors='coerce')

        # Eliminar filas con fechas inválidas (NaT).
        df_merged = df_merged.dropna(subset=['release_date'])

        # Agrupar por usuario y calcular la suma de las horas jugadas.
        aggregated = df_merged.groupby('user_id')['playtime_forever'].sum()

        # Encontrar el usuario con más horas jugadas.
        user_most_playtime = aggregated.idxmax()

        # Crear una lista de acumulación de horas jugadas por año.
        aggregated_by_year = df_merged.groupby(df_merged['release_date'].dt.year)['playtime_forever'].sum()
        hours_by_year = [{"Año": year, "Horas": hours} for year, hours in aggregated_by_year.items()]

        return {"Usuario con más horas jugadas para Género {}".format(genre_title): user_most_playtime, "Horas jugadas por año": hours_by_year}
    else:
        # Generar una lista de géneros válidos basados en 'categories'.
        valid_genres = [custom_title_case(category.replace('__', ' & ').replace('_', ' ')) for category in categories]
        return {"Error": "Género erróneo o inválido", "Géneros válidos": valid_genres}

def top_recommended_games_by_year(df_reviews, df_items, df_games, year):
    # Paso 1: Filtrar las reseñas que cumplen con las condiciones
    filtered_reviews = df_reviews[(df_reviews['recommend'] == True) & (df_reviews['sentiment_analysis'].isin([0, 1]))]

    # Paso 2: Unir los dataframes usando las columnas de identificación
    merged_df = pd.merge(filtered_reviews, df_items, on='item_id')
    merged_df = pd.merge(merged_df, df_games, left_on='item_id', right_on='id')

    # Paso 3: Filtrar las reseñas por el año dado
    merged_df['year'] = merged_df['posted'].dt.year
    games_for_year = merged_df[merged_df['year'] == year]

    # Paso 4: Agrupar las reseñas por juego y contar cuántas veces cada juego ha sido recomendado
    game_recommendations = games_for_year.groupby('title')['recommend'].sum().reset_index()

    # Paso 5: Ordenar los juegos recomendados en orden descendente según la cantidad de recomendaciones
    game_recommendations = game_recommendations.sort_values(by='recommend', ascending=False)

    # Paso 6: Tomar los tres primeros juegos de la lista ordenada
    top_3_games = game_recommendations.head(3)

    # Formatear el resultado como una lista de diccionarios
    result = [{"Puesto {}: {}".format(i+1, row['title'])} for i, row in top_3_games.iterrows()]

    return result

def top_recommended_games_by_year(year):
    df_games = pd.read_csv('datasets/games.csv')
    df_reviews = pd.read_csv('datasets/reviews.csv')

    # Reemplazar los valores '0000-00-00' por NaN
    df_games['release_date'] = df_games['release_date'].replace('0000-00-00', pd.NaT)
    
    # Convertir la columna 'release_date' a tipo datetime
    df_games['release_date'] = pd.to_datetime(df_games['release_date'], errors='coerce')

    # Filtrar las reseñas positivas o neutras y recomendadas
    filtered_reviews = df_reviews[(df_reviews['sentiment_analysis'].isin([1, 2])) & (df_reviews['recommend'] == True)]
    
    # Combinar los DataFrames utilizando el campo 'item_id'
    combined_df = pd.merge(filtered_reviews, df_games, left_on='item_id', right_on='id', how='inner')
    
    # Filtrar las reseñas para el año dado
    filtered_reviews_for_year = combined_df[combined_df['release_date'].dt.year == year]
    
    # Calcular los juegos mejor recomendados para ese año
    best_rated_games = filtered_reviews_for_year['title'].value_counts().head(3)
    
    # Crear la lista de resultados en el formato deseado
    result = [{"Puesto {}".format(i + 1): game} for i, (game, count) in enumerate(best_rated_games.items())]

    return result

def top_not_recommended_games_by_year(year):
    df_games = pd.read_csv('datasets/games.csv')
    df_reviews = pd.read_csv('datasets/reviews.csv')

    # Reemplazar los valores '0000-00-00' por NaN
    df_games['release_date'] = df_games['release_date'].replace('0000-00-00', pd.NaT)
    
    # Convertir la columna 'release_date' a tipo datetime
    df_games['release_date'] = pd.to_datetime(df_games['release_date'], errors='coerce')

    # Filtrar las reseñas negativas y no recomendadas
    filtered_reviews = df_reviews[(df_reviews['sentiment_analysis'] == 0) & (df_reviews['recommend'] == False)]
    
    # Combinar los DataFrames utilizando el campo 'item_id'
    combined_df = pd.merge(filtered_reviews, df_games, left_on='item_id', right_on='id', how='inner')
    
    # Filtrar las reseñas para el año dado
    filtered_reviews_for_year = combined_df[combined_df['release_date'].dt.year == year]
    
    # Calcular los juegos peor recomendados para ese año
    worst_rated_games = filtered_reviews_for_year['title'].value_counts().head(3)
    
    # Crear la lista de resultados en el formato deseado
    result = [{"Puesto {}".format(i + 1): game} for i, (game, count) in enumerate(worst_rated_games.items())]
    
    return result

def sentiment_analysis_by_year(year):
    import numpy as np

    df_games = pd.read_csv('datasets/games.csv')
    df_reviews = pd.read_csv('datasets/reviews.csv')

    # Reemplazar los valores '0000-00-00' por NaN
    df_games['release_date'] = df_games['release_date'].replace('0000-00-00', pd.NaT)
    
    # Convertir la columna 'release_date' a tipo datetime
    df_games['release_date'] = pd.to_datetime(df_games['release_date'], errors='coerce')

    filtered_reviews = df_reviews[df_reviews['item_id'].isin(df_games[df_games['release_date'].dt.year == year]['id'])]
    
    # Agrupar por el análisis de sentimiento y contar las reseñas
    result = filtered_reviews['sentiment_analysis'].value_counts()
    
    # Crear un diccionario con el resultado convertido a tipos nativos
    result_dict = {
        'Negative': int(result.get(0, 0)),
        'Neutral': int(result.get(1, 0)),
        'Positive': int(result.get(2, 0))
    }
    
    return result_dict

def get_similar_games(df_games, item_id, game_similarity, num_recomendaciones=5):
    from sklearn.metrics.pairwise import cosine_similarity

    if item_id not in df_games['id'].values:
        return "El ID de juego no existe."
    
    # Obtiene el índice del juego ingresado
    idx = df_games[df_games['id'] == item_id].index[0]
    
    # Obtiene las puntuaciones de similitud del juego ingresado con otros juegos
    sim_scores = list(enumerate(game_similarity[idx]))
    
    # Ordena los juegos según las puntuaciones de similitud en orden descendente
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    
    # Obtiene los índices de los juegos similares (excluyendo el juego ingresado)
    similar_games_idx = [x[0] for x in sim_scores[1:]]
    
    # Obtiene los títulos de los juegos recomendados
    recommended_games = df_games.iloc[similar_games_idx]['title'].head(num_recomendaciones).tolist()
    
    return recommended_games

def recommendation_per_game(id):
    from sklearn.metrics.pairwise import cosine_similarity
    # Cargar los datos necesarios
    df_games = pd.read_csv('datasets/games.csv')
    df_items = pd.read_csv('datasets/items.csv')
    df_reviews = pd.read_csv('datasets/reviews.csv')

    # Filtrar las columnas necesarias en df_reviews
    df_reviews_l = df_reviews[['user_id', 'item_id', 'recommend']]
    
    # Filtrar las columnas necesarias en df_items
    df_items_l = df_items[['user_id', 'item_id', 'playtime_forever']]
    
    # Unir df_reviews_l y df_items_l en función de 'item_id' y 'user_id'
    df_merged = pd.merge(df_reviews_l, df_items_l, on=['item_id', 'user_id'])
    
    # Pivotea los datos para obtener una matriz de usuario-juego
    user_item_matrix = df_merged.pivot_table(index='user_id', columns='item_id', values='recommend')
    user_item_matrix = user_item_matrix.fillna(0)  # Llena los valores faltantes con 0
    
    # Calcula la similitud del coseno entre juegos
    game_similarity = cosine_similarity(user_item_matrix.T)

    recommendations = get_similar_games(df_games, id, game_similarity)

    games_list = []
    
    for i, juego in enumerate(recommendations, 1):
        games_list.append(f"{i}. {juego}")
    
    return games_list

def recommendation_per_user(id):
    # Cargar los datos necesarios
    df_items = pd.read_csv('datasets/items.csv')

    # Encuentra el juego con la máxima cantidad de tiempo jugado por el usuario dado
    max_playtime_game_id = df_items[df_items['user_id'] == id]['playtime_forever'].idxmax()
    selected_game_id = df_items.loc[max_playtime_game_id]['item_id']

    return recommendation_per_game(selected_game_id)