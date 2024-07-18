# Informe Final del Proyecto: Visualización y Análisis de Anuncios en Reddit
## Introducción
El objetivo de este proyecto es extraer, procesar y visualizar datos de anuncios de diferentes subreddits en Reddit, presentando información estadística relevante a través de una página web. Utilizando la API de Reddit, se recopiló información de los anuncios más recientes y se calcularon estadísticas básicas para su análisis.

## Formación del Equipo y Configuración de GitHub
## Equipo
- Piero Orellana: Diseñador de la app.
- Estefany Sanchez Villena: Encargada de documentación.
- Fiorella Carrasco Lagos: Encargada de pruebas.
## Investigación y Planificación
### API Utilizada
Para obtener la información necesaria de los anuncios en Reddit, se utilizó la API de Reddit. Específicamente, se accedió al endpoint que permite obtener información de los posts en un subreddit.

Endpoint Principal Utilizado:
GET /r/{subreddit}/new/.json?limit=50
Parámetros Utilizados
subreddit: Nombre del subreddit del que se quieren obtener los anuncios. Ejemplo: advertising.
limit: Número de posts a obtener por solicitud. Por defecto, Reddit devuelve hasta 25 posts.
Código para Extraer Datos de la API
python
Copiar código
import requests

def obtener_anuncios(subreddit, limit=50):
    url = f"https://www.reddit.com/r/{subreddit}/new/.json?limit={limit}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        anuncios = response.json()['data']['children']
        return [anuncio['data'] for anuncio in anuncios]
    else:
        print(f"Error al obtener anuncios de {subreddit}: {response.status_code}")
        return []

# Ejemplo de uso
- anuncios = obtener_anuncios('advertising')
## Desarrollo del Extractor de Datos
Llamadas a la API: Utilizar “requests” para llamadas a la API de Reddit.
Extracción de información: Desarrollar código para extraer datos relevantes como impresiones, clics, coste, etc.
Almacenamiento: Guardar datos en base de datos o archivos CSV/JSON.
Transformación de la Información
Procesamiento y limpieza: Procesar y limpiar los datos extraídos.
Transformación útil: Calcular estadísticas básicas como promedio de impresiones y tasa de clics.
Preparación para visualización: Preparar datos para visualización en una página web.
## Desarrollo de la Página Web
HTML: Crear página web.
Visualización: Utilizar bibliotecas para representar datos gráficamente.
Interactividad: Incluir filtros y búsquedas para mejorar la experiencia del usuario.
Pruebas y Documentación
Pruebas: Realizar pruebas exhaustivas del extractor de datos y de la página web para asegurarse de que funcionan correctamente.
Documentación: Documentar el código y el proyecto en su totalidad.
