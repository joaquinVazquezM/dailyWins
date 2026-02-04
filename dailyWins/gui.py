import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from gestor_logros import GestorLogros
from estadisticas import Estadisticas
from visualizador import Visualizador
from datetime import datetime

class DailyWinsGUI:
    """
    Interfaz gráfica de usuario para DailyWins.
    Utiliza Tkinter para crear una experiencia visual moderna.
    """
    
    def __init__(self):
        """Constructor de la GUI."""
        self.gestor = GestorLogros()
        self.categorias = ["trabajo", "salud", "aprendizaje", "personal"]
        
        # Crear ventana principal
        self.root = tk.Tk()
        self.root.title("🎯 DailyWins - Registro de Logros")
        self.root.geometry("850x650")
        self.root.configure(bg="#f0f0f0")
        
        # Crear interfaz
        self.crear_widgets()
        self.actualizar_dashboard()
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        
        # ===== FRAME SUPERIOR: DASHBOARD =====
        frame_dashboard = tk.Frame(self.root, bg="#2c3e50", padx=20, pady=15)
        frame_dashboard.pack(fill=tk.X)
        
        # Título
        tk.Label(
            frame_dashboard,
            text="🎯 DAILYWINS",
            font=("Arial", 24, "bold"),
            bg="#2c3e50",
            fg="white"
        ).pack()
        
        # Frame para estadísticas rápidas
        stats_frame = tk.Frame(frame_dashboard, bg="#2c3e50")
        stats_frame.pack(pady=10)
        
        # Total de logros
        self.label_total = tk.Label(
            stats_frame,
            text="Total: 0",
            font=("Arial", 14),
            bg="#3498db",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED
        )
        self.label_total.pack(side=tk.LEFT, padx=5)
        
        # Racha
        self.label_racha = tk.Label(
            stats_frame,
            text="🔥 Racha: 0 días",
            font=("Arial", 14),
            bg="#e74c3c",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED
        )
        self.label_racha.pack(side=tk.LEFT, padx=5)
        
        # Última semana
        self.label_semana = tk.Label(
            stats_frame,
            text="Esta semana: 0",
            font=("Arial", 14),
            bg="#27ae60",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.RAISED
        )
        self.label_semana.pack(side=tk.LEFT, padx=5)
        
        # ===== FRAME CENTRAL: NOTEBOOK (PESTAÑAS) =====
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # PESTAÑA 1: REGISTRO
        tab_registro = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(tab_registro, text="✅ Registrar Logro")
        
        # Contenido de registro
        tk.Label(
            tab_registro,
            text="Describe tu logro:",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        ).pack(pady=(20, 5))
        
        self.entry_descripcion = tk.Entry(
            tab_registro,
            font=("Arial", 12),
            width=50
        )
        self.entry_descripcion.pack(pady=5)
        
        # Bind para registrar con Enter
        self.entry_descripcion.bind('<Return>', lambda e: self.registrar_logro())
        
        tk.Label(
            tab_registro,
            text="Categoría:",
            font=("Arial", 12, "bold"),
            bg="#ecf0f1"
        ).pack(pady=(20, 5))
        
        self.combo_categoria = ttk.Combobox(
            tab_registro,
            values=[cat.capitalize() for cat in self.categorias],
            font=("Arial", 12),
            state="readonly",
            width=30
        )
        self.combo_categoria.current(0)
        self.combo_categoria.pack(pady=5)
        
        tk.Button(
            tab_registro,
            text="✅ Registrar Logro",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            padx=30,
            pady=10,
            command=self.registrar_logro
        ).pack(pady=30)
        
        # PESTAÑA 2: HISTORIAL
        tab_historial = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(tab_historial, text="📋 Historial")
        
        # Área de texto con scroll
        self.text_historial = scrolledtext.ScrolledText(
            tab_historial,
            font=("Courier", 10),
            wrap=tk.WORD,
            width=80,
            height=20
        )
        self.text_historial.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Button(
            tab_historial,
            text="🔄 Actualizar Historial",
            font=("Arial", 12),
            bg="#3498db",
            fg="white",
            command=self.ver_historial
        ).pack(pady=10)
        
        # PESTAÑA 3: ESTADÍSTICAS
        tab_stats = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(tab_stats, text="📊 Estadísticas")
        
        # Área de texto para reporte
        self.text_stats = scrolledtext.ScrolledText(
            tab_stats,
            font=("Courier", 10),
            wrap=tk.WORD,
            width=80,
            height=15
        )
        self.text_stats.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Frame para botones
        btn_frame = tk.Frame(tab_stats, bg="#ecf0f1")
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="📈 Generar Reporte",
            font=("Arial", 11),
            bg="#9b59b6",
            fg="white",
            padx=15,
            pady=8,
            command=self.ver_estadisticas
        ).pack(side=tk.LEFT, padx=5)
        
        # PESTAÑA 4: GRÁFICOS ⭐ NUEVA
        tab_graficos = tk.Frame(notebook, bg="#ecf0f1")
        notebook.add(tab_graficos, text="📊 Gráficos")
        
        # Título
        tk.Label(
            tab_graficos,
            text="Visualización de Datos",
            font=("Arial", 16, "bold"),
            bg="#ecf0f1"
        ).pack(pady=20)
        
        # Frame para botones de gráficos
        graficos_frame = tk.Frame(tab_graficos, bg="#ecf0f1")
        graficos_frame.pack(pady=20)
        
        # Botón: Dashboard Completo
        tk.Button(
            graficos_frame,
            text="📊 Dashboard Completo",
            font=("Arial", 13, "bold"),
            bg="#2c3e50",
            fg="white",
            padx=25,
            pady=15,
            command=self.mostrar_dashboard_completo,
            width=25
        ).pack(pady=10)
        
        # Botón: Gráfico de Categorías
        tk.Button(
            graficos_frame,
            text="📈 Distribución por Categoría",
            font=("Arial", 13, "bold"),
            bg="#3498db",
            fg="white",
            padx=25,
            pady=15,
            command=self.mostrar_grafico_categorias,
            width=25
        ).pack(pady=10)
        
        # Botón: Tendencia Temporal
        tk.Button(
            graficos_frame,
            text="📉 Tendencia Temporal",
            font=("Arial", 13, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=25,
            pady=15,
            command=self.mostrar_grafico_tendencia,
            width=25
        ).pack(pady=10)
        
        # Botón: Calendario de Actividad
        tk.Button(
            graficos_frame,
            text="🗓️ Calendario de Actividad",
            font=("Arial", 13, "bold"),
            bg="#27ae60",
            fg="white",
            padx=25,
            pady=15,
            command=self.mostrar_grafico_calendario,
            width=25
        ).pack(pady=10)
        
        # Nota informativa
        tk.Label(
            tab_graficos,
            text="💡 Tip: Registra logros durante varios días para ver gráficos más completos",
            font=("Arial", 10, "italic"),
            bg="#ecf0f1",
            fg="#7f8c8d"
        ).pack(side=tk.BOTTOM, pady=20)
    
    def actualizar_dashboard(self):
        """Actualiza las estadísticas del dashboard superior."""
        stats = Estadisticas(self.gestor.obtener_todos())
        total = self.gestor.contar_total()
        racha = stats.calcular_racha()
        semana = stats.logros_ultima_semana()
        
        self.label_total.config(text=f"Total: {total}")
        self.label_racha.config(text=f"🔥 Racha: {racha} día(s)")
        self.label_semana.config(text=f"Esta semana: {semana}")
    
    def registrar_logro(self):
        """Registra un nuevo logro desde la GUI."""
        descripcion = self.entry_descripcion.get().strip()
        
        if not descripcion:
            messagebox.showwarning(
                "Campo vacío",
                "Por favor describe tu logro"
            )
            return
        
        categoria = self.combo_categoria.get().lower()
        logro = self.gestor.agregar_logro(descripcion, categoria)
        
        # Limpiar campo
        self.entry_descripcion.delete(0, tk.END)
        
        # Actualizar dashboard
        self.actualizar_dashboard()
        
        # Mensaje de éxito
        stats = Estadisticas(self.gestor.obtener_todos())
        racha = stats.calcular_racha()
        
        mensaje = f"✅ ¡Logro registrado!\n\n{logro}"
        
        if racha >= 7:
            mensaje += f"\n\n🔥🔥🔥 ¡INCREÍBLE! ¡{racha} días de racha!"
        elif racha >= 3:
            mensaje += f"\n\n🔥 ¡Excelente! ¡{racha} días consecutivos!"
        
        messagebox.showinfo("Éxito", mensaje)
        
        # Enfocar de nuevo en el campo de entrada
        self.entry_descripcion.focus()
    
    def ver_historial(self):
        """Muestra el historial de logros."""
        self.text_historial.delete(1.0, tk.END)
        
        logros = self.gestor.obtener_todos()
        
        if not logros:
            self.text_historial.insert(1.0, "📭 Aún no tienes logros registrados")
            return
        
        self.text_historial.insert(1.0, "═" * 70 + "\n")
        self.text_historial.insert(tk.END, "               📋 HISTORIAL DE LOGROS\n")
        self.text_historial.insert(tk.END, "═" * 70 + "\n\n")
        
        for i, logro in enumerate(reversed(logros), 1):
            self.text_historial.insert(tk.END, f"{i}. {logro}\n")
    
    def ver_estadisticas(self):
        """Muestra el reporte completo de estadísticas."""
        self.text_stats.delete(1.0, tk.END)
        
        stats = Estadisticas(self.gestor.obtener_todos())
        reporte = stats.generar_reporte()
        
        self.text_stats.insert(1.0, reporte)
    
    def mostrar_dashboard_completo(self):
        """Muestra el dashboard completo con todos los gráficos."""
        stats = Estadisticas(self.gestor.obtener_todos())
        
        if self.gestor.contar_total() == 0:
            messagebox.showinfo(
                "Sin datos",
                "📭 Registra algunos logros primero para ver los gráficos"
            )
            return
        
        viz = Visualizador(stats)
        viz.dashboard_completo()
    
    def mostrar_grafico_categorias(self):
        """Muestra el gráfico de distribución por categorías."""
        stats = Estadisticas(self.gestor.obtener_todos())
        
        if self.gestor.contar_total() == 0:
            messagebox.showinfo(
                "Sin datos",
                "📭 Registra algunos logros primero para ver los gráficos"
            )
            return
        
        viz = Visualizador(stats)
        viz.grafico_categorias()
    
    def mostrar_grafico_tendencia(self):
        """Muestra el gráfico de tendencia temporal."""
        stats = Estadisticas(self.gestor.obtener_todos())
        
        if self.gestor.contar_total() == 0:
            messagebox.showinfo(
                "Sin datos",
                "📭 Registra algunos logros primero para ver los gráficos"
            )
            return
        
        viz = Visualizador(stats)
        viz.grafico_tendencia()
    
    def mostrar_grafico_calendario(self):
        """Muestra el calendario de actividad."""
        stats = Estadisticas(self.gestor.obtener_todos())
        
        if self.gestor.contar_total() == 0:
            messagebox.showinfo(
                "Sin datos",
                "📭 Registra algunos logros primero para ver los gráficos"
            )
            return
        
        viz = Visualizador(stats)
        viz.grafico_calendario()
    
    def ejecutar(self):
        """Inicia el bucle principal de la GUI."""
        self.root.mainloop()


# ===== PUNTO DE ENTRADA =====
if __name__ == "__main__":
    app = DailyWinsGUI()
    app.ejecutar()