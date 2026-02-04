from gestor_logros import GestorLogros
from estadisticas import Estadisticas
import os

class DailyWinsApp:
    """
    Aplicación principal de DailyWins.
    Interfaz de consola para gestionar logros diarios.
    """
    
    def __init__(self):
        """Constructor de la aplicación."""
        self.gestor = GestorLogros()
        self.categorias = ["trabajo", "salud", "aprendizaje", "personal"]
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def mostrar_menu(self):
        """Muestra el menú principal."""
        # Calcular racha actual para mostrar en el menú
        stats = Estadisticas(self.gestor.obtener_todos())
        racha = stats.calcular_racha()
        
        print("\n" + "="*40)
        print("        🎯 DAILYWINS 🎯")
        print("="*40)
        print(f"📊 Total de logros: {self.gestor.contar_total()}")
        print(f"🔥 Racha actual: {racha} día(s)")
        print("="*40)
        print("1. ✅ Registrar logro")
        print("2. 📋 Ver últimos logros")
        print("3. 📈 Ver reporte completo")
        print("4. 🚪 Salir")
        print("="*40)
    
    def registrar_logro(self):
        """Registra un nuevo logro."""
        print("\n--- REGISTRAR NUEVO LOGRO ---")
        
        # Pedir descripción
        descripcion = input("Describe tu logro: ").strip()
        if not descripcion:
            print("❌ La descripción no puede estar vacía")
            input("Presiona ENTER para continuar...")
            return
        
        # Mostrar categorías
        print("\nCategorías disponibles:")
        for i, cat in enumerate(self.categorias, 1):
            print(f"{i}. {cat.capitalize()}")
        
        # Seleccionar categoría
        try:
            opcion = int(input("\nElige categoría (número): "))
            if 1 <= opcion <= len(self.categorias):
                categoria = self.categorias[opcion - 1]
            else:
                print("❌ Opción inválida, usando 'personal' por defecto")
                categoria = "personal"
        except ValueError:
            print("❌ Entrada inválida, usando 'personal' por defecto")
            categoria = "personal"
        
        # Agregar logro
        logro = self.gestor.agregar_logro(descripcion, categoria)
        print(f"\n✅ ¡Logro registrado exitosamente!")
        print(f"   {logro}")
        
        # Mostrar motivación según racha
        stats = Estadisticas(self.gestor.obtener_todos())
        racha = stats.calcular_racha()
        if racha >= 7:
            print(f"\n🔥🔥🔥 ¡INCREÍBLE! ¡{racha} días de racha!")
        elif racha >= 3:
            print(f"\n🔥 ¡Excelente! ¡{racha} días consecutivos!")
        
        input("\nPresiona ENTER para continuar...")
    
    def ver_logros(self):
        """Muestra los últimos logros."""
        print("\n--- ÚLTIMOS 10 LOGROS ---")
        
        logros = self.gestor.obtener_ultimos(10)
        
        if not logros:
            print("📭 Aún no tienes logros registrados")
        else:
            for i, logro in enumerate(reversed(logros), 1):
                print(f"{i}. {logro}")
        
        input("\nPresiona ENTER para continuar...")
    
    def mostrar_estadisticas(self):
        """Muestra el reporte completo de estadísticas."""
        # Crear objeto estadísticas con todos los logros
        stats = Estadisticas(self.gestor.obtener_todos())
        
        # Generar y mostrar reporte
        reporte = stats.generar_reporte()
        print(reporte)
        
        input("\nPresiona ENTER para continuar...")
    
    def ejecutar(self):
        """Bucle principal de la aplicación."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_menu()
            
            opcion = input("\nElige una opción: ").strip()
            
            if opcion == "1":
                self.registrar_logro()
            elif opcion == "2":
                self.ver_logros()
            elif opcion == "3":
                self.mostrar_estadisticas()
            elif opcion == "4":
                # Mostrar mensaje de despedida con estadísticas finales
                stats = Estadisticas(self.gestor.obtener_todos())
                total = self.gestor.contar_total()
                racha = stats.calcular_racha()
                
                print(f"\n{'='*40}")
                print(f"   📊 Sesión finalizada")
                print(f"   Total acumulado: {total} logros")
                print(f"   Racha actual: {racha} día(s)")
                print(f"{'='*40}")
                print("👋 ¡Sigue acumulando victorias! Hasta pronto.")
                break
            else:
                print("❌ Opción inválida")
                input("Presiona ENTER para continuar...")


# ===== PUNTO DE ENTRADA =====
if __name__ == "__main__":
    app = DailyWinsApp()
    app.ejecutar()