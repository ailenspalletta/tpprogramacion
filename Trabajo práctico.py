
def crear_encabezados(linea,numeros,nombres):
    lista_encabezados = []
    lista_original_acum = []
    lista_depurada = []
    for i in linea:
        if i == "":
            i = "unnamed"
        if i in lista_original_acum:
            lista_depurada.append(f"{i} {lista_original_acum.count(i) + 1}")
        else:
            lista_depurada.append(i)
        lista_original_acum.append(i)
    if numeros != None:
        for i in numeros:
            lista_encabezados.append(linea[i])
    elif nombres != None:
        for i in nombres:
            lista_encabezados.append(linea[linea.index(i)])
    else:
        lista_encabezados = linea
    return lista_depurada

def generar_linea(encabezados,linea):
    registro = {}
    for i in range(0,len(linea)):
        registro[encabezados[i]] = str(linea[i])
    return registro

def evaluar_tipo_de_dato(columna):
    if evaluar_booleano(columna):
        def convertir_booleano(string):
            if string.lower() == "true":
                return True
            if string.lower() == "false":
                return False 
        return convertir_booleano
    elif evaluar_float(columna):
        return float
    elif evaluar_int(columna):
        return int
    else:
        return str
 
def evaluar_booleano(columna):
    for i in columna:
        if i == "True".lower() or i == "False".lower():
            next
        else:
            return False
    return True

def evaluar_float(columna):
    for i in columna:
        try: 
            float(i)
        except ValueError:
            return False
    return True

def evaluar_int(columna):
    for i in columna:
        try:
            int(i)
        except ValueError:
            return False
    return True
       
def convertir_columna(columna,funcion):
    nueva_columna = []
    for i in columna:
        nueva_columna.append(funcion(i))
    return nueva_columna


# # Cosas que tiene que soportar el lector:
# Argumentos necesarios: ruta_archivo,separador, tipos_columnas 

# - Permitir distintos separadores, intentando inferir el separador correcto
# - Intentar inferir automáticamente el tipo de columnas, permitiendo que el usuario especifique el tipo
# - Indicar que hacer con las columnas que tienen todos valores nulos
# - Identificar que valores puede agrupar como booleanos
# - Especificar la cantidad de filas y columnas a leer
# - Filtrar las filas por un criterio



# Definición de función principal
def crear_dataset(
    ruta, separador = ",", tipo_columnas = None, nro_columnas_a_importar = None, nro_filas_a_importar = None, 
    nombres_columnas_a_importar = None, archivo_sin_encabezados = False):


    archivo = open(ruta,"r")

# Leer primera linea y construir encabezados, según si se indicó que la primer linea era de encabezados o no

    primera_linea = archivo.readline().rstrip("\n").split(separador)
    if archivo_sin_encabezados == False:
        encabezados = crear_encabezados(primera_linea,nro_columnas_a_importar,nombres_columnas_a_importar)
    elif archivo_sin_encabezados == True:
        pass#encabezados = lista de comprensión

# Crear la lista de registros e ir leyendo las lineas siguientes

    registros = []
    contador = 1

# Si se especificaron lineas específicas a importar, se va verificando cuales leer y cuales no
# Las lineas a leer se identifican como una lista numérica, NO como un rango. 
# Esto es por si se quieren saltear lineas
# Si no se especifica, se leen todas las lineas

    if nro_filas_a_importar != None:
        for linea in archivo:
            linea = linea.rstrip("\n").split(separador) 
            if contador not in nro_filas_a_importar:
                next
            registros.append(generar_linea(encabezados,linea))
            contador += 1
    elif nro_filas_a_importar == None:
        for linea in archivo:
            linea = linea.rstrip("\n").split(separador)
            registros.append(generar_linea(encabezados,linea))
    
    # Una vez construido los registros, se construyen las distintas columnas
    # Y se evalua su tipo de datos. Luego se reescriben con el tipo de dato definitvo

    for i in encabezados:
        columna = []
        for j in registros:
             columna.append(j[i])
        funcion_convertir_dato = evaluar_tipo_de_dato(columna)
        columna = convertir_columna(columna,funcion_convertir_dato)
        for k in registros:
            k[i] = columna[registros.index(k)]
    
    #codigo de prueba
    return encabezados,registros

a,b = crear_dataset("dataset_prueba.txt")



    

    
        




