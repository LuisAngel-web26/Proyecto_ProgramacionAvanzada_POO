import os
import sys

# Cambiar el directorio de trabajo al directorio del script para evitar problemas de rutas relativas
script_dir = os.path.dirname(os.path.abspath(__file__))
if script_dir:
    os.chdir(script_dir)

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from clases import GestionClinica, Administrador, Veterinario, Inventario, Paciente, Cita, Consulta, Propietario, Factura
import pandas as pd
from datetime import datetime, date
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# --- CONFIGURACIÓN DE ESTILO PREMIUM ---
# --- CONFIGURACIÓN DE ESTILO PREMIUM ---
COLOR_PRIMARIO = "#1B5E20"    # Verde Bosque profundo
COLOR_SECUNDARIO = "#FFFFFF"  # Blanco puro
COLOR_ACENTO = "#E8F5E9"      # Verde menta muy suave
COLOR_SIDEBAR = "#2E7D32"     # Verde medio para sidebar
COLOR_TEXTO = "#212121"       # Gris casi negro
COLOR_TEXTO_LIGHT = "#757575" # Gris suave
COLOR_BOTON = "#43A047"       # Verde vibrante
COLOR_BOTON_HOVER = "#388E3C"
COLOR_PELIGRO = "#D32F2F"     # Rojo
COLOR_ADVERTENCIA = "#FBC02D" # Amarillo

FUENTE_TITULO = ("Segoe UI", 28, "bold")
FUENTE_SUBTITULO = ("Segoe UI", 16, "bold")
FUENTE_HEADER = ("Segoe UI", 12, "bold")
FUENTE_NORMAL = ("Segoe UI", 10)
FUENTE_SMALL = ("Segoe UI", 9)

