from fastapi import FastAPI

import functions

app = FastAPI()
app.title = 'Sistema de regomendacion de juegos basado en Steam'
app.version = '0.0.1'


@app.get('/', tags=['home'])
def welcome():
    return {'mesage': 'Welcome!'}

@app.get('/PlayTimeGenre/{genre}', tags=['reports'])
def PlayTimeGenre(genre: str):
    return functions.year_with_most_playtime_for_genre(genre)

@app.get('/UserForGenre/{genre}', tags=['reports'])
def UserForGenre(genre: str):
    return functions.user_with_most_playtime_for_genre(genre)

@app.get('/UsersRecommend/{year}', tags=['reports'])
def UsersRecommend(year: int):
    return functions.top_recommended_games_by_year(year)

@app.get('/UsersNotRecommend/{year}', tags=['reports'])
def UsersNotRecommend(year: int):
    return functions.top_not_recommended_games_by_year(year)

@app.get('/sentiment_analysis/{year}', tags=['reports'])
def sentiment_analysis(year: int):
    return functions.sentiment_analysis_by_year(year)



@app.get('/game_recommendation/{id}', tags=['recommendations'])
def game_recommendation(id: int):
    return functions.recommendation_per_game(id)

@app.get('/user_recommendation/{id}', tags=['recommendations'])
def user_recommendation(id: str):
    return functions.recommendation_per_user(id)