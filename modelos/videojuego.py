class Videojuego:
    def __init__(self, titulo, genero, estudio, rating):
        self._titulo = titulo
        self._genero = genero
        self._estudio = estudio
        self._rating = rating

    def get_titulo(self):
        return self._titulo

    def get_genero(self):
        return self._genero

    def get_rating(self):
        return self._rating

    def __repr__(self):
        return f"{self._titulo} ({self._genero}) - Estudio: {self._estudio}  {self._rating}"