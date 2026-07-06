/* FACTURA PRO — SCRIPT.JS
   Conecta los botones de index.html con el servidor Flask (app.py)

/* Estado temporal en el navegador: lo que el usuario
   va agregando a la factura/compra ANTES de enviarla
   al servidor. */
let productosFactura = [];
let productosCompra = [];

/*NAVEGACIÓN ENTRE PANTALLAS */
function mostrarPantalla(id) {
  document.querySelectorAll(".pantalla").forEach((p) => p.classList.remove("activa"));
  document.getElementById(id).classList.add("activa");

  const pantallasConCaja = [
    "pantalla-menu",
    "pantalla-factura",
    "pantalla-compra",
    "pantalla-inventario",
    "pantalla-reportes",
  ];
  if (pantallasConCaja.includes(id)) cargarCaja();

  if (id === "pantalla-inventario") cargarInventario();
  if (id === "pantalla-reportes") cargarReportes("todos");
  if (id === "pantalla-menu") actualizarEstadoMenu();

  window.scrollTo(0, 0);
}

/* LOGIN*/
async function verificarLogin() {
  const usuario = document.getElementById("input-usuario").value;
  const contrasena = document.getElementById("input-password").value;
  const errorBox = document.getElementById("login-error");

  try {
    const resp = await fetch(`${API}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ usuario, contrasena }),
    });
    const data = await resp.json();

    if (data.ok) {
      errorBox.classList.add("oculto");
      document.getElementById("input-usuario").value = "";
      document.getElementById("input-password").value = "";
      mostrarPantalla("pantalla-menu");
    } else {
      errorBox.textContent = data.error || "Usuario o contraseña incorrectos.";
      errorBox.classList.remove("oculto");
    }
  } catch (e) {
    errorBox.textContent = "No se pudo conectar con el servidor. ¿Está corriendo app.py?";
    errorBox.classList.remove("oculto");
  }
}

function cerrarSesion() {
  mostrarPantalla("pantalla-inicio");
}

/* MENÚ PRINCIPAL */
async function actualizarEstadoMenu() {
  const card = document.getElementById("menu-card-facturar");
  try {
    const resp = await fetch(`${API}/inventario`);
    const data = await resp.json();

    if (data.length === 0) {
      card.classList.add("deshabilitado");
      card.onclick = null;
    } else {
      card.classList.remove("deshabilitado");
      card.onclick = () => mostrarPantalla("pantalla-factura");
    }
  } catch (e) {
    /* si falla la conexión, dejamos la tarjeta como esté */
  }
}

/* FACTURA*/
function toggleDatosCliente() {
  const tipo = document.getElementById("fac-tipo").value;
  document.getElementById("bloque-datos-cliente").style.display =
    tipo === "final" ? "none" : "block";
}

function agregarProductoFactura() {
  const nombre = document.getElementById("fac-producto").value.trim();
  const cantidad = parseInt(document.getElementById("fac-cantidad").value, 10);
  const precio = parseFloat(document.getElementById("fac-precio").value);
  const iva = parseFloat(document.getElementById("fac-iva").value);

  if (!nombre) return alert("Ingresa el nombre del producto.");
  if (!cantidad || cantidad <= 0) return alert("Ingresa una cantidad válida.");
  if (isNaN(precio) || precio < 0) return alert("Ingresa un precio válido.");

  productosFactura.push({ nombre, cantidad, precio, iva });
  renderTablaFactura();

  document.getElementById("fac-producto").value = "";
  document.getElementById("fac-cantidad").value = "";
  document.getElementById("fac-precio").value = "";
  document.getElementById("fac-producto").focus();
}

function eliminarProductoFactura(i) {
  productosFactura.splice(i, 1);
  renderTablaFactura();
}

function renderTablaFactura() {
  const tbody = document.getElementById("body-productos-fac");
  const wrap = document.getElementById("tabla-productos-fac");

  if (productosFactura.length === 0) {
    wrap.classList.add("oculto");
    tbody.innerHTML = "";
    return;
  }

  wrap.classList.remove("oculto");
  tbody.innerHTML = productosFactura
    .map((p, i) => {
      const subtotal = p.cantidad * p.precio * (1 + p.iva / 100);
      return `<tr>
        <td>${i + 1}</td>
        <td>${p.nombre}</td>
        <td>${p.cantidad}</td>
        <td>$${p.precio.toFixed(2)}</td>
        <td>${p.iva}%</td>
        <td>$${subtotal.toFixed(2)}</td>
        <td><button class="btn-eliminar" onclick="eliminarProductoFactura(${i})">✕</button></td>
      </tr>`;
    })
    .join("");
}

async function generarFactura() {
  if (productosFactura.length === 0) return alert("Agrega al menos un producto.");

  const tipo = document.getElementById("fac-tipo").value;
  const payload = {
    fecha: document.getElementById("fac-fecha").value,
    nombre:
      tipo === "final" ? "CONSUMIDOR FINAL" : document.getElementById("fac-nombre").value,
    cedula: tipo === "final" ? "-" : document.getElementById("fac-cedula").value,
    productos: productosFactura,
  };

  try {
    const resp = await fetch(`${API}/facturar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await resp.json();

    if (!data.ok) return alert(data.error || "No se pudo generar la factura.");

    actualizarCajaDisplay(data.caja);
    mostrarFacturaGenerada(data);
  } catch (e) {
    alert("No se pudo conectar con el servidor. ¿Está corriendo app.py?");
  }
}

function mostrarFacturaGenerada(data) {
  document.querySelector("#pantalla-factura .seccion-formulario").classList.add("oculto");
  document.getElementById("vista-factura").classList.remove("oculto");

  document.getElementById("fac-numero").textContent = "#" + data.numero;
  document.getElementById("fac-fecha-display").textContent = data.fecha;
  document.getElementById("disp-nombre").textContent = data.cliente;
  document.getElementById("disp-cedula").textContent = data.cedula;

  document.getElementById("body-factura-final").innerHTML = data.productos
    .map(
      (p, i) => `<tr>
        <td>${i + 1}</td>
        <td>${p.producto}</td>
        <td>${p.cantidad}</td>
        <td>$${p.precio.toFixed(2)}</td>
        <td>${p.iva}%</td>
        <td>$${p.total.toFixed(2)}</td>
      </tr>`
    )
    .join("");

  document.getElementById("fac-subtotal").textContent = "$" + data.subtotal.toFixed(2);
  document.getElementById("fac-iva-total").textContent = "$" + data.iva.toFixed(2);
  document.getElementById("fac-total-final").textContent = "$" + data.total.toFixed(2);
}

function nuevaFactura() {
  productosFactura = [];
  renderTablaFactura();
  document.getElementById("fac-nombre").value = "";
  document.getElementById("fac-cedula").value = "";
  document.getElementById("fac-fecha").value = "";

  document.getElementById("vista-factura").classList.add("oculto");
  document.querySelector("#pantalla-factura .seccion-formulario").classList.remove("oculto");
}

/*REGISTRAR COMPRA*/
function agregarProductoCompra() {
  const nombre = document.getElementById("com-producto").value.trim();
  const cantidad = parseInt(document.getElementById("com-cantidad").value, 10);
  const valor = parseFloat(document.getElementById("com-valor").value);

  if (!nombre) return alert("Ingresa el nombre del producto.");
  if (!cantidad || cantidad <= 0) return alert("Ingresa una cantidad válida.");
  if (isNaN(valor) || valor < 0) return alert("Ingresa un valor válido.");

  productosCompra.push({ nombre, cantidad, valor });
  renderTablaCompra();

  document.getElementById("com-producto").value = "";
  document.getElementById("com-cantidad").value = "";
  document.getElementById("com-valor").value = "";
  document.getElementById("com-producto").focus();
}

function eliminarProductoCompra(i) {
  productosCompra.splice(i, 1);
  renderTablaCompra();
}

function renderTablaCompra() {
  const tbody = document.getElementById("body-productos-com");
  const wrap = document.getElementById("tabla-productos-com");

  if (productosCompra.length === 0) {
    wrap.classList.add("oculto");
    tbody.innerHTML = "";
    return;
  }

  wrap.classList.remove("oculto");
  tbody.innerHTML = productosCompra
    .map((p, i) => {
      const subtotal = p.cantidad * p.valor;
      return `<tr>
        <td>${i + 1}</td>
        <td>${p.nombre}</td>
        <td>${p.cantidad}</td>
        <td>$${p.valor.toFixed(2)}</td>
        <td>$${subtotal.toFixed(2)}</td>
        <td><button class="btn-eliminar" onclick="eliminarProductoCompra(${i})">✕</button></td>
      </tr>`;
    })
    .join("");
}

async function registrarCompra() {
  if (productosCompra.length === 0) return alert("Agrega al menos un producto.");

  const proveedor = document.getElementById("com-proveedor").value.trim();
  if (!proveedor) return alert("Ingresa el nombre del proveedor.");

  const payload = {
    fecha: document.getElementById("com-fecha").value,
    proveedor,
    productos: productosCompra,
  };

  try {
    const resp = await fetch(`${API}/comprar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await resp.json();

    if (!data.ok) return alert(data.error || "No se pudo registrar la compra.");

    actualizarCajaDisplay(data.caja);
    document.getElementById("com-exito").classList.remove("oculto");
  } catch (e) {
    alert("No se pudo conectar con el servidor. ¿Está corriendo app.py?");
  }
}

function nuevaCompra() {
  productosCompra = [];
  renderTablaCompra();
  document.getElementById("com-proveedor").value = "";
  document.getElementById("com-fecha").value = "";
  document.getElementById("com-exito").classList.add("oculto");
}

/* INVENTARIO */
async function cargarInventario() {
  const tbody = document.getElementById("body-inventario");
  const vacio = document.getElementById("inv-vacio");
  const tabla = document.getElementById("tabla-inventario");

  try {
    const resp = await fetch(`${API}/inventario`);
    const data = await resp.json();

    if (data.length === 0) {
      tabla.classList.add("oculto");
      vacio.textContent =
        "No hay productos en el inventario aún. Registra compras para comenzar.";
      vacio.classList.remove("oculto");
      return;
    }

    tabla.classList.remove("oculto");
    vacio.classList.add("oculto");

    const etiquetas = {
      disponible: '<span class="badge verde"> Disponible</span>',
      bajo: '<span class="badge naranja"> Stock bajo</span>',
      agotado: '<span class="badge rojo"> Agotado</span>',
    };

    tbody.innerHTML = data
      .map(
        (p, i) => `<tr>
          <td>${i + 1}</td>
          <td>${p.nombre}</td>
          <td>${p.stock}</td>
          <td>${etiquetas[p.estado]}</td>
        </tr>`
      )
      .join("");
  } catch (e) {
    tabla.classList.add("oculto");
    vacio.textContent = "No se pudo conectar con el servidor. ¿Está corriendo app.py?";
    vacio.classList.remove("oculto");
  }
}

/* REPORTES */
async function cargarReportes(filtro) {
  const tbody = document.getElementById("body-reportes");
  const vacio = document.getElementById("rep-vacio");
  const tabla = document.getElementById("tabla-reportes");

  try {
    const resp = await fetch(`${API}/reportes?filtro=${filtro}`);
    const data = await resp.json();

    if (data.movimientos.length === 0) {
      tabla.classList.add("oculto");
      vacio.textContent = "No hay movimientos registrados todavía.";
      vacio.classList.remove("oculto");
      return;
    }

    tabla.classList.remove("oculto");
    vacio.classList.add("oculto");

    tbody.innerHTML = data.movimientos
      .map(
        (r) => `<tr>
          <td>${r.fecha}</td>
          <td>${r.tipo}</td>
          <td>${r.contraparte}</td>
          <td>${r.producto}</td>
          <td>${r.cantidad}</td>
          <td>$${r.total.toFixed(2)}</td>
        </tr>`
      )
      .join("");
  } catch (e) {
    tabla.classList.add("oculto");
    vacio.textContent = "No se pudo conectar con el servidor. ¿Está corriendo app.py?";
    vacio.classList.remove("oculto");
  }
}

function filtrarReporte(tipo, btn) {
  document.querySelectorAll(".btn-filtro").forEach((b) => b.classList.remove("activo"));
  btn.classList.add("activo");
  cargarReportes(tipo);
}

/*CAJA (DINERO DEL NEGOCIO */
async function cargarCaja() {
  try {
    const resp = await fetch(`${API}/caja`);
    const data = await resp.json();

    actualizarCajaDisplay(data.caja);

    if (!data.iniciada) {
      document.getElementById("modal-caja").classList.remove("oculto");
    }
  } catch (e) {
    /* si falla la conexión, dejamos el valor como esté */
  }
}

function actualizarCajaDisplay(monto) {
  document.querySelectorAll(".caja-display").forEach((el) => {
    el.textContent = ` Caja: $${monto.toFixed(2)}`;
  });
}

async function iniciarCaja() {
  const input = document.getElementById("input-caja-inicial");
  const monto = parseFloat(input.value);

  if (isNaN(monto) || monto < 0) return alert("Ingresa un monto inicial válido.");

  try {
    const resp = await fetch(`${API}/caja/iniciar`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ monto }),
    });
    const data = await resp.json();

    if (!data.ok) return alert(data.error || "No se pudo iniciar la caja.");

    document.getElementById("modal-caja").classList.add("oculto");
    input.value = "";
    actualizarCajaDisplay(data.caja);
  } catch (e) {
    alert("No se pudo conectar con el servidor. ¿Está corriendo app.py?");
  }
}

/* ════════════════
   INICIALIZACIÓN
════════════════ */
document.addEventListener("DOMContentLoaded", () => {
  toggleDatosCliente();
});