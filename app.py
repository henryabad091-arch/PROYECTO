# FACTURA PRO — APP.PY

# FLASK puente entre el navegador y los módulos .py.
from flask import Flask, jsonify, request

# Módulos de lógica de negocio
import facturas
import compras
import inventario
import reportes
import credenciales

app = Flask(__name__, static_folder=".", static_url_path="")


#SERVIR EL FRONTEND
@app.route("/")
def home():
    return app.send_static_file("index.html")


#LOGIN
@app.route("/api/login", methods=["POST"])
def api_login():
    datos     = request.get_json(force=True) or {}
    usuario   = (datos.get("usuario")   or "").strip()
    contrasena = (datos.get("contrasena") or "").strip()

    if usuario == credenciales.USUARIO_VALIDO and contrasena == credenciales.PASSWORD_VALIDO:
        return jsonify(ok=True)

    return jsonify(ok=False, error="Usuario o contraseña incorrectos."), 401


#INVENTARIO
@app.route("/api/inventario", methods=["GET"])
def api_inventario():
    resultado = inventario.obtener_inventario()
    return jsonify(resultado)


#FACTURAR
@app.route("/api/facturar", methods=["POST"])
def api_facturar():
    datos = request.get_json(force=True) or {}

    resultado = facturas.generar_factura(
        fecha           = (datos.get("fecha")    or "").strip(),
        nombre_cliente  = (datos.get("nombre")   or "").strip(),
        cedula_cliente  = (datos.get("cedula")   or "").strip(),
        productos_in    =  datos.get("productos") or [],
    )

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado)

#COMPRAR
@app.route("/api/comprar", methods=["POST"])
def api_comprar():
    datos = request.get_json(force=True) or {}

    resultado = compras.registrar_compra(
        fecha= (datos.get("fecha")      or "").strip(),
        proveedor= (datos.get("proveedor")  or "").strip(),
        productos_in =  datos.get("productos")  or [],
    )

    if not resultado["ok"]:
        return jsonify(resultado), 400

    return jsonify(resultado)


#REPORTES
@app.route("/api/reportes", methods=["GET"])
def api_reportes():
    filtro    = request.args.get("filtro", "todos")
    resultado = reportes.obtener_reportes(filtro)
    return jsonify(resultado)


#PUNTO DE ENTRADA
if __name__ == "__main__":
    print(" ")
    print("=" * 55)
    print("   FACTURA PRO corriendo en http://127.0.0.1:5000")
    print("=" * 55)
    app.run(debug=True)
