# 🐾 Huellitas - Sistema Médico Veterinario
> **Sistema Profesional de Gestión Clínica, Expedientes, Inventario y Facturación**

Bienvenido a **Huellitas**, una aplicación de escritorio premium diseñada para la administración integral de clínicas veterinarias. Este software ha sido desarrollado bajo un paradigma robusto de **Programación Orientada a Objetos (POO)** en Python, combinando una interfaz gráfica de usuario moderna y estilizada mediante **Tkinter (ttk)**, persistencia de datos local transparente en archivos **CSV (Pandas)**, y capacidades avanzadas de análisis estadístico (**Matplotlib**).

---

## ✨ Características Principales

*   **Seguridad y Control de Acceso (RBAC):** Autenticación de usuarios diferenciando privilegios de **Administrador** y **Veterinario**.
*   **Gestión Integral de Expedientes:** Registro minucioso de mascotas (pacientes) y sus dueños (propietarios), manteniendo vinculaciones directas de pertenencia de 1 a N.
*   **Agenda Médica Dinámica:** Sistema completo de agendamiento y control de citas con actualización de estados en tiempo real (Pendiente, Confirmada, Cancelada, Completada).
*   **Consultorio Clínico Automatizado:** Permite al cuerpo médico registrar signos vitales (peso, temperatura, frecuencia cardíaca), diagnósticos y tratamientos, además de generar recetas médicas integradas al inventario.
*   **Punto de Venta e Integración de Recetas:** Módulo de cobro que vincula automáticamente las recetas del veterinario y las tasas de consulta médica a la caja registradora, disminuyendo el stock en tiempo real y generando tickets de venta profesionales imprimibles en pantalla.
*   **Inventario con Alertas de Stock:** Catálogo de insumos médicos con notificaciones visuales en color rojo (alertas) cuando los medicamentos o suministros caen por debajo del stock mínimo.
*   **Estadísticas y Análisis de Datos:** Gráficos estadísticos dinámicos (barras y áreas) que analizan las visitas de pacientes y los ingresos de caja acumulados por día de manera interactiva.
*   **API y Enciclopedia de Razas:** Un asistente de razas (perros y gatos) con pautas específicas de cuidados veterinarios, historial de recetas y citas generales.

---

## 🏛️ Arquitectura del Sistema

El sistema implementa una arquitectura desacoplada basada en el patrón de diseño **Controller-Model-View (MCV-like)**:
*   **Modelo (`clases.py`):** Define las clases puras de negocio y la lógica de manipulación de datos, incluyendo la persistencia y carga desde archivos CSV utilizando `pandas`.
*   **Vista y Controlador (`main.py`):** Implementa la interfaz gráfica mediante `Tkinter`. `AppHuellitas` funciona como el controlador global, administrando la navegación entre las diferentes vistas (`Vistas`) e interactuando directamente con el manejador de datos `GestionClinica`.

### Relación y Uso de Clases (POO)

A continuación se detalla la lista de las clases principales del backend y su aplicación en el flujo del sistema:

*   **`Usuario`** $\rightarrow$ Clase base de seguridad que define el inicio de sesión y perfiles de cuenta comunes, heredada por `Administrador` y `Veterinario`.
*   **`Administrador`** $\rightarrow$ Utilizada para el registro y gestión de empleados, auditorías generales de recetas o citas registradas y control de estadísticas comerciales.
*   **`Veterinario`** $\rightarrow$ Utilizada para realizar exploraciones físicas, emitir diagnósticos/tratamientos y prescribir recetas médicas.
*   **`Paciente`** $\rightarrow$ Representa al expediente de la mascota, vinculando sus visitas clínicas, peso actualizado e historial de consultas.
*   **`Propietario`** $\rightarrow$ Representa al cliente (dueño) en la base de datos, enlazando múltiples mascotas de su propiedad para control administrativo.
*   **`Cita`** $\rightarrow$ Utilizada para la planificación de turnos en la agenda y la administración de la cola de espera diaria en consultorio.
*   **`Consulta`** $\rightarrow$ Registra el informe clínico de la visita de una mascota, sirviendo de base para la importación automática de recetas en caja.
*   **`Inventario`** $\rightarrow$ Utilizada para administrar medicamentos e insumos médicos, controlar stock físico y alertar en existencias críticas (< 5).
*   **`Factura`** $\rightarrow$ Utilizada para el cobro mercantil en caja (16% IVA), selección de métodos de pago y la generación interactiva del ticket.
*   **`AnalizadorDatos`** $\rightarrow$ Proporciona los métodos para estructurar la información médica y graficar el rendimiento histórico del negocio.
*   **`GestionClinica`** $\rightarrow$ Funciona como el orquestador principal de datos del sistema, regulando la lectura y escritura persistente en los archivos CSV.

