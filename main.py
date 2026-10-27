from lector.lectorTabla import LectorTabla


# El codigo que esta aca es un simple ejemplo para que vean como funciona ya el programa. ejecuten este programa y veran como funciona
tabla = LectorTabla(ruta="datos/productos.csv",tiene_encabezado=True)

print(tabla.leer_tabla())















"""
# Variantes:

# En el caso de que el archivo no tenga encabezado, se le solicita al usuario que cree los nombres de los encabezados separados por coma:

tabla = LectorTabla(ruta="datos/productossinencab.csv",tiene_encabezado=True)

print(tabla.leer_tabla())

# En el caso de que los datos estén separados por punto y coma (también se podría probar con otros separadores)

tabla = LectorTabla(ruta="datos/productospuntoycoma.csv",tiene_encabezado=True)

print(tabla.leer_tabla())

# En el caso de que haya un encabezado vacío, se le pide al usuario que complete el nombre del encabezado (se considera el caso de que coloque dos veces el mismo nombre de encabezado)
# También se podría probar para el caso de que no haya ningún encabezado

tabla1 = LectorTabla(ruta="datos/encabezadovacio.csv",tiene_encabezado=True)

print(tabla1.leer_tabla())

# En el caso de que haya una celda vacía, reemplaza el valor por None

tabla = LectorTabla(ruta="datos/celdavacia.csv",tiene_encabezado=True)

print(tabla.leer_tabla())

"""