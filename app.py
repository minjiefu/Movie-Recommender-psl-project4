import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash import Input, Output, dcc, html
from dash.dependencies import ALL, State

from myfuns import (get_displayed_movies, get_recommended_movies)

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def get_movie_card(movie, with_rating=False):
    return html.Div(
        dbc.Card(
            [
                dbc.CardImg(
                    src=
                    f"https://liangfgithub.github.io/MovieImages/{movie.movie_id}.jpg?raw=true",
                    top=True,
                ),
                dbc.CardBody([
                    html.H6(movie.title,
                            className="card-title text-center",
                            style={"margin-bottom": "0"}),
                ]),
            ] + ([
                dcc.RadioItems(
                    options=[
                        {
                            "label": "1",
                            "value": "1"
                        },
                        {
                            "label": "2",
                            "value": "2"
                        },
                        {
                            "label": "3",
                            "value": "3"
                        },
                        {
                            "label": "4",
                            "value": "4"
                        },
                        {
                            "label": "5",
                            "value": "5"
                        },
                    ],
                    className="text-center",
                    id={
                        "type": "movie_rating",
                        "movie_id": movie.movie_id
                    },
                    inputClassName="m-1",
                    labelClassName="px-1",
                    style={
                        "display": "flex",
                        "justify-content": "center",
                        "margin-top": "0",
                    },
                )
            ] if with_rating else []),
            className="h-100",
        ),
        className="col mb-4",
    )


movies = get_displayed_movies()

EXPLAINER = """This example shows how to use callbacks to render graphs inside
if the data generating process is expensive, switching tabs is still quick."""

app.layout = dbc.Container([
    html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(html.H2([
                        html.I(className="fas fa-film",
                               style={'marginRight': '10px'}),
                        "MinJie Movie Recommender"
                    ],
                                    style={
                                        'fontSize': '48px',
                                        'color': '#fff',
                                    }),
                            style={
                                'textAlign': 'center',
                            })
                ],
                className="mb-4",
                style={'backgroundColor': '#074013'}  
            ),
            dcc.Markdown(EXPLAINER),
            dbc.Row([
                html.H1("Rate some movies below"),
            ],
                    className="sticky-top bg-white py-2"),
            html.Div([
                get_movie_card(movie, with_rating=True)
                for idx, movie in movies.iterrows()
            ],
                     className="row row-cols-1 row-cols-5 scrollable-div",
                     id="rating-movies",
                     style={
                         'height': '460px',
                         'overflow-y': 'auto',
                     }),
            dbc.Row([
                dbc.Button(
                    children=[
                        "Get recommendations",
                    ],
                    size="lg",
                    className="btn-success",
                    id="button-recommend",
                )
            ],
                    className="sticky-top bg-white py-2"),
        ],
        id="rate-movie-container",
    ),
    
    
    dbc.Row([
        html.H1("Your recommendations"),
    ],
            id="your-recommendation",
            style={
                "display": "none", 
            },
            className="sticky-top bg-white py-2"),
    dcc.Loading(
        [
            html.Div(
                dcc.Link(
                    "Try again",
                    href="/",
                    refresh=True,
                    style={
                        'background-color': 'white',
                        'color': 'green',
                        'padding': '10px 20px',
                        'border-radius': '5px',
                        'text-decoration': 'none',
                        'border': '2px solid green',  
                        'margin-top': '0px',
                        'margin-bottom': '10px',
                        'align-self': 'flex-start',  
                    },
                ),
                style={
                    'display': 'flex',
                    'justify-content': 'flex-start'
                }  
            ),
            html.Div(
                className="row row-cols-1 row-cols-5",
                id="recommended-movies",
            ),
        ],
        type="circle",
    ),
])


@app.callback(
    Output("rate-movie-container", "style"),
    Output("your-recommendation", "style"),
    [Input("button-recommend", "n_clicks")],
    prevent_initial_call=True,
)
def on_recommend_button_clicked(n):
    return {"display": "none"}, {"display": "block"}


@app.callback(
    Output("recommended-movies", "children"),
    [Input("button-recommend", "n_clicks")],
    [
        State({
            "type": "movie_rating",
            "movie_id": ALL
        }, "value"),
        State({
            "type": "movie_rating",
            "movie_id": ALL
        }, "id"),
    ],
    prevent_initial_call=True,
)
def on_getting_recommendations(style, ratings, ids):
    rating_input = {
        ids[i]["movie_id"]: int(rating)
        for i, rating in enumerate(ratings) if rating is not None
    }
    

    recommended_movies = get_recommended_movies(rating_input)

    return [
        get_movie_card(movie) for idx, movie in recommended_movies.iterrows()
    ]


@app.callback(
    Output("button-recommend", "disabled"),
    Input({
        "type": "movie_rating",
        "movie_id": ALL
    }, "value"),
)
def update_button_recommened_visibility(values):
    return not list(filter(None, values))


if __name__ == "__main__":
    app.run_server()
