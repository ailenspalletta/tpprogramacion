

class LectorTabla:
    def __init__(self, ruta: str, separador: str = ",", tiene_encabezado: float = False):
        self.tabla = ruta
        self.separador = separador
        self.tiene_encabezado = tiene_encabezado

    # Metodo principal
    # Este es el que hace exactamente lo que pide el objetivo del TP, leer y retornar el archivo.
    def leer_tabla(self):
        with open(self.tabla,"r") as archivo:
            lineas = archivo.read().strip().split("\n")
        # Aqui lo hice en el caso de que si tenga encabezado pero pueden programar abajo, que pasaria si no hay encabezado
        if self.tiene_encabezado == True:
            encabezado = lineas[0].split(",")

        resultado = []

        # Aqui es donde se podria modificar para la pauta donde pregunta de que linea hasta que linea debe leer en el archivo
        # Se empieza en la linea '1' ya que la linea '0' es el mismo encabezado
        for linea in lineas[1:]:

            # En este caso separamos los valores por una ',' ya que en el caso perfecto es un archivo CSV pero si programan la pautas donde tienen
            # otro separador, desde aca seria muy facil
            valores = linea.split(",")
            fila_dict = {}

            for i in range(len(encabezado)):
                clave = encabezado[i].strip()
                valor = valores[i].strip()

                valor_final = self._convertir_tipo_de_dato(valor)
                fila_dict[clave] =  valor_final

                
            resultado.append(fila_dict)
        return resultado


    # En la siguiente seccion se crean los metodos
    # En mi recomiendacion, lo ideal es que los metodos que se utilizan solamente para ayudar al 'Metodo principal', se crean siendo protegidos 
    # Por principios de encapsulamiento en POO
    def _convertir_tipo_de_dato(self,dato):
        if "." in dato and dato.replace(".","", 1).isdigit():
            dato_final = float(dato)
        elif dato.isdigit():
            dato_final = int(dato)
        else:
            dato_final = dato
        return dato_final


