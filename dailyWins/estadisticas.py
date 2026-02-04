from datetime import datetime, timedelta
from collections import Counter

class Estadisticas:
    """
    Procesa y calcula estadísticas sobre los logros.
    Responsable de análisis de datos y generación de reportes.
    """
    
    def __init__(self, logros):
        """
        Constructor de estadísticas.
        
        Args:
            logros (list[Logro]): Lista de logros a analizar
        """
        self.logros = logros
    
    def contar_por_categoria(self):
        """
        Cuenta cuántos logros hay en cada categoría.
        
        Returns:
            dict: {categoria: cantidad}
        """
        categorias = [logro.categoria for logro in self.logros]
        return dict(Counter(categorias))
    
    def calcular_racha(self):
        """
        Calcula la racha actual de días consecutivos con logros.
        
        Returns:
            int: Número de días consecutivos (hasta hoy)
        """
        if not self.logros:
            return 0
        
        # Obtener fechas únicas ordenadas
        fechas = sorted(set(logro.fecha for logro in self.logros), reverse=True)
        
        # Verificar racha desde hoy hacia atrás
        racha = 0
        fecha_actual = datetime.now().date()
        
        for fecha_str in fechas:
            fecha_logro = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            diferencia = (fecha_actual - fecha_logro).days
            
            if diferencia == racha:
                racha += 1
            else:
                break
        
        return racha
    
    def logros_ultima_semana(self):
        """
        Cuenta logros de los últimos 7 días.
        
        Returns:
            int: Cantidad de logros en la última semana
        """
        fecha_limite = datetime.now() - timedelta(days=7)
        fecha_limite_str = fecha_limite.strftime("%Y-%m-%d")
        
        return sum(1 for logro in self.logros if logro.fecha >= fecha_limite_str)
    
    def logros_ultimo_mes(self):
        """
        Cuenta logros de los últimos 30 días.
        
        Returns:
            int: Cantidad de logros en el último mes
        """
        fecha_limite = datetime.now() - timedelta(days=30)
        fecha_limite_str = fecha_limite.strftime("%Y-%m-%d")
        
        return sum(1 for logro in self.logros if logro.fecha >= fecha_limite_str)
    
    def categoria_favorita(self):
        """
        Identifica la categoría con más logros.
        
        Returns:
            tuple: (categoria, cantidad) o (None, 0) si no hay logros
        """
        if not self.logros:
            return (None, 0)
        
        conteo = self.contar_por_categoria()
        categoria_top = max(conteo.items(), key=lambda x: x[1])
        return categoria_top
    
    def promedio_diario(self):
        """
        Calcula el promedio de logros por día (desde el primer logro).
        
        Returns:
            float: Promedio de logros diarios
        """
        if not self.logros:
            return 0.0
        
        fechas_unicas = set(logro.fecha for logro in self.logros)
        dias_activos = len(fechas_unicas)
        
        return len(self.logros) / dias_activos if dias_activos > 0 else 0.0
    

    def logros_por_dia(self):
        """
        Agrupa logros por fecha.
        
        Returns:
            dict: {fecha: cantidad}
        """
        from collections import Counter
        fechas = [logro.fecha for logro in self.logros]
        return dict(Counter(fechas))
    
   
    def generar_reporte(self):
        """
        Genera un reporte completo en texto.
        
        Returns:
            str: Reporte formateado con todas las estadísticas
        """
        total = len(self.logros)
        
        if total == 0:
            return "📭 Aún no tienes logros registrados.\n💡 ¡Registra tu primer logro para comenzar!"
        
        racha = self.calcular_racha()
        semana = self.logros_ultima_semana()
        mes = self.logros_ultimo_mes()
        cat_fav, cat_cantidad = self.categoria_favorita()
        promedio = self.promedio_diario()
        
        reporte = f"""
╔══════════════════════════════════════╗
║       📊 REPORTE DE ESTADÍSTICAS     ║
╚══════════════════════════════════════╝

📈 TOTALES
   • Total de logros: {total}
   • Promedio diario: {promedio:.1f} logros/día

🔥 RACHA
   • Días consecutivos: {racha} día(s)
   {"   🎉 ¡Sigue así!" if racha >= 3 else "   💪 ¡A por más días!"}

📅 PERÍODO RECIENTE
   • Última semana (7 días): {semana} logros
   • Último mes (30 días): {mes} logros

🏆 CATEGORÍA FAVORITA
   • {cat_fav.capitalize()}: {cat_cantidad} logros

📊 DISTRIBUCIÓN POR CATEGORÍA
"""
        
        # Agregar gráfico de barras
        conteo = self.contar_por_categoria()
        for categoria, cantidad in sorted(conteo.items(), key=lambda x: x[1], reverse=True):
            porcentaje = (cantidad / total) * 100
            barra = "█" * int(porcentaje / 5)
            reporte += f"   {categoria.capitalize():12} {cantidad:3} ({porcentaje:.1f}%) {barra}\n"
        
        return reporte


# ===== PRUEBA DE LA CLASE (Eliminar después) =====
if __name__ == "__main__":
    from gestor_logros import GestorLogros
    
    # Cargar logros existentes
    gestor = GestorLogros()
    
    # Crear objeto estadísticas
    stats = Estadisticas(gestor.obtener_todos())
    
    # Mostrar reporte completo
    print(stats.generar_reporte())
    
    # Pruebas individuales
    print("\n--- PRUEBAS ADICIONALES ---")
    print(f"Racha actual: {stats.calcular_racha()} días")
    print(f"Logros última semana: {stats.logros_ultima_semana()}")
    print(f"Categoría favorita: {stats.categoria_favorita()}")