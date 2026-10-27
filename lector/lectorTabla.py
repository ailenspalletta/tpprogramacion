


class LectorTabla:
    def __init__(
        self, ruta: str, separador: str = ",", tiene_encabezado: bool = False,
        linea_inicio: int = None, tipo_datos_columnas = None, columnas_a_leer = None
                ):
        self.tabla = ruta
        self.separador = separador
        self.tiene_encabezado = tiene_encabezado
        self.linea_inicio = linea_inicio # Nueva variable para guardar desde qué línea empezar a leer
        self.tipo_datos_columnas = tipo_datos_columnas
        self.columnas_a_leer = columnas_a_leer

# ---------------------------------------------------------        
 
    """
    COSAS POR HACER
    - Seleccionar solo algunas columnas
    - Filtrar por nombre, cantidad, etc

    """

    """"
       Metodo principal
        En este metodo solo se mostrara la estructura, lo demas se hara adentro de un metodo diferente (que luego se usara adentro del metodo principal)
        ¿Por que?
        Esto es necesario, si luego queremos modificar la estructura principal, no tendremos que 
          estar leyendo todo el codigo y evitar romper algo que no debamos
        ¿Y si quiero modificar algo puntual?
        Voy al metodo externo en especifico con sus propias variables y lo modifico sin tener que
          romper toda la estructura del metodo principal
    """
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
        

# -----------------------------------------------------

    def _validarEncabezado(self,lineas):
        # Si detecta un campo vacío en el encabezado del archivo, te pide completarlo y si el que se coloca está repetido te pide que pongas otro nombre
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
        # Si no tiene encabezado, separamos la primera linea (lineas[0]) usando el separador correcto
        primer_linea = lineas[0].split(self.separador)
        print(f"El archivo no tiene encabezado. Se detectaron {len(primer_linea)} columnas.")
        entrada_usuario = input("Ingresa los nombres de las columnas separados por coma (deja vacio para usar Column_1, Column_2...): ")
        if entrada_usuario.strip():
            nombres_usuario = [n.strip() for n in entrada_usuario.split(",")]
            encabezado = []
            encabezado_sin_filtrar = []
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
                encabezado_sin_filtrar.append(nombre)
        
        else:
            encabezado = [f"Column_{i+1}" for i in range(len(primer_linea))]
            encabezado_sin_filtrar = [f"Column_{i+1}" for i in range(len(primer_linea))]

        return encabezado,encabezado_sin_filtrar

    def _validamosRecorteArchivo(self,lineas):
        # Si el usuario no indico nada, se inicia desde la primer linea
        # Si el usuario indico un numero, se inicia desde ese numero mientras sea valido
        # Si indico otra cosa que no sea un numero, arrancamos desde el inicio 
        total_lineas = len(lineas) - 1
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
        tipo_columna = int

        for i in self.dataset:
            valor = str(i[nombre_columna]).strip()

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
        return tipo_columna


    def _tiparDataset(self):
        columnas = list(self.dataset[0].keys())

        tipos_datos_columnas = {}
        for i in columnas:
            tipos_datos_columnas[i] = self._detectarTipoColumna(i)


        for fila in self.dataset:
            for col, funcion_convertir in tipos_datos_columnas.items():
                fila[col] = funcion_convertir(fila[col].strip())




















