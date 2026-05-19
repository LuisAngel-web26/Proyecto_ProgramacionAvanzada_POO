# 📖 Guía de Usuario - Sistema Médico Veterinario Huellitas
> **Manual de Usuario Paso a Paso para la Operación del Sistema**

Bienvenido a la **Guía de Usuario oficial de Huellitas**. Este documento está diseñado para acompañar al personal clínico y administrativo en el uso eficiente de todas las funciones del sistema. Siga las instrucciones detalladas a continuación para realizar operaciones comerciales y médicas fluidas y libres de errores.

---

## 📌 Índice de Contenidos
1. [Acceso al Sistema (Login)](#1-acceso-al-sistema-login)
2. [Gestión de Clientes (Propietarios)](#2-gestión-de-clientes-propietarios)
3. [Expedientes de Mascotas (Pacientes)](#3-expedientes-de-mascotas-pacientes)
4. [Agenda y Citas Médicas](#4-agenda-y-citas-médicas)
5. [Consultorio Médico y Recetas (Veterinario)](#5-consultorio-médico-y-recetas-veterinario)
6. [Catálogo e Inventario de Insumos](#6-catálogo-e-inventario-de-insumos)
7. [Módulo de Caja y Facturación (Punto de Venta)](#7-módulo-de-caja-y-facturación-punto-de-venta)
8. [Administración de Personal (Empleados)](#8-administración-de-personal-empleados)
9. [Reportes y Gráficos Estadísticos](#9-reportes-y-gráficos-estadísticos)
10. [Conectividad, Asistente de Razas e Historiales](#10-conectividad-asistente-de-razas-e-historiales)

---

## 1. Acceso al Sistema (Login)

Al abrir la aplicación, se presentará una pantalla de acceso con diseño elegante sobre una imagen de fondo.

1.  **Ingresar Credenciales:**
    *   Escriba su nombre de usuario en el campo **USUARIO**.
    *   Escriba su contraseña secreta en el campo **CONTRASEÑA** (los caracteres se ocultarán automáticamente).
2.  **Iniciar Sesión:**
    *   Haga clic en el botón verde **INICIAR SESIÓN** o presione la tecla *Enter*.
    *   Si los datos son correctos, ingresará al **Dashboard (Panel de Control)** y se adaptará el menú lateral (sidebar) según su rol de usuario asignado.

> 💡 **Nota:** Si las credenciales no coinciden, el sistema mostrará un mensaje de error advirtiendo el acceso denegado.

---

## 2. Gestión de Clientes (Propietarios)

Antes de registrar una mascota, es indispensable dar de alta a su dueño para establecer la relación de pertenencia.

1.  **Navegación:** En el menú lateral izquierdo, haga clic en la opción **Propietarios**.
2.  **Registrar Nuevo Propietario:**
    *   Ubique la tarjeta superior titulada **👥 REGISTRO DE NUEVO PROPIETARIO**.
    *   Escriba los datos obligatorios marcados con un asterisco (`*`): **DNI** (Identificación única) y **Nombre completo**.
    *   Ingrese los campos opcionales pero muy recomendados: **Teléfono** y **Correo** electrónico.
    *   Haga clic en el botón verde **💾 GUARDAR PROPIETARIO**.
3.  **Visualización:** El nuevo cliente se agregará de inmediato a la tabla inferior y se almacenará en los archivos CSV.

---

## 3. Expedientes de Mascotas (Pacientes)

Una vez que el dueño está registrado, puede dar de alta a su mascota en la base de datos de expedientes médicos.

1.  **Navegación:** En el menú lateral izquierdo, seleccione la opción **Pacientes**.
2.  **Registrar Nueva Mascota:**
    *   Ubique el formulario superior **REGISTRO DE PACIENTE**.
    *   Rellene los campos obligatorios: **Nombre** y **Especie** (ej: Canino, Felino).
    *   Ingrese la **Raza** de la mascota y su **Peso (kg)** actual.
    *   En el campo **DNI Dueño**, escriba con precisión el DNI exacto del cliente que dio de alta en el paso anterior.
    *   Haga clic en el botón **REGISTRAR MASCOTA**.
3.  **Vinculación:** El sistema buscará el DNI del propietario. Si lo encuentra, vinculará la mascota automáticamente a su cuenta. En caso de no encontrarlo, registrará a la mascota sin dueño asignado, emitiendo una advertencia.
4.  **Expedientes:** Se asignará automáticamente un código de paciente único (ej: `1001`, `1002`) y aparecerá en la tabla histórica.

---

## 4. Agenda y Citas Médicas

Este módulo administra la planificación de visitas en la clínica.

1.  **Navegación:** Seleccione la opción **Citas** en el menú lateral.
2.  **Agendar Turno:**
    *   Complete los campos del formulario superior **AGENDAR NUEVA CITA**.
    *   Escriba el **ID Paciente** de la mascota (ej: `1001`).
    *   Defina la **Fecha** en formato `AAAA-MM-DD` (ej: `2026-05-20`). El sistema auto-rellena la fecha del día actual por comodidad.
    *   Establezca la **Hora** en formato militar `HH:MM` (ej: `10:30`, `16:00`).
    *   Describa el **Motivo** breve de la consulta (ej: "Vacunación Sextuple", "Dolor estomacal").
    *   Haga clic en el botón verde **AGENDAR**.
3.  **Control de Estados:**
    *   Seleccione una cita de la tabla interactiva inferior.
    *   Puede cancelarla haciendo clic en el botón rojo **CANCELAR SELECCIONADA** en la parte inferior izquierda.
    *   El veterinario marcará automáticamente la cita como **Completada** al finalizar su consulta médica en el consultorio.

---

## 5. Consultorio Médico y Recetas (Veterinario)

*Módulo exclusivo para usuarios con rol de **Veterinario**.* Permite realizar la atención clínica diagnóstica de las mascotas en tiempo real.

1.  **Navegación:** Diríjase a la pestaña **Consultas**.
2.  **Selección de Paciente:**
    *   La tabla izquierda muestra únicamente las citas programadas que están en estado **Pendiente** o **Confirmada**.
    *   Haga clic sobre una cita. La sección superior derecha mostrará inmediatamente el resumen clínico de la mascota (Nombre, especie, raza, peso registrado anteriormente y el motivo).
3.  **Evaluación Física y Signos:**
    *   Revise y actualice el **Peso Actual** en kilogramos.
    *   Mida y capture la **Temperatura (°C)** del animal (ej: `38.5`).
    *   Ingrese la **Frecuencia Cardíaca** en latidos por minuto (`lpm`).
4.  **Diagnóstico y Tratamiento:**
    *   Escriba en el campo de texto de **Diagnóstico** las conclusiones de la exploración (ej: "Infección estomacal aguda por ingesta de alimento descompuesto").
    *   Detalle las pautas terapéuticas en el campo **Tratamiento** (ej: "Dieta blanda por 48 horas y tratamiento con antibiótico").
5.  **Generación de Receta Médica:**
    *   En el marco inferior **RECETA / MEDICAMENTOS**, despliegue la lista de **Insumo**.
    *   Seleccione el medicamento requerido (el menú muestra el stock disponible actual).
    *   Indique la **Cantidad** de unidades prescritas.
    *   Haga clic en el botón verde **Añadir**. El medicamento aparecerá en el cuadro de texto inferior de la receta. Repita para prescribir múltiples fármacos.
6.  **Finalizar Consulta:**
    *   Haga clic en el botón **GUARDAR CONSULTA Y COMPLETAR**.
    *   **¿Qué hace el sistema automáticamente?**
        *   Crea una consulta médica con un código de folio clínico único (ej: `CON-2514`).
        *   Vincula la consulta al expediente histórico de la mascota.
        *   Actualiza el peso actual del animal de forma global.
        *   Marca la cita seleccionada como **Completada**.
        *   Genera y abre una ventana emergente premium con el formato imprimible de la **RECETA MÉDICA** detallando el diagnóstico y las tomas.
        *   Guarda los datos de forma permanente en los archivos locales CSV.

---

## 6. Catálogo e Inventario de Insumos

Módulo comercial para el abastecimiento y actualización de precios de la clínica.

1.  **Navegación:** Ingrese a la opción **Inventario** desde el menú lateral.
2.  **Registro de Nuevos Suministros:**
    *   En la sección superior **NUEVO PRODUCTO**, defina un **ID** único (ej: `MED-010`), **Nombre** del insumo, **Stock** inicial (unidades enteras) y **Precio** de venta comercial.
    *   Haga clic en el botón **AGREGAR**.
3.  **Actualización Rápida de Stock:**
    *   Haga clic en cualquier producto de la tabla inferior interactiva.
    *   Ingrese la cantidad total en el campo **ACTUALIZAR STOCK DEL SELECCIONADO**.
    *   Haga clic en **GUARDAR** para registrar el cambio de existencias.
4.  **Buscador Inteligente:**
    *   Use la barra de texto superior **Buscar** para filtrar insumos por nombre o ID en tiempo real a medida que escribe.
5.  **Alertas Visuales:**
    *   Cualquier producto cuyo stock sea inferior a 5 unidades se resaltará automáticamente en color **rojo suave** con texto rojo destacado para indicar desabastecimiento crítico.

---

## 7. Módulo de Caja y Facturación (Punto de Venta)

Módulo financiero para realizar la venta de insumos y el cobro integrado de servicios médicos.

1.  **Navegación:** Diríjase al menú lateral y haga clic en **Facturación**.
2.  **Integración Directa con Recetas del Veterinario (Método Automatizado):**
    *   En la parte superior izquierda, localice el menú desplegable **Receta Médica**.
    *   Este menú contiene la lista de todas las consultas médicas del día que tienen recetas de medicamentos pendientes de cobro.
    *   Seleccione la consulta del paciente correspondiente.
    *   Haga clic en el botón **⚡ CARGAR RECETA EN CARRITO**.
    *   **¿Qué ocurre?**
        *   El sistema carga el DNI del propietario de la mascota de forma automática en el campo cliente.
        *   Inserta en la tabla del carrito todos los medicamentos prescritos por el doctor ajustando la cantidad en base al stock físico actual.
        *   Agrega de forma dinámica la tasa estándar del **Servicio: Consulta Médica Veterinaria** ($250.00 pesos).
3.  **Carga Manual de Productos (Venta libre):**
    *   Escriba el nombre del insumo en el buscador manual.
    *   Seleccione el producto de la lista interactiva.
    *   Haga clic en **🛒 AÑADIR SELECCIONADO**. Se sumará al carrito de compras sumando una unidad por cada clic.
4.  **Proceso de Cobro:**
    *   Revise los cálculos comerciales actualizados automáticamente en el recuadro verde de la derecha (**Subtotal**, **16% de IVA** y el **TOTAL** a pagar).
    *   Confirme que el **DNI Cliente / Propietario** esté completo en el campo de texto.
    *   Seleccione el **Método de Pago** utilizado por el cliente (Efectivo, Tarjeta o Transferencia).
    *   Haga clic en el gran botón verde **💵 GENERAR VENTA Y TICKET**.
5.  **Ticket de Compra:**
    *   El sistema validará la transacción, disminuirá definitivamente las unidades vendidas del stock del inventario general, guardará los registros financieros y abrirá en pantalla un **Ticket de Venta** profesional en letra Courier diseñado para ser entregado al cliente.
6.  **Vaciar Carrito:** Si desea anular la carga actual, presione el botón rojo **🗑️ VACIAR CARRITO**.

---

## 8. Administración de Personal (Empleados)

*Módulo exclusivo para usuarios con rol de **Administrador**.* Permite gestionar el equipo de trabajo interno.

1.  **Navegación:** Ingrese a la opción **Personal** en el sidebar lateral.
2.  **Registrar Empleado:**
    *   Complete los campos básicos requeridos en el panel derecho **NUEVO EMPLEADO**: **ID Usuario** (clave de acceso), **Nombre** del trabajador, **Contraseña** de acceso al sistema y **Rol** (Administrador o Veterinario).
    *   **Si selecciona "Administrador":** Complete los campos inferiores de nivel de seguridad y departamento.
    *   **Si selecciona "Veterinario":** Ingrese la **Cédula Prof.** y la **Especialidad**.
3.  **Validación de Seguridad:**
    *   Al registrar un *Veterinario*, el sistema valida rigurosamente que la **Cédula Profesional** conste únicamente de **7 u 8 dígitos numéricos**. Si introduce letras o longitudes incorrectas, la aplicación impedirá el registro para garantizar la legitimidad profesional.
4.  **Haga clic en** **REGISTRAR EMPLEADO** para guardar al nuevo miembro del equipo.

---

## 9. Reportes y Gráficos Estadísticos

*Módulo exclusivo para usuarios con rol de **Administrador**.* Proporciona herramientas avanzadas de análisis empresarial.

1.  **Navegación:** Ingrese a la pestaña **Reportes**.
2.  **Consultar Gráfica de Visitas:**
    *   Haga clic en el botón **📊 VER VISITAS POR MES**.
    *   Se dibujará e incrustará de forma premium una gráfica de barras de Matplotlib que muestra el volumen de citas médicas por día/mes atendidas en la veterinaria.
3.  **Consultar Gráfica de Ventas e Ingresos:**
    *   Haga clic en el botón **📈 REPORTE DE VENTAS**.
    *   Se generará un gráfico de área sombreada estilizado que representa el comportamiento financiero de ingresos totales generados en caja por día de forma continua. Cada nodo del gráfico tiene una etiqueta flotante con el importe exacto acumulado (ej: `$4,520.50`).

---

## 10. Conectividad, Asistente de Razas e Historiales

Este módulo de herramientas se adapta según el rol que haya iniciado sesión, actuando como un centro de conectividad.

1.  **Navegación:** Haga clic en la pestaña **Conectividad & APIs** (también llamada *Configuracion*).
2.  **Asistente de Razas Veterinarias (Ambos Roles):**
    *   Permite a médicos y administradores consultar especificaciones de cuidado sobre razas de perros y gatos.
    *   Seleccione una raza de la lista (ej: *Golden Retriever*, *Gato Siamés*).
    *   Haga clic en **🔍 CONSULTAR**.
    *   La pantalla mostrará un cargador de progreso (UX spinner) simulando la consulta en tiempo real a una API externa (The Dog / Cat API). Tras un segundo, desplegará la información detallada del animal: grupo, esperanza de vida, temperamento y las **pautas de cuidados clínicos y veterinarios recomendados** indispensables para guiar al médico en la consulta.
3.  **Agregar y Editar Razas (Administrador):**
    *   Los administradores pueden enriquecer la enciclopedia local haciendo clic en **➕ AGREGAR** o editando la información con **✏️ EDITAR**.
    *   Se abrirá un formulario dinámico que guardará los cambios permanentemente en `data/razas.csv`.
4.  **Supervisión de Auditoría Administrativa (Administrador):**
    *   Los administradores visualizarán a la derecha accesos directos de control administrativo:
        *   **📋 VER RECETAS DADAS:** Despliega una ventana interactiva de gran tamaño para buscar, filtrar y auditar por texto libre todas las consultas médicas diagnósticas registradas que generaron una receta en la clínica.
        *   **📅 VER CITAS REGISTRADAS:** Abre una tabla completa que detalla el historial de todas las citas agendadas, coloreando visualmente cada fila según su estado actual (Amarillo suave para *Pendiente*, Verde suave para *Completada* y Rojo suave para *Cancelada*).
