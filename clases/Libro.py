class Libro:
    def __init__(
        self,
        titulo: str,
        autor,
        cantidad_paginas: int,
        fecha_publicacion: str,
        editorial: str,
    ):
        self.titulo = titulo
        self.autor = autor
        self.cantidad_paginas = cantidad_paginas
        self.fecha_publicacion = fecha_publicacion
        self.editorial = editorial

    def imprimir_datos(self):
        print(f"El titulo del libro es {self.titulo} y su autor es {self.autor}")


nuevo_libro = Libro(
    "Estudio en escarlata", "Arthur Conan Doyle", "256", "4/08/1896", "British Company"
)

nuevo_libro.imprimir_datos()
