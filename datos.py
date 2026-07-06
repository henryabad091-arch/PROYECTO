
# FACTURA PRO — DATOS.PY
# Aquí estan los vectores de datos que usan todos los módulos.

#Matriz para los Inventario [nombre, stock]
inventario = []

#Matriz para los Reportes [fecha, tipo, contraparte, producto, cantidad, total]
reportes = []

#Matriz para las Facturas [numero, fecha, cliente, cedula, subtotal, iva, total]
facturas = []

#Contador de número de factura
numero_factura = [1]

#Dinero disponible del negocio.
caja_actual = [0.0]
caja_iniciada = [False]