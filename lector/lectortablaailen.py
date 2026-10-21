class LectorTabla:
    def __init__(self, ruta: str, separador: str = ",", tiene_encabezado: float = False, linea_inicio: int | None = None, tipo_datos_columnas = None):
        self.tabla = ruta
        self.separador = separador
        self.tiene_encabezado = tiene_encabezado
        self.linea_inicio = linea_inicio # Nueva variable para guardar desde qué línea empezar a leer
        self.tipo_datos_columnas = tipo_datos_columnas
        
    # Metodo principal
    # Este es el que hace exactamente lo que pide el objetivo del TP, leer y retornar el archivo.
    def leer_tabla(self):
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
            # Si detecta un campo vacío en el encabezado del archivo, te pide completarlo y si el que se coloca está repetido te pide que pongas otro nombre
            encabezado_crudo = lineas[0].split(self.separador)
            encabezado = []
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
                encabezado.append(nombre)           
        else:
            # Si no tiene encabezado, separamos la primera linea (lineas[0]) usando el separador correcto
            primer_linea = lineas[0].split(self.separador)
            print(f"El archivo no tiene encabezado. Se detectaron {len(primer_linea)} columnas.")
            entrada_usuario = input("Ingresa los nombres de las columnas separados por coma (deja vacio para usar Column_1, Column_2...): ")
            if entrada_usuario.strip():
                nombres_usuario = [n.strip() for n in entrada_usuario.split(",")]
                encabezado = []
                for i in range(len(primer_linea)):
                    # Si el usuario puso un nombre para esta posición, lo tomamos; si no, queda vacío para pedirlo
                    nombre = nombres_usuario[i].strip() if i < len(nombres_usuario) else ""
                    while True:
                        if not nombre:
                            nombre = input(f"Falta el nombre para la columna {i+1} (Dato de muestra: '{primer_linea[i].strip()}'). Ingresa un nombre válido: ").strip()
                        elif nombre in encabezado:
                            print(f"-> ¡Error de duplicado! Ya asignaste el nombre '{nombre}' a una columna anterior.")
                            nombre = input(f"El nombre '{nombre}' ya fue usado. Ingresa un nombre diferente para la columna {i+1}: ").strip()
                        else:
                            break
                    encabezado.append(nombre)
            else:
                encabezado = [f"Column_{i+1}" for i in range(len(primer_linea))]
        self.encabezado = encabezado
        resultado = []

        # Pedimos al usuario por consola que indique desde qué línea quiere empezar a leer
        entrada_linea = input(f"El archivo tiene {len(lineas)} líneas. ¿Desde qué línea deseas empezar a leer? (Presiona Enter para el inicio automático): ")
        if entrada_linea.strip():
            self.linea_inicio = int(entrada_linea)

        # Si se indicó una línea de inicio, recortamos la lista antes de que empiece la lógica
        if self.linea_inicio is not None:
          lineas = lineas[self.linea_inicio - 1 :]

        # Se empieza en la linea '1' ya que la linea '0' es el mismo encabezado

        for linea in lineas[1:]:

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

            for i in range(len(encabezado)):
                clave = encabezado[i].strip()
                valor = valores[i].strip()

                valor_final = str(valor)
                fila_dict[clave] =  valor_final

                
            resultado.append(fila_dict)

        # Luego de construir el dataset, se asigna a la propiedad dataset del objeto de clase
        # Y se ejecuta la funcion de transformar columna, que modifica los tipos de dato del dataset

        self.dataset = resultado
        self._transformar_columnas_dataset(encabezado,self.tipo_datos_columnas)                        
        return resultado


    # En la siguiente seccion se crean los metodos
    # En mi recomendacion, lo ideal es que los metodos que se utilizan solamente para ayudar al 'Metodo principal', se crean siendo protegidos 
    # Por principios de encapsulamiento en POO

    
    # En función de una lista de columnas proveídas, y una lista de tipos de datos de prioridad
    # Se reconstruye cada columna, se evalúa que tipo de datos es el más adecuado y se transforma la columna
    # con dicho tipo de datos, luego se reemplaza la columna en el dataset original. 
    # Los tipos de datos porveídos tienen prioridad, si no se pasó ninguno, el programa evalúa cual es el tipo
    # más adecuado 

    def _transformar_columnas_dataset(self,encabezados,lista_tipo_datos):

        # Si no se pasó ningun argumento de tipos de datos, se genera una lista de None
        if lista_tipo_datos == None:
            lista_tipo_datos = [None for x in range(0,len(encabezados))]

        # Se va iterenado sobre un par columna/tipo de dato sugerido
        for i,o in zip(encabezados,lista_tipo_datos):
            columna_cruda = []
            columna_transformada = []
            # Se reconstruye la columna a evaluar por separado en una lista
            for j in self.dataset:
                columna_cruda.append(j[i])
            # En base a la columna cruda, se evalua que función se necesita para transformarla y se devuelve la funcion
            funcion = evaluar_funcion_transformacion(columna_cruda,o)
            # Se transforma la columna curda con la función que se evaluó
            for k in columna_cruda:
                columna_transformada.append(funcion(k))
            # Se reemplaza en el dataset la columna original por la columna con el tipo de dato correcto
            for m,n in zip(self.dataset,columna_transformada):
                m[i] = n


    # Se aportan como argumentos una lista de columnas y otra lista de funciones
    # Se va aplicando el filtrado por par de columna/función sucesivamente 
    # Se filtra el mismo dataset, no se devuelve una copia

    def filtrar_dataset(self,columnas,funciones):
        for a,b in zip(columnas,funciones):
            self.dataset = [i for i in self.dataset if b(i[a])]


    # Se aporta como argumento una lista de columnas (con nombre), y se construye un nuevo dataset
    # a partir del dataset del objeto, únicamente con aquellas columnas que se pasaron.
    # Se devuelve un nuevo dataset, no modifica la propiedad del objeto de clase

    def crear_consulta(self,columnas):
        consulta = []
        for i in self.dataset:
            diccionario = {}
            for j in columnas:
                diccionario[j] = i[j]
            consulta.append(diccionario)
        return consulta

    


    
    # Comentado porque no se usa más la función

    # def _convertir_tipo_de_dato(self,dato):
    #     # Limpiamos espacios y comillas residuales que impiden evaluar correctamente con .isdigit()
    #     dato = dato.strip().replace('"', '').replace("'", "")
    #     # CONTROL DE CELDA VACÍA: Si no contiene nada, devolvemos un valor seguro (ej: None, 0 o "")
    #     if not dato:
    #         return None
    #     if "." in dato and dato.replace(".","", 1).isdigit():
    #         dato_final = float(dato)
    #     elif dato.isdigit():
    #         dato_final = int(dato)
    #     else:
    #         dato_final = dato
    #     return dato_final
        

