import requests
import json
from datetime import datetime
import csv


def fetch_reddit_data(subreddit):
    url = f"https://www.reddit.com/r/{subreddit}/.json"
    headers = {'User-agent': 'Mozilla/5.0'}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        
        anuncios = []
        for post in data['data']['children']:
            anuncio = {
                'title': post['data']['title'],
                'author': post['data']['author'],
                'score': post['data']['score'],
                'num_comments': post['data']['num_comments'],
                'created_utc': datetime.utcfromtimestamp(post['data']['created_utc']).strftime('%Y-%m-%d %H:%M:%S'),
                'subreddit': post['data']['subreddit'],
                'url': post['data']['url'],
                'ups': post['data']['ups'],
                'downs': post['data']['downs'],
                'selftext': post['data']['selftext'],
                'thumbnail': post['data']['thumbnail'],
                'permalink': f"https://www.reddit.com{post['data']['permalink']}"
            }
            anuncios.append(anuncio)
        
        return anuncios
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la solicitud: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar la respuesta JSON: {e}")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def fetch_multiple_subreddits(subreddits):
    all_anuncios = []
    for subreddit in subreddits:
        print(f"Fetching data from subreddit: {subreddit}")
        anuncios = fetch_reddit_data(subreddit)
        all_anuncios.extend(anuncios)
    
    # Guardar todos los anuncios en un archivo JSON
    with open('all_anuncios.json', 'w') as f:
        json.dump(all_anuncios, f, indent=4)
    print("Datos guardados en 'all_anuncios.json'")
    
    return all_anuncios
def convertir_json_a_csv():
    with open('all_anuncios.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    
    csv_file = 'anuncios.csv'
    with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['title', 'author', 'score', 'num_comments', 'created_utc', 'subreddit', 'url', 'ups', 'downs', 'selftext', 'thumbnail', 'permalink']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for anuncio in data:
            writer.writerow(anuncio)
    
    print(f"Datos convertidos a CSV en '{csv_file}'")