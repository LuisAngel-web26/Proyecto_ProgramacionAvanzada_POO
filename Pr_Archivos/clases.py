import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
from typing import List, Optional
import os

# --- SISTEMA DE USUARIOS Y PERSONAL ---

class Usuario:
    """Clase base para todos los usuarios del sistema."""
    def __init__(self, id_usuario: str, nombre: str, password: str, rol: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self._password = password  # Atributo protegido
        self.rol = rol
        self.esta_activo = False

    def iniciar_sesion(self, password: str) -> bool:
        if self._password == password:
            self.esta_activo = True
            print(f"Usuario {self.nombre} ha iniciado sesión correctamente.")
            return True
        print("Contraseña incorrecta.")
        return False

    def cerrar_sesion(self):
        self.esta_activo = False
        print(f"El usuario {self.nombre} ha cerrado sesión.")

    def cambiar_password(self, nueva_password: str):
        self._password = nueva_password
        print("Contraseña actualizada con éxito.")

class Administrador(Usuario):
    """Usuario con privilegios de gestión total."""
    def __init__(self, id_usuario, nombre, password, nivel_seguridad: int, departamento: str):
        super().__init__(id_usuario, nombre, password, "Administrador")
        self.nivel_seguridad = nivel_seguridad
        self.departamento = departamento

    def registrar_empleado(self, empleado_data: dict):
        # Lógica para guardar en base de datos o lista global
        print(f"Empleado {empleado_data.get('nombre')} registrado por Admin {self.nombre}")

    def analizar_inventario(self, df_inventario: pd.DataFrame):
        """Genera alertas si hay poco stock usando pandas."""
        bajo_stock = df_inventario[df_inventario['cantidad'] < 5]
        return bajo_stock

class Veterinario(Usuario):
    """Personal médico que realiza consultas."""
    def __init__(self, id_usuario, nombre, password, cedula: str, especialidad: str, horario: str):
        super().__init__(id_usuario, nombre, password, "Veterinario")
        self.cedula_profesional = cedula
        self.especialidad = especialidad
        self.horario_consulta = horario

    def generar_receta(self, paciente_id: str, medicamentos: List[str]):
        fecha = date.today()
        print(f"Receta generada por Dr. {self.nombre} para paciente {paciente_id} en fecha {fecha}")
        return {"veterinario": self.nombre, "fecha": fecha, "medicamentos": medicamentos}

# --- ENTIDADES PRINCIPALES ---

class Paciente:
    """Representa a una mascota en la clínica."""
    def __init__(self, id_paciente: str, nombre: str, especie: str, raza: str, fecha_nacimiento: date, peso_actual: float):
        self.id_paciente = id_paciente
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = fecha_nacimiento
        self.peso_actual = peso_actual
        self.historial_consultas = []

    def calcular_edad(self) -> int:
        hoy = date.today()
        edad = hoy.year - self.fecha_nacimiento.year - ((hoy.month, hoy.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
        return edad

    def actualizar_peso(self, nuevo_peso: float):
        self.peso_actual = nuevo_peso
        print(f"Peso de {self.nombre} actualizado a {nuevo_peso} kg.")

    def obtener_resumen(self) -> str:
        return f"Paciente: {self.nombre} | Especie: {self.especie} | Edad: {self.calcular_edad()} años | Peso: {self.peso_actual}kg"

class Propietario:
    """Dueño de las mascotas."""
    def __init__(self, dni: str, nombre: str, telefono: str, correo: str, direccion: str):
        self.dni = dni
        self.nombre = nombre
        self.telefono = telefono
        self.correo = correo
        self.direccion = direccion
        self.mascotas: List[Paciente] = []

    def vincular_mascota(self, mascota: Paciente):
        if mascota not in self.mascotas:
            self.mascotas.append(mascota)
            print(f"Mascota {mascota.nombre} vinculada a {self.nombre}")

    def actualizar_contacto(self, telefono=None, correo=None, direccion=None):
        if telefono: self.telefono = telefono
        if correo: self.correo = correo
        if direccion: self.direccion = direccion
        print("Datos de contacto actualizados.")

# --- GESTIÓN DE CITAS Y CONSULTAS ---

class Cita:
    """Reserva de tiempo para atención."""
    def __init__(self, id_cita: str, fecha: date, hora: str, motivo: str, paciente: Paciente):
        self.id_cita = id_cita
        self.fecha = fecha
        self.hora = hora
        self.motivo = motivo
        self.paciente = paciente
        self.estado = "Pendiente" # Pendiente, Confirmada, Cancelada, Completada

    def cambiar_estado(self, nuevo_estado: str):
        estados_validos = ["Pendiente", "Confirmada", "Cancelada", "Completada"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
            print(f"Cita {self.id_cita} marcada como {nuevo_estado}")

class Consulta:
    """Registro médico de una visita."""
    def __init__(self, id_consulta: str, paciente: Paciente, veterinario: Veterinario, 
                 temperatura: float, fc: int, diagnostico: str, tratamiento: str, fecha: datetime = None, medicamentos: str = ""):
        self.id_consulta = id_consulta
        self.paciente = paciente
        self.veterinario = veterinario
        self.fecha = fecha if fecha else datetime.now()
        self.temperatura = temperatura
        self.frecuencia_cardiaca = fc
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.medicamentos = medicamentos

    def registrar_en_historial(self):
        self.paciente.historial_consultas.append(self)
        print(f"Consulta {self.id_consulta} agregada al historial de {self.paciente.nombre}")

# --- ADMINISTRACIÓN Y FINANZAS ---

# --- ADMINISTRACIÓN Y FINANZAS ---

class Inventario:
    """Gestión de insumos médicos."""
    def __init__(self, id_producto: str, nombre: str, stock: int, precio: float):
        self.id_producto = id_producto
        self.nombre = nombre
        self.stock = stock
        self.precio_unitario = precio

    def actualizar_stock(self, cantidad: int):
        self.stock += cantidad
        if self.stock < 0: self.stock = 0
        print(f"Stock de {self.nombre} actualizado. Total: {self.stock}")

    def verificar_alerta(self) -> bool:
        return self.stock < 5

class Factura:
    """Documento de cobro."""
    def __init__(self, folio: str, propietario: Propietario, subtotal: float, metodo_pago: str, items: List[dict] = None):
        self.folio = folio
        self.propietario = propietario
        self.items = items if items else []
        self.subtotal = subtotal
        self.iva = subtotal * 0.16
        self.total = self.subtotal + self.iva
        self.metodo_pago = metodo_pago
        self.estado = "Pagada"
        self.fecha = datetime.now()

    def aplicar_descuento(self, porcentaje: float):
        descuento = self.total * (porcentaje / 100)
        self.total -= descuento
        print(f"Descuento del {porcentaje}% aplicado. Nuevo total: {self.total}")

    def imprimir_ticket(self) -> str:
        ticket = f"\n--- TICKET DE VENTA ---\n"
        ticket += f"Folio: {self.folio}\n"
        ticket += f"Fecha: {self.fecha.strftime('%Y-%m-%d %H:%M')}\n"
        ticket += f"Cliente: {self.propietario.nombre if self.propietario else 'Publico General'}\n"
        ticket += "-"*25 + "\n"
        for item in self.items:
            ticket += f"{item['nombre'][:15]:<15} x{item['cantidad']} ${item['total']:.2f}\n"
        ticket += "-"*25 + "\n"
        ticket += f"Subtotal: ${self.subtotal:.2f}\n"
        ticket += f"IVA (16%): ${self.iva:.2f}\n"
        ticket += f"TOTAL: ${self.total:.2f}\n"
        ticket += f"Método: {self.metodo_pago}\n"
        ticket += "-----------------------\n"
        return ticket

# --- ANÁLISIS DE DATOS ---

class AnalizadorDatos:
    """Clase para reportes estadísticos."""
    @staticmethod
    def graficar_visitas_por_mes(df_consultas: pd.DataFrame):
        if df_consultas.empty: return
        df_consultas['mes'] = pd.to_datetime(df_consultas['fecha']).dt.month
        df_consultas['mes'].value_counts().sort_index().plot(kind='bar', color='skyblue')
        plt.title("Visitas por Mes")
        plt.xlabel("Mes")
        plt.ylabel("Cantidad de Consultas")
        plt.show()

    @staticmethod
    def exportar_reporte_csv(data: List[dict], filename: str):
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Reporte exportado como {filename}")

# --- MANEJADOR GLOBAL (Útil para Tkinter) ---

class GestionClinica:
    """Manejador central para conectar las ventanas de Tkinter con la lógica."""
    def __init__(self):
        self.usuarios: List[Usuario] = []
        self.pacientes: List[Paciente] = []
        self.propietarios: List[Propietario] = []
        self.inventario: List[Inventario] = []
        self.citas: List[Cita] = []
        self.facturas: List[Factura] = []
        self.consultas: List[Consulta] = []
        self.usuario_actual: Optional[Usuario] = None
        self.razas: dict = {}

    def cargar_razas(self):
        if os.path.exists("data/razas.csv"):
            df = pd.read_csv("data/razas.csv")
            for _, row in df.iterrows():
                self.razas[str(row['raza'])] = {
                    'tipo': str(row['tipo']),
                    'vida': str(row['vida']),
                    'temperamento': str(row['temperamento']),
                    'cuidados': str(row['cuidados'])
                }
        else:
            db_defaults = {
                "Pastor Alemán": {
                    "tipo": "Perro de Trabajo",
                    "vida": "10 - 13 años",
                    "temperamento": "Alerta, Curioso, Obediente, Leal, Valiente",
                    "cuidados": "Requiere estimulación física y mental constante. Cepillado regular. Alta propensión a displasia de cadera. Excelente para guardia."
                },
                "Labrador Retriever": {
                    "tipo": "Perro de Compañía / Caza",
                    "vida": "10 - 12 años",
                    "temperamento": "Apacible, Intelligent, Extrovertido, Ágil, Confiado",
                    "cuidados": "Propenso a la obesidad, controle la dieta. Adora nadar. Requiere mucho ejercicio cardiovascular."
                },
                "Golden Retriever": {
                    "tipo": "Perro Cobrador",
                    "vida": "10 - 12 años",
                    "temperamento": "Inteligente, Amigable, Confiable, Bondadoso",
                    "cuidados": "Alta pérdida de pelo. Requiere cepillado diario. Muy dócil y fácil de adiestrar, ideal para terapia."
                },
                "Chihuahua": {
                    "tipo": "Perro de Compañía",
                    "vida": "12 - 20 años",
                    "temperamento": "Devoto, Vivaz, Alerta, Rápido, Valiente",
                    "cuidados": "Sensible al frío. Propenso a problemas dentales. Aunque es pequeño, necesita disciplina para evitar el síndrome del perro pequeño."
                },
                "Gato Persa": {
                    "tipo": "Felino Exótico",
                    "vida": "12 - 17 años",
                    "temperamento": "Tranquilo, Afectuoso, Silencioso, Dócil",
                    "cuidados": "El pelaje largo requiere cepillado diario indispensable para evitar nudos. Propenso a afecciones respiratorias por hocico chato."
                },
                "Gato Siamés": {
                    "tipo": "Felino de Puntas de Color",
                    "vida": "11 - 15 años",
                    "temperamento": "Muy Comunicativo, Cariñoso, Activo, Social",
                    "cuidados": "Muy vocal (maúlla mucho para comunicarse). Requiere compañía constante o juguetes interactivos para evitar estrés."
                },
                "Gato Maine Coon": {
                    "tipo": "Felino Gigante",
                    "vida": "12 - 15 años",
                    "temperamento": "Amigable, Juguetón, Paciente, Independiente",
                    "cuidados": "Es el gato doméstico más grande. Cepillado semanal. Monitoree de cerca la salud cardíaca (miocardiopatía hipertrófica)."
                },
                "Husky Siberiano": {
                    "tipo": "Perro de Trineo",
                    "vida": "12 - 15 años",
                    "temperamento": "Extrovertido, Amigable, Gentil, Inteligente",
                    "cuidados": "Poderoso instinto de escape. Requiere vallas muy altas. Muda de pelo masiva dos veces al año. Excelente en climas templados/fríos."
                }
            }
            self.razas = db_defaults
            self.guardar_razas()

    def guardar_razas(self):
        data = []
        for raza, info in self.razas.items():
            data.append({
                'raza': raza,
                'tipo': info['tipo'],
                'vida': info['vida'],
                'temperamento': info['temperamento'],
                'cuidados': info['cuidados']
            })
        pd.DataFrame(data).to_csv("data/razas.csv", index=False)

    def login(self, id_u, pwd):
        for u in self.usuarios:
            if u.id_usuario == id_u and u.iniciar_sesion(pwd):
                self.usuario_actual = u
                return True
        return False

    def cargar_datos(self):
        """Carga todos los datos desde CSV."""
        try:
            # Usuarios
            if os.path.exists("data/usuarios.csv"):
                df_u = pd.read_csv("data/usuarios.csv")
                for _, row in df_u.iterrows():
                    if row['rol'] == "Administrador":
                        u = Administrador(str(row['id_usuario']), row['nombre'], str(row['password']), int(row['nivel_seguridad']), row['departamento'])
                    else:
                        u = Veterinario(str(row['id_usuario']), row['nombre'], str(row['password']), row['cedula'], row['especialidad'], row['horario'])
                    self.usuarios.append(u)
            
            # Inventario
            if os.path.exists("data/inventario.csv"):
                df_i = pd.read_csv("data/inventario.csv")
                for _, row in df_i.iterrows():
                    self.inventario.append(Inventario(str(row['id_producto']), row['nombre'], int(row['stock']), float(row['precio'])))
            
            # Propietarios
            if os.path.exists("data/propietarios.csv"):
                df_prop = pd.read_csv("data/propietarios.csv")
                for _, row in df_prop.iterrows():
                    self.propietarios.append(Propietario(str(row['dni']), row['nombre'], str(row['telefono']), row['correo'], row['direccion']))

            # Pacientes
            if os.path.exists("data/pacientes.csv"):
                df_p = pd.read_csv("data/pacientes.csv")
                for _, row in df_p.iterrows():
                    p = Paciente(str(row['id_paciente']), row['nombre'], row['especie'], row['raza'], datetime.strptime(row['fecha_nacimiento'], '%Y-%m-%d').date(), float(row['peso']))
                    self.pacientes.append(p)
                    # Vincular con propietario if exists
                    if 'dni_propietario' in row and not pd.isna(row['dni_propietario']):
                        prop = next((pr for pr in self.propietarios if pr.dni == str(row['dni_propietario'])), None)
                        if prop: prop.vincular_mascota(p)

            # Citas
            if os.path.exists("data/citas.csv"):
                df_c = pd.read_csv("data/citas.csv")
                for _, row in df_c.iterrows():
                    pac = next((p for p in self.pacientes if p.id_paciente == str(row['id_paciente'])), None)
                    if pac:
                        cita = Cita(str(row['id_cita']), datetime.strptime(row['fecha'], '%Y-%m-%d').date(), row['hora'], row['motivo'], pac)
                        cita.estado = row['estado']
                        self.citas.append(cita)

            # Facturas
            if os.path.exists("data/facturas.csv"):
                df_f = pd.read_csv("data/facturas.csv")
                for _, row in df_f.iterrows():
                    prop = next((pr for pr in self.propietarios if pr.dni == str(row.get('dni_propietario'))), None)
                    f = Factura(str(row['folio']), prop, float(row['subtotal']), str(row['metodo_pago']))
                    f.total = float(row['total'])
                    try:
                        f.fecha = datetime.strptime(str(row['fecha']), '%Y-%m-%d %H:%M:%S')
                    except:
                        f.fecha = datetime.now()
                    self.facturas.append(f)

            # Consultas
            if os.path.exists("data/consultas.csv"):
                df_con = pd.read_csv("data/consultas.csv")
                for _, row in df_con.iterrows():
                    pac = next((p for p in self.pacientes if p.id_paciente == str(row['id_paciente'])), None)
                    vet = next((u for u in self.usuarios if u.id_usuario == str(row['id_veterinario'])), None)
                    if pac and vet:
                        try:
                            fecha_val = datetime.strptime(str(row['fecha']), '%Y-%m-%d %H:%M:%S')
                        except:
                            fecha_val = datetime.now()
                        meds = str(row.get('medicamentos', '')) if not pd.isna(row.get('medicamentos')) else ''
                        con = Consulta(str(row['id_consulta']), pac, vet, float(row['temperatura']), int(row['frecuencia_cardiaca']), str(row['diagnostico']), str(row['tratamiento']), fecha_val, meds)
                        self.consultas.append(con)
                        pac.historial_consultas.append(con)

            # Cargar razas
            self.cargar_razas()

        except Exception as e:
            print(f"Error al cargar datos: {e}")

    def guardar_todo(self):
        self.guardar_usuarios()
        self.guardar_inventario()
        self.guardar_pacientes()
        self.guardar_propietarios()
        self.guardar_citas()
        self.guardar_facturas()
        self.guardar_consultas()
        self.guardar_razas()

    def guardar_usuarios(self):
        data = []
        for u in self.usuarios:
            row = {
                'id_usuario': u.id_usuario, 'nombre': u.nombre, 'password': u._password, 'rol': u.rol,
                'nivel_seguridad': getattr(u, 'nivel_seguridad', ''), 'departamento': getattr(u, 'departamento', ''),
                'cedula': getattr(u, 'cedula_profesional', ''), 'especialidad': getattr(u, 'especialidad', ''),
                'horario': getattr(u, 'horario_consulta', '')
            }
            data.append(row)
        pd.DataFrame(data).to_csv("data/usuarios.csv", index=False)

    def guardar_inventario(self):
        data = [{'id_producto': i.id_producto, 'nombre': i.nombre, 'stock': i.stock, 'precio': i.precio_unitario} for i in self.inventario]
        pd.DataFrame(data).to_csv("data/inventario.csv", index=False)

    def guardar_pacientes(self):
        data = []
        for p in self.pacientes:
            # Buscar el DNI del propietario
            dni_prop = ""
            for prop in self.propietarios:
                if p in prop.mascotas:
                    dni_prop = prop.dni
                    break
            data.append({
                'id_paciente': p.id_paciente, 'nombre': p.nombre, 'especie': p.especie, 
                'raza': p.raza, 'fecha_nacimiento': p.fecha_nacimiento.strftime('%Y-%m-%d'), 
                'peso': p.peso_actual, 'dni_propietario': dni_prop
            })
        pd.DataFrame(data).to_csv("data/pacientes.csv", index=False)

    def guardar_propietarios(self):
        data = [{'dni': pr.dni, 'nombre': pr.nombre, 'telefono': pr.telefono, 'correo': pr.correo, 'direccion': pr.direccion} for pr in self.propietarios]
        pd.DataFrame(data).to_csv("data/propietarios.csv", index=False)

    def guardar_citas(self):
        data = []
        for c in self.citas:
            data.append({
                'id_cita': c.id_cita, 'fecha': c.fecha.strftime('%Y-%m-%d'), 
                'hora': c.hora, 'motivo': c.motivo, 'id_paciente': c.paciente.id_paciente, 
                'estado': c.estado
            })
        pd.DataFrame(data).to_csv("data/citas.csv", index=False)

    def guardar_facturas(self):
        data = []
        for f in self.facturas:
            data.append({
                'folio': f.folio, 'dni_propietario': f.propietario.dni if f.propietario else '',
                'subtotal': f.subtotal, 'total': f.total, 'metodo_pago': f.metodo_pago,
                'fecha': f.fecha.strftime('%Y-%m-%d %H:%M:%S')
            })
        pd.DataFrame(data).to_csv("data/facturas.csv", index=False)

    def guardar_consultas(self):
        data = []
        for c in self.consultas:
            data.append({
                'id_consulta': c.id_consulta, 'id_paciente': c.paciente.id_paciente, 
                'id_veterinario': c.veterinario.id_usuario, 'fecha': c.fecha.strftime('%Y-%m-%d %H:%M:%S'),
                'temperatura': c.temperatura, 'frecuencia_cardiaca': c.frecuencia_cardiaca, 
                'diagnostico': c.diagnostico, 'tratamiento': c.tratamiento,
                'medicamentos': c.medicamentos
            })
        pd.DataFrame(data).to_csv("data/consultas.csv", index=False)