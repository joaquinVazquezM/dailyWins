import json
import os
from logro import Logro

class GestorLogros:
    """
    Gestiona la colección de logros diarios.
    Responsable de almacenamiento, recuperación y estadísticas.
    """
    
    def __init__(self, archivo="logros.json"):
        """
        Constructor del gestor.
        
        Args:
            archivo (str): Nombre del archivo para persistencia
        """
        self.logros = []
        self.archivo = archivo
        self.cargar()  # Cargar logros existentes al iniciar
    
    def agregar_logro(self, descripcion, categoria):
        """
        Crea y agrega un nuevo logro a la colección.
        
        Args:
            descripcion (str): Descripción del logro
            categoria (str): Categoría del logro
        
        Returns:
            Logro: El logro creado
        """
        nuevo_logro = Logro(descripcion, categoria)
        self.logros.append(nuevo_logro)
        self.guardar()  # Guardar automáticamente
        return nuevo_logro
    
    def obtener_todos(self):
        """
        Retorna todos los logros registrados.
        
        Returns:
            list[Logro]: Lista completa de logros
        """
        return self.logros
    
    def obtener_ultimos(self, n=5):
        """
        Retorna los últimos N logros.
        
        Args:
            n (int): Cantidad de logros a retornar
        
        Returns:
            list[Logro]: Últimos N logros (más recientes primero)
        """
        return self.logros[-n:] if len(self.logros) >= n else self.logros
    
    def contar_total(self):
        """
        Cuenta el total de logros registrados.
        
        Returns:
            int: Cantidad total de logros
        """
        return len(self.logros)
    
    def guardar(self):
        """
        Guarda todos los logros en archivo JSON.
        
        Returns:
            bool: True si se guardó exitosamente
        """
        try:
            datos = [logro.to_dict() for logro in self.logros]
            with open(self.archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False
    
    def cargar(self):
        """
        Carga los logros desde el archivo JSON.
        
        Returns:
            bool: True si se cargó exitosamente
        """
        if not os.path.exists(self.archivo):
            return False
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            
            # Reconstruir objetos Logro desde el diccionario
            self.logros = []
            for item in datos:
                logro = Logro(item['descripcion'], item['categoria'])
                # Restaurar fecha y hora originales
                logro.fecha = item['fecha']
                logro.hora = item['hora']
                self.logros.append(logro)
            
            return True
        except Exception as e:
            print(f"Error al cargar: {e}")
            return False
        
if __name__ == "__main__":
    # Crear gestor
    gestor = GestorLogros()
    
    # Agregar logros de prueba
    gestor.agregar_logro("Estudié Python 1 hora", "aprendizaje")
    gestor.agregar_logro("Hice 20 flexiones", "salud")
    gestor.agregar_logro("Terminé reporte mensual", "trabajo")
    
    # Mostrar estadísticas
    print(f"Total de logros: {gestor.contar_total()}")
    print("\n=== ÚLTIMOS 3 LOGROS ===")
    for logro in gestor.obtener_ultimos(3):
        print(logro)
    
    print(f"\n✅ Logros guardados en '{gestor.archivo}'")