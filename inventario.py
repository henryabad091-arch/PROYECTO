# FACTURA PRO — INVENTARIO.PY
# Funciones para buscar productos y actualizar el stock.

import datos

#FUNCIONES PARA BUSCAR PRODUCTOS
def buscar_producto(nombre):
    #Busca un producto en el inventario por nombre
    nombre_lower = nombre.lower()
    for i in range(len(datos.inventario)):
        if datos.inventario[i][0].lower() == nombre_lower:
            return i
    return -1

#FUNCIONES PARA ACTUALIZAR EL STOCK
def sumar_stock(nombre, cantidad):
    #Suma cantidad al stock de un producto.
    #Si el producto no existe, lo crea.
    idx = buscar_producto(nombre)
    if idx >= 0:
        datos.inventario[idx][1] += cantidad
    else:
        datos.inventario.append([nombre, cantidad])

#FUNCION PARA RESTAR EL STOCK
def restar_stock(nombre, cantidad):
    #Resta cantidad al stock de un producto.
    #No deja el stock en negativo
    idx = buscar_producto(nombre)
    if idx >= 0:
        datos.inventario[idx][1] -= cantidad
        if datos.inventario[idx][1] < 0:
            datos.inventario[idx][1] = 0

#FUNCION PARA OBTENER EL INVENTARIO
def obtener_inventario():
    #Matriz con el inventario y el estado de cada producto
    resultado = []
    for nombre, stock in datos.inventario:
        if stock > 10:
            estado = "disponible"
        elif stock > 0:
            estado = "bajo"
        else:
            estado = "agotado"
        resultado.append({"nombre": nombre, "stock": stock, "estado": estado})
    return resultado