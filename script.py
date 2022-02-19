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
PAG_INICIAL = 786

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
                        dict["id"] = response_json['data']['movies'][i].get("id")
                        dict["title"] = response_json['data']['movies'][i].get("title")
                        dict["url"] = response_json['data']['movies'][i].get("url")
                        dict["year"] = response_json['data']['movies'][i].get("year")
                        dict["rating"] = response_json['data']['movies'][i].get("rating")
                        dict["genres"] = response_json['data']['movies'][i].get("genres")
                        dict["synopsis"] = response_json['data']['movies'][i].get("synopsis")
                        dict["language"] = response_json['data']['movies'][i].get("language")
                        dict["mpa_rating"] = response_json['data']['movies'][i].get("mpa_rating")
                        detalles = self.obtenerDetalles(dict["id"])
                        dict["like_count"] = detalles[0]
                        dict["download_count"] = detalles[1]
                        #self.contenido.append(dict)
                        i += 1
                        self.guardar(dict)
                    print("Pagina ", contador_pags, " de ", total_pags)
                    contador_pags += 1
            

    def obtenerDetalles(self, id):
        """Metodo para obtener los likes y descargas de una pelicula
        Parameters
        ----------
        id: int
            Id de la pelicula a obtener los likes
        Returns
        ----------
        detalles: list
            Lista con los likes en el primer lugar y las descargas en el segundo
        """
        args = {'movie_id' : id}
        response = requests.get(self.url_detalles, params = args)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            detalles = []
            likes = response_json['data']['movie'].get("like_count")
            descargas = response_json['data']['movie'].get("download_count")
            detalles.append(likes)
            detalles.append(descargas)
            return detalles

    def obtenerDescargas(self, id):
        """Metodo para obtener las descargas de una pelicula"""
        args = {'movie_id' : id}
        response = requests.get(self.url_detalles, params = args)
        if response.status_code == 200:
            response_json = json.loads(response.text)
            descargas = response_json['data']['movie'].get("download_count")
            return descargas

    def obtenerComentarios(self):
        """Metodo para obtener comentarios de una pelicula"""
        #Endpoint roto
    def guardar(self, dict):
        """Metodo para guardar el contenido en un archivo json
        Parameters
        ----------
        dict: dictionary
            Diccionario con todo el contenido de una pelicula
        """
        with open('resultados.json', 'a') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)
            if dict["id"] == 1:
                f.write("\n")
            else:
                f.write(",\n")

        
    def obtenerReviews(self):
        """Metodo para obtener la review de IMDb de una pelicula"""
        #Endpoint roto


    

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
    
    with open('resultados.json', 'a') as f:
            f.write("[\n")
    peliculas = Peliculas()
    peliculas.obtenerContenido()
    #print(peliculas.contenido)
    with open('resultados.json', 'a') as f:
            f.write("]")
    """ with open('data.json', 'w') as f:
        json.dump(peliculas.contenido, f, ensure_ascii=False, indent=4) """


