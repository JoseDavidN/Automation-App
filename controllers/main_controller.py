from views.app import AppView
from config.config_manager import ConfigManager
# from controllers.config_controller import ConfigController
# from controllers.database_controller import DatabaseController
# from controllers.excel_controller import ExcelController
# from controllers.email_controller import EmailController


class MainController:
    """
    Controlador principal que coordina la interacción entre los diferentes
    componentes de la aplicación.
    
    Este controlador inicializa todos los controladores secundarios y
    la vista principal, y sirve como punto central de comunicación.
    """

    def __init__(self, root):
        """
        Inicializa el controlador principal.
        
        Args:
            root: Ventana raíz de la aplicación (CTk)
        """
        # Inicializar el gestor de configuraciones
        self.config_manager = ConfigManager()

        # Inicializar controladores secundarios
        # self.config_controller = ConfigController(self)
        # self.database_controller = DatabaseController(self)
        # self.excel_controller = ExcelController(self)
        # self.email_controller = EmailController(self)

        # Inicializar la vista principal
        self.view = AppView(root, self)

        # Cargar las configuraciones iniciales
        self._load_initial_settings()

    def _load_initial_settings(self):
        """
        Carga las configuraciones iniciales de la aplicación.
        """
        # Aplicar tema desde configuración
        app_config = self.config_manager.get_config("app")
        if app_config:
            theme = app_config.get("theme", "system")
            color_theme = app_config.get("color_theme", "blue")

            # Actualizar tema en la vista
            self.view.set_appearance_mode(theme)
            self.view.set_color_theme(color_theme)

            # Verificar si las funcionalidades de BD están habilitadas
            db_enabled = self.config_manager.get_config("database", "enabled")
            # self.view.set_database_features_state(db_enabled)

    def save_config(self, section, key, value):
        """
        Guarda un valor en la configuración.
        
        Args:
            section (str): Sección de la configuración
            key (str): Clave dentro de la sección
            value: Valor a guardar
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        return self.config_manager.set_config(section, key, value)

    def get_config(self, section=None, key=None):
        """
        Obtiene un valor de la configuración.
        
        Args:
            section (str, opcional): Sección de la configuración
            key (str, opcional): Clave dentro de la sección
            
        Returns:
            El valor de configuración solicitado o toda la configuración
        """
        return self.config_manager.get_config(section, key)

    def update_section(self, section, values):
        """
        Actualiza una sección completa de la configuración.
        
        Args:
            section (str): Sección de la configuración a actualizar
            values (dict): Diccionario con los nuevos valores
            
        Returns:
            bool: True si se guardó correctamente, False en caso contrario
        """
        return self.config_manager.update_section(section, values)

    def check_database_connection(self):
        """
        Verifica si la conexión a la base de datos está configurada y activa.
        
        Returns:
            bool: True si la conexión está disponible, False en caso contrario
        """
        return self.database_controller.check_connection()

    def toggle_database_features(self, enabled):
        """
        Activa o desactiva las funcionalidades relacionadas con la base de datos.
        
        Args:
            enabled (bool): True para activar, False para desactivar
            
        Returns:
            bool: True si se cambió correctamente, False en caso contrario
        """
        # Actualizar configuración
        result = self.save_config("database", "enabled", enabled)

        # Actualizar estado en la interfaz
        if result:
            self.view.set_database_features_state(enabled)

        return result
