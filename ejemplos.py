# EJEMPLO 1: Creación de consultas específicas
# Este ejemplo demuestra cómo trabaja la función crear_consulta(columnas). 
# Extrae un subconjunto de datos (por ejemplo, solo queremos saber el stock de los artículos) 
# sin modificar la lista original que guardó el objeto.

tabla = LectorTabla(ruta="datos/productos.csv", tiene_encabezado=True)
tabla.leer_tabla() # Carga inicial de datos

# Se ejecuta el método para extraer solo las columnas de interés
# Si se pasa una columna inexistente, el código lanzará ValueError 
datos_stock = tabla.crear_consulta(columnas=["Nombres", "Cantidad"])

print("\n--- VISTA DE CONSULTA (SÓLO STOCK) ---")
for registro in datos_stock:
    # Los diccionarios de esta nueva lista ya no contienen la clave 'Precio'
    print(f"Producto: {registro['Nombres']:<12} -> Stock disponible: {registro['Cantidad']}")


# EJEMPLO 2: Filtrado avanzado y eliminación manual de duplicados
# El método filtrar_dataset modifica directamente la lista interna self.dataset aplicando funciones. 
# En este ejemplo, usaremos una función lambda para buscar productos que cuesten más de $1000 y agregaremos 
# lógica externa para que no imprima las filas repetidas que tiene el archivo (como Cuaderno y Lapicera).

tabla = LectorTabla(ruta="datos/productos.csv", tiene_encabezado=True)
tabla.leer_tabla()

# Aplicamos el método de filtrado pasando listas en ambos argumentos
tabla.filtrar_dataset(
    columnas=["Precio"],
    funciones=[lambda precio: precio > 1000]
)

print("\n--- PRODUCTOS MÁS CAROS (> $1000) SIN DUPLICADOS ---")

# Usamos un conjunto de Python para recordar qué productos ya mostramos
productos_ya_mostrados = set()

# Recorremos el dataset interno que modificó la función
for fila in tabla.dataset:
    nombre = fila['Nombres']
    
    # Si el nombre ya está en el conjunto, saltamos a la siguiente fila
    if nombre in productos_ya_mostrados:
        continue
    
    # Si es nuevo, lo registramos y lo mostramos
    productos_ya_mostrados.add(nombre)
    print(f"✓ {nombre:<12} | Precio: ${fila['Precio']:.2f} | Unidades: {fila['Cantidad']}")

# EJEMPLO 3: Buscar el producto más caro y el más barato (extremos)
# Este ejemplo analiza la lista de diccionarios para encontrar de forma automática 
# qué artículo tiene el mayor y menor precio, simulando un control de inventario básico.

tabla = LectorTabla(ruta="datos/productos.csv", tiene_encabezado=True)
lista_productos = tabla.leer_tabla()

# Inicializamos las variables con el primer producto de la lista
producto_mas_caro = lista_productos[0]
producto_mas_barato = lista_productos[0]

# Recorremos el dataset buscando los extremos matemáticos
for fila in lista_productos:
    if fila['Precio'] > producto_mas_caro['Precio']:
        producto_mas_caro = fila
    if fila['Precio'] < producto_mas_barato['Precio']:
        producto_mas_barato = fila

print("\n=== REPORTE DE EXTREMOS DE PRECIOS ===")
print(f"🔺 Más caro: {producto_mas_caro['Nombres']} -> ${producto_mas_caro['Precio']:.2f}")
print(f"🔻 Más barato: {producto_mas_barato['Nombres']} -> ${producto_mas_barato['Precio']:.2f}")

# EJEMPLO 4: Agrupar y consolidar stock (sumar cantidades de duplicados)
# Como en el archivo de prueba hay filas repetidas (por ejemplo, Cuaderno aparece en la fila 0 y en la 3), 
# este ejemplo utiliza un diccionario acumulador de Python para agrupar los artículos por su nombre 
# y sumar sus cantidades totales.

tabla = LectorTabla(ruta="datos/productos.csv", tiene_encabezado=True)
lista_productos = tabla.leer_tabla()

# Creamos un diccionario vacío para consolidar los totales
inventario_consolidado = {}

# Recorremos los diccionarios
for fila in lista_productos:
    nombre = fila['Nombres']
    cantidad = fila['Cantidad']
    
    # Si el producto ya está en el diccionario, le sumamos la cantidad
    if nombre in inventario_consolidado:
        inventario_consolidado[nombre] += cantidad
    # Si es la primera vez que aparece, lo registramos con su cantidad actual
    else:
        inventario_consolidado[nombre] = cantidad

print("\n=== STOCK TOTAL CONSOLIDADO (SIN DUPLICADOS) ===")
print(f"{'Producto':<12} | {'Total Unidades':<14}")
print("-" * 31)
for prod, total_cant in inventario_consolidado.items():
    print(f"{prod:<12} | {total_cant:<14}")

# EJEMPLO 5: Filtrar por múltiples criterios a la vez
# El método filtrar_dataset recorre de forma paralela las columnas y las funciones con un zip. 
# Esto significa que se puede aplicar más de un filtro en la misma ejecución. 
# En este ejemplo buscaremos productos que cumplan dos condiciones: que su nombre empiece con la letra "C" 
# y que haya 10 o menos unidades en stock.

tabla = LectorTabla(ruta="datos/productos.csv", tiene_encabezado=True)
tabla.leer_tabla()

# Definimos los criterios en listas paralelas como lo pide la función
columnas_filtros = ["Nombres", "Cantidad"]
funciones_filtros = [
    lambda nombre: nombre.startswith("C"),  # Condición 1: Que empiece con 'C'
    lambda cantidad: cantidad <= 10         # Condición 2: Stock bajo (<= 10)
]

# Aplicamos el método con ambos filtros a la vez
tabla.filtrar_dataset(columnas=columnas_filtros, funciones=funciones_filtros)

print("\n=== ALERTAS DE STOCK: PRODUCTOS CON 'C' CON STOCK BAJO (<= 10) ===")
if not tabla.dataset:
    print("No se encontraron productos que coincidan con los filtros.")
else:
    # Control de duplicados: Creamos un conjunto para registrar los nombres ya mostrados
    productos_ya_mostrados = set()

    for fila in tabla.dataset:
        nombre = fila['Nombres']
        cantidad = fila['Cantidad']
        
        # Si el nombre ya está en nuestro registro, 'continue' salta a la siguiente fila sin imprimir nada
        if nombre in productos_ya_mostrados:
            continue
            
        # Si es la primera vez que aparece, lo agregamos al registro y mostramos la alerta
        productos_ya_mostrados.add(nombre)
        print(f"⚠️ ¡Alerta! El producto '{nombre:<10}' está con stock bajo. Stock actual: {cantidad}")