# FUNCIONES AUXILARES: No forman parte de la clase, pero la clase las usa, por ende no se debe
# importar unicamente la clase, si no que se debe importar el módulo entero 

# se provee una columna (lista con valores) y un tipo de dato
# Si el tipo de dato ya está especificado por el usuario (es disitnto de None o vacío), se devuelve una función
# directamente usando un diccionario como referencia. Esto implica que los valores que puede proveer el usuario
# son los strings que existen como clave en el diccionario
# Si no se pasó un tipo de dato, se va evaluando secuencialmente de manera excluyente, cual es el tipo de dato
# Y se devuelve dicha función

def evaluar_funcion_transformacion(columna,tipo_dato):
    diccionario = {
        "None": convertir_none, "str": str, "int": int,
        "float":float, "bool": convertir_bool}
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
    for i in lista:
        if i == "" or i == "None":
            continue
        else:
            return False
    return True

def evaluar_bool(lista):
    for i in lista:
        i = i.strip().lower()
        if i == "true" or i == "false":
            continue
        else:
            return False
    return True 


def evaluar_int(lista):
    for i in lista:
        try:
            int(i)
        except ValueError:
            return False
    return True

def evaluar_float(lista):
    for i in lista:
        try:
            float(i)
        except ValueError:
            return False
    return True
            
def convertir_none(valor):
    return None

def convertir_bool(valor):
    valor = valor.strip().lower()
    if valor == "true":
        return True
    if valor == "false":
        return False
