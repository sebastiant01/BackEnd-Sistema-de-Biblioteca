class Libros:
    def __init__(self, titulo: str, autor: str):
        self.titulo = titulo
        self.autor = autor

    def imprimir_data(self):
        print(f"El titulo del libro es: {self.titulo} y el autor es: {self.autor}")
