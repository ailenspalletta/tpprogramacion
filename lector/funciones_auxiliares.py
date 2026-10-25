
"""
Funciones auxiliares para evaluar e inferir tipos de datos.

Este módulo contiene funciones para determinar el tipo de dato más adecuado
para una columna y convertir sus valores a los tipos admitidos por el lector.
"""


def evaluar_funcion_transformacion(columna, tipo_dato):
    """
    Determina qué función debe utilizarse para transformar una columna.

    Si se especifica un tipo de dato, devuelve la función de conversión
    correspondiente. Si no se especifica, evalúa los valores de la columna
    y devuelve la función asociada al tipo inferido.

    Parámetros
    ----------
    columna : list
        Valores de una columna, representados inicialmente como cadenas.
    tipo_dato : str o None
        Tipo solicitado: 'None', 'str', 'int', 'float' o 'bool'.
        Si es None o una cadena vacía, se infiere el tipo.

    Devuelve
    --------
    callable
        Función que convierte un valor individual de la columna.
    """
    diccionario = {
        "None": convertir_none,
        "str": str,
        "int": int,
        "float": float,
        "bool": convertir_bool}

    if not (tipo_dato == None or tipo_dato == ""):
        return diccionario[tipo_dato]
    else:
        if evaluar_none(columna):
            return convertir_none
        if evaluar_bool(columna):
            return convertir_bool
        if evaluar_int(columna):
            return int
        if evaluar_float(columna):
            return float
        return str


def evaluar_none(lista):
    """
    Comprueba si todos los valores representan valores nulos.

    Se consideran nulos las cadenas vacías y la cadena 'None'.

    Parámetros
    ----------
    lista : list
        Valores que se desean evaluar.

    Devuelve
    --------
    bool
        True si todos los valores son cadenas vacías o 'None';
        False en caso contrario.
    """
    for i in lista:
        if i == "" or i == "None":
            continue
        else:
            return False
    return True


def evaluar_bool(lista):
    """
    Comprueba si todos los valores de una lista representan booleanos.

    La comparación ignora mayúsculas, minúsculas y espacios exteriores.

    Parámetros
    ----------
    lista : list
        Valores que se desean evaluar.

    Devuelve
    --------
    bool
        True si cada valor es 'true' o 'false'; False en caso contrario.
    """
    for i in lista:
        i = i.strip().lower()
        if i == "true" or i == "false":
            continue
        else:
            return False
    return True


def evaluar_int(lista):
    """
    Comprueba si todos los valores de una lista pueden convertirse a enteros.

    Parámetros
    ----------
    lista : list
        Valores que se desean evaluar.

    Devuelve
    --------
    bool
        True si todos los valores admiten int(); False si alguno genera
        ValueError.
    """
    for i in lista:
        try:
            int(i)
        except ValueError:
            return False
    return True


def evaluar_float(lista):
    """
    Comprueba si todos los valores pueden convertirse a números float.

    Parámetros
    ----------
    lista : list
        Valores que se desean evaluar.

    Devuelve
    --------
    bool
        True si todos los valores admiten float(); False si alguno genera
        ValueError.
    """
    for i in lista:
        try:
            float(i)
        except ValueError:
            return False
    return True


def convertir_none(valor):
    """
    Convierte un valor de entrada en None.

    Parámetros
    ----------
    valor : str
        Valor que se reemplazará por None.

    Devuelve
    --------
    None
        Siempre devuelve None.
    """
    return None


def convertir_bool(valor):
    """
    Convierte las cadenas 'true' y 'false' a valores booleanos.

    La conversión ignora mayúsculas, minúsculas y espacios exteriores.

    Parámetros
    ----------
    valor : str
        Cadena que se desea convertir.

    Devuelve
    --------
    bool o None
        True para 'true', False para 'false' y None si el valor no coincide.
    """
    valor = valor.strip().lower()
    if valor == "true":
        return True
    if valor == "false":
        return False