---

## 📂 Estructura del Proyecto

La estructura física del proyecto se organiza de la siguiente manera:

```text
Pr_ProgramacionAvanzada/
│
├── clases.py              # Backend: Modelos de clases, lógica de negocio y persistencia CSV.
├── main.py                # Frontend: Interfaz gráfica (Tkinter), Vistas y Eventos.
│
├── data/                  # Almacenamiento local persistente (Archivos CSV).
│   ├── citas.csv          # Base de datos de citas registradas.
│   ├── consultas.csv      # Historial médico detallado y prescripciones.
│   ├── facturas.csv       # Historial de transacciones de caja y facturación.
│   ├── inventario.csv     # Catálogo e inventario de productos e insumos médicos.
│   ├── pacientes.csv      # Expedientes de las mascotas registradas.
│   ├── propietarios.csv   # Información de dueños y contactos.
│   ├── razas.csv          # Enciclopedia local de razas y cuidados clínicos.
│   └── usuarios.csv       # Base de datos de usuarios (Administradores y Veterinarios).
│
├── informacion/           # Documentación del Proyecto.
│   ├── README.md          # Descripción técnica y detalles generales del sistema.
│   └── Guia_Usuario.md    # Manual explicativo del funcionamiento del programa.
│
├── logo.png               # Recursos gráficos: Logotipo del sistema.
└── background.png         # Recursos gráficos: Fondo estilizado del login.
```

---

## ⚙️ Especificación del Backend (`clases.py`)

El núcleo operativo está compuesto por clases fuertemente tipadas y estructuradas bajo POO. A continuación se detallan sus componentes:

### 1. Sistema de Usuarios y Personal
*   **`Usuario` (Clase Base):** Contiene los atributos comunes de acceso (`id_usuario`, `nombre`, `_password` [protegido], `rol`, `esta_activo`).
    *   `iniciar_sesion(password)`: Compara la contraseña y activa la sesión.
    *   `cerrar_sesion()`: Desactiva el estado del usuario.
    *   `cambiar_password(nueva_password)`: Permite actualizar la clave de acceso.
*   **`Administrador` (Hereda de `Usuario`):**
    *   Atributos adicionales: `nivel_seguridad` (entero), `departamento`.
    *   `analizar_inventario(df_inventario)`: Utiliza filtros Pandas para identificar insumos con bajo stock.
*   **`Veterinario` (Hereda de `Usuario`):**
    *   Atributos adicionales: `cedula_profesional`, `especialidad`, `horario_consulta`.
    *   `generar_receta(paciente_id, medicamentos)`: Genera un diccionario con la prescripción del doctor.

### 2. Entidades Principales
*   **`Paciente`:** Representa a la mascota en tratamiento.
    *   Atributos: `id_paciente`, `nombre`, `especie`, `raza`, `fecha_nacimiento`, `peso_actual`, `historial_consultas`.
    *   `calcular_edad()`: Retorna los años exactos del animal basándose en la fecha actual.
    *   `actualizar_peso(nuevo_peso)`: Modifica el peso y registra el cambio.
    *   `obtener_resumen()`: Retorna una cadena de texto descriptiva estructurada con datos clínicos básicos.
*   **`Propietario`:** Dueño de las mascotas.
    *   Atributos: `dni`, `nombre`, `telefono`, `correo`, `direccion`, `mascotas` (Lista de objetos `Paciente`).
    *   `vincular_mascota(mascota)`: Establece la relación bidireccional agregando el objeto `Paciente` a su colección privada.
    *   `actualizar_contacto(...)`: Modifica dinámicamente los medios de localización del cliente.

