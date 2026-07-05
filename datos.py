# ============================================================
# FACTURA PRO — DATOS.PY
# Aquí viven los vectores de datos que usan todos los módulos.
# Es el único lugar donde se guardan los datos en memoria.
# ============================================================

# Inventario: cada elemento es [nombre, stock]
inventario = []

# Reportes: cada elemento es [fecha, tipo, contraparte, producto, cantidad, total]
reportes = []

# Facturas emitidas: cada elemento es [numero, fecha, cliente, cedula, subtotal, iva, total]
facturas = []

# Contador de número de factura
numero_factura = [1]
