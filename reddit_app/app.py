from flask import Flask, render_template, jsonify, redirect, url_for
import requests
from data_fetcher import convertir_json_a_csv
import plotly.graph_objs as go
import pandas as pd
import json

app = Flask(__name__)

# Ruta para la página de inicio
@app.route('/')
def inicio():
    return redirect(url_for('mostrar_inicio'))

@app.route('/inicio')
def mostrar_inicio():
    return render_template('inicio.html')

# Ruta para la página principal (donde se muestran los anuncios)
@app.route('/index')
def index():
    subreddits = [
        'advertising', 'marketing', 'socialmedia', 'digitalmarketing',
        'entrepreneur', 'business', 'smallbusiness', 'startups',
        'ecommerce', 'SEO', 'content_marketing'
    ]
    return render_template('index.html', subreddits=subreddits)

# Ruta para obtener los anuncios de Reddit
@app.route('/anuncios/<subreddit>')
def obtener_anuncios(subreddit):
    if subreddit == 'all':
        all_anuncios = []
        for sub in ['advertising', 'marketing', 'socialmedia', 'digitalmarketing',
                    'entrepreneur', 'business', 'smallbusiness', 'startups',
                    'ecommerce', 'SEO', 'content_marketing']:
            reddit_url = f"https://www.reddit.com/r/{sub}/new/.json?limit=50"
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(reddit_url, headers=headers)
            if response.status_code == 200:
                anuncios = response.json()['data']['children']
                for anuncio in anuncios:
                    anuncio_data = anuncio['data']
                    formatted_anuncio = {
                        'subreddit': anuncio_data['subreddit'],
                        'title': anuncio_data['title'],
                        'author': anuncio_data['author'],
                        'score': anuncio_data['score'],
                        'num_comments': anuncio_data['num_comments'],
                        'created_utc': anuncio_data['created_utc'],
                        'url': anuncio_data['url'],
                        'ups': anuncio_data['ups'],
                        'downs': anuncio_data['downs'],
                        'selftext': anuncio_data['selftext'],
                        'thumbnail': anuncio_data['thumbnail'],
                        'permalink': f"https://www.reddit.com{anuncio_data['permalink']}"
                    }
                    all_anuncios.append(formatted_anuncio)
            else:
                print(f"Error al obtener anuncios de {subreddit}: {response.status_code}")
        return jsonify(all_anuncios)
    else:
        reddit_url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit=50"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(reddit_url, headers=headers)

        if response.status_code == 200:
            anuncios = response.json()['data']['children']
            formatted_anuncios = []

            for anuncio in anuncios:
                anuncio_data = anuncio['data']
                formatted_anuncio = {
                    'subreddit': anuncio_data['subreddit'],
                    'title': anuncio_data['title'],
                    'author': anuncio_data['author'],
                    'score': anuncio_data['score'],
                    'num_comments': anuncio_data['num_comments'],
                    'created_utc': anuncio_data['created_utc'],
                    'url': anuncio_data['url'],
                    'ups': anuncio_data['ups'],
                    'downs': anuncio_data['downs'],
                    'selftext': anuncio_data['selftext'],
                    'thumbnail': anuncio_data['thumbnail'],
                    'permalink': f"https://www.reddit.com{anuncio_data['permalink']}"
                }
                formatted_anuncios.append(formatted_anuncio)

            return jsonify(formatted_anuncios)
        else:
            return jsonify([])

# Función para generar el gráfico circular con Plotly y obtener datos para la tabla de ups
def generar_grafico_circular_y_tabla_ups():
    # Leer datos desde un archivo JSON (simulado para ejemplo)
    with open('all_anuncios.json', 'r') as file:
        data = json.load(file)

    # Convertir a DataFrame de pandas
    df = pd.DataFrame(data)

    # Calcular la cantidad de anuncios por subreddit
    subreddit_counts = df['subreddit'].value_counts()

    # Crear el gráfico circular (pie chart) con Plotly
    fig_pie = go.Figure(data=[go.Pie(labels=subreddit_counts.index, values=subreddit_counts.values)])
    fig_pie.update_layout(title='Cantidad de Anuncios por Subreddit')

    # Guardar el gráfico como imagen en el directorio 'static'
    fig_pie.write_image("static/pie_chart.png", width=800, height=500)

    # Calcular los subreddits con mayor cantidad de ups
    subreddit_ups = df.groupby('subreddit')['ups'].sum().sort_values(ascending=False).head(5).to_dict()

    return fig_pie, subreddit_ups

# Ruta para la información general del subreddit
@app.route('/general_info')
def general_info():
    # Generar el gráfico circular con Plotly y obtener datos para la tabla de ups
    fig_pie, subreddit_ups = generar_grafico_circular_y_tabla_ups()

    # Renderizar el template 'general_info.html' con el gráfico circular y la tabla de ups
    return render_template('general_info.html', fig_pie=fig_pie.to_json(), subreddit_ups=subreddit_ups)

# Ruta para obtener el gráfico circular como JSON para Plotly.js
@app.route('/get_pie_chart')
def get_pie_chart():
    fig_pie, _ = generar_grafico_circular_y_tabla_ups()
    return jsonify(fig_pie)

if __name__ == '__main__':
    app.run(debug=True)


