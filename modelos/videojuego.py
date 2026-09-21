class Videojuego:
    def __init__(self, titulo, genero, estudio, rating:float):
        self.__titulo = titulo
        self.__genero = genero
        self.__estudio = estudio
        self.__rating = rating

    def get_titulo(self):
        return self.__titulo

    def get_genero(self):
        return self.__genero

    def get_rating(self):
        return self.__rating

    def __repr__(self):
        return f"{self.__titulo} ({self.__genero}) - Estudio: {self.__estudio}  {self.__rating}"


