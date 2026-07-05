# ============================================================
# FACTURA PRO — REPORTES.PY
# Funciones para registrar y consultar movimientos.
# ============================================================

import datos


def registrar_movimiento(fecha, tipo, contraparte, producto, cantidad, total):
    """
    Guarda un movimiento (venta o compra) en el vector de reportes.
    """
    datos.reportes.append([
        fecha,
        tipo,
        contraparte,
        producto,
        cantidad,
        round(float(total), 2)
    ])


def obtener_reportes(filtro="todos"):
    """
    Devuelve los movimientos según el filtro: 'todos', 'venta' o 'compra'.
    También calcula el total acumulado.
    """
    if filtro == "venta":
        lista = [r for r in datos.reportes if r[1] == "Venta"]
    elif filtro == "compra":
        lista = [r for r in datos.reportes if r[1] == "Compra"]
    else:
        lista = datos.reportes

    movimientos = [
        {
            "fecha":        r[0],
            "tipo":         r[1],
            "contraparte":  r[2],
            "producto":     r[3],
            "cantidad":     r[4],
            "total":        r[5],
        }
        for r in lista
    ]

    total_acumulado = round(sum(r[5] for r in lista), 2)

    return {"movimientos": movimientos, "total": total_acumulado}
