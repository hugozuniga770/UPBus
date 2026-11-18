"""Ayudas para las vistas: leer los datos de entrada con un serializador."""


def leer(serializador_clase, datos):
    """Valida el formato de los datos y devuelve un diccionario limpio.

    El formato (campos que faltan, tipos) es tarea de la vista. Las reglas del
    negocio van en `reglas.py`.
    """
    serializador = serializador_clase(data=datos)
    serializador.is_valid(raise_exception=True)
    return serializador.validated_data
