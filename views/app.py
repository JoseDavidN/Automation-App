import customtkinter as ctk
# from views.config_tab import ConfigTab
# from views.connection_tab import ConnectionTab
# from views.excel_tab import ExcelTab
# from views.email_tab import EmailTab
# from views.preview_tab import PreviewTab


class AppView:
    """
    Vista principal de la aplicación que organiza todos los tabs y componentes de la interfaz.
    Esta clase administra la interfaz de usuario y delega la lógica al controlador principal.
    """

    def __init__(self, root, controller):
        """
        Inicializa la vista principal.
        
        Args:
            root: Ventana raíz de la aplicación (CTk)
            controller: Instancia del controlador principal
        """
        
        self.root = root
        self.controller = controller

        # Configurar el layout principal
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Crear un marco principal para contener todo
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Configurar el layout del marco principal
        self.main_frame.grid_columnconfigure(0, weight=1)
        # Espacio para un banner o información
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(
            1, weight=1)  # Espacio para el tabview
        # Espacio para la barra de estado
        self.main_frame.grid_rowconfigure(2, weight=0)

        # Crear un banner o cabecera
        self.create_header()

        # Crear TabView para organizar las diferentes vistas
        self.create_tabview()

        # Crear la barra de estado
        self.create_status_bar()

        # Inicializar los controladores de estado
        self.database_enabled = False

    def create_header(self):
        """
        Crea el encabezado de la aplicación.
        """
        header_frame = ctk.CTkFrame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 10))
        header_frame.grid_columnconfigure(0, weight=1)

        # Título de la aplicación
        title_label = ctk.CTkLabel(
            header_frame,
            text="Herramienta de Automatización",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Botones de configuración rápida (opcionales)
        settings_button = ctk.CTkButton(
            header_frame,
            text="⚙️",
            width=40,
            command=self.open_config_tab
        )
        settings_button.grid(row=0, column=1, padx=5, pady=5)

    def create_tabview(self):
        """
        Crea el sistema de pestañas (tabs) para la aplicación.
        """
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        # Crear las pestañas
        self.tab_config = self.tabview.add("Configuración")
        self.tab_connection = self.tabview.add("Conexión")
        self.tab_excel = self.tabview.add("Excel")
        self.tab_email = self.tabview.add("Email")
        self.tab_preview = self.tabview.add("Vista Previa")

        # Configurar el layout de cada pestaña
        for tab in [self.tab_config, self.tab_connection, self.tab_excel, self.tab_email, self.tab_preview]:
            tab.grid_columnconfigure(0, weight=1)
            tab.grid_rowconfigure(0, weight=1)

        # Inicializar cada pestaña con su propia clase
        # self.config_view = ConfigTab(self.tab_config, self.controller)
        # self.connection_view = ConnectionTab(
        #     self.tab_connection, self.controller)
        # self.excel_view = ExcelTab(self.tab_excel, self.controller)
        # self.email_view = EmailTab(self.tab_email, self.controller)
        # self.preview_view = PreviewTab(self.tab_preview, self.controller)

    def create_status_bar(self):
        """
        Crea la barra de estado en la parte inferior de la aplicación.
        """
        status_frame = ctk.CTkFrame(self.main_frame, height=30)
        status_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=(10, 5))
        status_frame.grid_columnconfigure(0, weight=1)
        status_frame.grid_columnconfigure(1, weight=0)

        # Texto de estado
        self.status_label = ctk.CTkLabel(
            status_frame, text="Listo", anchor="w")
        self.status_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Indicador de conexión a base de datos
        self.db_status_frame = ctk.CTkFrame(
            status_frame, fg_color="transparent")
        self.db_status_frame.grid(row=0, column=1, padx=10, pady=5)

        self.db_status_label = ctk.CTkLabel(self.db_status_frame, text="BD:")
        self.db_status_label.grid(row=0, column=0, padx=(0, 5))

        self.db_status_indicator = ctk.CTkLabel(
            self.db_status_frame,
            text="✗",
            text_color="red",
            width=20
        )
        self.db_status_indicator.grid(row=0, column=1, padx=0)

    def set_status(self, message):
        """
        Actualiza el mensaje de la barra de estado.
        
        Args:
            message (str): Mensaje a mostrar
        """
        self.status_label.configure(text=message)

    def set_database_status(self, connected):
        """
        Actualiza el indicador de estado de la conexión a la base de datos.
        
        Args:
            connected (bool): True si está conectado, False en caso contrario
        """
        if connected:
            self.db_status_indicator.configure(text="✓", text_color="green")
        else:
            self.db_status_indicator.configure(text="✗", text_color="red")

    def set_database_features_state(self, enabled):
        """
        Activa o desactiva las funcionalidades relacionadas con la base de datos.
        
        Args:
            enabled (bool): True para activar, False para desactivar
        """
        self.database_enabled = enabled

        # Actualizar la interfaz en las pestañas que dependen de la BD
        self.connection_view.set_state(enabled)
        self.email_view.set_database_features_state(enabled)

        # Actualizar indicador solo si cambia el estado
        is_connected = self.controller.check_database_connection()
        self.set_database_status(enabled and is_connected)

    def open_config_tab(self):
        """
        Abre la pestaña de configuración.
        """
        self.tabview.set("Configuración")

    def set_appearance_mode(self, mode):
        """
        Configura el modo de apariencia de la aplicación.
        
        Args:
            mode (str): "System", "Dark" o "Light"
        """
        ctk.set_appearance_mode(mode)

    def set_color_theme(self, theme):
        """
        Configura el tema de color de la aplicación.
        
        Args:
            theme (str): Nombre del tema de color ("blue", "green", etc.)
        """
        ctk.set_default_color_theme(theme)
