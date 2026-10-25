
"""
Módulo que contiene la clase LectorTabla.

Permite leer archivos de texto organizados en tablas, procesar sus
encabezados, seleccionar líneas y columnas, transformar tipos de datos,
filtrar registros y crear consultas.
"""

from os import path
from warnings import warn
import funciones_auxiliares as f


class LectorTabla:
    """
    Lee y procesa un archivo de texto organizado en forma de tabla.

    Permite configurar el separador, indicar si existe un encabezado,
    seleccionar un rango de líneas y columnas, y convertir los valores
    de las columnas a tipos de datos explícitos o inferidos.

    El dataset procesado queda disponible en el atributo dataset y los
    nombres de las columnas en encabezado.
    """

    def __init__(
        self, ruta: str, separador: str = None, tiene_encabezado: bool = False,
        linea_inicio: int | None = None, linea_fin: int | None = None, tipo_datos_columnas: list | None = None,
        columnas_a_leer: list | None = None):
        """
        Inicializa el lector, valida los argumentos y procesa el archivo.

        Parámetros
        ----------
        ruta : str
            Ruta del archivo de texto que se leerá.
        separador : str o None, opcional
            Delimitador entre campos. Si es None, se intenta detectar.
        tiene_encabezado : bool, opcional
            Indica si la primera línea contiene nombres de columnas.
        linea_inicio : int o None, opcional
            Índice de la primera línea que se incluirá en la lectura.
        linea_fin : int o None, opcional
            Índice de la última línea que se incluirá en la lectura.
        tipo_datos_columnas : list o None, opcional
            Tipos de datos prioritarios para las columnas.
        columnas_a_leer : list o None, opcional
            Nombres de las columnas que se conservarán, si hay encabezado.

        Raises
        ------
        TypeError
            Si algún argumento no tiene el tipo esperado.
        ValueError
            Si los argumentos son incompatibles o el archivo está vacío.
        """
        # Validaciones iniciales de tipos de dato de argumentos:
        if not isinstance(ruta, str):
            raise TypeError("La ruta proveída debe ser un string")
        if not isinstance(separador, str) and separador != None:
            raise TypeError("El separador proveído debe ser un string")
        if not isinstance(tiene_encabezado, bool):
            raise TypeError("El argumento tiene_encabezado debe ser booleano")
        if not isinstance(linea_inicio, int) and linea_inicio != None:
            raise TypeError("La linea de inicio debe ser un número entero o None")
        if not isinstance(linea_fin, int) and linea_fin != None:
            raise TypeError("La linea de Fin debe ser un número entero o None")
        if not isinstance(tipo_datos_columnas, list) and tipo_datos_columnas != None:
            raise TypeError("El argumento tipo_datos_columnas debe ser una lista o None")
        if not isinstance(columnas_a_leer, list) and columnas_a_leer != None:
            raise TypeError("El argumento columnas_a_leer debe ser una lista o None")

        # Validaciones de argumentos coherentes:
        if tipo_datos_columnas != None and columnas_a_leer != None:
            if len(tipo_datos_columnas) != len(columnas_a_leer):
                raise ValueError("La cantidad de tipos de datos debe coincidircon la cantidad de columnas a leer")

        if tiene_encabezado == False and columnas_a_leer != None:
            raise ValueError("Si el dataset no tiene encabezados, no se pueden especificar columnas a leer, se leen todas")

        if path.getsize(ruta) == 0:
            raise ValueError("El archivo proveído está vacío, compruebe si la ruta ingresada es correcta")

        self.tabla = ruta
        self.separador = separador
        self.tiene_encabezado = tiene_encabezado
        self.linea_inicio = linea_inicio
        self.linea_fin = linea_fin
        self.tipo_datos_columnas = tipo_datos_columnas
        self.columnas_a_leer = columnas_a_leer
        self.leer_tabla()

    def leer_tabla(self):
        """
        Lee el archivo y construye el dataset procesado.

        Detecta o utiliza el separador indicado, prepara los encabezados,
        recorta las líneas solicitadas, comprueba la cantidad de campos
        de cada fila y transforma los valores de las columnas.

        Devuelve
        --------
        list[dict]
            Filas del archivo representadas como diccionarios.
        """
        with open(self.tabla, "r") as archivo:
            lineas = archivo.read().strip().split("\n")

        # Si no se especificó el separador, se intenta detectar.
        if self.separador == None:
            candidatos = [",", ";", "\t", "|", "||"]
            separador_detectado = max(candidatos,key=lambda sep: lineas[0].count(sep))
            if lineas[0].count(separador_detectado) > 0:
                self.separador = separador_detectado

        # Procesamiento de encabezados.
        if self.tiene_encabezado == True:
            encabezado_crudo = lineas[0].split(self.separador)
            encabezado = []
            encabezado_sin_filtrar = []

            for i in range(len(encabezado_crudo)):
                nombre = encabezado_crudo[i].strip()

                while True:
                    if not nombre:
                        nombre = input(f"Se detectó un encabezado vacío en la columna {i+1} del archivo. Ingresa un nombre válido: ").strip()
                    elif nombre in encabezado_crudo and encabezado_crudo.index(nombre) != i:
                        print(f"-> ¡Error! El nombre '{nombre}' está asignado originalmente a la columna {encabezado_crudo.index(nombre)+1}.")
                        nombre = input(f"Ingresa un nombre diferente para la columna {i+1}: ").strip()
                    elif nombre in encabezado:
                        nombre = input(
                            f"Ya usaste el nombre '{nombre}' en una columna anterior. Ingresa otro nombre para la columna {i+1}: ").strip()
                    else:
                        break

                if self.columnas_a_leer == None:
                    encabezado.append(nombre)
                else:
                    if nombre in self.columnas_a_leer:
                        encabezado.append(nombre)

                encabezado_sin_filtrar.append(nombre)

        else:
            primer_linea = lineas[0].split(self.separador)
            print(
                f"El archivo no tiene encabezado. Se detectaron {len(primer_linea)} columnas.")
            entrada_usuario = input(
                "Ingresa los nombres de las columnas separados por coma (deja vacio para usar Column_1, Column_2...): ")

            if entrada_usuario.strip():
                nombres_usuario = [n.strip() for n in entrada_usuario.split(",")]
                encabezado = []
                encabezado_sin_filtrar = []

                for i in range(len(primer_linea)):
                    nombre = (
                        nombres_usuario[i].strip()
                        if i < len(nombres_usuario)
                        else "")

                    while True:
                        if not nombre:
                            nombre = input(
                                f"Falta el nombre para la columna {i+1} (Dato de muestra: '{primer_linea[i].strip()}'). Ingresa un nombre válido: ").strip()
                        elif nombre in encabezado:
                            print(f"-> ¡Error de duplicado! Ya asignaste el nombre '{nombre}' a una columna anterior.")
                            nombre = input(f"El nombre '{nombre}' ya fue usado. Ingresa un nombre diferente para la columna {i+1}: ").strip()
                        else:
                            break

                    encabezado.append(nombre)
                    encabezado_sin_filtrar.append(nombre)

            else:
                encabezado = [f"Column_{i+1}" for i in range(len(primer_linea))]
                encabezado_sin_filtrar = [f"Column_{i+1}" for i in range(len(primer_linea))]

        self.encabezado = encabezado
        self.encabezado_sin_filtrar = encabezado_sin_filtrar
        resultado = []

        # Resolver la línea de inicio si no fue especificada.
        if self.linea_inicio is None:
            if self.tiene_encabezado:
                linea_inicio = 1
            else:
                linea_inicio = 0
        else:
            linea_inicio = self.linea_inicio
            if self.tiene_encabezado == True and self.linea_inicio == 0:
                warn("Se especificó que el dataset tiene encabezados, pero por la linea de inicio especificada, estos encabezados tambien se incluyeron como el primer registro")

        # Resolver la línea final si no fue especificada.
        if self.linea_fin is None:
            linea_fin = len(lineas) - 1
        else:
            linea_fin = self.linea_fin

        # Validar que el rango sea válido.
        if linea_inicio < 0 or linea_inicio >= len(lineas):
            raise ValueError("La línea de inicio está fuera del rango del archivo")

        if linea_fin < 0 or linea_fin >= len(lineas):
            raise ValueError("La línea final está fuera del rango del archivo")

        if linea_inicio > linea_fin:
            raise ValueError("La línea de inicio no puede ser posterior a la línea final")

        # Recortar las líneas, incluyendo la línea final.
        lineas_recortadas = lineas[linea_inicio:linea_fin + 1]

        for linea in lineas_recortadas:

            if self.separador == ",":
                # Se reemplazan las comas internas de los textos entre comillas.
                while '"' in linea:
                    inicio = linea.find('"')
                    fin = linea.find('"', inicio + 1)
                    if fin != -1:
                        texto_comillas = linea[inicio:fin+1]
                        texto_limpio = texto_comillas.replace('"', '').replace(',', '.')
                        linea = linea.replace(texto_comillas, texto_limpio)
                    else:
                        break

            valores = linea.split(self.separador)
            fila_dict = {}

            # Validar que cada fila tenga la cantidad esperada de campos.
            if len(valores) != len(encabezado_sin_filtrar):
                raise ValueError(
                    "Atención! Se detectó una linea con más campos que los encabezados del dataset, corrija el dataset e intente nuevamente")

            for i in range(len(encabezado_sin_filtrar)):
                clave = encabezado_sin_filtrar[i].strip()
                valor = valores[i].strip()

                if encabezado_sin_filtrar[i] not in encabezado:
                    continue

                valor_final = str(valor)
                fila_dict[clave] = valor_final

            # Advertir si una fila contiene únicamente valores vacíos.
            if all(valor == "" for valor in fila_dict.values()):
                warn(f"Atención! en la linea número {lineas_recortadas.index(linea)} solo hay valores vacíos, se mantuvo el registro con solo valores vacíos")

            resultado.append(fila_dict)

        self.dataset = resultado
        self._transformar_columnas_dataset(encabezado,self.tipo_datos_columnas)
        return resultado

    def _transformar_columnas_dataset(self, encabezados, lista_tipo_datos):
        """
        Convierte los valores de las columnas a los tipos correspondientes.

        Utiliza los tipos prioritarios indicados o infiere el tipo a partir
        de los valores de cada columna. Modifica self.dataset directamente.

        Parámetros
        ----------
        encabezados : list
            Nombres de las columnas que se transformarán.
        lista_tipo_datos : list o None
            Tipos de datos prioritarios, en el mismo orden que encabezados.

        Raises
        ------
        ValueError
            Si la cantidad de tipos especificados no coincide con las columnas.
        """
        if lista_tipo_datos == None:
            lista_tipo_datos = [None for x in range(0, len(encabezados))]

        if len(lista_tipo_datos) != len(encabezados):
            raise ValueError("Se pasó una cantidad de tipos de datos sugeridos distinta a la cantidad de columnas que se leen")

        for i, o in zip(encabezados, lista_tipo_datos):
            columna_cruda = []
            columna_transformada = []

            for j in self.dataset:
                columna_cruda.append(j[i])

            funcion = f.evaluar_funcion_transformacion(columna_cruda, o)

            for k in columna_cruda:
                try:
                    columna_transformada.append(funcion(k))
                except ValueError:
                    print("Atención!!!! Al intentar convertir hacer la conversión de uno de los tipos de dato se produjo un error")
                    print("Revise los tipos de datos que se pasó, ya que el programa toma estos tipos de datos como prioritarios sin revisar si son coherentes")
                    raise

            for m, n in zip(self.dataset, columna_transformada):
                m[i] = n

    def filtrar_dataset(self, columnas: list, funciones: list):
        """
        Filtra el dataset aplicando funciones sobre las columnas indicadas.

        Cada función se aplica a los valores de su columna correspondiente.
        Se conservan las filas para las que la función devuelve un valor
        verdadero. Este método modifica self.dataset directamente.

        Parámetros
        ----------
        columnas : list
            Nombres de las columnas sobre las que se aplicarán los filtros.
        funciones : list
            Funciones de filtrado, emparejadas por posición con columnas.

        Raises
        ------
        TypeError
            Si columnas o funciones no son listas.
        ValueError
            Si las listas tienen longitudes distintas o alguna columna no existe.
        """
        if not isinstance(columnas, list):
            raise TypeError("El argumento de columnas debe ser una lista")
        if not isinstance(funciones, list):
            raise TypeError("El argumento de funciones debe ser una lista")

        if len(columnas) != len(funciones):
            raise ValueError("la lista de columnas y funciones deben coincidir")

        if any(x not in self.encabezado for x in columnas):
            raise ValueError("Al menos una de las columnas proveídas para el filtrado no existe en el dataset")

        for a, b in zip(columnas, funciones):
            self.dataset = [i for i in self.dataset if b(i[a])]

    def crear_consulta(self, columnas: list):
        """
        Crea una consulta que contiene únicamente las columnas solicitadas.

        Construye y devuelve una nueva lista de diccionarios. No modifica
        self.dataset.

        Parámetros
        ----------
        columnas : list
            Nombres de las columnas que se incluirán en la consulta.

        Devuelve
        --------
        list[dict]
            Nueva lista de filas con las columnas solicitadas.

        Raises
        ------
        TypeError
            Si columnas no es una lista.
        ValueError
            Si alguna de las columnas solicitadas no existe.
        """
        if not isinstance(columnas, list):
            raise TypeError("El argumento de columnas debe ser una lista")

        if any(x not in self.encabezado for x in columnas):
            raise ValueError("Al menos una de las columnas proveídas para la consulta no existe en el dataset")

        consulta = []
        for i in self.dataset:
            diccionario = {}
            for j in columnas:
                diccionario[j] = i[j]
            consulta.append(diccionario)

        return consulta
