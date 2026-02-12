# Erp_Minimarket
Desarrollo de un ERP diseñado específicamente para minimarket estos almacenes de barrio que buscan la organización de que serian las áreas del inventario y contabilidad, atreves de una plataforma web desarrollada en Python principalmente con el framework de DJANGO, HTML, CSS, BOOTSTRAP y AJAX. Pretendiendo generar una interfaz intuitiva para dueños de negocios de mayores edades.
Este proyecto esta planificado para ir escalando en las tecnologias que van surgiendo con el paso del tiempo.

---

## Tecnologías Utilizadas
- **Backend:** Django REST Framework  
- **Frontend:** Templates HTML, CSS, AJAX, Bootstrap  
- **Base de Datos:** MySQL

---

## Aplicaciones del Sistema
- **Empresa**
- **Usuarios**
- **Clientes**
- **Proveedores**
- **Contabilidad**
- **Compra**
- **Venta**
- **Inventario**

---

## Funcionalidades Generales

### Gestión de Compras
Integra las aplicaciones **Compra**, **Inventario**, **Empresa**, **Proveedores**, **Usuarios** y **Contabilidad**.  
Permite registrar compras de productos, actualizando automáticamente el inventario y los movimientos de caja. Opcionalmente, puede obtener información del proveedor mediante la **API del SII** o ingresarse manualmente para registrar gastos con o sin boleta de comercios menores.  
El sistema genera automáticamente los documentos correspondientes (boletas, facturas, notas de débito o crédito) y asocia la transacción con el usuario responsable.

### Gestión de Ventas
Involucra las aplicaciones **Venta**, **Inventario**, **Empresa**, **Clientes**, **Usuarios** y **Contabilidad**.  
Actualiza las existencias del inventario y los movimientos de caja al registrar una venta. De manera escalable, se prevé la integración con sistemas de pago electrónicos (tarjetas de crédito/débito) y reconocimiento de productos mediante cámara.  
Por ahora, la identificación de productos se realiza a través de código de barras con lector láser. Cada transacción se vincula automáticamente con el vendedor, y es posible registrar clientes para seguimiento y análisis de preferencias.

### CRUD Básico
Permite la gestión de datos principales: información de empresa, usuarios (con roles como vendedor, administrador o supervisor), proveedores y clientes.  
El sistema puede operar de forma completamente independiente, sin depender de APIs externas, garantizando autonomía y flexibilidad ante posibles fallos en la transferencia de datos.

### Gestión Contable y de Incidencias
La aplicación de **Contabilidad** permite registrar pérdidas o incidencias como mermas, robos o extravíos de mercancías, realizando los ajustes pertinentes en el inventario y la contabilidad general.

### Dashboards e Informes
Incluye paneles predefinidos que presentan datos provenientes de las aplicaciones de **Compra**, **Venta** e **Inventario**, con el objetivo de facilitar la toma de decisiones mediante análisis visual y estadísticas en tiempo real.

---

## Planes de Escalabilidad
- Incorporar **lector de facturas** (imagen, PDF o electrónica) para registro automatizado.  
- Integrar **reconocimiento de productos por cámara** para control de seguridad y eficiencia.  
- Implementar **API del SII** para la gestión automática de datos de proveedores.  
- Desarrollar **API de conexión con dispositivos de cobro** (MovilPOS y otros sistemas de pago).

---

### Autor
Desarrollado con **Django** y **Django REST Framework** como parte de un sistema integral de gestión empresarial.