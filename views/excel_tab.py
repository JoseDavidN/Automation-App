import customtkinter as ctk
import os
from pathlib import Path
from tkinter import filedialog


class ExcelTab:
    """
    Tab para la funcionalidad de formateo de Excel.
    Permite al usuario cargar archivos Excel y aplicar formatos.
    """

    def __init__(self, parent, controller):
        """
        Inicializa el tab de Excel.
        
        Args:
            parent: Frame contenedor (tab del CTkTabview)
            controller: Instancia del controlador principal
        """
        self.parent = parent
        self.controller = controller
        self.excel_controller = controller.excel_controller

        # Crear el layout principal
        self.create_widgets()

        # Cargar configuración inicial
        self.load_config()

    def create_widgets(self):
        """
        Crea los widgets para el tab de Excel.
        """
        # Frame principal con scrollbar
        self.main_frame = ctk.CTkScrollableFrame(self.parent)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Sección: Selección de archivo
        self.create_file_section()

        # Separador
        self.separator1 = ctk.CTkFrame(
            self.main_frame, height=2, fg_color="grey")
        self.separator1.grid(row=1, column=0, sticky="ew", padx=10, pady=15)

        # Sección: Opciones de formato
        self.create_format_section()

        # Separador
        self.separator2 = ctk.CTkFrame(
            self.main_frame, height=2, fg_color="grey")
        self.separator2.grid(row=3, column=0, sticky="ew", padx=10, pady=15)

        # Sección: Acciones
        self.create_actions_section()

    def create_file_section(self):
        """
        Crea la sección para seleccionar archivos Excel.
        """
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=10)
        file_frame.grid_columnconfigure(1, weight=1)

        # Título de la sección
        title_label = ctk.CTkLabel(
            file_frame,
            text="Selección de Archivo",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=3,
                         sticky="w", padx=10, pady=(10, 20))

        # Selector de archivo
        file_label = ctk.CTkLabel(file_frame, text="Archivo Excel:")
        file_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.file_var = ctk.StringVar()
        self.file_entry = ctk.CTkEntry(
            file_frame, textvariable=self.file_var, width=300)
        self.file_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        self.browse_button = ctk.CTkButton(
            file_frame,
            text="Examinar",
            command=self.browse_file
        )
        self.browse_button.grid(row=1, column=2, sticky="e", padx=10, pady=10)

        # Archivos recientes
        recent_label = ctk.CTkLabel(file_frame, text="Archivos recientes:")
        recent_label.grid(row=2, column=0, sticky="w", padx=10, pady=(20, 10))

        self.recent_files_frame = ctk.CTkFrame(
            file_frame, fg_color="transparent")
        self.recent_files_frame.grid(
            row=3, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
        self.recent_files_frame.grid_columnconfigure(0, weight=1)

        # Se cargarán dinámicamente en load_config()

    def create_format_section(self):
        """
        Crea la sección para las opciones de formato.
        """
        format_frame = ctk.CTkFrame(self.main_frame)
        format_frame.grid(row=2, column=0, sticky="ew", padx=0, pady=10)
        format_frame.grid_columnconfigure(0, weight=1)
        format_frame.grid_columnconfigure(1, weight=1)

        # Título de la sección
        title_label = ctk.CTkLabel(
            format_frame,
            text="Opciones de Formato",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2,
                         sticky="w", padx=10, pady=(10, 20))

        # Color de encabezado
        header_label = ctk.CTkLabel(format_frame, text="Color de encabezado:")
        header_label.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        # Frame para color y su visualización
        color_frame = ctk.CTkFrame(format_frame, fg_color="transparent")
        color_frame.grid(row=1, column=1, sticky="w", padx=10, pady=10)

        self.header_color_var = ctk.StringVar(value="4F81BD")
        self.header_color_entry = ctk.CTkEntry(
            color_frame,
            textvariable=self.header_color_var,
            width=100
        )
        self.header_color_entry.grid(row=0, column=0, padx=(0, 10))

        # Muestra de color
        self.color_preview = ctk.CTkFrame(
            color_frame, width=30, height=30, fg_color="#4F81BD")
        self.color_preview.grid(row=0, column=1)

        # Actualizar la muestra de color cuando cambie el valor
        self.header_color_var.trace_add("write", self.update_color_preview)

        # Crear tablas
        self.create_tables_var = ctk.BooleanVar(value=True)
        create_tables_checkbox = ctk.CTkCheckBox(
            format_frame,
            text="Crear tablas en Excel",
            variable=self.create_tables_var
        )
        create_tables_checkbox.grid(
            row=2, column=0, sticky="w", padx=10, pady=10)

        # Estilo de tabla
        style_label = ctk.CTkLabel(format_frame, text="Estilo de tabla:")
        style_label.grid(row=3, column=0, sticky="w", padx=10, pady=10)

        self.table_style_var = ctk.StringVar(value="TableStyleMedium9")
        table_styles = [
            "TableStyleLight1", "TableStyleLight2", "TableStyleLight3",
            "TableStyleMedium1", "TableStyleMedium2", "TableStyleMedium3",
            "TableStyleMedium9", "TableStyleMedium10", "TableStyleMedium11",
            "TableStyleDark1", "TableStyleDark2", "TableStyleDark3"
        ]

        table_style_combobox = ctk.CTkComboBox(
            format_frame,
            values=table_styles,
            variable=self.table_style_var,
            width=200
        )
        table_style_combobox.grid(
            row=3, column=1, sticky="w", padx=10, pady=10)

        # Opciones avanzadas
        advanced_button = ctk.CTkButton(
            format_frame,
            text="Opciones avanzadas",
            command=self.open_advanced_options
        )
        advanced_button.grid(row=4, column=0, columnspan=2,
                             sticky="w", padx=10, pady=(20, 10))

    def create_actions_section(self):
        """
        Crea la sección para las acciones disponibles.
        """
        actions_frame = ctk.CTkFrame(self.main_frame)
        actions_frame.grid(row=4, column=0, sticky="ew", padx=0, pady=10)
        actions_frame.grid_columnconfigure(0, weight=1)
        actions_frame.grid_columnconfigure(1, weight=1)

        # Título de la sección
        title_label = ctk.CTkLabel(
            actions_frame,
            text="Acciones",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.grid(row=0, column=0, columnspan=2,
                         sticky="w", padx=10, pady=(10, 20))

        # Botón de vista previa
        preview_button = ctk.CTkButton(
            actions_frame,
            text="Vista Previa",
            command=self.preview_excel
        )
        preview_button.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

        # Botón de formatear
        format_button = ctk.CTkButton(
            actions_frame,
            text="Formatear Excel",
            command=self.format_excel,
            fg_color="#2D7D46",  # Verde para indicar acción principal
            hover_color="#235e35"
        )
        format_button.grid(row=1, column=1, sticky="ew", padx=20, pady=10)

        # Botón de guardar configuración como predeterminada
        save_config_button = ctk.CTkButton(
            actions_frame,
            text="Guardar como configuración predeterminada",
            command=self.save_default_config
        )
        save_config_button.grid(
            row=2, column=0, columnspan=2, sticky="ew", padx=20, pady=(20, 10))

    def browse_file(self):
        """
        Abre el diálogo para seleccionar un archivo Excel.
        """
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo Excel",
            filetypes=[("Archivos Excel", "*.xlsx *.xls")]
        )

        if file_path:
            self.file_var.set(file_path)
            self.add_to_recent_files(file_path)

    def update_color_preview(self, *args):
        """
        Actualiza el preview del color cuando cambia el valor.
        """
        try:
            color_hex = self.header_color_var.get()
            if not color_hex.startswith("#"):
                color_hex = f"#{color_hex}"
            self.color_preview.configure(fg_color=color_hex)
        except Exception:
            # Si el color no es válido, mantener el anterior
            pass

    def load_config(self):
        """
        Carga la configuración desde el gestor de configuraciones.
        """
        # Obtener configuración de Excel
        excel_config = self.controller.get_config("excel")
        if excel_config and "default_format" in excel_config:
            format_config = excel_config["default_format"]

            # Actualizar los widgets con los valores de configuración
            if "header_color" in format_config:
                self.header_color_var.set(format_config["header_color"])

            if "create_tables" in format_config:
                self.create_tables_var.set(format_config["create_tables"])

            if "table_style" in format_config:
                self.table_style_var.set(format_config["table_style"])

        # Cargar archivos recientes
        self.load_recent_files()

    def load_recent_files(self):
        """
        Carga y muestra la lista de archivos recientes.
        """
        # Limpiar el frame de archivos recientes
        for widget in self.recent_files_frame.winfo_children():
            widget.destroy()

        # Obtener lista de archivos recientes
        excel_config = self.controller.get_config("excel")
        recent_files = []

        if excel_config and "recent_files" in excel_config:
            recent_files = excel_config["recent_files"]

        # Si no hay archivos recientes
        if not recent_files:
            no_files_label = ctk.CTkLabel(
                self.recent_files_frame,
                text="No hay archivos recientes",
                text_color="gray"
            )
            no_files_label.grid(row=0, column=0, padx=10, pady=5)
            return

        # Mostrar archivos recientes (máximo 5)
        for i, file_path in enumerate(recent_files[:5]):
            file_name = os.path.basename(file_path)

            # Frame para contener el archivo y el botón de eliminar
            file_item_frame = ctk.CTkFrame(
                self.recent_files_frame, fg_color="transparent")
            file_item_frame.grid(row=i, column=0, sticky="ew", padx=5, pady=2)
            file_item_frame.grid_columnconfigure(0, weight=1)

            # Botón para cargar el archivo reciente
            file_button = ctk.CTkButton(
                file_item_frame,
                text=file_name,
                anchor="w",
                fg_color="transparent",
                text_color=("gray10", "gray90"),
                hover_color=("gray70", "gray30"),
                command=lambda path=file_path: self.file_var.set(path)
            )
            file_button.grid(row=0, column=0, sticky="ew", padx=5, pady=2)

            # Botón para eliminar de recientes
            delete_button = ctk.CTkButton(
                file_item_frame,
                text="×",
                width=30,
                fg_color="transparent",
                hover_color=("gray70", "gray30"),
                command=lambda path=file_path: self.remove_from_recent_files(
                    path)
            )
            delete_button.grid(row=0, column=1, padx=5, pady=2)

    def add_to_recent_files(self, file_path):
        """
        Agrega un archivo a la lista de archivos recientes.
        
        Args:
            file_path (str): Ruta del archivo a agregar
        """
        excel_config = self.controller.get_config("excel") or {}
        recent_files = excel_config.get("recent_files", [])

        # Eliminar si ya existe (para ponerlo al principio)
        if file_path in recent_files:
            recent_files.remove(file_path)

        # Agregar al principio
        recent_files.insert(0, file_path)

        # Mantener solo los últimos 10 archivos
        recent_files = recent_files[:10]

        # Actualizar configuración
        if "excel" not in self.controller.get_config():
            self.controller.update_section(
                "excel", {"recent_files": recent_files})
        else:
            excel_config["recent_files"] = recent_files
            self.controller.update_section("excel", excel_config)

        # Recargar la lista
        self.load_recent_files()

    def remove_from_recent_files(self, file_path):
        """
        Elimina un archivo de la lista de archivos recientes.
        
        Args:
            file_path (str): Ruta del archivo a eliminar
        """
        excel_config = self.controller.get_config("excel") or {}
        recent_files = excel_config.get("recent_files", [])

        if file_path in recent_files:
            recent_files.remove(file_path)

            # Actualizar configuración
            excel_config["recent_files"] = recent_files
            self.controller.update_section("excel", excel_config)

            # Recargar la lista
            self.load_recent_files()

    def save_default_config(self):
        """
        Guarda la configuración actual como predeterminada.
        """
        format_config = {
            "header_color": self.header_color_var.get(),
            "create_tables": self.create_tables_var.get(),
            "table_style": self.table_style_var.get()
        }

        excel_config = self.controller.get_config("excel") or {}
        excel_config["default_format"] = format_config

        if self.controller.update_section("excel", excel_config):
            self.controller.view.set_status(
                "Configuración guardada como predeterminada")

    def open_advanced_options(self):
        """
        Abre un diálogo para opciones avanzadas de formato.
        """
        # Crear ventana de diálogo
        dialog = ctk.CTkToplevel(self.parent)
        dialog.title("Opciones avanzadas de formato")
        dialog.geometry("500x400")
        dialog.grab_set()  # Modal

        # Implementar opciones avanzadas aquí
        label = ctk.CTkLabel(
            dialog, text="Opciones avanzadas de formato (a implementar)")
        label.pack(padx=20, pady=20)

    def preview_excel(self):
        """
        Realiza una vista previa del formato en el archivo Excel.
        """
        file_path = self.file_var.get()

        if not file_path:
            self.controller.view.set_status("Seleccione un archivo Excel")
            return

        if not os.path.exists(file_path):
            self.controller.view.set_status(
                f"El archivo {file_path} no existe")
            return

        # Obtener opciones de formato
        format_options = {
            "header_color": self.header_color_var.get(),
            "create_tables": self.create_tables_var.get(),
            "table_style": self.table_style_var.get()
        }

        # Mostrar vista previa (implementar en el controlador)
        result = self.excel_controller.preview_format(
            file_path, format_options)

        if result:
            self.controller.view.set_status("Vista previa generada")
            # Cambiar a la pestaña de vista previa
            self.controller.view.tabview.set("Vista Previa")
        else:
            self.controller.view.set_status("Error al generar vista previa")

    def format_excel(self):
        """
        Formatea el archivo Excel con las opciones especificadas.
        """
        file_path = self.file_var.get()

        if not file_path:
            self.controller.view.set_status("Seleccione un archivo Excel")
            return

        if not os.path.exists(file_path):
            self.controller.view.set_status(
                f"El archivo {file_path} no existe")
            return

        # Obtener opciones de formato
        format_options = {
            "header_color": self.header_color_var.get(),
            "create_tables": self.create_tables_var.get(),
            "table_style": self.table_style_var.get()
        }

        # Formatear archivo (implementar en el controlador)
        result = self.excel_controller.format_excel(file_path, format_options)

        if result:
            self.controller.view.set_status(
                f"Archivo {os.path.basename(file_path)} formateado correctamente")
            self.add_to_recent_files(file_path)
        else:
            self.controller.view.set_status("Error al formatear el archivo")
