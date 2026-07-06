# FACTURA PRO — COMPRAS.PY
# Toda la lógica para registrar una compra a un proveedor:
# validar datos, calcular totales y actualizar el inventario.
 
import datetime
import numpy as np
 
import inventario
import reportes
import caja
import datos

#FUNCIONES PARA OBTENER LA FECHA
def obtener_fecha_hoy():

    #Devuelve la fecha de hoy en formato DD/MM/AAAA.
    return datetime.date.today().strftime("%d/%m/%Y")
 
#FUNCION PRINCIPAL PARA REGISTRAR UNA COMPRA
def registrar_compra(fecha, proveedor, productos_in):

    # Usar fecha de hoy si no se ingresó ninguna
    if not fecha:
        fecha = obtener_fecha_hoy()
 
    # El proveedor no puede estar vacío
    if not proveedor or proveedor.strip() == "":
        return {"ok": False, "error": "El nombre del proveedor no puede estar vacío."}
 
    # Verificar que haya productos
    if len(productos_in) == 0:
        return {"ok": False, "error": "No se ingresaron productos."}
 
    #MATRIZ PARA VALIDAR CADA PRODUCTO
    productos_validos = []
 
    for p in productos_in:
        nombre = (p.get("nombre") or "").strip()
 
        if nombre == "":
            return {"ok": False, "error": "El nombre del producto no puede estar vacío."}
 
        try:
            cantidad = int(p.get("cantidad"))
            valor    = float(p.get("valor"))
        except (TypeError, ValueError):
            return {"ok": False, "error": f"Datos inválidos para '{nombre}'."}
 
        if cantidad <= 0:
            return {"ok": False, "error": f"Cantidad inválida para '{nombre}'."}
 
        productos_validos.append([nombre, cantidad, valor])
 
    #CALCULAR TOTALES CON NUMPY
    cantidades= np.array([f[1] for f in productos_validos])
    valores = np.array([f[2] for f in productos_validos])
    subtotales_fila = cantidades * valores
    total_compra= float(np.sum(subtotales_fila))
    if not caja.hay_fondos_suficientes(total_compra):
        return {
            "ok": False,
            "error": f"    Fondos insuficientes    ."
        }
 
    #ACTUALIZAR INVENTARIO Y REGISTRAR EN REPORTES
    detalle = []
    for i, fila in enumerate(productos_validos):
        inventario.sumar_stock(fila[0], fila[1])
        reportes.registrar_movimiento(fecha, "Compra", proveedor, fila[0], fila[1], subtotales_fila[i])
        detalle.append({
            "producto": fila[0],
            "cantidad": fila[1],
            "valor":    fila[2],
            "subtotal": round(float(subtotales_fila[i]), 2),
        })
 
    #ACTUALIZAR LA CAJA
    caja.restar_dinero(total_compra)
 
    return {
        "ok":        True,
        "fecha":     fecha,
        "proveedor": proveedor,
        "productos": detalle,
        "total":     round(total_compra, 2),
        "caja":      round(caja.obtener_caja()["caja"], 2),
    }
 