### 3. Citas y Consultorio Clínico
*   **`Cita`:** Reservas de turnos médicos.
    *   Atributos: `id_cita`, `fecha`, `hora`, `motivo`, `paciente`, `estado`.
    *   `cambiar_estado(nuevo_estado)`: Modifica de manera controlada el estado a valores autorizados (`Pendiente`, `Confirmada`, `Cancelada`, `Completada`).
*   **`Consulta`:** Expediente clínico generado por una visita médica.
    *   Atributos: `id_consulta`, `paciente`, `veterinario`, `fecha`, `temperatura`, `frecuencia_cardiaca`, `diagnostico`, `tratamiento`, `medicamentos` (en formato ID:Cantidad).
    *   `registrar_en_historial()`: Vincula la consulta de forma activa dentro de la colección histórica del `Paciente`.

### 4. Administración y Finanzas
*   **`Inventario`:** Control del catálogo farmacéutico.
    *   Atributos: `id_producto`, `nombre`, `stock`, `precio_unitario`.
    *   `actualizar_stock(cantidad)`: Modifica el stock de forma matemática previniendo valores negativos.
    *   `verificar_alerta()`: Retorna `True` si las unidades disponibles son menores a 5.
*   **`Factura`:** Registra cobros comerciales.
    *   Atributos: `folio`, `propietario`, `items` (lista de productos comprados), `subtotal`, `iva` (16%), `total`, `metodo_pago`, `fecha`, `estado`.
    *   `aplicar_descuento(porcentaje)`: Modifica el monto total aplicando la deducción.
    *   `imprimir_ticket()`: Retorna un ticket de venta formateado monosegmentado para impresoras térmicas.

### 5. Controladores de Datos y Sistema
*   **`AnalizadorDatos`:** Métodos estáticos auxiliares para graficación y exportaciones directas de reportes en formato CSV.
*   **`GestionClinica` (Manejador Central):** Inicializa colecciones vacías de datos y asume el rol de base de datos en memoria del sistema. Contiene los métodos para cargar (`cargar_datos()`) y guardar (`guardar_todo()`, `guardar_usuarios()`, `guardar_inventario()`, etc.) todos los archivos CSV dentro de la carpeta `data/`.

---

## 🖥️ Especificación del Frontend (`main.py`)

La interfaz de usuario ha sido programada con el framework **Tkinter** incorporando estilos de diseño modernos y minimalistas basados en componentes web planos:

### Vistas Disponibles (Módulos):
1.  **`LoginVista`:** Interfaz de acceso. Valida credenciales, ajusta el fondo dinámicamente (`background.png`) y asigna la sesión de usuario activa.
2.  **`DashboardVista` (Inicio):** Panel centralizado de estadísticas. Muestra tarjetas con métricas dinámicas de ingresos, stock crítico, pacientes y la cola de citas programadas para el día de hoy.
3.  **`PacientesVista` (Expedientes):** Interfaz para consultar expedientes médicos y registrar nuevas mascotas, permitiendo la asignación inmediata de su propietario por DNI.
4.  **`PropietariosVista` (Clientes):** Formulario premium de registro y tabla de búsqueda de clientes.
5.  **`CitasVista` (Agenda):** Calendario y agenda interactiva de citas que permite agendar nuevos turnos y cambiar estados a Cancelada o Completada.
6.  **`ConsultasVista` (Consultorio):** Módulo exclusivo para médicos veterinarios. Permite seleccionar mascotas de la cola de citas, registrar variables biológicas (temperatura, peso, frecuencia), capturar diagnósticos y tratamientos en tiempo real, prescribir medicamentos del inventario y guardar el historial médico.
7.  **`InventarioVista`:** Módulo para la inserción de insumos y actualización rápida del stock clínico. Resalta automáticamente en color rojo suave los insumos con stock crítico (< 5 unidades).
8.  **`FacturacionVista` (Caja):** Sistema POS que integra consultas y recetas. Permite autocompletar la venta a partir de las recetas del veterinario, agregar artículos manualmente, calcular impuestos (16% IVA), seleccionar métodos de pago y emitir tickets de compra.
9.  **`EmpleadosVista` (Personal):** Exclusivo de Administradores. Registra y cataloga a nuevos empleados. Para veterinarios, exige la validación numérica de la cédula profesional (7 u 8 dígitos).
10. **`ReportesVista` (Estadísticas):** Exclusivo de Administradores. Genera y embebe dentro de Tkinter gráficos vectoriales interactivos de Matplotlib (Visitas diarias y Análisis de área de ingresos financieros).
11. **`ConfiguracionVista` (Conectividad & APIs):**
    *   **Asistente de Razas Veterinarias:** Simula una petición API externa en segundo plano mostrando un cargador (UX loading spinner) y desplegando datos sobre temperamento y cuidados clínicos recomendados.
    *   **Controles de Admin:** Brinda acceso y búsquedas inteligentes en todo el historial clínico y agenda de citas.

