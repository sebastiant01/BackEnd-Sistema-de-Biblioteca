from src.entities.MaterialBiblioteca import MaterialBiblioteca


class Biblioteca:
    """
    Representa una biblioteca que gestiona un catálogo de materiales
    (por ejemplo, libros o revistas) organizados por código, autor y título.

    La biblioteca permite:
        - Registrar nuevos materiales.
        - Consultar el catálogo completo.
        - Buscar materiales por autor.
        - Buscar materiales por código único.
        - Buscar materiales por coincidencia parcial en el título.

    Attributes:
        nombre (str):
            Nombre identificador de la biblioteca.

        por_autor (dict[str, list[MaterialBiblioteca]]):
            Diccionario que agrupa los materiales por autor.
            La clave es el nombre del autor y el valor es una lista
            de materiales asociados.

        por_codigo (dict[str, MaterialBiblioteca]):
            Diccionario que almacena los materiales registrados
            usando su código único como clave.

        por_titulo (dict[str, MaterialBiblioteca]):
            Diccionario que almacena materiales usando el título
            como clave (este dict es de uso opcional dependiendo de la clase).
    """

    def __init__(self, nombre: str) -> None:
        """
        Inicializa una nueva instancia de Biblioteca.

        Args:
            nombre (str): Nombre de la biblioteca.
        """
        self.nombre: str = nombre
        self.por_autor: dict[str, list[MaterialBiblioteca]] = {}
        self.por_codigo: dict[str, MaterialBiblioteca] = {}
        self.por_titulo: dict[str, MaterialBiblioteca] = {}

    def registrar_material(
        self,
        codigo: str,
        autor: str,
        titulo: str,
        material: MaterialBiblioteca,
    ) -> None:
        """
        Registra un nuevo material en la biblioteca.

        El material se almacena:
            - En el diccionario 'por_codigo' usando su código único.
            - En el diccionario 'por_autor' agrupado bajo el nombre del autor.
            - En el diccionario 'por_titulo' usando su título.

        Args:
            codigo (str):
                Código único que identifica el material.

            autor (str):
                Nombre del autor asociado al material.

            titulo (str):
                Título del material.

            material (MaterialBiblioteca):
                Instancia del material que se desea registrar.

        Returns:
            None
        """
        self.por_codigo[codigo] = material
        self.por_titulo[titulo] = material

        if autor not in self.por_autor:
            self.por_autor[autor] = []

        self.por_autor[autor].append(material)

    def mostrar_catalogo(self) -> str:
        """
        Genera una representación textual del catálogo completo
        de la biblioteca.

        Returns:
            str:
                Cadena formateada que contiene:
                    - Nombre de la biblioteca.
                    - Total de materiales registrados.
                    - Información detallada de cada material con su código.

                Si no hay materiales registrados,
                devuelve un mensaje indicando que el catálogo está vacío.
        """
        if not self.por_codigo:
            return "El catálogo está vacío."

        resultado: str = f"=== Catálogo de {self.nombre} ===\n"
        resultado += f"Total de elementos: {len(self.por_codigo)}\n\n"

        for codigo, material in self.por_codigo.items():
            resultado += f"Código: {codigo}\n"
            resultado += f"Material -> {material}\n"
            resultado += "-" * 100 + "\n"

        return resultado

    def buscar_por_autor(self, autor: str) -> list[MaterialBiblioteca] | str:
        """
        Busca materiales registrados bajo un autor específico.

        Args:
            autor (str): Nombre del autor a consultar.

        Returns:
            list[MaterialBiblioteca]:
                Lista de materiales asociadas al autor,
                si existe en el registro.

            str:
                Mensaje indicando que no hay registro del autor,
                si no se encuentra.
        """
        return self.por_autor.get(autor, "No hay registro de este autor.")

    def buscar_por_codigo(self, codigo: str) -> MaterialBiblioteca | str:
        """
        Busca un material por su código único.

        Args:
            codigo (str): Código identificador del material.

        Returns:
            MaterialBiblioteca:
                El material correspondiente si existe.

            str:
                Mensaje indicando que no hay registro del elemento,
                si el código no se encuentra.
        """
        return self.por_codigo.get(codigo, "No hay registro de este elemento.")

    def buscar_por_titulo(self, titulo: str) -> list[MaterialBiblioteca] | str:
        """
        Busca materiales cuya coincidencia en el título contenga
        el fragmento proporcionado (búsqueda parcial e insensible
        a mayúsculas/minúsculas).

        Args:
            titulo (str):
                Fragmento del título que se desea buscar.

        Returns:
            list[MaterialBiblioteca]:
                Lista de materiales que coinciden con el fragmento.

            str:
                Mensaje indicando que no se encontraron resultados.
        """
        fragmento_titulo: str = titulo.lower()
        resultados: list[MaterialBiblioteca] = []

        for material in self.por_codigo.values():
            if fragmento_titulo in material.titulo.lower():
                resultados.append(material)

        if not resultados:
            return "No se encontraron existencias relacionadas a este título."

        return resultados
