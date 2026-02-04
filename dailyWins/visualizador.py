import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from collections import Counter
import numpy as np

class Visualizador:
    """
    Genera gráficos visuales de los logros usando matplotlib.
    Responsable de la visualización de datos y análisis gráfico.
    """
    
    def __init__(self, estadisticas):
        """
        Constructor del visualizador.
        
        Args:
            estadisticas (Estadisticas): Objeto con datos procesados
        """
        self.stats = estadisticas
        
        # Configuración de estilo
        plt.style.use('seaborn-v0_8-darkgrid')
        self.colores = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    def grafico_categorias(self):
        """
        Crea un gráfico de barras con logros por categoría.
        """
        conteo = self.stats.contar_por_categoria()
        
        if not conteo:
            print("⚠️ No hay datos para mostrar")
            return
        
        categorias = list(conteo.keys())
        valores = list(conteo.values())
        
        # Crear figura
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
        fig.suptitle('📊 Distribución de Logros por Categoría', 
                     fontsize=16, fontweight='bold')
        
        # GRÁFICO 1: Barras
        barras = ax1.bar(categorias, valores, color=self.colores[:len(categorias)])
        ax1.set_xlabel('Categoría', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Cantidad de Logros', fontsize=12, fontweight='bold')
        ax1.set_title('Gráfico de Barras', fontsize=14)
        
        # Agregar valores encima de las barras
        for barra in barras:
            altura = barra.get_height()
            ax1.text(barra.get_x() + barra.get_width()/2., altura,
                    f'{int(altura)}',
                    ha='center', va='bottom', fontweight='bold')
        
        # GRÁFICO 2: Torta
        ax2.pie(valores, labels=categorias, autopct='%1.1f%%',
               colors=self.colores[:len(categorias)], startangle=90)
        ax2.set_title('Gráfico Circular', fontsize=14)
        
        plt.tight_layout()
        plt.show()
    
    def grafico_tendencia(self, dias=30):
        """
        Crea un gráfico de líneas con la tendencia de logros en el tiempo.
        
        Args:
            dias (int): Número de días a mostrar
        """
        logros_dia = self.stats.logros_por_dia()
        
        if not logros_dia:
            print("⚠️ No hay datos para mostrar")
            return
        
        # Preparar datos
        fechas = sorted(logros_dia.keys())
        
        # Filtrar últimos N días
        fecha_limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
        fechas = [f for f in fechas if f >= fecha_limite]
        
        if not fechas:
            print(f"⚠️ No hay datos en los últimos {dias} días")
            return
        
        # Convertir a datetime
        fechas_dt = [datetime.strptime(f, "%Y-%m-%d") for f in fechas]
        cantidades = [logros_dia[f] for f in fechas]
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(14, 6))
        fig.suptitle(f'📈 Tendencia de Logros - Últimos {dias} Días', 
                     fontsize=16, fontweight='bold')
        
        # Gráfico de línea
        ax.plot(fechas_dt, cantidades, marker='o', linewidth=2, 
               markersize=8, color='#3498db', label='Logros diarios')
        
        # Línea de promedio
        promedio = np.mean(cantidades)
        ax.axhline(y=promedio, color='#e74c3c', linestyle='--', 
                  linewidth=2, label=f'Promedio: {promedio:.1f}')
        
        # Configuración de ejes
        ax.set_xlabel('Fecha', fontsize=12, fontweight='bold')
        ax.set_ylabel('Cantidad de Logros', fontsize=12, fontweight='bold')
        ax.legend(loc='upper left', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # Formato de fechas en eje X
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(fechas)//10)))
        plt.xticks(rotation=45)
        
        plt.tight_layout()
        plt.show()
    
    def grafico_calendario(self):
        """
        Crea un mapa de calor tipo calendario (últimos 30 días).
        """
        logros_dia = self.stats.logros_por_dia()
        
        # Generar últimos 30 días
        hoy = datetime.now()
        dias = [(hoy - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]
        
        # Obtener cantidades (0 si no hay logros ese día)
        cantidades = [logros_dia.get(dia, 0) for dia in dias]
        
        # Crear matriz 5x6 (5 semanas de 6 días)
        matriz = np.array(cantidades[:30]).reshape(5, 6)
        
        # Crear figura
        fig, ax = plt.subplots(figsize=(12, 8))
        fig.suptitle('🗓️ Calendario de Actividad - Últimos 30 Días', 
                     fontsize=16, fontweight='bold')
        
        # Mapa de calor
        im = ax.imshow(matriz, cmap='YlGn', aspect='auto', vmin=0)
        
        # Configurar ejes
        ax.set_xticks(np.arange(6))
        ax.set_yticks(np.arange(5))
        ax.set_xticklabels(['Día 1-6', 'Día 7-12', 'Día 13-18', 
                           'Día 19-24', 'Día 25-30', ''])
        ax.set_yticklabels([f'Semana {i+1}' for i in range(5)])
        
        # Agregar valores en cada celda
        for i in range(5):
            for j in range(6):
                if i*6 + j < 30:
                    text = ax.text(j, i, matriz[i, j],
                                 ha="center", va="center", color="black",
                                 fontweight='bold', fontsize=12)
        
        # Barra de colores
        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label('Logros por día', rotation=270, labelpad=20, fontweight='bold')
        
        plt.tight_layout()
        plt.show()
    
    def dashboard_completo(self):
        """
        Crea un dashboard con múltiples gráficos en una sola ventana.
        """
        conteo = self.stats.contar_por_categoria()
        logros_dia = self.stats.logros_por_dia()
        
        if not conteo and not logros_dia:
            print("⚠️ No hay datos suficientes para mostrar el dashboard")
            return
        
        # Crear figura con subplots
        fig = plt.figure(figsize=(16, 10))
        fig.suptitle('🎯 DAILYWINS - Dashboard Completo', 
                     fontsize=18, fontweight='bold')
        
        # GRÁFICO 1: Barras por categoría (arriba izquierda)
        if conteo:
            ax1 = plt.subplot(2, 2, 1)
            categorias = list(conteo.keys())
            valores = list(conteo.values())
            barras = ax1.bar(categorias, valores, color=self.colores[:len(categorias)])
            ax1.set_title('Logros por Categoría', fontsize=14, fontweight='bold')
            ax1.set_ylabel('Cantidad')
            
            for barra in barras:
                altura = barra.get_height()
                ax1.text(barra.get_x() + barra.get_width()/2., altura,
                        f'{int(altura)}', ha='center', va='bottom')
        
        # GRÁFICO 2: Torta (arriba derecha)
        if conteo:
            ax2 = plt.subplot(2, 2, 2)
            ax2.pie(valores, labels=categorias, autopct='%1.1f%%',
                   colors=self.colores[:len(categorias)], startangle=90)
            ax2.set_title('Distribución Porcentual', fontsize=14, fontweight='bold')
        
        # GRÁFICO 3: Tendencia últimos 14 días (abajo izquierda)
        if logros_dia:
            ax3 = plt.subplot(2, 2, 3)
            fechas = sorted(logros_dia.keys())[-14:]
            fechas_dt = [datetime.strptime(f, "%Y-%m-%d") for f in fechas]
            cantidades = [logros_dia[f] for f in fechas]
            
            ax3.plot(fechas_dt, cantidades, marker='o', linewidth=2,
                    markersize=6, color='#3498db')
            ax3.set_title('Tendencia (Últimos 14 días)', fontsize=14, fontweight='bold')
            ax3.set_ylabel('Logros')
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
            plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45)
            ax3.grid(True, alpha=0.3)
        
        # GRÁFICO 4: Estadísticas textuales (abajo derecha)
        ax4 = plt.subplot(2, 2, 4)
        ax4.axis('off')
        
        total = len(self.stats.logros)
        racha = self.stats.calcular_racha()
        semana = self.stats.logros_ultima_semana()
        mes = self.stats.logros_ultimo_mes()
        cat_fav, cat_cant = self.stats.categoria_favorita()
        promedio = self.stats.promedio_diario()
        
        stats_text = f"""
        📊 RESUMEN EJECUTIVO
        
        Total de logros: {total}
        
        🔥 Racha actual: {racha} día(s)
        
        📅 Última semana: {semana} logros
        📅 Último mes: {mes} logros
        
        ⭐ Promedio diario: {promedio:.1f}
        
        🏆 Categoría favorita:
           {cat_fav.capitalize() if cat_fav else 'N/A'} ({cat_cant} logros)
        """
        
        ax4.text(0.1, 0.5, stats_text, fontsize=12, 
                verticalalignment='center', family='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))
        
        plt.tight_layout()
        plt.show()


# ===== PRUEBA DE LA CLASE (Eliminar después) =====
if __name__ == "__main__":
    from gestor_logros import GestorLogros
    from estadisticas import Estadisticas
    
    # Cargar datos
    gestor = GestorLogros()
    stats = Estadisticas(gestor.obtener_todos())
    
    # Crear visualizador
    viz = Visualizador(stats)
    
    # Probar gráficos
    print("Mostrando dashboard completo...")
    viz.dashboard_completo()