---

## 💾 Modelo de Persistencia (`data/`)

Los archivos de persistencia almacenan los datos de forma estructurada en formato **CSV**. La codificación y conversión se realiza automáticamente mediante la librería `pandas` en cada operación de guardado o actualización en la UI.

| Archivo | Columnas Principales | Descripción |
| :--- | :--- | :--- |
| **`usuarios.csv`** | `id_usuario`, `nombre`, `password`, `rol`, `nivel_seguridad`, `departamento`, `cedula`, `especialidad`, `horario` | Credenciales e información de empleados. |
| **`pacientes.csv`** | `id_paciente`, `nombre`, `especie`, `raza`, `fecha_nacimiento`, `peso`, `dni_propietario` | Historial descriptivo de mascotas y vínculo a dueños. |
| **`propietarios.csv`** | `dni`, `nombre`, `telefono`, `correo`, `direccion` | Catálogo de clientes de la veterinaria. |
| **`citas.csv`** | `id_cita`, `fecha`, `hora`, `motivo`, `id_paciente`, `estado` | Control de agenda médica. |
| **`consultas.csv`** | `id_consulta`, `id_paciente`, `id_veterinario`, `fecha`, `temperatura`, `frecuencia_cardiaca`, `diagnostico`, `tratamiento`, `medicamentos` | Expediente médico y recetas emitidas (ID:Cant). |
| **`inventario.csv`** | `id_producto`, `nombre`, `stock`, `precio` | Stock de insumos, medicamentos y tarifas. |
| **`facturas.csv`** | `folio`, `dni_propietario`, `subtotal`, `total`, `metodo_pago`, `fecha` | Transacciones comerciales y caja diaria. |
| **`razas.csv`** | `raza`, `tipo`, `vida`, `temperamento`, `cuidados` | Enciclopedia técnica de razas. |

---

## 🛠️ Tecnologías y Dependencias

El sistema requiere las siguientes tecnologías y librerías de Python:

*   **Python 3.8 o superior:** Motor de ejecución del programa.
*   **Pandas (`pandas`):** Para el procesamiento, lectura y escritura eficiente de las bases de datos locales CSV.
*   **Pillow (`PIL`):** Para la carga, redimensionamiento dinámico y renderizado de imágenes JPG/PNG en la interfaz gráfica.
*   **Matplotlib (`matplotlib`):** Para la generación de gráficos vectoriales incluidos dinámicamente en el módulo de reportes.
*   **Tkinter / ttk:** (Incluido en la librería estándar de Python) Utilizado para el desarrollo del ecosistema visual y las ventanas del programa.

---

## 🚀 Instalación y Puesta en Marcha

Para iniciar el programa en su computadora local, siga estas instrucciones paso a paso:

### 1. Clonar o descargar el repositorio
Asegúrese de guardar todos los archivos (`clases.py`, `main.py`, la carpeta `data` y los recursos gráficos `logo.png` / `background.png`) en el mismo directorio de trabajo.

### 2. Instalar dependencias
Abra su terminal o consola de comandos de Windows (cmd / PowerShell) y ejecute la instalación de las librerías necesarias mediante `pip`:

```bash
pip install pandas pillow matplotlib
```

### 3. Ejecutar la aplicación
Ejecute el script principal de la interfaz de usuario `main.py`:

```bash
python main.py
```

### 4. Credenciales por defecto
Puede ingresar al sistema utilizando cualquiera de las siguientes cuentas pre-registradas en su base de datos local:

*   **Administrador:**
    *   **Usuario:** `admin`
    *   **Contraseña:** `admin123`
*   **Veterinario:**
    *   **Usuario:** `vet01`
    *   **Contraseña:** `vet123`

---
> 🐾 *Desarrollado con dedicación para garantizar la salud de nuestras mascotas y la eficiencia administrativa de tu clínica.*
