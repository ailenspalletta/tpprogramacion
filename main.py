from lector.lector_tabla import LectorTabla

# En main se creara la interfaz del tp, mientras que la logica del TP se crea en la carpeta 'lector', aqui es donde se pone a prueba el lector
# La parte visible del proyecto, en pocas palabras

# El codigo que esta aca es un simple ejemplo para que vean como funciona ya el programa. ejecuten este programa y veran como funciona
tabla = LectorTabla(ruta="datos/productos.csv",tiene_encabezado=True)

print(tabla.leer_tabla())