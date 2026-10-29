


class LectorTabla:
    def __init__(
        self, ruta: str, separador: str = ",", tiene_encabezado: bool = False,
        linea_inicio: int = None, columnas_a_leer = None
                ):
        """
        Inicializa una nueva instancia de la clase LectorTabla.

        Configura los parámetros iniciales para la lectura, recorte y 
        procesamiento del archivo de texto plano.

        Parámetros
        ----------
        ruta : str
            Ruta del archivo de texto o CSV que se desea leer.
        separador : str, opcional
            Carácter o cadena delimitadora de las columnas (por defecto es ",").
        tiene_encabezado : bool, opcional
            Indica si la primera línea del archivo contiene los nombres de las 
            columnas (por defecto es False).
        linea_inicio : int, opcional
            Número de línea a partir de la cual se comenzarán a leer los datos 
            (por defecto es None).
        tipo_datos_columnas : dict o list, opcional
            Especificación de los tipos de datos esperados para las columnas 
            (por defecto es None).
        columnas_a_leer : list, opcional
            Lista con los nombres de las columnas específicas que se desean 
            incluir en la lectura (por defecto es None, lo que incluye todas).
        """
        
        self.tabla = ruta
        self.separador = separador
        self.tiene_encabezado = tiene_encabezado
        self.linea_inicio = linea_inicio 
        self.columnas_a_leer = columnas_a_leer

# ---------------------------------------------------------        

    def leer_tabla(self):
        """
        Lee el archivo especificado, procesa su contenido y estructura el dataset.

        Ejecuta el flujo principal de carga: abre el archivo, autodetecta el 
        separador si se mantuvo el valor por defecto (","), valida o genera 
        los encabezados, recorta las líneas según el rango deseado, construye 
        la lista de diccionarios filtrando las columnas solicitadas e infiere 
        los tipos de datos de cada columna. Guarda el resultado en 
        self.dataset.

        Devuelve
        --------
        list[dict]
            Lista de diccionarios donde cada diccionario representa una fila 
            del archivo con sus valores convertidos a sus tipos de datos 
            correspondientes (int, float, str o None).

        Raises
        ------
        FileNotFoundError
            Si la ruta del archivo indicada en self.tabla no existe.
        """

        with open(self.tabla,"r") as archivo:
            lineas = archivo.read().strip().split("\n")

        
        # Si el separador es el por defecto (","), verificamos si realmente es ese o si hay otro más probable
        if self.separador == ",":
            candidatos = [",", ";", "\t", "|", "||"]
            # Contamos cuál de los separadores comunes aparece más veces en la primera línea
            separador_detectado = max(candidatos, key=lambda sep: lineas[0].count(sep))
            # Si el ganador aparece al menos una vez, lo adoptamos como el separador oficial
            if lineas[0].count(separador_detectado) > 0:
                self.separador = separador_detectado

        # Si tiene encabezado
        if self.tiene_encabezado == True:
            encabezado,encabezado_sin_filtrar = self._validarEncabezado(lineas=lineas)  
        # Si no tiene encabezado
        else:
            encabezado,encabezado_sin_filtrar = self._creamosEncabezado(lineas=lineas)

        self.encabezado = encabezado
        self.encabezado_sin_filtrar = encabezado_sin_filtrar
        resultado = []


        # Se valida desde y hasta donde mostrar del archivo
        lineas_recortadas,lineas_a_mostrar = self._validamosRecorteArchivo(lineas=lineas)
        print(f"Se imprimen {lineas_a_mostrar} lineas del archivo")

        for linea in lineas_recortadas:

            if self.separador == ",":
                # Buscamos patrones con comillas y comas internas y las unificamos con puntos
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

            for i in range(len(encabezado_sin_filtrar)):
                clave = encabezado_sin_filtrar[i].strip()
                valor = valores[i].strip()

                if encabezado_sin_filtrar[i] not in encabezado:
                    continue
                
                valor_final = str(valor)
                fila_dict[clave] =  valor_final

            resultado.append(fila_dict)
        self.dataset = resultado  

        self._tiparDataset()
        return self.dataset
        


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


