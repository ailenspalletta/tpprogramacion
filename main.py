from lector.lectorTabla import LectorTabla

tabla = LectorTabla(ruta="datos/productos.csv",tiene_encabezado=True)

print(tabla.leer_tabla())



