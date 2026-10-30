from lector.lectorTabla import LectorTabla

tabla = LectorTabla(ruta="datos/productos.csv",tiene_encabezado=True)

print(tabla.leer_tabla())

# Convertir la lista de diccionario a un Data Frame de pandas

import pandas as pd

# Instanciamos la clase con los parámetros que necesitamos
lector = LectorTabla(
    ruta="datos/productos.csv",                 
    tiene_encabezado=True,         
)

# Obtenemos la lista de diccionarios ejecutando el método
lista_datos = lector.leer_tabla()

# Conversión a Data Frame
df = pd.DataFrame(lista_datos)

# Mostrar el resultado en la terminal
print("\n--- DATAFRAME DE PANDAS RESULTANTE ---")
print(df)
