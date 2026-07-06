# FACTURA PRO — FACTURAS.PY
# Toda la lógica para generar una factura:
# validar productos, calcular totales y guardar la factura.
 
import datetime
import numpy as np
 
import datos
import inventario
import reportes
import caja
 
#FUNCIONES PARA OBTENER LA FECHA
def obtener_fecha_hoy():
    #Devuelve la fecha de hoy en #formato DD/MM/AAAA.
    return datetime.date.today().strftime("%d/%m/%Y")
 
#FUNCION PRINCIPAL PARA GENERAR UNA FACTURA
def generar_factura(fecha, nombre_cliente, cedula_cliente, productos_in):

    # Usar fecha de hoy si no se ingresó ninguna
    if not fecha:
        fecha = obtener_fecha_hoy()
 
    # Usar "CONSUMIDOR FINAL" si no hay nombre
    if not nombre_cliente:
        nombre_cliente = "CONSUMIDOR FINAL"
 
    if not cedula_cliente:
        cedula_cliente = "-"
 
    # Verificar que haya productos
    if len(productos_in) == 0:
        return {"ok": False, "error": "No se ingresaron productos."}
 
    #VALIDAR CADA PRODUCTO
    acumulado = {}        # cuánto se lleva de cada producto en esta factura

    #Matriz para los productos de la factura [nombre, cantidad, precio, iva]
    productos_validos = []
    
    #Verificar que los productos existan en el inventario y que haya stock suficiente
    for p in productos_in:
        nombre   = (p.get("nombre") or "").strip()
        try:
            cantidad = int(p.get("cantidad"))
            precio   = float(p.get("precio"))
            iva      = float(p.get("iva"))
        except (TypeError, ValueError):
            return {"ok": False, "error": f"Datos inválidos para '{nombre}'."}
 
        if cantidad <= 0:
            return {"ok": False, "error": f"Cantidad inválida para '{nombre}'."}
 
        # El producto debe existir en el inventario
        idx = inventario.buscar_producto(nombre)
        if idx == -1:
            return {"ok": False, "error": f"'{nombre}' no existe en el inventario."}
 
        # No superar el stock disponible
        ya_agregado      = acumulado.get(nombre.lower(), 0)
        stock_disponible = datos.inventario[idx][1] - ya_agregado
 
        if cantidad > stock_disponible:
            return {
                "ok": False,
                "error": f"Stock insuficiente de '{nombre}'. Disponible: {max(stock_disponible, 0)} unidad(es)."
            }
 
        acumulado[nombre.lower()] = ya_agregado + cantidad
        productos_validos.append([nombre, cantidad, precio, iva])
 
    #CALCULAR TOTALES CON NUMPY
    cantidades= np.array([f[1] for f in productos_validos])
    precios= np.array([f[2] for f in productos_validos])
    ivas= np.array([f[3] for f in productos_validos])
    
    #Calcular subtotales, IVA y totales por fila
    subtotales_fila = cantidades * precios
    iva_fila= subtotales_fila * (ivas / 100)
    totales_fila= subtotales_fila + iva_fila
     
    #Calcular totales generales
    subtotal_base = float(np.sum(subtotales_fila))
    total_iva= float(np.sum(iva_fila))
    total_final= subtotal_base + total_iva
 
    #NÚMERO DE FACTURA
    num = f"001-001-{str(datos.numero_factura[0]).zfill(9)}"
    datos.numero_factura[0] += 1
 
    # GUARDAR FACTURA
    datos.facturas.append([
        num, fecha, nombre_cliente, cedula_cliente,
        round(subtotal_base, 2), round(total_iva, 2), round(total_final, 2)
    ])
 
    # ACTUALIZAR INVENTARIO
    detalle = []
    for i, fila in enumerate(productos_validos):
        inventario.restar_stock(fila[0], fila[1])
        reportes.registrar_movimiento(fecha, "Venta", nombre_cliente, fila[0], fila[1], totales_fila[i])
        detalle.append({
            "producto": fila[0],
            "cantidad": fila[1],
            "precio": fila[2],
            "iva": fila[3],
            "subtotal":round(float(subtotales_fila[i]), 2),
            "total": round(float(totales_fila[i]), 2),
        })
 
    #ACTUALIZAR LA CAJA
    caja.sumar_dinero(total_final)
 

    return {
        "ok": True,
        "numero":num,
        "fecha": fecha,
        "cliente": nombre_cliente,
        "cedula": cedula_cliente,
        "productos":detalle,
        "subtotal":round(subtotal_base, 2),
        "iva": round(total_iva, 2),
        "total":round(total_final, 2),
        "caja":round(datos.caja_actual[0], 2),
    }