class AppHuellitas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Huellitas - Sistema Médico Veterinario v2.0")
        self.geometry("1200x800")
        self.state('zoomed')
        self.configure(bg=COLOR_SECUNDARIO)
        
        self.sistema = GestionClinica()
        self.sistema.cargar_datos()
        
        # Estilo global
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="white", foreground=COLOR_TEXTO, rowheight=35, fieldbackground="white", font=FUENTE_NORMAL)
        style.map("Treeview", background=[('selected', COLOR_BOTON)])
        style.configure("Treeview.Heading", background=COLOR_ACENTO, foreground=COLOR_PRIMARIO, font=("Segoe UI", 11, "bold"))
        
        self.container = tk.Frame(self, bg=COLOR_SECUNDARIO)
        self.container.pack(fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        self.vistas = {}
        self.crear_vistas()
        self.mostrar_vista("Login")

    def crear_vistas(self):
        vistas_clases = [
            LoginVista, DashboardVista, InventarioVista, EmpleadosVista, 
            PacientesVista, CitasVista, ConsultasVista, FacturacionVista,
            PropietariosVista, ReportesVista, ConfiguracionVista
        ]
        for V in vistas_clases:
            nombre = V.__name__.replace("Vista", "")
            vista = V(parent=self.container, controller=self)
            self.vistas[nombre] = vista
            vista.grid(row=0, column=0, sticky="nsew")

    def mostrar_vista(self, nombre):
        vista = self.vistas.get(nombre)
        if vista:
            if hasattr(vista, "actualizar"): vista.actualizar()
            vista.tkraise()

# --- COMPONENTES REUTILIZABLES ---
def crear_header(parent, titulo, sub=None):
    header = tk.Frame(parent, bg=COLOR_SECUNDARIO, pady=20)
    header.pack(fill="x", padx=40)
    tk.Label(header, text=titulo.upper(), font=FUENTE_TITULO, fg=COLOR_PRIMARIO, bg=COLOR_SECUNDARIO).pack(anchor="w")
    if sub:
        tk.Label(header, text=sub, font=FUENTE_NORMAL, fg=COLOR_TEXTO_LIGHT, bg=COLOR_SECUNDARIO).pack(anchor="w")
    tk.Frame(header, height=2, bg=COLOR_ACENTO).pack(fill="x", pady=(10, 0))
    return header

class Card(tk.Frame):
    def __init__(self, parent, titulo, valor, color_bg="#FFFFFF", color_fg=COLOR_PRIMARIO):
        super().__init__(parent, bg=color_bg, padx=20, pady=20, highlightthickness=1, highlightbackground="#E0E0E0")
        tk.Label(self, text=titulo, font=FUENTE_SMALL, fg=COLOR_TEXTO_LIGHT, bg=color_bg).pack(anchor="w")
        tk.Label(self, text=valor, font=FUENTE_TITULO, fg=color_fg, bg=color_bg).pack(anchor="w", pady=(5, 0))

# --- VISTAS ---

class LoginVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        
        fondo_cargado = False
        try:
            self.bg_original = Image.open("background.png")
            self.bg_photo = ImageTk.PhotoImage(self.bg_original)
            self.canvas = tk.Canvas(self, highlightthickness=0)
            self.canvas.pack(fill="both", expand=True)
            self.bg_item = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
            
            self.login_frame = tk.Frame(self, bg=COLOR_SECUNDARIO, padx=50, pady=50)
            self.canvas.create_window(0, 0, window=self.login_frame, anchor="center", tags="login_box")
            
            # Sombra simulada
            self.login_frame.config(highlightbackground="#E0E0E0", highlightthickness=1)
            
            self.bind("<Configure>", self.redimensionar_fondo)
            fondo_cargado = True
        except Exception as e:
            print(f"Error login UI (background image could not load, using simple theme): {e}")
            # Si falla el fondo, colocamos la caja de login directamente en el centro del frame
            self.login_frame = tk.Frame(self, bg=COLOR_SECUNDARIO, padx=50, pady=50)
            self.login_frame.place(relx=0.5, rely=0.5, anchor="center")
            self.login_frame.config(highlightbackground="#E0E0E0", highlightthickness=1)
            
        # Los componentes de login siempre se crean, sin importar si cargó el fondo o no
        tk.Label(self.login_frame, text="BIENVENIDO", font=FUENTE_TITULO, fg=COLOR_PRIMARIO, bg=COLOR_SECUNDARIO).pack()
        tk.Label(self.login_frame, text="Ingrese sus credenciales para continuar", font=FUENTE_NORMAL, fg=COLOR_TEXTO_LIGHT, bg=COLOR_SECUNDARIO).pack(pady=(0, 40))
        
        tk.Label(self.login_frame, text="USUARIO", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, fg=COLOR_PRIMARIO).pack(anchor="w")
        self.ent_user = tk.Entry(self.login_frame, font=FUENTE_NORMAL, width=35, relief="flat", highlightthickness=1, highlightbackground="#BDBDBD")
        self.ent_user.pack(pady=(5, 20), ipady=10)
        
        tk.Label(self.login_frame, text="CONTRASEÑA", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, fg=COLOR_PRIMARIO).pack(anchor="w")
        self.ent_pass = tk.Entry(self.login_frame, font=FUENTE_NORMAL, width=35, relief="flat", highlightthickness=1, highlightbackground="#BDBDBD", show="*")
        self.ent_pass.pack(pady=(5, 40), ipady=10)
        
        btn_login = tk.Button(self.login_frame, text="INICIAR SESIÓN", bg=COLOR_BOTON, fg="white", font=FUENTE_SUBTITULO, 
                             bd=0, cursor="hand2", padx=20, pady=10, command=self.validar_login)
        btn_login.pack(fill="x")

    def redimensionar_fondo(self, event):
        if event.widget != self:
            return
        w, h = event.width, event.height
        if w > 0 and h > 0:
            resized = self.bg_original.resize((w, h), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(resized)
            self.canvas.itemconfig(self.bg_item, image=self.bg_photo)
            self.canvas.coords("login_box", w//2, h//2)

    def validar_login(self):
        if self.controller.sistema.login(self.ent_user.get(), self.ent_pass.get()):
            self.controller.mostrar_vista("Dashboard")
        else:
            messagebox.showerror("Acceso Denegado", "El usuario o la contraseña son incorrectos.")

class Sidebar(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SIDEBAR, width=280)
        self.controller = controller
        self.pack_propagate(False)
        
        # Logo y nombre
        brand_frame = tk.Frame(self, bg=COLOR_SIDEBAR, pady=40)
        brand_frame.pack(fill="x")
        tk.Label(brand_frame, text="🐾 HUELLITAS", fg="white", bg=COLOR_SIDEBAR, font=FUENTE_SUBTITULO).pack()
        
        self.menu_container = tk.Frame(self, bg=COLOR_SIDEBAR)
        self.menu_container.pack(fill="both", expand=True)
        
        # Info usuario al fondo
        self.user_frame = tk.Frame(self, bg="#266229", pady=20)
        self.user_frame.pack(side="bottom", fill="x")
        self.lbl_u = tk.Label(self.user_frame, text="User Name", fg="white", bg="#266229", font=FUENTE_HEADER)
        self.lbl_u.pack()
        self.lbl_r = tk.Label(self.user_frame, text="Role", fg=COLOR_ACENTO, bg="#266229", font=FUENTE_SMALL)
        self.lbl_r.pack()

    def refrescar_menu(self):
        for w in self.menu_container.winfo_children(): w.destroy()
        u = self.controller.sistema.usuario_actual
        if not u: return
        
        self.lbl_u.config(text=u.nombre.upper())
        self.lbl_r.config(text=u.rol.upper())
        
        opciones = [
            ("Inicio", "Dashboard", "🏠"),
            ("Pacientes", "Pacientes", "🐶"),
            ("Propietarios", "Propietarios", "👤"),
            ("Citas", "Citas", "📅"),
            ("Consultas", "Consultas", "⚕️"),
            ("Inventario", "Inventario", "📦"),
            ("Facturación", "Facturacion", "💰"),
            ("Personal", "Empleados", "👥"),
            ("Reportes", "Reportes", "📊"),
            ("Conectividad & APIs", "Configuracion", "🌐"),
            ("Cerrar Sesión", "Login", "🚪")
        ]
        
        for txt, vista, icon in opciones:
            if u.rol == "Administrador":
                if vista not in ["Dashboard", "Propietarios", "Empleados", "Reportes", "Configuracion", "Login"]:
                    continue
            else:
                if vista in ["Empleados", "Reportes"]:
                    continue
                
            btn = tk.Button(self.menu_container, text=f"  {icon}  {txt}", bg=COLOR_SIDEBAR, fg="white", 
                           relief="flat", font=FUENTE_NORMAL, anchor="w", padx=25, pady=12, 
                           cursor="hand2", activebackground=COLOR_BOTON, bd=0,
                           command=lambda v=vista: self.controller.mostrar_vista(v))
            btn.pack(fill="x")

class DashboardVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_ACENTO)
        self.controller = controller
        
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        self.main_content = tk.Frame(self, bg=COLOR_ACENTO)
        self.main_content.pack(side="right", fill="both", expand=True)
        
        crear_header(self.main_content, "Panel de Control", "Bienvenido al sistema de gestión Huellitas")
        
        self.stats_frame = tk.Frame(self.main_content, bg=COLOR_ACENTO)
        self.stats_frame.pack(fill="x", padx=40, pady=20)
        
        # Cuadrícula para Tarjetas (Cards)
        self.cards = {}
        labels = [("Pacientes Totales", "0"), ("Citas de Hoy", "0"), ("Stock Bajo", "0"), ("Ingresos Hoy", "$0.00")]
        for i, (t, v) in enumerate(labels):
            card = Card(self.stats_frame, t, v)
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            self.stats_frame.grid_columnconfigure(i, weight=1)
            self.cards[t] = card

        # Sección inferior (Citas próximas)
        tk.Label(self.main_content, text="PRÓXIMAS CITAS", font=FUENTE_HEADER, bg=COLOR_ACENTO, fg=COLOR_PRIMARIO).pack(anchor="w", padx=40, pady=(20, 10))
        self.tree = ttk.Treeview(self.main_content, columns=("Hora", "Paciente", "Motivo", "Estado"), show="headings", height=10)
        for c in ("Hora", "Paciente", "Motivo", "Estado"): self.tree.heading(c, text=c)
        self.tree.pack(fill="x", padx=40)

    def actualizar(self):
        self.sidebar.refrescar_menu()
        s = self.controller.sistema
        
        # Actualizar Tarjetas (Cards)
        self.cards["Pacientes Totales"].winfo_children()[1].config(text=str(len(s.pacientes)))
        citas_hoy = [c for c in s.citas if c.fecha == date.today()]
        self.cards["Citas de Hoy"].winfo_children()[1].config(text=str(len(citas_hoy)))
        stock_bajo = [i for i in s.inventario if i.verificar_alerta()]
        self.cards["Stock Bajo"].winfo_children()[1].config(text=str(len(stock_bajo)), fg=COLOR_PELIGRO if stock_bajo else COLOR_PRIMARIO)
        
        # Calcular e ingresar los ingresos del día de hoy
        ingresos_hoy = sum(f.total for f in s.facturas if f.fecha.date() == date.today())
        self.cards["Ingresos Hoy"].winfo_children()[1].config(text=f"${ingresos_hoy:.2f}")
        
        # Actualizar Citas
        for i in self.tree.get_children(): self.tree.delete(i)
        for c in sorted(citas_hoy, key=lambda x: x.hora):
            self.tree.insert("", "end", values=(c.hora, c.paciente.nombre, c.motivo, c.estado))

class InventarioVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        
        crear_header(main, "Inventario", "Administración de medicamentos e insumos")
        
        # Formulario de Nuevo Producto
        nuevo_frame = tk.LabelFrame(main, text=" NUEVO PRODUCTO ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, padx=20, pady=20)
        nuevo_frame.pack(fill="x", padx=40, pady=5)
        
        tk.Label(nuevo_frame, text="ID:", bg=COLOR_SECUNDARIO).grid(row=0, column=0, padx=5)
        self.ent_nuevo_id = tk.Entry(nuevo_frame, width=10)
        self.ent_nuevo_id.grid(row=0, column=1, padx=5)
        
        tk.Label(nuevo_frame, text="Nombre:", bg=COLOR_SECUNDARIO).grid(row=0, column=2, padx=5)
        self.ent_nuevo_nom = tk.Entry(nuevo_frame, width=20)
        self.ent_nuevo_nom.grid(row=0, column=3, padx=5)
        
        tk.Label(nuevo_frame, text="Stock:", bg=COLOR_SECUNDARIO).grid(row=0, column=4, padx=5)
        self.ent_nuevo_stk = tk.Entry(nuevo_frame, width=10)
        self.ent_nuevo_stk.grid(row=0, column=5, padx=5)
        
        tk.Label(nuevo_frame, text="Precio:", bg=COLOR_SECUNDARIO).grid(row=0, column=6, padx=5)
        self.ent_nuevo_pre = tk.Entry(nuevo_frame, width=10)
        self.ent_nuevo_pre.grid(row=0, column=7, padx=5)
        
        tk.Button(nuevo_frame, text="AGREGAR", bg=COLOR_BOTON, fg="white", command=self.agregar_producto).grid(row=0, column=8, padx=20)

        # Formulario de edición manual
        edit_frame = tk.Frame(main, bg=COLOR_ACENTO, padx=20, pady=15)
        edit_frame.pack(fill="x", padx=40, pady=5)
        
        tk.Label(edit_frame, text="ACTUALIZAR STOCK DEL SELECCIONADO:", font=FUENTE_HEADER, bg=COLOR_ACENTO).grid(row=0, column=0, sticky="w")
        
        self.ent_stock = tk.Entry(edit_frame, width=15)
        self.ent_stock.grid(row=0, column=1, padx=10)
        
        tk.Button(edit_frame, text="GUARDAR", bg=COLOR_BOTON, fg="white", command=self.cambiar_stock).grid(row=0, column=2, padx=10)
        
        # Buscador
        search_frame = tk.Frame(main, bg=COLOR_SECUNDARIO)
        search_frame.pack(fill="x", padx=40, pady=10)
        tk.Label(search_frame, text="🔍 Buscar:", bg=COLOR_SECUNDARIO).pack(side="left")
        self.ent_search = tk.Entry(search_frame, width=40)
        self.ent_search.pack(side="left", padx=10)
        self.ent_search.bind("<KeyRelease>", lambda e: self.actualizar())

        self.tree = ttk.Treeview(main, columns=("ID", "Nombre", "Stock", "Precio"), show="headings")
        for c in ("ID", "Nombre", "Stock", "Precio"): self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Configuración de resaltado para stock bajo (< 5)
        self.tree.tag_configure("low_stock", background="#FFEBEE", foreground=COLOR_PELIGRO, font=("Segoe UI", 10, "bold"))
        self.tree.tag_configure("normal_stock", foreground=COLOR_TEXTO)

    def actualizar(self):
        self.sidebar.refrescar_menu()
        for i in self.tree.get_children(): self.tree.delete(i)
        query = self.ent_search.get().lower()
        for p in self.controller.sistema.inventario:
            if query in p.nombre.lower() or query in p.id_producto.lower():
                tag = "low_stock" if p.verificar_alerta() else "normal_stock"
                self.tree.insert("", "end", values=(p.id_producto, p.nombre, p.stock, f"${p.precio_unitario:.2f}"), tags=(tag,))

    def cambiar_stock(self):
        sel = self.tree.selection()
        if not sel: return messagebox.showwarning("Atención", "Seleccione un producto")
        try:
            nuevo = int(self.ent_stock.get())
            pid = self.tree.item(sel[0])['values'][0]
            for p in self.controller.sistema.inventario:
                if str(p.id_producto) == str(pid):
                    diff = nuevo - p.stock
                    p.actualizar_stock(diff)
                    self.controller.sistema.guardar_inventario()
                    self.actualizar()
                    messagebox.showinfo("Éxito", "Stock actualizado")
                    return
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")

    def agregar_producto(self):
        pid = self.ent_nuevo_id.get()
        nom = self.ent_nuevo_nom.get()
        try:
            stk = int(self.ent_nuevo_stk.get())
            pre = float(self.ent_nuevo_pre.get())
            if not pid or not nom: raise ValueError
            if any(p.id_producto == pid for p in self.controller.sistema.inventario):
                return messagebox.showerror("Error", "ID de producto ya existe")
            nuevo = Inventario(pid, nom, stk, pre)
            self.controller.sistema.inventario.append(nuevo)
            self.controller.sistema.guardar_inventario()
            self.actualizar()
            self.ent_nuevo_id.delete(0, 'end')
            self.ent_nuevo_nom.delete(0, 'end')
            self.ent_nuevo_stk.delete(0, 'end')
            self.ent_nuevo_pre.delete(0, 'end')
            messagebox.showinfo("Éxito", "Producto agregado")
        except ValueError:
            messagebox.showerror("Error", "Datos inválidos en el formulario")

class PacientesVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        
        crear_header(main, "Expedientes", "Registro completo de pacientes")
        
        # Formulario de Registro
        reg_frame = tk.LabelFrame(main, text=" REGISTRO DE PACIENTE ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, padx=20, pady=20)
        reg_frame.pack(fill="x", padx=40, pady=10)
        
        fields = ["Nombre", "Especie", "Raza", "Peso (kg)", "DNI Dueño"]
        self.p_ents = {}
        for i, f in enumerate(fields):
            tk.Label(reg_frame, text=f, bg=COLOR_SECUNDARIO).grid(row=0, column=i*2, padx=5, sticky="w")
            ent = tk.Entry(reg_frame, width=15)
            ent.grid(row=0, column=i*2+1, padx=5)
            self.p_ents[f] = ent
            
        tk.Button(reg_frame, text="REGISTRAR MASCOTA", bg=COLOR_BOTON, fg="white", command=self.registrar).grid(row=0, column=12, padx=20)

        self.tree = ttk.Treeview(main, columns=("ID", "Nombre", "Especie", "Raza", "Peso"), show="headings")
        for c in ("ID", "Nombre", "Especie", "Raza", "Peso"): self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=40, pady=20)

    def actualizar(self):
        self.sidebar.refrescar_menu()
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in self.controller.sistema.pacientes:
            self.tree.insert("", "end", values=(p.id_paciente, p.nombre, p.especie, p.raza, p.peso_actual))

    def registrar(self):
        vals = {k: v.get() for k, v in self.p_ents.items()}
        if not vals["Nombre"] or not vals["Especie"]: return messagebox.showerror("Error", "Nombre y Especie son obligatorios")
        
        try:
            pid = str(len(self.controller.sistema.pacientes) + 1001)
            nuevo = Paciente(pid, vals["Nombre"], vals["Especie"], vals["Raza"], date.today(), float(vals["Peso (kg)"] or 0))
            
            # Vincular a propietario si existe
            if vals["DNI Dueño"]:
                prop = next((pr for pr in self.controller.sistema.propietarios if pr.dni == vals["DNI Dueño"]), None)
                if prop: prop.vincular_mascota(nuevo)
                else: messagebox.showwarning("Atención", "Propietario no encontrado. Se registró sin dueño.")
            
            self.controller.sistema.pacientes.append(nuevo)
            self.controller.sistema.guardar_pacientes()
            self.actualizar()
            for e in self.p_ents.values(): e.delete(0, "end")
            messagebox.showinfo("Éxito", f"Paciente {nuevo.nombre} registrado con ID {pid}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

class CitasVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        
        crear_header(main, "Agenda", "Gestión de citas y turnos")
        
        # Formulario de Agenda
        f = tk.LabelFrame(main, text=" AGENDAR NUEVA CITA ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, padx=20, pady=20)
        f.pack(fill="x", padx=40, pady=10)
        
        tk.Label(f, text="ID Paciente:", bg=COLOR_SECUNDARIO).grid(row=0, column=0)
        self.ent_pid = tk.Entry(f, width=10)
        self.ent_pid.grid(row=0, column=1, padx=5)
        
        tk.Label(f, text="Fecha (AAAA-MM-DD):", bg=COLOR_SECUNDARIO).grid(row=0, column=2)
        self.ent_fecha = tk.Entry(f, width=15)
        self.ent_fecha.insert(0, date.today().strftime('%Y-%m-%d'))
        self.ent_fecha.grid(row=0, column=3, padx=5)
        
        tk.Label(f, text="Hora (HH:MM):", bg=COLOR_SECUNDARIO).grid(row=0, column=4)
        self.ent_hora = tk.Entry(f, width=10)
        self.ent_hora.grid(row=0, column=5, padx=5)
        
        tk.Label(f, text="Motivo:", bg=COLOR_SECUNDARIO).grid(row=0, column=6)
        self.ent_motivo = tk.Entry(f, width=20)
        self.ent_motivo.grid(row=0, column=7, padx=5)
        
        tk.Button(f, text="AGENDAR", bg=COLOR_BOTON, fg="white", command=self.agendar).grid(row=0, column=8, padx=10)

        self.tree = ttk.Treeview(main, columns=("ID", "Fecha", "Hora", "Paciente", "Motivo", "Estado"), show="headings")
        for c in ("ID", "Fecha", "Hora", "Paciente", "Motivo", "Estado"): self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True, padx=40, pady=10)
        
        btn_f = tk.Frame(main, bg=COLOR_SECUNDARIO)
        btn_f.pack(fill="x", padx=40, pady=10)
        tk.Button(btn_f, text="CANCELAR SELECCIONADA", bg=COLOR_PELIGRO, fg="white", command=lambda: self.status("Cancelada")).pack(side="left", padx=5)
        tk.Button(btn_f, text="MARCAR COMPLETADA", bg=COLOR_BOTON, fg="white", command=lambda: self.status("Completada")).pack(side="left", padx=5)

    def actualizar(self):
        self.sidebar.refrescar_menu()
        for i in self.tree.get_children(): self.tree.delete(i)
        for c in sorted(self.controller.sistema.citas, key=lambda x: (x.fecha, x.hora)):
            self.tree.insert("", "end", values=(c.id_cita, c.fecha, c.hora, c.paciente.nombre, c.motivo, c.estado))

    def agendar(self):
        pid = self.ent_pid.get()
        paciente = next((p for p in self.controller.sistema.pacientes if p.id_paciente == pid), None)
        if not paciente: return messagebox.showerror("Error", "Paciente no encontrado")
        
        try:
            nueva = Cita(str(len(self.controller.sistema.citas)+1), 
                         datetime.strptime(self.ent_fecha.get(), '%Y-%m-%d').date(),
                         self.ent_hora.get(), self.ent_motivo.get(), paciente)
            self.controller.sistema.citas.append(nueva)
            self.controller.sistema.guardar_citas()
            self.actualizar()
            messagebox.showinfo("Éxito", "Cita agendada")
        except Exception as e:
            messagebox.showerror("Error", "Formato de fecha inválido (AAAA-MM-DD)")

    def status(self, s):
        sel = self.tree.selection()
        if not sel: 
            return messagebox.showwarning("Atención", "Por favor, seleccione una cita de la lista antes de cambiar su estado.")
        cid = self.tree.item(sel[0])['values'][0]
        for c in self.controller.sistema.citas:
            if str(c.id_cita) == str(cid):
                c.cambiar_estado(s)
                self.controller.sistema.guardar_citas()
                self.actualizar()
                return

class FacturacionVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        self.carrito = []
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        
        crear_header(main, "Caja", "Módulo de ventas y facturación")
        
        # División en dos columnas
        cols = tk.Frame(main, bg=COLOR_SECUNDARIO)
        cols.pack(fill="both", expand=True, padx=40, pady=10)
        
        right = tk.Frame(cols, bg="#F9F9F9", width=350, padx=20, pady=20)
        right.pack(side="right", fill="both")
        
        left = tk.Frame(cols, bg=COLOR_SECUNDARIO)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Sección 1 del Panel Izquierdo: Cargar recetas
        receta_loader = tk.LabelFrame(left, text=" 🔌 INTEGRACIÓN DE CONSULTAS Y RECETAS ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, fg=COLOR_PRIMARIO, padx=15, pady=10)
        receta_loader.pack(fill="x", pady=(0, 15))
        
        tk.Label(receta_loader, text="Receta Médica:", bg=COLOR_SECUNDARIO).pack(side="left", padx=5)
        self.combo_consultas = ttk.Combobox(receta_loader, state="readonly", width=45)
        self.combo_consultas.pack(side="left", padx=5, fill="x", expand=True)
        
        tk.Button(receta_loader, text="⚡ CARGAR RECETA EN CARRITO", bg=COLOR_BOTON, fg="white", font=FUENTE_SMALL, command=self.cargar_receta_consulta).pack(side="left", padx=5)
        
        # Sección 2 del Panel Izquierdo: Buscador manual
        tk.Label(left, text="🔍 BUSCAR Y AGREGAR MANUALMENTE", font=FUENTE_HEADER, bg=COLOR_SECUNDARIO).pack(anchor="w")
        self.ent_prod = tk.Entry(left, font=FUENTE_NORMAL)
        self.ent_prod.pack(fill="x", pady=5)
        self.ent_prod.bind("<KeyRelease>", self.filtrar_prod)
        
        self.list_prod = tk.Listbox(left, height=6, font=FUENTE_NORMAL)
        self.list_prod.pack(fill="x")
        
        btn_add_manual = tk.Button(left, text="🛒 AÑADIR SELECCIONADO", bg=COLOR_BOTON, fg="white", font=FUENTE_NORMAL, command=self.add_to_cart)
        btn_add_manual.pack(pady=10, fill="x")
        
        tk.Label(left, text="🛒 DETALLE DEL CARRITO DE COMPRAS", font=FUENTE_HEADER, bg=COLOR_SECUNDARIO).pack(anchor="w", pady=(10, 0))
        self.tree_cart = ttk.Treeview(left, columns=("Nombre", "Cant", "Precio", "Total"), show="headings", height=8)
        for c in ("Nombre", "Cant", "Precio", "Total"): self.tree_cart.heading(c, text=c)
        self.tree_cart.pack(fill="x")
        
        # Panel de cobro (Derecha)
        tk.Label(right, text="RESUMEN DE FACTURACIÓN", font=FUENTE_SUBTITULO, bg="#F9F9F9", fg=COLOR_PRIMARIO).pack(pady=10)
        
        total_bg_frame = tk.Frame(right, bg=COLOR_ACENTO, padx=15, pady=15, highlightthickness=1, highlightbackground=COLOR_PRIMARIO)
        total_bg_frame.pack(fill="x", pady=10)
        
        self.lbl_sub = tk.Label(total_bg_frame, text="Subtotal: $0.00", bg=COLOR_ACENTO, font=FUENTE_NORMAL, fg=COLOR_TEXTO)
        self.lbl_sub.pack(anchor="w")
        self.lbl_iva = tk.Label(total_bg_frame, text="IVA (16%): $0.00", bg=COLOR_ACENTO, font=FUENTE_NORMAL, fg=COLOR_TEXTO)
        self.lbl_iva.pack(anchor="w")
        self.lbl_total = tk.Label(total_bg_frame, text="TOTAL: $0.00", bg=COLOR_ACENTO, font=FUENTE_SUBTITULO, fg=COLOR_PRIMARIO)
        self.lbl_total.pack(pady=(10, 0))
        
        tk.Label(right, text="DNI Cliente / Propietario:", bg="#F9F9F9", font=FUENTE_NORMAL).pack(anchor="w", pady=(15, 0))
        self.ent_dni = tk.Entry(right, font=FUENTE_NORMAL)
        self.ent_dni.pack(fill="x", pady=5)
        
        tk.Label(right, text="Método de Pago:", bg="#F9F9F9", font=FUENTE_NORMAL).pack(anchor="w", pady=(10, 0))
        self.combo_pago = ttk.Combobox(right, values=["Efectivo", "Tarjeta", "Transferencia"], state="readonly", font=FUENTE_NORMAL)
        self.combo_pago.pack(fill="x", pady=5)
        self.combo_pago.current(0)
        
        tk.Button(right, text="💵 GENERAR VENTA Y TICKET", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, pady=15, command=self.finalizar).pack(fill="x", pady=15)
        tk.Button(right, text="🗑️ VACIAR CARRITO", bg=COLOR_PELIGRO, fg="white", font=FUENTE_NORMAL, command=self.clear).pack(fill="x")

    def actualizar(self):
        self.sidebar.refrescar_menu()
        self.filtrar_prod(None)
        
        # Llenar menú desplegable de consultas con recetas pendientes
        self.combo_consultas['values'] = [
            f"{c.id_consulta} | Paciente: {c.paciente.nombre} ({c.fecha.strftime('%d/%m %H:%M')})"
            for c in self.controller.sistema.consultas if c.medicamentos
        ]
        if self.combo_consultas['values']:
            self.combo_consultas.current(0)
        else:
            self.combo_consultas.set("No hay recetas pendientes")

    def filtrar_prod(self, event):
        self.list_prod.delete(0, "end")
        q = self.ent_prod.get().lower()
        for p in self.controller.sistema.inventario:
            if q in p.nombre.lower() or q in p.id_producto.lower():
                self.list_prod.insert("end", f"{p.id_producto} | {p.nombre} | ${p.precio_unitario:.2f} ({p.stock} disp.)")

    def cargar_receta_consulta(self):
        sel_idx = self.combo_consultas.current()
        if sel_idx < 0:
            return messagebox.showwarning("Atención", "Por favor, seleccione una receta de la lista primero.")
        
        txt = self.combo_consultas.get()
        con_id = txt.split(" | ")[0]
        con = next((c for c in self.controller.sistema.consultas if c.id_consulta == con_id), None)
        if not con: return
        
        # Autocompletar DNI del propietario
        dni_prop = ""
        for prop in self.controller.sistema.propietarios:
            if con.paciente in prop.mascotas:
                dni_prop = prop.dni
                break
        
        if dni_prop:
            self.ent_dni.delete(0, 'end')
            self.ent_dni.insert(0, dni_prop)
        
        # Cargar productos automáticamente
        self.carrito = []
        meds_raw = con.medicamentos.split(";")
        for item_raw in meds_raw:
            if not item_raw: continue
            pid, cant_str = item_raw.split(":")
            cant = int(cant_str)
            prod = next((p for p in self.controller.sistema.inventario if p.id_producto == pid), None)
            if prod:
                stock_a_cargar = min(cant, prod.stock)
                if stock_a_cargar <= 0:
                    messagebox.showwarning("Sin Stock", f"El medicamento {prod.nombre} está agotado.")
                    continue
                if stock_a_cargar < cant:
                    messagebox.showwarning("Stock Insuficiente", f"Se ajustó {prod.nombre} de x{cant} a x{stock_a_cargar} por stock disponible.")
                
                self.carrito.append({
                    'id': pid, 'nombre': prod.nombre, 'precio': prod.precio_unitario,
                    'cantidad': stock_a_cargar, 'total': stock_a_cargar * prod.precio_unitario
                })
        
        # Agregar una tasa dinámica de consulta médica veterinaria
        self.carrito.append({
            'id': 'SERV-CONS', 'nombre': "Servicio: Consulta Médica Veterinaria", 'precio': 250.0,
            'cantidad': 1, 'total': 250.0
        })
        
        self.update_cart_view()
        messagebox.showinfo("Éxito", f"Se cargó la receta de {con.paciente.nombre} y la tasa de consulta.")

    def add_to_cart(self):
        sel = self.list_prod.curselection()
        if not sel: 
            return messagebox.showwarning("Atención", "Por favor, seleccione un producto de la lista primero.")
        txt = self.list_prod.get(sel[0])
        pid = txt.split(" | ")[0]
        prod = next((p for p in self.controller.sistema.inventario if p.id_producto == pid), None)
        if prod:
            if prod.stock <= 0: 
                return messagebox.showwarning("Sin Stock", f"No quedan unidades disponibles de {prod.nombre}")
            
            # Verificar si ya está en el carrito
            for item in self.carrito:
                if item['id'] == pid:
                    if item['cantidad'] >= prod.stock:
                        return messagebox.showwarning("Sin Stock", f"No puedes exceder el stock disponible ({prod.stock}) de {prod.nombre}")
                    item['cantidad'] += 1
                    item['total'] = item['cantidad'] * prod.precio_unitario
                    self.update_cart_view()
                    return
            self.carrito.append({'id': pid, 'nombre': prod.nombre, 'precio': prod.precio_unitario, 'cantidad': 1, 'total': prod.precio_unitario})
            self.update_cart_view()

    def update_cart_view(self):
        for i in self.tree_cart.get_children(): self.tree_cart.delete(i)
        sub = 0
        for item in self.carrito:
            self.tree_cart.insert("", "end", values=(item['nombre'], item['cantidad'], f"${item['precio']:.2f}", f"${item['total']:.2f}"))
            sub += item['total']
        
        iva = sub * 0.16
        total = sub + iva
        self.lbl_sub.config(text=f"Subtotal: ${sub:.2f}")
        self.lbl_iva.config(text=f"IVA (16%): ${iva:.2f}")
        self.lbl_total.config(text=f"TOTAL: ${total:.2f}")

    def clear(self):
        self.carrito = []
        self.update_cart_view()

    def finalizar(self):
        if not self.carrito: 
            return messagebox.showwarning("Carrito Vacío", "No hay ningún artículo en el carrito de compras para facturar.")
            
        dni = self.ent_dni.get().strip()
        if not dni:
            return messagebox.showwarning("Cliente Faltante", "Ingrese el DNI del propietario para registrar la venta.")
            
        prop = next((p for p in self.controller.sistema.propietarios if p.dni == dni), None)
        if not prop:
            return messagebox.showerror("Error", f"No se encontró ningún propietario registrado con el DNI: {dni}")
        
        sub = sum(item['total'] for item in self.carrito)
        factura = Factura(f"FAC-{datetime.now().strftime('%M%S')}", prop, sub, self.combo_pago.get(), self.carrito)
        
        # Descontar stock
        for item in self.carrito:
            if item['id'] == 'SERV-CONS': continue
            p = next((prod for prod in self.controller.sistema.inventario if prod.id_producto == item['id']), None)
            if p: p.actualizar_stock(-item['cantidad'])
        
        self.controller.sistema.guardar_inventario()
        
        # Guardar factura
        self.controller.sistema.facturas.append(factura)
        self.controller.sistema.guardar_facturas()
        
        ticket = factura.imprimir_ticket()
        
        # Mostrar ticket en una ventana nueva
        win = tk.Toplevel(self)
        win.title("Ticket de Venta")
        win.geometry("300x500")
        txt = tk.Text(win, font=("Courier New", 10))
        txt.insert("1.0", ticket)
        txt.pack(fill="both", expand=True)
        tk.Button(win, text="CERRAR", command=win.destroy).pack()
        
        messagebox.showinfo("Éxito", "Venta realizada y facturada correctamente")
        self.clear()

class PropietariosVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        
        # Barra lateral (Sidebar)
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        # Área principal
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        crear_header(main, "Clientes", "Gestión de dueños de mascotas y propietarios")
        
        # Tarjeta estilizada para el registro
        card = tk.Frame(main, bg="white", bd=1, relief="solid", highlightthickness=0)
        card.pack(fill="x", padx=40, pady=15)
        
        # Encabezado / Título de la tarjeta
        card_title = tk.Label(card, text="👥 REGISTRO DE NUEVO PROPIETARIO", bg="white", fg=COLOR_PRIMARIO, font=FUENTE_HEADER, pady=10, anchor="w")
        card_title.pack(fill="x", padx=20)
        
        # Contenedor de entradas del formulario
        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        fields = ["DNI", "Nombre", "Teléfono", "Correo"]
        self.ents = {}
        
        for i, lbl in enumerate(fields):
            col = tk.Frame(form_frame, bg="white")
            col.grid(row=0, column=i, padx=10, sticky="ew")
            form_frame.columnconfigure(i, weight=1)
            
            label_text = f"{lbl} *" if lbl in ["DNI", "Nombre"] else lbl
            tk.Label(col, text=label_text, bg="white", fg="#555555", font=("Arial", 9, "bold"), anchor="w").pack(fill="x", pady=(0, 3))
            
            e = tk.Entry(col, font=FUENTE_NORMAL, bg="#f9f9f9", relief="flat", bd=0, highlightthickness=1, highlightbackground="#cccccc", highlightcolor=COLOR_PRIMARIO)
            e.pack(fill="x", ipady=6)
            self.ents[lbl] = e
            
        btn_col = tk.Frame(form_frame, bg="white")
        btn_col.grid(row=0, column=len(fields), padx=10, sticky="ew")
        form_frame.columnconfigure(len(fields), weight=1)
        
        tk.Label(btn_col, text="", bg="white", font=("Arial", 9)).pack(fill="x", pady=(0, 3))
        btn = tk.Button(
            btn_col, text="💾 GUARDAR PROPIETARIO", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, 
            relief="flat", cursor="hand2", activebackground="#2c7a4b", activeforeground="white",
            command=self.guardar
        )
        btn.pack(fill="x", ipady=4)
        
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#277043"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=COLOR_BOTON))

        # Contenedor de Treeview estilizado
        tree_frame = tk.Frame(main, bg="white", bd=1, relief="solid")
        tree_frame.pack(fill="both", expand=True, padx=40, pady=(10, 30))
        
        style = ttk.Style()
        style.configure("Custom.Treeview", font=FUENTE_NORMAL, rowheight=30)
        style.configure("Custom.Treeview.Heading", font=FUENTE_HEADER, background="#e8f5e9", foreground=COLOR_PRIMARIO)
        
        self.tree = ttk.Treeview(
            tree_frame, columns=("DNI", "Nombre", "Teléfono", "Correo"), 
            show="headings", style="Custom.Treeview"
        )
        
        cols_config = {
            "DNI": {"width": 120, "anchor": "center"},
            "Nombre": {"width": 250, "anchor": "w"},
            "Teléfono": {"width": 150, "anchor": "center"},
            "Correo": {"width": 250, "anchor": "w"}
        }
        
        for col_name, conf in cols_config.items():
            self.tree.heading(col_name, text=col_name, anchor="center")
            self.tree.column(col_name, width=conf["width"], anchor=conf["anchor"])
            
        sb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        self.tree.tag_configure("even", background="#ffffff")
        self.tree.tag_configure("odd", background="#f5f7f6")

    def actualizar(self):
        self.sidebar.refrescar_menu()
        for i in self.tree.get_children(): self.tree.delete(i)
        for idx, p in enumerate(self.controller.sistema.propietarios):
            tag = "odd" if idx % 2 != 0 else "even"
            self.tree.insert("", "end", values=(p.dni, p.nombre, p.telefono, p.correo), tags=(tag,))

    def guardar(self):
        d = {k: v.get().strip() for k, v in self.ents.items()}
        if not d["DNI"] or not d["Nombre"]: 
            return messagebox.showwarning("Campos Vacíos", "Por favor, complete los campos obligatorios (*): DNI y Nombre.")
            
        if any(p.dni == d["DNI"] for p in self.controller.sistema.propietarios):
            return messagebox.showerror("Duplicado", f"Ya existe un propietario registrado con el DNI: {d['DNI']}.")
            
        nuevo = Propietario(d["DNI"], d["Nombre"], d["Teléfono"], d["Correo"], "Dirección Pendiente")
        self.controller.sistema.propietarios.append(nuevo)
        self.controller.sistema.guardar_propietarios()
        
        for e in self.ents.values():
            e.delete(0, 'end')
            
        self.actualizar()
        messagebox.showinfo("Éxito", "Propietario registrado correctamente.")

class EmpleadosVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        crear_header(main, "Personal", "Gestión de usuarios del sistema")
        
        # División en columnas
        cols = tk.Frame(main, bg=COLOR_SECUNDARIO)
        cols.pack(fill="both", expand=True, padx=40, pady=10)
        
        right = tk.LabelFrame(cols, text=" NUEVO EMPLEADO ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, padx=20, pady=20, width=380)
        right.pack(side="right", fill="both")
        
        left = tk.Frame(cols, bg=COLOR_SECUNDARIO)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        self.tree = ttk.Treeview(left, columns=("ID", "Nombre", "Rol", "Especialidad"), show="headings")
        for c in ("ID", "Nombre", "Rol", "Especialidad"): self.tree.heading(c, text=c)
        self.tree.pack(fill="both", expand=True)
        
        # Campos del formulario
        tk.Label(right, text="ID Usuario:", bg=COLOR_SECUNDARIO).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_id = tk.Entry(right, font=FUENTE_NORMAL, width=20)
        self.ent_id.grid(row=0, column=1, pady=5)
        
        tk.Label(right, text="Nombre:", bg=COLOR_SECUNDARIO).grid(row=1, column=0, sticky="w", pady=5)
        self.ent_nombre = tk.Entry(right, font=FUENTE_NORMAL, width=20)
        self.ent_nombre.grid(row=1, column=1, pady=5)
        
        tk.Label(right, text="Contraseña:", bg=COLOR_SECUNDARIO).grid(row=2, column=0, sticky="w", pady=5)
        self.ent_pass = tk.Entry(right, font=FUENTE_NORMAL, show="*", width=20)
        self.ent_pass.grid(row=2, column=1, pady=5)
        
        tk.Label(right, text="Rol:", bg=COLOR_SECUNDARIO).grid(row=3, column=0, sticky="w", pady=5)
        self.combo_rol = ttk.Combobox(right, values=["Administrador", "Veterinario"], state="readonly", width=18)
        self.combo_rol.grid(row=3, column=1, pady=5)
        self.combo_rol.current(0)
        
        # Campos estáticos para ambos roles
        tk.Label(right, text="Cédula Prof.:", bg=COLOR_SECUNDARIO).grid(row=4, column=0, sticky="w", pady=5)
        self.ent_cedula = tk.Entry(right, font=FUENTE_NORMAL, width=20)
        self.ent_cedula.grid(row=4, column=1, pady=5)
        
        tk.Label(right, text="Especialidad:", bg=COLOR_SECUNDARIO).grid(row=5, column=0, sticky="w", pady=5)
        self.ent_esp = tk.Entry(right, font=FUENTE_NORMAL, width=20)
        self.ent_esp.grid(row=5, column=1, pady=5)
        
        tk.Label(right, text="Horario:", bg=COLOR_SECUNDARIO).grid(row=6, column=0, sticky="w", pady=5)
        self.ent_horario = tk.Entry(right, font=FUENTE_NORMAL, width=20)
        self.ent_horario.grid(row=6, column=1, pady=5)
        
        tk.Button(right, text="REGISTRAR EMPLEADO", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, command=self.guardar_empleado).grid(row=7, column=0, columnspan=2, pady=20, sticky="ew")

    def guardar_empleado(self):
        uid = self.ent_id.get()
        nom = self.ent_nombre.get()
        pwd = self.ent_pass.get()
        rol = self.combo_rol.get()
        
        if not uid or not nom or not pwd or not rol:
            return messagebox.showerror("Error", "Todos los campos básicos son requeridos")
            
        if any(u.id_usuario == uid for u in self.controller.sistema.usuarios):
            return messagebox.showerror("Error", "ID Usuario ya existe")
            
        try:
            if rol == "Administrador":
                try:
                    niv = int(self.ent_cedula.get() or 1)
                except ValueError:
                    niv = 1
                dep = self.ent_esp.get() or "General"
                nuevo = Administrador(uid, nom, pwd, niv, dep)
            else:
                ced = self.ent_cedula.get().strip()
                if not (ced.isdigit() and len(ced) in [7, 8]):
                    return messagebox.showerror("Cédula Profesional Inválida", "La cédula profesional de un Veterinario debe constar únicamente de 7 u 8 dígitos numéricos.")
                esp = self.ent_esp.get() or "General"
                hor = self.ent_horario.get() or "09:00 - 18:00"
                nuevo = Veterinario(uid, nom, pwd, ced, esp, hor)
                
            self.controller.sistema.usuarios.append(nuevo)
            self.controller.sistema.guardar_usuarios()
            self.actualizar()
            
            # Limpiar formulario
            self.ent_id.delete(0, 'end')
            self.ent_nombre.delete(0, 'end')
            self.ent_pass.delete(0, 'end')
            self.ent_cedula.delete(0, 'end')
            self.ent_esp.delete(0, 'end')
            self.ent_horario.delete(0, 'end')
            self.combo_rol.set('Administrador')
            
            messagebox.showinfo("Éxito", f"Empleado {nom} registrado correctamente")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        self.sidebar.refrescar_menu()
        for i in self.tree.get_children(): self.tree.delete(i)
        for u in self.controller.sistema.usuarios:
            extra = getattr(u, 'especialidad', getattr(u, 'departamento', 'N/A'))
            self.tree.insert("", "end", values=(u.id_usuario, u.nombre, u.rol, extra))

class ConsultasVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        self.receta_items = []
        self.cita_seleccionada = None
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        crear_header(main, "Consultorio", "Atención Médica y Registro Clínico")
        
        cols = tk.Frame(main, bg=COLOR_SECUNDARIO)
        cols.pack(fill="both", expand=True, padx=40, pady=10)
        
        right = tk.LabelFrame(cols, text=" CONSULTA MÉDICA ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, padx=20, pady=15, width=420)
        right.pack(side="right", fill="both")
        
        left = tk.Frame(cols, bg=COLOR_SECUNDARIO)
        left.pack(side="left", fill="both", expand=True, padx=(0, 20))
        
        # Izquierda: Lista de Citas
        tk.Label(left, text="CITAS EN ESPERA / PROGRAMADAS", font=FUENTE_HEADER, bg=COLOR_SECUNDARIO, fg=COLOR_PRIMARIO).pack(anchor="w", pady=(0, 5))
        
        # Contenedor para Treeview y barra de desplazamiento
        tree_container = tk.Frame(left, bg=COLOR_SECUNDARIO)
        tree_container.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(tree_container, columns=("CitaID", "Paciente", "Fecha", "Hora", "Motivo"), show="headings", height=15)
        
        # Configurar columnas con anchos específicos para evitar recortes
        cols_config = {
            "CitaID": {"width": 60, "anchor": "center"},
            "Paciente": {"width": 95, "anchor": "w"},
            "Fecha": {"width": 95, "anchor": "center"},
            "Hora": {"width": 65, "anchor": "center"},
            "Motivo": {"width": 140, "anchor": "w"}
        }
        for col_name, conf in cols_config.items():
            self.tree.heading(col_name, text=col_name, anchor="center")
            self.tree.column(col_name, width=conf["width"], anchor=conf["anchor"])
            
        sb_y = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb_y.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        sb_y.pack(side="right", fill="y")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_cita_select)
        
        # Derecha: Formulario de Consulta
        self.lbl_paciente_info = tk.Label(right, text="Seleccione una cita de la lista", font=FUENTE_NORMAL, fg=COLOR_TEXTO_LIGHT, bg=COLOR_SECUNDARIO, justify="left", anchor="w")
        self.lbl_paciente_info.pack(fill="x", pady=(0, 15))
        
        # Diseño de cuadrícula para valores
        form_frame = tk.Frame(right, bg=COLOR_SECUNDARIO)
        form_frame.pack(fill="x")
        
        tk.Label(form_frame, text="Peso Actual (kg):", bg=COLOR_SECUNDARIO).grid(row=0, column=0, sticky="w", pady=5)
        self.ent_peso = tk.Entry(form_frame, font=FUENTE_NORMAL, width=15)
        self.ent_peso.grid(row=0, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Temp. (°C):", bg=COLOR_SECUNDARIO).grid(row=0, column=2, sticky="w", pady=5)
        self.ent_temp = tk.Entry(form_frame, font=FUENTE_NORMAL, width=15)
        self.ent_temp.grid(row=0, column=3, pady=5, padx=5)
        
        tk.Label(form_frame, text="Freq. Card. (lpm):", bg=COLOR_SECUNDARIO).grid(row=1, column=0, sticky="w", pady=5)
        self.ent_fc = tk.Entry(form_frame, font=FUENTE_NORMAL, width=15)
        self.ent_fc.grid(row=1, column=1, pady=5, padx=5)
        
        tk.Label(form_frame, text="Diagnóstico:", bg=COLOR_SECUNDARIO).grid(row=2, column=0, sticky="nw", pady=5)
        self.ent_diag = tk.Text(form_frame, font=FUENTE_NORMAL, height=3, width=40, relief="solid", bd=1, highlightthickness=0)
        self.ent_diag.grid(row=2, column=1, columnspan=3, pady=5, padx=5, sticky="ew")
        
        tk.Label(form_frame, text="Tratamiento:", bg=COLOR_SECUNDARIO).grid(row=3, column=0, sticky="nw", pady=5)
        self.ent_trata = tk.Text(form_frame, font=FUENTE_NORMAL, height=3, width=40, relief="solid", bd=1, highlightthickness=0)
        self.ent_trata.grid(row=3, column=1, columnspan=3, pady=5, padx=5, sticky="ew")
        
        # Receta (Marco de Receta)
        receta_frame = tk.LabelFrame(right, text=" RECETA / MEDICAMENTOS ", bg=COLOR_SECUNDARIO, font=FUENTE_SMALL, padx=10, pady=10)
        receta_frame.pack(fill="both", expand=True, pady=10)
        
        tk.Label(receta_frame, text="Insumo:", bg=COLOR_SECUNDARIO).grid(row=0, column=0, sticky="w")
        self.combo_insumo = ttk.Combobox(receta_frame, state="readonly", width=22)
        self.combo_insumo.grid(row=0, column=1, padx=5)
        
        tk.Label(receta_frame, text="Cant:", bg=COLOR_SECUNDARIO).grid(row=0, column=2, sticky="w")
        self.ent_cant = tk.Entry(receta_frame, width=5)
        self.ent_cant.grid(row=0, column=3, padx=5)
        self.ent_cant.insert(0, "1")
        
        tk.Button(receta_frame, text="Añadir", bg=COLOR_BOTON, fg="white", font=FUENTE_SMALL, command=self.add_medicamento).grid(row=0, column=4, padx=5)
        
        self.list_receta = tk.Listbox(receta_frame, height=5, font=FUENTE_SMALL)
        self.list_receta.grid(row=1, column=0, columnspan=5, sticky="ew", pady=(10, 0))
        
        # Acciones
        btn_action_frame = tk.Frame(right, bg=COLOR_SECUNDARIO)
        btn_action_frame.pack(fill="x", pady=10)
        tk.Button(btn_action_frame, text="GUARDAR CONSULTA Y COMPLETAR", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, pady=10, command=self.finalizar_consulta).pack(fill="x", side="left", expand=True)
        tk.Button(btn_action_frame, text="LIMPIAR RECETA", bg=COLOR_PELIGRO, fg="white", command=self.limpiar_receta).pack(fill="x", side="right", padx=5)

    def on_cita_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        cid = self.tree.item(sel[0])['values'][0]
        self.cita_seleccionada = next((c for c in self.controller.sistema.citas if str(c.id_cita) == str(cid)), None)
        
        if self.cita_seleccionada:
            p = self.cita_seleccionada.paciente
            info = f"PACIENTE: {p.nombre} ({p.especie})\nRAZA: {p.raza} | PESO REG.: {p.peso_actual} kg\nMOTIVO: {self.cita_seleccionada.motivo}"
            self.lbl_paciente_info.config(text=info, fg=COLOR_PRIMARIO, font=FUENTE_HEADER)
            self.ent_peso.delete(0, 'end')
            self.ent_peso.insert(0, str(p.peso_actual))
            self.ent_temp.delete(0, 'end')
            self.ent_fc.delete(0, 'end')
            self.ent_diag.delete("1.0", "end")
            self.ent_trata.delete("1.0", "end")
            self.receta_items = []
            self.list_receta.delete(0, 'end')

    def add_medicamento(self):
        sel_idx = self.combo_insumo.current()
        if sel_idx < 0: return
        txt = self.combo_insumo.get()
        pid = txt.split(" | ")[0]
        prod = next((p for p in self.controller.sistema.inventario if p.id_producto == pid), None)
        try:
            cant = int(self.ent_cant.get())
            if not prod or cant <= 0: raise ValueError
            if prod.stock < cant:
                return messagebox.showwarning("Stock Bajo", f"Solo quedan {prod.stock} unidades de {prod.nombre}")
            
            # Verificar si ya fue agregado
            for item in self.receta_items:
                if item['id'] == pid:
                    item['cantidad'] += cant
                    self.actualizar_receta_lista()
                    return
            self.receta_items.append({'id': pid, 'nombre': prod.nombre, 'cantidad': cant})
            self.actualizar_receta_lista()
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")

    def actualizar_receta_lista(self):
        self.list_receta.delete(0, 'end')
        for item in self.receta_items:
            self.list_receta.insert('end', f"{item['nombre']} x{item['cantidad']}")

    def limpiar_receta(self):
        self.receta_items = []
        self.list_receta.delete(0, 'end')

    def finalizar_consulta(self):
        if not self.cita_seleccionada:
            return messagebox.showwarning("Atención", "Seleccione una cita en espera")
            
        try:
            peso = float(self.ent_peso.get())
            temp = float(self.ent_temp.get() or 38.5)
            fc = int(self.ent_fc.get() or 80)
            diag = self.ent_diag.get("1.0", "end-1c").strip()
            trata = self.ent_trata.get("1.0", "end-1c").strip()
            
            if not diag or not trata:
                return messagebox.showerror("Error", "Diagnóstico y Tratamiento son requeridos")
                
            p = self.cita_seleccionada.paciente
            vet = self.controller.sistema.usuario_actual
            if not isinstance(vet, Veterinario):
                vet = next((u for u in self.controller.sistema.usuarios if isinstance(u, Veterinario)), None)
                if not vet:
                    return messagebox.showerror("Error", "No hay un Veterinario asignado para realizar la consulta")
            
            # Create Consulta
            con_id = f"CON-{datetime.now().strftime('%M%S')}"
            meds_str = ";".join([f"{item['id']}:{item['cantidad']}" for item in self.receta_items])
            nueva_con = Consulta(con_id, p, vet, temp, fc, diag, trata, medicamentos=meds_str)
            self.controller.sistema.consultas.append(nueva_con)
            p.historial_consultas.append(nueva_con)
            
            # Actualizar peso del paciente
            p.actualizar_peso(peso)
            
            # Completar Cita
            self.cita_seleccionada.cambiar_estado("Completada")
            
            # Descontar stock de medicamentos
            for item in self.receta_items:
                prod = next((pr for pr in self.controller.sistema.inventario if pr.id_producto == item['id']), None)
                if prod: prod.actualizar_stock(-item['cantidad'])
            
            # Guardar todo
            self.controller.sistema.guardar_todo()
            
            # Mostrar ticket / Resumen de receta
            receta_txt = "--- RECETA VETERINARIA ---\n"
            receta_txt += f"Consulta: {con_id}\nFecha: {datetime.now().strftime('%Y-%m-%d')}\n"
            receta_txt += f"Paciente: {p.nombre}\nVeterinario: Dr. {vet.nombre}\n"
            receta_txt += "="*25 + "\n"
            receta_txt += f"Diagnóstico: {diag}\n"
            receta_txt += f"Tratamiento: {trata}\n"
            receta_txt += "="*25 + "\nMedicamentos:\n"
            for item in self.receta_items:
                receta_txt += f"- {item['nombre']} x{item['cantidad']}\n"
            
            win = tk.Toplevel(self)
            win.title("Receta e Historial")
            win.geometry("300x500")
            txt = tk.Text(win, font=("Courier New", 10))
            txt.insert("1.0", receta_txt)
            txt.pack(fill="both", expand=True)
            tk.Button(win, text="CERRAR", command=win.destroy).pack()
            
            messagebox.showinfo("Éxito", "Consulta registrada y cita completada con éxito.")
            self.cita_seleccionada = None
            self.lbl_paciente_info.config(text="Seleccione una cita de la lista", fg=COLOR_TEXTO_LIGHT, font=FUENTE_NORMAL)
            
            # Limpiar todos los campos del formulario de consulta
            self.ent_peso.delete(0, 'end')
            self.ent_temp.delete(0, 'end')
            self.ent_fc.delete(0, 'end')
            self.ent_diag.delete("1.0", "end")
            self.ent_trata.delete("1.0", "end")
            self.receta_items = []
            self.list_receta.delete(0, 'end')
            
            self.actualizar()
            
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos en Peso, Temp y Freq. Cardíaca")

    def actualizar(self):
        self.sidebar.refrescar_menu()
        
        # Cargar citas pendientes/confirmadas
        for i in self.tree.get_children(): self.tree.delete(i)
        for c in sorted(self.controller.sistema.citas, key=lambda x: (x.fecha, x.hora)):
            if c.estado in ["Pendiente", "Confirmada"]:
                self.tree.insert("", "end", values=(c.id_cita, c.paciente.nombre, c.fecha, c.hora, c.motivo))
                
        # Llenar combobox de inventario
        self.combo_insumo['values'] = [f"{p.id_producto} | {p.nombre} ({p.stock} disp.)" for p in self.controller.sistema.inventario]
        if self.combo_insumo['values']:
            self.combo_insumo.current(0)

class ReportesVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        crear_header(main, "Estadísticas", "Análisis de rendimiento de la clínica")
        
        btn_frame = tk.Frame(main, bg=COLOR_SECUNDARIO)
        btn_frame.pack(fill="x", padx=40, pady=10)
        
        tk.Button(btn_frame, text="📊 VER VISITAS POR MES", font=FUENTE_SUBTITULO, bg=COLOR_BOTON, fg="white", pady=10, command=self.mostrar_visitas).pack(side="left", padx=10)
        tk.Button(btn_frame, text="📈 REPORTE DE VENTAS", font=FUENTE_SUBTITULO, bg=COLOR_BOTON, fg="white", pady=10, command=self.mostrar_ventas).pack(side="left", padx=10)
        
        self.grafico_frame = tk.Frame(main, bg=COLOR_SECUNDARIO)
        self.grafico_frame.pack(fill="both", expand=True, padx=40, pady=20)
        self.canvas_widget = None

    def limpiar_grafico(self):
        if self.canvas_widget:
            self.canvas_widget.destroy()
            self.canvas_widget = None

    def mostrar_visitas(self):
        self.limpiar_grafico()
        # Creamos la figura con el color de fondo exacto de la ventana
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=COLOR_SECUNDARIO)
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLOR_SECUNDARIO)
        
        citas = self.controller.sistema.citas
        if not citas:
            ax.text(0.5, 0.5, 'No hay datos de citas registrados', ha='center', va='center', 
                    fontsize=13, fontweight='bold', color=COLOR_TEXTO_LIGHT, family='Segoe UI')
            ax.set_title("Citas por Día", fontsize=16, fontweight='bold', color=COLOR_PRIMARIO, family='Segoe UI', pad=25)
            # Quitar ejes si no hay datos
            for spine in ax.spines.values(): spine.set_visible(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        else:
            df = pd.DataFrame([c.__dict__ for c in citas])
            # Asegurar tipo de fecha y agrupar por día
            df['fecha_dt'] = pd.to_datetime(df['fecha']).dt.date
            conteos = df.groupby('fecha_dt').size().sort_index()
            
            # Formatear etiquetas del eje X como "Día de Mes" en español
            meses_es = {
                'Jan': 'Ene', 'Feb': 'Feb', 'Mar': 'Mar', 'Apr': 'Abr', 'May': 'May', 'Jun': 'Jun',
                'Jul': 'Jul', 'Aug': 'Ago', 'Sep': 'Sep', 'Oct': 'Oct', 'Nov': 'Nov', 'Dec': 'Dic'
            }
            x_labels = []
            for d in conteos.index:
                dt_obj = pd.to_datetime(d)
                eng_mon = dt_obj.strftime('%b')
                esp_mon = meses_es.get(eng_mon, eng_mon)
                x_labels.append(f"{dt_obj.day} de {esp_mon}")
            
            # Dibujar barras elegantes con anchos controlados y zorder
            bars = ax.bar(x_labels, conteos.values, color=COLOR_BOTON, edgecolor='none', width=0.4, zorder=3)
            
            # Título y etiquetas estéticos
            ax.set_title("Cantidad de Citas por Día", pad=25, fontsize=16, fontweight='bold', color=COLOR_PRIMARIO, family='Segoe UI')
            ax.set_ylabel("Cantidad de Citas", fontsize=11, fontweight='bold', color=COLOR_TEXTO_LIGHT, family='Segoe UI', labelpad=12)
            
            # Cuadrícula horizontal extremadamente suave
            ax.grid(axis='y', linestyle='-', linewidth=0.5, color='#E0E0E0', zorder=0)
            
            # Ocultar espinas (bordes) superior y derecha para un acabado premium flat
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E0E0E0')
            ax.spines['bottom'].set_color('#E0E0E0')
            
            # Formato de los textos de los ejes
            ax.tick_params(axis='both', colors=COLOR_TEXTO, labelsize=10)
            
            # Rotar automáticamente si hay varias fechas para evitar superposiciones
            if len(conteos) > 4:
                fig.autofmt_xdate()
            
            # Agregar etiquetas de valores sobre las barras utilizando el método nativo optimizado
            ax.bar_label(bars, padding=6, fontsize=10, fontweight='bold', color=COLOR_PRIMARIO, family='Segoe UI')
            
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def mostrar_ventas(self):
        self.limpiar_grafico()
        # Creamos la figura con el color de fondo exacto de la ventana
        fig = Figure(figsize=(8, 5), dpi=100, facecolor=COLOR_SECUNDARIO)
        ax = fig.add_subplot(111)
        ax.set_facecolor(COLOR_SECUNDARIO)
        
        facturas = self.controller.sistema.facturas
        if not facturas:
            ax.text(0.5, 0.5, 'No hay datos de ventas registrados', ha='center', va='center', 
                    fontsize=13, fontweight='bold', color=COLOR_TEXTO_LIGHT, family='Segoe UI')
            ax.set_title("Ventas por Día", fontsize=16, fontweight='bold', color=COLOR_PRIMARIO, family='Segoe UI', pad=25)
            # Quitar ejes si no hay datos
            for spine in ax.spines.values(): spine.set_visible(False)
            ax.get_xaxis().set_visible(False)
            ax.get_yaxis().set_visible(False)
        else:
            df = pd.DataFrame([{ 'fecha': f.fecha, 'total': f.total } for f in facturas])
            df['fecha'] = pd.to_datetime(df['fecha']).dt.date
            ventas_dia = df.groupby('fecha')['total'].sum()
            
            # Dibujar un gráfico de área moderno y premium (línea gruesa + relleno sombreado)
            ax.plot(ventas_dia.index, ventas_dia.values, color=COLOR_PRIMARIO, linestyle='-', linewidth=3, 
                    marker='o', markersize=8, markerfacecolor='white', markeredgewidth=2.5, markeredgecolor=COLOR_PRIMARIO, zorder=3)
            ax.fill_between(ventas_dia.index, ventas_dia.values, color=COLOR_PRIMARIO, alpha=0.1, zorder=2)
            
            # Título y etiquetas estéticos
            ax.set_title("Ventas Totales por Día ($)", pad=25, fontsize=16, fontweight='bold', color=COLOR_PRIMARIO, family='Segoe UI')
            ax.set_ylabel("Ingresos totales ($ MXN)", fontsize=11, fontweight='bold', color=COLOR_TEXTO_LIGHT, family='Segoe UI', labelpad=12)
            
            # Cuadrícula muy sutil y elegante
            ax.grid(True, linestyle='-', linewidth=0.5, color='#E0E0E0', zorder=0)
            
            # Ocultar espinas (bordes) superior y derecha
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#E0E0E0')
            ax.spines['bottom'].set_color('#E0E0E0')
            
            # Formato de ticks y fechas rotadas
            ax.tick_params(axis='both', colors=COLOR_TEXTO, labelsize=10)
            fig.autofmt_xdate()
            
            # Anotaciones estilizadas arriba de cada punto
            for i, txt in enumerate(ventas_dia.values):
                ax.annotate(f"${txt:,.2f}", (ventas_dia.index[i], ventas_dia.values[i]), 
                            textcoords="offset points", xytext=(0, 12), ha='center',
                            fontsize=9, fontweight='bold', color=COLOR_PRIMARIO, family='Segoe UI')
            
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def actualizar(self): self.sidebar.refrescar_menu()

# --- SERVIDOR REST API LOCAL EN SEGUNDO PLANO ---
import threading
api_server = None
api_thread = None

def run_api_server(port, sistema):
    global api_server
    from http.server import HTTPServer, BaseHTTPRequestHandler
    import json
    
    class APIHandler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Silenciar salida normal de logs para evitar spam en consola
            
        def do_GET(self):
            if self.path == '/api/pacientes':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                data = [{'id': p.id_paciente, 'nombre': p.nombre, 'especie': p.especie, 'raza': p.raza, 'peso': p.peso_actual} for p in sistema.pacientes]
                self.wfile.write(json.dumps(data).encode('utf-8'))
            elif self.path == '/api/inventario':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                data = [{'id': i.id_producto, 'nombre': i.nombre, 'stock': i.stock, 'precio': i.precio_unitario} for i in sistema.inventario]
                self.wfile.write(json.dumps(data).encode('utf-8'))
            elif self.path == '/api/citas':
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                data = [{'id': c.id_cita, 'fecha': str(c.fecha), 'hora': c.hora, 'paciente': c.paciente.nombre, 'motivo': c.motivo, 'estado': c.estado} for c in sistema.citas]
                self.wfile.write(json.dumps(data).encode('utf-8'))
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Endpoint no encontrado'}).encode('utf-8'))

    try:
        api_server = HTTPServer(('localhost', port), APIHandler)
        api_server.serve_forever()
    except Exception as e:
        print(f"Error en servidor REST API: {e}")

def stop_api_server():
    global api_server
    if api_server:
        api_server.shutdown()
        api_server.server_close()
        api_server = None

class ConfiguracionVista(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_SECUNDARIO)
        self.controller = controller
        self.sidebar = Sidebar(self, controller)
        self.sidebar.pack(side="left", fill="y")
        
        main = tk.Frame(self, bg=COLOR_SECUNDARIO)
        main.pack(side="right", fill="both", expand=True)
        crear_header(main, "Conectividad & APIs", "Asistente de Razas y Reportes Clínicos")
        
        self.cols = tk.Frame(main, bg=COLOR_SECUNDARIO)
        self.cols.pack(fill="both", expand=True, padx=40, pady=10)
        
        # Panel Izquierdo: Enciclopedia
        self.left = tk.LabelFrame(self.cols, text=" 🐶 ASISTENTE DE RAZAS VETERINARIAS (API) ", bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, fg=COLOR_PRIMARIO, padx=20, pady=20)
        
        tk.Label(self.left, text="Seleccione una raza de interés:", bg=COLOR_SECUNDARIO, font=FUENTE_NORMAL).pack(anchor="w")
        self.combo_razas = ttk.Combobox(self.left, state="readonly", font=FUENTE_NORMAL)
        self.combo_razas.pack(fill="x", pady=10)
        
        # Acciones para razas (Consultar, Agregar, Editar)
        breed_actions = tk.Frame(self.left, bg=COLOR_SECUNDARIO)
        breed_actions.pack(fill="x", pady=(5, 10))
        
        btn_consultar = tk.Button(breed_actions, text="🔍 CONSULTAR", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, command=self.fetch_breed_info)
        btn_consultar.pack(side="left", fill="x", expand=True, padx=(0, 5))
        
        btn_agregar = tk.Button(breed_actions, text="➕ AGREGAR", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, command=self.abrir_formulario_raza)
        btn_agregar.pack(side="left", fill="x", expand=True, padx=5)
        
        btn_editar = tk.Button(breed_actions, text="✏️ EDITAR", bg="#FFA000", fg="white", font=FUENTE_HEADER, command=self.abrir_formulario_raza_edicion)
        btn_editar.pack(side="left", fill="x", expand=True, padx=(5, 0))
        
        # Área de visualización de información
        self.info_frame = tk.Frame(self.left, bg=COLOR_ACENTO, padx=15, pady=15, highlightthickness=1, highlightbackground=COLOR_PRIMARIO)
        self.info_frame.pack(fill="both", expand=True, pady=15)
        
        self.lbl_raza_title = tk.Label(self.info_frame, text="Raza: Seleccione una", font=FUENTE_SUBTITULO, fg=COLOR_PRIMARIO, bg=COLOR_ACENTO)
        self.lbl_raza_title.pack(anchor="w", pady=(0, 10))
        
        self.lbl_raza_details = tk.Label(self.info_frame, text="Presione el botón para consultar los datos técnicos e instrucciones de cuidado veterinario.", font=FUENTE_NORMAL, fg=COLOR_TEXTO, bg=COLOR_ACENTO, justify="left", wraplength=450)
        self.lbl_raza_details.pack(anchor="w")
        
        # Panel Derecho: Panel de Administración
        self.right = tk.LabelFrame(self.cols, bg=COLOR_SECUNDARIO, font=FUENTE_HEADER, fg=COLOR_PRIMARIO, padx=20, pady=20, width=420)

    def fetch_breed_info(self):
        raza = self.combo_razas.get()
        if not raza: return
        
        # Simulación de carga de API (pantalla de carga UX / spinner)
        win = tk.Toplevel(self)
        win.title("Consultando API externa...")
        win.geometry("300x120")
        win.transient(self)
        win.grab_set()
        
        tk.Label(win, text="🐾 Solicitando datos a The Dog/Cat API...", font=FUENTE_NORMAL).pack(pady=20)
        prog = ttk.Progressbar(win, mode="indeterminate", length=200)
        prog.pack()
        prog.start()
        
        def done():
            win.destroy()
            info = self.controller.sistema.razas.get(raza, {})
            self.lbl_raza_title.config(text=f"Raza: {raza}")
            det_text = f"• Grupo: {info.get('tipo', 'N/A')}\n" \
                       f"• Esperanza de Vida: {info.get('vida', 'N/A')}\n" \
                       f"• Temperamento: {info.get('temperamento', 'N/A')}\n\n" \
                       f"• Cuidados Clínicos Recomendados:\n{info.get('cuidados', 'N/A')}"
            self.lbl_raza_details.config(text=det_text)
            
        self.after(1000, done)

    def abrir_formulario_raza(self, editar_raza=None):
        win = tk.Toplevel(self)
        win.title("Agregar Raza" if not editar_raza else "Editar Detalles de Raza")
        win.geometry("450x580")
        win.transient(self)
        win.grab_set()
        
        tk.Label(win, text="🏆 DATOS DE LA RAZA", font=FUENTE_SUBTITULO, fg=COLOR_PRIMARIO).pack(pady=15)
        
        form = tk.Frame(win, padx=20)
        form.pack(fill="both", expand=True)
        
        # Nombre
        tk.Label(form, text="Nombre de la Raza *:", font=FUENTE_HEADER).pack(anchor="w")
        ent_nombre = tk.Entry(form, font=FUENTE_NORMAL)
        ent_nombre.pack(fill="x", pady=(3, 10))
        if editar_raza:
            ent_nombre.insert(0, editar_raza)
            ent_nombre.config(state="disabled") # No se puede cambiar el nombre al editar
            
        # Grupo/Tipo
        tk.Label(form, text="Grupo o Tipo * (ej: Perro de Trabajo, Felino Exótico):", font=FUENTE_HEADER).pack(anchor="w")
        ent_tipo = tk.Entry(form, font=FUENTE_NORMAL)
        ent_tipo.pack(fill="x", pady=(3, 10))
        
        # Esperanza de Vida
        tk.Label(form, text="Esperanza de Vida (ej: 10 - 12 años):", font=FUENTE_HEADER).pack(anchor="w")
        ent_vida = tk.Entry(form, font=FUENTE_NORMAL)
        ent_vida.pack(fill="x", pady=(3, 10))
        
        # Temperamento
        tk.Label(form, text="Temperamento * (ej: Juguetón, Alerta, Cariñoso):", font=FUENTE_HEADER).pack(anchor="w")
        ent_temp = tk.Entry(form, font=FUENTE_NORMAL)
        ent_temp.pack(fill="x", pady=(3, 10))
        
        # Cuidados Clínicos
        tk.Label(form, text="Cuidados Clínicos Recomendados * (Multilínea):", font=FUENTE_HEADER).pack(anchor="w")
        txt_cuidados = tk.Text(form, font=FUENTE_NORMAL, height=6, relief="solid", bd=1)
        txt_cuidados.pack(fill="both", expand=True, pady=(3, 15))
        
        # Pre-rellenar campos si se está editando
        if editar_raza:
            info = self.controller.sistema.razas.get(editar_raza, {})
            ent_tipo.insert(0, info.get('tipo', ''))
            ent_vida.insert(0, info.get('vida', ''))
            ent_temp.insert(0, info.get('temperamento', ''))
            txt_cuidados.insert("1.0", info.get('cuidados', ''))
            
        def guardar_raza():
            nom = ent_nombre.get().strip() if not editar_raza else editar_raza
            tipo = ent_tipo.get().strip()
            vida = ent_vida.get().strip()
            temp = ent_temp.get().strip()
            cuidados = txt_cuidados.get("1.0", "end-1c").strip()
            
            if not nom or not tipo or not temp or not cuidados:
                return messagebox.showwarning("Campos Vacíos", "Por favor complete los campos obligatorios (*).")
                
            self.controller.sistema.razas[nom] = {
                'tipo': tipo,
                'vida': vida or "No especificado",
                'temperamento': temp,
                'cuidados': cuidados
            }
            self.controller.sistema.guardar_razas()
            self.actualizar()
            
            # Seleccionar raza nueva o editada en el combobox
            self.combo_razas.set(nom)
            self.fetch_breed_info() # Auto refresh
            
            win.destroy()
            messagebox.showinfo("Éxito", f"Raza '{nom}' guardada correctamente.")
            
        tk.Button(win, text="💾 GUARDAR RAZA", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, pady=10, command=guardar_raza).pack(fill="x", side="bottom", pady=15, padx=20)

    def abrir_formulario_raza_edicion(self):
        raza = self.combo_razas.get()
        if not raza:
            return messagebox.showwarning("Atención", "Por favor, seleccione una raza para editar.")
        self.abrir_formulario_raza(editar_raza=raza)

    def mostrar_recetas_popup(self):
        win = tk.Toplevel(self)
        win.title("Historial de Recetas Emitidas")
        win.geometry("900x550")
        win.transient(self)
        win.grab_set()
        
        # Header
        header = tk.Frame(win, bg=COLOR_SECUNDARIO, pady=15)
        header.pack(fill="x", padx=20)
        tk.Label(header, text="📋 REPORTE GENERAL DE RECETAS EMITIDAS", font=FUENTE_SUBTITULO, fg=COLOR_PRIMARIO, bg=COLOR_SECUNDARIO).pack(anchor="w")
        tk.Label(header, text="Busque y filtre el historial de recetas emitidas en las consultas médicas de Huellitas.", font=FUENTE_NORMAL, fg=COLOR_TEXTO_LIGHT, bg=COLOR_SECUNDARIO).pack(anchor="w")
        tk.Frame(header, height=2, bg=COLOR_ACENTO).pack(fill="x", pady=(10, 0))
        
        # Barra de Búsqueda
        search_frame = tk.Frame(win, padx=20, pady=10)
        search_frame.pack(fill="x")
        tk.Label(search_frame, text="🔍 Buscar por Paciente, Veterinario o Diagnóstico:", font=FUENTE_HEADER).pack(side="left", padx=(0, 10))
        ent_search = tk.Entry(search_frame, font=FUENTE_NORMAL, width=40)
        ent_search.pack(side="left", fill="x", expand=True)
        
        # Tabla (Treeview)
        table_frame = tk.Frame(win, padx=20, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("id_con", "fecha", "paciente", "vet", "diagnostico", "receta")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        tree.heading("id_con", text="ID Consulta")
        tree.heading("fecha", text="Fecha / Hora")
        tree.heading("paciente", text="Paciente")
        tree.heading("vet", text="Veterinario")
        tree.heading("diagnostico", text="Diagnóstico")
        tree.heading("receta", text="Receta (Medicamentos)")
        
        tree.column("id_con", width=90, anchor="center")
        tree.column("fecha", width=130, anchor="center")
        tree.column("paciente", width=120)
        tree.column("vet", width=120)
        tree.column("diagnostico", width=150)
        tree.column("receta", width=250)
        
        sb_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        sb_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        def populate_recetas(filter_text=""):
            for row in tree.get_children():
                tree.delete(row)
            
            q = filter_text.lower()
            for c in self.controller.sistema.consultas:
                if not c.medicamentos or str(c.medicamentos).strip() == "":
                    continue
                
                p_name = c.paciente.nombre
                v_name = c.veterinario.nombre
                diag = c.diagnostico
                meds = c.medicamentos
                
                if q and (q not in p_name.lower() and q not in v_name.lower() and q not in diag.lower() and q not in meds.lower()):
                    continue
                
                fecha_str = c.fecha.strftime('%Y-%m-%d %H:%M') if hasattr(c.fecha, 'strftime') else str(c.fecha)
                tree.insert("", "end", values=(c.id_consulta, fecha_str, p_name, v_name, diag, meds))
                
        def on_search(event):
            populate_recetas(ent_search.get())
            
        ent_search.bind("<KeyRelease>", on_search)
        populate_recetas()

    def mostrar_citas_popup(self):
        win = tk.Toplevel(self)
        win.title("Historial de Citas Registradas")
        win.geometry("950x550")
        win.transient(self)
        win.grab_set()
        
        # Encabezado
        header = tk.Frame(win, bg=COLOR_SECUNDARIO, pady=15)
        header.pack(fill="x", padx=20)
        tk.Label(header, text="📅 HISTORIAL GENERAL DE CITAS REGISTRADAS", font=FUENTE_SUBTITULO, fg=COLOR_PRIMARIO, bg=COLOR_SECUNDARIO).pack(anchor="w")
        tk.Label(header, text="Consulte todas las citas agendadas, pendientes y completadas de la clínica.", font=FUENTE_NORMAL, fg=COLOR_TEXTO_LIGHT, bg=COLOR_SECUNDARIO).pack(anchor="w")
        tk.Frame(header, height=2, bg=COLOR_ACENTO).pack(fill="x", pady=(10, 0))
        
        # Barra de Búsqueda
        search_frame = tk.Frame(win, padx=20, pady=10)
        search_frame.pack(fill="x")
        tk.Label(search_frame, text="🔍 Buscar por Paciente, Propietario o Motivo:", font=FUENTE_HEADER).pack(side="left", padx=(0, 10))
        ent_search = tk.Entry(search_frame, font=FUENTE_NORMAL, width=40)
        ent_search.pack(side="left", fill="x", expand=True)
        
        # Tabla (Treeview)
        table_frame = tk.Frame(win, padx=20, pady=10)
        table_frame.pack(fill="both", expand=True)
        
        columns = ("id_cita", "fecha", "hora", "paciente", "propietario", "motivo", "estado")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")
        
        tree.heading("id_cita", text="ID Cita")
        tree.heading("fecha", text="Fecha")
        tree.heading("hora", text="Hora")
        tree.heading("paciente", text="Paciente")
        tree.heading("propietario", text="Propietario")
        tree.heading("motivo", text="Motivo de Consulta")
        tree.heading("estado", text="Estado")
        
        tree.column("id_cita", width=80, anchor="center")
        tree.column("fecha", width=100, anchor="center")
        tree.column("hora", width=80, anchor="center")
        tree.column("paciente", width=120)
        tree.column("propietario", width=150)
        tree.column("motivo", width=220)
        tree.column("estado", width=100, anchor="center")
        
        # Etiquetas de estilo para estados
        tree.tag_configure("Pendiente", background="#FFFDE7", foreground="#F57F17") # Amarillo suave
        tree.tag_configure("Completada", background="#E8F5E9", foreground="#2E7D32") # Verde suave
        tree.tag_configure("Cancelada", background="#FFEBEE", foreground="#C62828") # Rojo suave
        
        sb_y = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        sb_x = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)
        
        tree.grid(row=0, column=0, sticky="nsew")
        sb_y.grid(row=0, column=1, sticky="ns")
        sb_x.grid(row=1, column=0, sticky="ew")
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        def populate_citas(filter_text=""):
            for row in tree.get_children():
                tree.delete(row)
            
            q = filter_text.lower()
            for c in self.controller.sistema.citas:
                p_name = c.paciente.nombre
                motivo = c.motivo
                estado = c.estado
                
                # Buscar propietario
                owner = next((prop for prop in self.controller.sistema.propietarios if c.paciente in prop.mascotas), None)
                owner_name = owner.nombre if owner else "Sin Propietario"
                
                if q and (q not in p_name.lower() and q not in owner_name.lower() and q not in motivo.lower() and q not in estado.lower()):
                    continue
                
                fecha_str = c.fecha.strftime('%Y-%m-%d') if hasattr(c.fecha, 'strftime') else str(c.fecha)
                
                tag = "Pendiente"
                if "complet" in estado.lower():
                    tag = "Completada"
                elif "cancel" in estado.lower():
                    tag = "Cancelada"
                    
                tree.insert("", "end", values=(c.id_cita, fecha_str, c.hora, p_name, owner_name, motivo, estado), tags=(tag,))
                
        def on_search(event):
            populate_citas(ent_search.get())
            
        ent_search.bind("<KeyRelease>", on_search)
        populate_citas()

    def actualizar(self):
        self.sidebar.refrescar_menu()
        
        # Refrescar combobox
        self.combo_razas['values'] = sorted(list(self.controller.sistema.razas.keys()))
        if self.combo_razas['values'] and not self.combo_razas.get():
            self.combo_razas.current(0)
            
        # Obtener rol del usuario que inició sesión
        u = self.controller.sistema.usuario_actual
        if not u: return
        
        # Restablecer el empaquetado del diseño
        self.left.pack_forget()
        self.right.pack_forget()
        for widget in self.right.winfo_children():
            widget.destroy()
            
        if u.rol == "Administrador":
            # Mostrar asistente de razas (izquierda) + botones de admin (derecha)
            self.left.pack(side="left", fill="both", expand=True, padx=(0, 20))
            self.lbl_raza_details.config(wraplength=450) # Ajuste de línea normal
            
            # Configurar panel derecho para botones de reportes de administrador
            self.right.config(text=" 📊 CONSULTAS GENERALES ", width=400)
            self.right.pack_propagate(False)
            self.right.pack(side="right", fill="both", expand=False)
            
            tk.Label(self.right, text="Accesos directos para la supervisión y control administrativo de recetas y citas:", bg=COLOR_SECUNDARIO, font=FUENTE_NORMAL, fg=COLOR_TEXTO_LIGHT, justify="left", wraplength=350).pack(anchor="w", pady=(0, 30))
            
            btn_recetas = tk.Button(self.right, text="📋 VER RECETAS DADAS", bg=COLOR_PRIMARIO, fg="white", font=FUENTE_HEADER, command=self.mostrar_recetas_popup, pady=15)
            btn_recetas.pack(fill="x", pady=15)
            
            btn_citas = tk.Button(self.right, text="📅 VER CITAS REGISTRADAS", bg=COLOR_BOTON, fg="white", font=FUENTE_HEADER, command=self.mostrar_citas_popup, pady=15)
            btn_citas.pack(fill="x", pady=15)
            
        else:
            # Mostrar asistente de razas (izquierda) a pantalla completa! Sin servidor, sin botones de admin.
            self.left.pack(fill="both", expand=True)
            self.lbl_raza_details.config(wraplength=850) # Ajuste de línea más ancho para pantalla completa

if __name__ == "__main__":
    app = AppHuellitas()
    app.mainloop()
