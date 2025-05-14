import json
import os
from pathlib import Path


class ConfigManager:
    """
    Clase para gestionar las configuraciones de la aplicación.
    Maneja la carga y guardado de configuraciones en formato JSON.
    """

    def __init__(self, config_file="config.json", default_config_file=None):
        """
        Inicializa el gestor de configuraciones.
        
        Args:
            config_file (str): Ruta del archivo de configuración del usuario.
            default_config_file (str): Ruta del archivo de configuración por defecto.
        """
        # Determinar las rutas de configuración
        self.app_dir = Path.home() / ".automationApp"
        self.config_path = self.app_dir / config_file

        # Si se proporciona ruta de configuración por defecto, usarla
        if default_config_file:
            self.default_config_path = Path(default_config_file)
        else:
            # Usar la configuración por defecto incluida en el paquete
            package_dir = Path(__file__).parent
            self.default_config_path = package_dir / "default_config.json"

        # Configuración actual
        self.config = {}

        # Asegurar que el directorio de configuración existe
        self.app_dir.mkdir(parents=True, exist_ok=True)

        # Cargar configuración
        self.load_config()

    def load_config(self):
        """
        Carga la configuración desde el archivo.
        Si no existe, crea uno nuevo con los valores por defecto.
        """
        try:
            # Intentar cargar el archivo de configuración existente
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                print(f"Configuración cargada desde {self.config_path}")
            else:
                # Si no existe, cargar la configuración por defecto
                with open(self.default_config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # Y guardarla en el archivo de configuración del usuario
                self.save_config()
                print(
                    f"Configuración por defecto cargada y guardada en {self.config_path}")
        except Exception as e:
            print(f"Error al cargar la configuración: {e}")
            # En caso de error, crear una configuración mínima
            self.config = {
                "database": {
                    "enabled": False,
                    "host": "",
                    "port": "",
                    "user": "",
                    "password": "",
                    "database": ""
                },
                "email": {
                    "smtp_server": "",
                    "smtp_port": 587,
                    "sender_email": "",
                    "use_ssl": False,
                    "use_tls": True
                },
                "excel": {
                    "default_format": {
                        "header_color": "4F81BD",
                        "create_tables": True,
                        "table_style": "TableStyleMedium9"
                    }
                },
                "app": {
                    "theme": "system",
                    "color_theme": "blue",
                    "temp_dir": "temp",
                    "auto_cleanup": True
                }
            }
            self.save_config()

    def save_config(self):
        """
        Guarda la configuración actual en el archivo.
        """
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            print(f"Configuración guardada en {self.config_path}")
            return True
        except Exception as e:
            print(f"Error al guardar la configuración: {e}")
            return False

    def get_config(self, section=None, key=None):
        """
        Obtiene un valor de configuración.
        
        Args:
            section (str, opcional): Sección de la configuración.
            key (str, opcional): Clave específica dentro de la sección.
        
        Returns:
            El valor de configuración solicitado o toda la configuración.
        """
        if section is None:
            return self.config

        if section not in self.config:
            return None

        if key is None:
            return self.config[section]

        return self.config[section].get(key, None)

    def set_config(self, section, key, value):
        """
        Establece un valor de configuración.
        
        Args:
            section (str): Sección de la configuración.
            key (str): Clave dentro de la sección.
            value: Valor a establecer.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section][key] = value
        return self.save_config()

    def update_section(self, section, values):
        """
        Actualiza una sección completa de la configuración.
        
        Args:
            section (str): Sección de la configuración a actualizar.
            values (dict): Diccionario con los nuevos valores.
        
        Returns:
            bool: True si se guardó correctamente, False en caso contrario.
        """
        if section not in self.config:
            self.config[section] = {}

        self.config[section].update(values)
        return self.save_config()


# Ejemplo de uso:
if __name__ == "__main__":
    config = ConfigManager()
    print(config.get_config())
