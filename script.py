from re import I
import requests
import json

"""Endpoints de la API"""
MOVIE_LIST = "https://yts.mx/api/v2/list_movies.json"
MOVIE_DETAILS = "https://yts.mx/api/v2/movie_details.json"
MOVIE_SUGGESTIONS = "https://yts.mx/api/v2/movie_suggestions.json"
MOVIE_COMMENTS = "https://yts.mx/api/v2/movie_comments.json"
MOVIE_REVIEWS = "https://yts.mx/api/v2/movie_reviews.json"
MOVIE_PARENTAL = "https://yts.mx/api/v2/movie_parental_guides.json"
LIMITE_PELICULAS = 50
PAG_INICIAL = 1

class Peliculas:
    def  __init__(self):
        """Constructor"""
        self.url_lista = MOVIE_LIST
        self.url_detalles = MOVIE_DETAILS
        self.url_sugerencias = MOVIE_SUGGESTIONS
        self.url_comentarios = MOVIE_COMMENTS
        self.url_reviews = MOVIE_REVIEWS
        self.url_parental = MOVIE_PARENTAL
        self.limite_peliculas = LIMITE_PELICULAS
        self.contenido = []

    def obtenerCantPags(self, limite, cantidad_peliculas):
        """Metodo para obtener la cantidad de paginas de la plataforma
        Parameters
        ----------
        limite: int
            Cantidad de peliculas por pagina
        cantidad_peliculas: int
            Total de peliculas en la plataforma
        """
        total_pags = cantidad_peliculas/limite
        if (round(total_pags)-total_pags) != 0:
            total_pags += 1

        self.total_pags = int(total_pags)

    def obtenerContenido(self):
        """Metodo para obtener el contenido de la plataforma"""
        response = requests.get(self.url_lista)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            cantidad_peliculas = response_json["data"]["movie_count"]
            self.obtenerCantPags(limite = LIMITE_PELICULAS, cantidad_peliculas = cantidad_peliculas)
            contador_pags = PAG_INICIAL
            total_pags = self.total_pags
            while contador_pags != (total_pags + 1):
                args = {'page' : contador_pags, "limit" : LIMITE_PELICULAS}
                response = requests.get(self.url_lista, params = args)
                if response.status_code == 200:
                    response_json = json.loads(response.text)
                    i = 0
                    for i in range(len(response_json['data']['movies'])):
                        dict = {}
                        dict["id"] = response_json['data']['movies'][i]["id"]
                        dict["title"] = response_json['data']['movies'][i]["title"]
                        self.contenido.append(dict)
                        i += 1
                    contador_pags += 1
            

    def obtenerDetalles(self):
        """Metodo para obtener los detalles de una pelicula"""

    def obtenerSugerencias(self):
        """Metodo para obtener sugerencias en base a una pelicula"""

    def obtenerComentarios(self):
        """Metodo para obtener comentarios de una pelicula"""

    def obtenerReviews(self):
        """Metodo para obtener la review de IMDb de una pelicula"""

    def obtenerParental(self):
        """Metodo para obtener la calificacion parental de una pelicula"""

    

if __name__ == "__main__":
    """CODIGO DE PRUEBA"""
    """ url = MOVIE_LIST
    #args = {"movie_id" : 10}
    response = requests.get(url)
    if response.status_code == 200:
        response_json = json.loads(response.text)
        print(response_json)
    elif response.status_code == 404:
        print("ERROR") """


    peliculas = Peliculas()
    peliculas.obtenerContenido()
    print(peliculas.contenido)











"""     total_pages = 39300/20
    page_number = 1
     """
"""     
    while page_number != total_pages+1:
        args = {'page': page_number}
        response = requests.get(url, params = args)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            print(response_json['data']['page_number'])
            page_number += 1 """

