from datetime import datetime

class Logro:
    """
    Representa un logro diario del usuario.
    Registra automáticamente la fecha y hora de creación.
    """
    
    def __init__(self, descripcion, categoria):
        """
        Constructor de la clase Logro.
        
        Args:
            descripcion (str): Breve descripción del logro
            categoria (str): Categoría (trabajo, salud, aprendizaje, personal)
        """
        self.descripcion = descripcion
        self.categoria = categoria
        
        # Captura automática de fecha y hora
        ahora = datetime.now()
        self.fecha = ahora.strftime("%Y-%m-%d")  # Formato: 2026-01-23
        self.hora = ahora.strftime("%H:%M")       # Formato: 14:30
    
    def __str__(self):
        """
        Representación en texto del logro.
        
        Returns:
            str: Formato legible del logro
        """
        return f"[{self.fecha} {self.hora}] ({self.categoria}) - {self.descripcion}"
    
    def to_dict(self):
        """
        Convierte el logro a diccionario (útil para guardar en JSON/CSV).
        
        Returns:
            dict: Diccionario con los atributos del logro
        """
        return {
            'descripcion': self.descripcion,
            'categoria': self.categoria,
            'fecha': self.fecha,
            'hora': self.hora
        }


# ===== PRUEBA DE LA CLASE (Eliminar después) =====
if __name__ == "__main__":
    # Crear un logro de prueba
    logro1 = Logro("Completé 30 minutos de ejercicio", "salud")
    
    # Probar __str__()
    print(logro1)
    
    # Probar to_dict()
    print(logro1.to_dict())