import hashlib


class Security:

    def generar_hash(self, contrasena_plana: str) -> str:
        bytes_contrasena = contrasena_plana.encode("utf-8")
        hash_puro = hashlib.sha256(bytes_contrasena)
        contrasena_hasheada = hash_puro.hexdigest()

        return contrasena_hasheada

    def verificar_contrasena_ingresada(
        self, contrasena_plana: str, contrasena_hasheada_guardada: str
    ) -> bool:

        hash_intento = self.generar_hash(contrasena_plana)

        return hash_intento == contrasena_hasheada_guardada


security = Security()
