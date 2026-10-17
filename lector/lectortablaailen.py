class LectorTabla:
    def __init__(self, ruta: str, separador: str = ",", tiene_encabezado: float = False, linea_inicio: int | None = None):
        self.tabla = ruta
        self.separador = separador
        self.tiene_encabezado = tiene_encabezado
        self.linea_inicio = linea_inicio # Nueva variable para guardar desde qué línea empezar a leer
        
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

                valor_final = self._convertir_tipo_de_dato(valor)
                fila_dict[clave] =  valor_final

                
            resultado.append(fila_dict)
                                  
        return resultado
    
    # En la siguiente seccion se crean los metodos
    # En mi recomendacion, lo ideal es que los metodos que se utilizan solamente para ayudar al 'Metodo principal', se crean siendo protegidos 
    # Por principios de encapsulamiento en POO
    def _convertir_tipo_de_dato(self,dato):
        # Limpiamos espacios y comillas residuales que impiden evaluar correctamente con .isdigit()
        dato = dato.strip().replace('"', '').replace("'", "")
        # CONTROL DE CELDA VACÍA: Si no contiene nada, devolvemos un valor seguro (ej: None, 0 o "")
        if not dato:
            return None
        if "." in dato and dato.replace(".","", 1).isdigit():
            dato_final = float(dato)
        elif dato.isdigit():
            dato_final = int(dato)
        else:
            dato_final = dato
        return dato_final
