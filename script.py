import requests
import json

"""Endpoints de la API"""
MOVIE_LIST = "https://yts.mx/api/v2/list_movies.json"
MOVIE_DETAILS = "https://yts.mx/api/v2/movie_details.json"
#MOVIE_COMMENTS = "https://yts.mx/api/v2/movie_comments.json" #Endpoint roto
#MOVIE_REVIEWS = "https://yts.mx/api/v2/movie_reviews.json" #Endpoint roto

LIMITE_PELICULAS = 50
PAG_INICIAL = 1
RESULTADOS_ARCHIVO = 'resultados.json'

class Peliculas:
    """Clase para navegar por las peliculas del sitio https://yts.mx/
    ...

    Attributes
    ----------
    url_lista: string
        URL del endpoint para obtener la lista de peliculas
    url_detalles: string
        URL del endpoint para obtener el detalle de una pelicula
    limite_peliculas: int
        Cantidad de peliculas por pagina
    
    Methods
    -------
    obtenerCantPags(self, limite, cantidad_peliculas)
        Obtiene cantidad de paginas para el enpoint Movie List
    obtenerContenido(self)
        Obtiene el contenido de la plataforma junto a otros datos
    obtenerDetalles(self, id)
        Obtiene likes y comentarios de una pelicula
    guardar(self, dict, type)
        Guarda en un archivo .json
    """
    def  __init__(self):
        """Constructor"""
        self.url_lista = MOVIE_LIST
        self.url_detalles = MOVIE_DETAILS
        #self.url_comentarios = MOVIE_COMMENTS #Endpoint roto
        #self.url_reviews = MOVIE_REVIEWS #Endpoint roto
        self.limite_peliculas = LIMITE_PELICULAS
        #self.contenido = [] #De esta forma se guarda todo en una lista y luego se guarda en el json

    def obtenerCantPags(self, limite, cantidad_peliculas):
        """Metodo para obtener la cantidad de paginas de la plataforma para el enpoint Movie List
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
        """Metodo para obtener el contenido de la plataforma
        Obtiene:
            id - title - url - year - rating - genres - synopsis - language - mpa_rating
        """
        response = requests.get(self.url_lista)

        if response.status_code == 200:
            response_json = json.loads(response.text)
            cantidad_peliculas = response_json["data"]["movie_count"]
            self.obtenerCantPags(limite = LIMITE_PELICULAS, cantidad_peliculas = cantidad_peliculas)
            contador_pags = PAG_INICIAL
            total_pags = self.total_pags
            contador_peliculas = (PAG_INICIAL - 1) * LIMITE_PELICULAS

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
                        #dict["comments"] = self.obtenerComentarios(dict["id"]) #Endpoint roto
                        #dict["reviews"] = self.obtenerReviews(dict["id"]) #Endpoint roto

                        #De esta forma se guarda todo en una lista y luego se guarda en el json
                        #self.contenido.append(dict)
                        i += 1
                        contador_peliculas += 1
                        
                        #De esta forma se guarda pelicula por pelicula en el json
                        if contador_peliculas == cantidad_peliculas:
                            self.guardar(dict, True)
                        else:
                            self.guardar(dict, False)

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
            likes = response_json['data']['movie'].get("like_count", " ")
            descargas = response_json['data']['movie'].get("download_count", " ")
            detalles.append(likes)
            detalles.append(descargas)
            return detalles

    def guardar(self, dict, type):
        """Metodo para guardar el contenido en un archivo json
        Parameters
        ----------
        dict: dictionary
            Diccionario con todo el contenido de una pelicula
            
        type: bool
            Tipo de escritura a realizar. Si es True solo hace 
            un salto de linea, si es False escribe una "," y salta de linea
        """
        with open(RESULTADOS_ARCHIVO, 'a') as f:
            json.dump(dict, f, indent=4)
            if type == True:
                f.write("\n")
            else:
                f.write(",\n")
        
    #def obtenerReviews(self):
        """Metodo para obtener la review de IMDb de una pelicula"""
        #Endpoint roto

    #def obtenerComentarios(self):
        """Metodo para obtener comentarios de una pelicula"""
        #Endpoint roto


if __name__ == "__main__":
    #De esta forma se guarda pelicula por pelicula en el json
    if PAG_INICIAL == 1:
        with open(RESULTADOS_ARCHIVO, 'a') as f:
            f.write("[\n")
    peliculas = Peliculas()
    peliculas.obtenerContenido()
    with open(RESULTADOS_ARCHIVO, 'a') as f:
        f.write("]")

    #De esta forma se guarda todo en una lista y luego se guarda en el json
    #peliculas = Peliculas()
    #peliculas.obtenerContenido()
    #with open(RESULTADOS_ARCHIVO, 'w') as f:
    #    json.dump(peliculas.contenido, f, indent=4)


