# FACTURA PRO — CAJA.PY
# Controla el dinero disponible del negocio

import datos
 

#FUNCIONES PARA INICIAR Y REINICIAR LA CAJA
def iniciar_caja(monto):

    #Define el capital inicial con el que arranca el negocio.
    if datos.caja_iniciada[0]:
        return {"ok": False, "error": "La caja ya fue iniciada."}
    
    try:
        monto = float(monto)
    except (TypeError, ValueError):
        return {"ok": False, "error": "El monto inicial no es válido."}
 
    if monto < 0:
        return {"ok": False, "error": "El monto inicial no puede ser negativo."}
 
    datos.caja_actual[0] = monto
    datos.caja_iniciada[0] = True
 
    return {"ok": True, "caja": round(datos.caja_actual[0], 2)}
 

def reiniciar_caja(monto):
    try:
        monto = float(monto)
    except (TypeError, ValueError):
        return {"ok": False, "error": "El monto inicial no es válido."}
 
    if monto < 0:
        return {"ok": False, "error": "El monto inicial no puede ser negativo."}
 
    datos.caja_actual[0] = monto
    datos.caja_iniciada[0] = True
 
    return {"ok": True, "caja": round(datos.caja_actual[0], 2)}
 
#FUNCIONES PARA SUMAR Y RESTAR DINERO DE LA CAJA
def sumar_dinero(monto):
    datos.caja_actual[0] += monto
 
def restar_dinero(monto):
    datos.caja_actual[0] -= monto

def hay_fondos_suficientes(monto):
    return datos.caja_actual[0] >= monto

def obtener_caja():
    return {
        "caja":     round(datos.caja_actual[0], 2),
        "iniciada": datos.caja_iniciada[0],
    }