# ------------METODOS PROTEGIDOS-----------------------------------------

    def _validarEncabezado(self,lineas):
        """
        Valida y corrige los nombres de las columnas presentes en la primera línea.

        Separa la primera línea del archivo utilizando el delimitador configurado
        y verifica que no existan nombres de columnas vacíos ni duplicados. Si
        detecta algún problema, solicita al usuario por consola que ingrese un
        nombre válido. Además, filtra las columnas si se especificó el atributo
        self.columnas_a_leer.

        Parámetros
        ----------
        lineas : list[str]
            Lista con todas las líneas de texto leídas del archivo.

        Devuelve
        --------
        tuple[list[str], list[str]]
            Una tupla con dos listas:
            - encabezado: Nombres de las columnas validadas (filtradas según
              self.columnas_a_leer).
            - encabezado_sin_filtrar: Todos los nombres de las columnas
              validadas en su orden original.
        """

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
                # Validamos también que no se repita un nombre que ya se eligió manualmente antes
                elif nombre in encabezado:
                    nombre = input(f"Ya usaste el nombre '{nombre}' en una columna anterior. Ingresa otro nombre para la columna {i+1}: ").strip()
                else:
                    break # El nombre es válido y no está repetido, salimos del bucle
            if self.columnas_a_leer == None:
                encabezado.append(nombre)
            else:
                if nombre in (self.columnas_a_leer):
                    encabezado.append(nombre)
            encabezado_sin_filtrar.append(nombre) 
        return encabezado, encabezado_sin_filtrar  
        
    def _creamosEncabezado(self,lineas):

        """
        Genera los nombres de las columnas cuando el archivo no posee encabezado.

        Determina la cantidad de columnas a partir de la primera línea del archivo
        y solicita al usuario por consola que ingrese los nombres separados por
        coma. Si el usuario omite la entrada, asigna nombres genéricos por
        defecto (Column_1, Column_2, etc.). Si ingresa nombres incompletos o
        duplicados, solicita su corrección interactivamente.

        Parámetros
        ----------
        lineas : list[str]
            Lista con todas las líneas de texto leídas del archivo.

        Devuelve
        --------
        tuple[list[str], list[str]]
            Una tupla con dos listas idénticas (encabezado y
            encabezado_sin_filtrar) que contienen los nombres asignados a cada
            columna.
        """
        primer_linea = lineas[0].split(self.separador)
        print(f"El archivo no tiene encabezado. Se detectaron {len(primer_linea)} columnas.")
        entrada_usuario = input("Ingresa los nombres de las columnas separados por coma (deja vacio para usar Column_1, Column_2...): ")
        
        encabezado_sin_filtrar = []

        if entrada_usuario.strip():
            nombres_usuario = [n.strip() for n in entrada_usuario.split(",")]
            for i in range(len(primer_linea)):
                nombre = nombres_usuario[i].strip() if i < len(nombres_usuario) else ""
                while True:
                    if not nombre:
                        nombre = input(f"Falta el nombre para la columna {i+1} (Dato de muestra: '{primer_linea[i].strip()}'). Ingresa un nombre válido: ").strip()
                    elif nombre in encabezado_sin_filtrar:
                        print(f"-> ¡Error de duplicado! Ya asignaste el nombre '{nombre}' a una columna anterior.")
                        nombre = input(f"El nombre '{nombre}' ya fue usado. Ingresa un nombre diferente para la columna {i+1}: ").strip()
                    else:
                        break
                encabezado_sin_filtrar.append(nombre)
        else:
            encabezado_sin_filtrar = [f"Column_{i+1}" for i in range(len(primer_linea))]

        if self.columnas_a_leer is None:
            encabezado = list(encabezado_sin_filtrar)
        else:
            encabezado = [col for col in encabezado_sin_filtrar if col in self.columnas_a_leer]

        return encabezado, encabezado_sin_filtrar

    def _validamosRecorteArchivo(self,lineas):
        """
        Determina y recorta el rango de líneas de datos que se procesarán.

        Valida el atributo self.linea_inicio (solicitándolo por consola si se 
        ingresó un valor fuera de rango o inválido) y pide interactivamente 
        al usuario hasta qué línea desea leer. Recorta la lista original 
        omitiendo la primera línea (índice 0) y ajustando el rango elegido.

        Parámetros
        ----------
        lineas : list[str]
            Lista con todas las líneas de texto leídas del archivo.

        Devuelve
        --------
        tuple[list[str], int]
            Una tupla que contiene:
            - lineas_recortadas: Sublista con las líneas seleccionadas para 
              procesar.
            - lineas_a_mostrar: Cantidad total de líneas incluidas en el 
              recorte.
        """

        recorte = 1 if self.tiene_encabezado else 0
        total_lineas = len(lineas) - recorte
        print(f"El archivo tiene un total de {total_lineas} líneas.")
        
        if self.linea_inicio is None:
            self.linea_inicio = 1
        else:
            while True:
                try:
                    self.linea_inicio = int(self.linea_inicio)
        
                    if 1 <= self.linea_inicio <= total_lineas:
                        break
        
                    print(f"Por favor, introduce un numero entre 1 y {total_lineas}.")
                    self.linea_inicio = input("¿Desde qué línea deseas leer? ")
        
                except ValueError:
                    print("Entrada no valida. Se continuara desde el inicio.")
                    self.linea_inicio = 1
                    break
        # Pedir línea de fin
        while True:
            try:
                entrada_fin = input(f"¿Hasta qué línea deseas leer? (Presiona Enter para ir hasta el final): ").strip()
                if not entrada_fin:
                    linea_fin = total_lineas
                    break
                linea_fin = int(entrada_fin)
                if self.linea_inicio <= linea_fin <= total_lineas:
                    break
                print(f"Por favor, introduce un número entre {self.linea_inicio} y {total_lineas}.")
            except ValueError:
                print("Entrada no válida. Por favor, introduce un número entero.")
        
        lineas_recortadas = lineas[self.linea_inicio : linea_fin + 1] # recortar la lista usando el rango del usuario (ajustando al índice de Python)
        lineas_a_mostrar = (linea_fin + 1) - self.linea_inicio 

        return lineas_recortadas, lineas_a_mostrar


    def _detectarTipoColumna(self,nombre_columna):
        """
        Infiere el tipo de dato uniforme más adecuado para una columna.

        Recorre todos los valores de la columna indicada en self.dataset 
        evaluando su compatibilidad según la jerarquía: int -> float -> str. 
        Las celdas vacías se ignoran durante la detección para no degradar 
        el tipo de la columna.

        Parámetros
        ----------
        nombre_columna : str
            Nombre de la columna (clave del diccionario) a analizar.

        Devuelve
        --------
        type
            El constructor del tipo de dato inferido para la columna 
            (int, float o str).
        """

        tipo_columna = int
        tipo_columna = int
        todos_vacios = True  # Bandera para saber si hay al menos un dato real

        for i in self.dataset:
            valor = str(i[nombre_columna]).strip()

            if valor == "":
                continue

            todos_vacios = False  

            if tipo_columna is int:
                try:
                    int(valor)
                    continue
                except ValueError:
                    tipo_columna = float

            if tipo_columna is float:
                try:
                    float(valor)
                except ValueError:
                    return str
        return str if todos_vacios else tipo_columna


    def _tiparDataset(self):
        """
        Convierte los valores de self.dataset a sus tipos de datos inferidos.

        Determina primero el tipo de dato correspondiente a cada columna 
        mediante _detectarTipoColumna y luego recorre todas las filas 
        aplicando la conversión in-place. Los valores vacíos ("") se 
        convierten en None. No devuelve ningún valor, ya que modifica 
        self.dataset directamente.
        """
        if not self.dataset:
            return

        columnas = list(self.dataset[0].keys())

        tipos_datos_columnas = {}
        for i in columnas:
            tipos_datos_columnas[i] = self._detectarTipoColumna(i)

        for fila in self.dataset:
            for col, funcion_convertir in tipos_datos_columnas.items():
                valor_limpio = str(fila[col]).strip()

                if valor_limpio == "":
                    fila[col] = None
                else:
                    fila[col] = funcion_convertir(valor_limpio)




















