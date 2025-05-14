import os
import shutil
from pathlib import Path
from models.excel_model import ExcelModel


class ExcelController:
    """
    Controlador para manejar operaciones relacionadas con archivos Excel.
    Coordina la interacción entre la vista y el modelo de datos Excel.
    """

    def __init__(self, main_controller):
        """
        Inicializa el controlador de Excel.
        
        Args:
            main_controller: Controlador principal de la aplicación
        """
        self.main_controller = main_controller
        self.excel_model = ExcelModel()

        # Crear directorio temporal si no existe
        self.temp_dir = self._get_temp_dir()
        os.makedirs(self.temp_dir, exist_ok=True)

    def _get_temp_dir(self):
        """
        Obtiene la ruta del directorio temporal para archivos.
        
        Returns:
            Path: Ruta del directorio temporal
        """
        app_config = self.main_controller.get_config("app")
        temp_dir_name = app_config.get(
            "temp_dir", "temp") if app_config else "temp"

        # Crear directorio temporal en la carpeta de la aplicación
        app_dir = Path.home() / ".automationApp"
        return app_dir / temp_dir_name

    def format_excel(self, file_path, format_options):
        """
        Formatea un archivo Excel con las opciones especificadas.
        
        Args:
            file_path (str): Ruta del archivo Excel a formatear
            format_options (dict): Opciones de formato
        
        Returns:
            bool: True si el formateo fue exitoso, False en caso contrario
        """
        try:
            # Convertir boolean de string a Python bool si es necesario
            if isinstance(format_options.get("create_tables"), str):
                format_options["create_tables"] = format_options["create_tables"].lower(
                ) == "true"

            # Llamar al modelo para formatear el archivo
            return self.excel_model.format_excel(
                file_path,
                header_color=format_options.get("header_color", "4F81BD"),
                crear_tablas=format_options.get("create_tables", True),
                tabla_estilo=format_options.get(
                    "table_style", "TableStyleMedium9")
            )
        except Exception as e:
            print(f"Error al formatear Excel: {e}")
            return False

    def preview_format(self, file_path, format_options):
        """
        Genera una vista previa del formato en un archivo temporal.
        
        Args:
            file_path (str): Ruta del archivo Excel original
            format_options (dict): Opciones de formato
        
        Returns:
            str: Ruta del archivo temporal con la vista previa, o None si falló
        """
        try:
            # Crear nombre del archivo temporal
            file_name = os.path.basename(file_path)
            temp_file = os.path.join(self.temp_dir, f"preview_{file_name}")

            # Copiar el archivo original al temporal
            shutil.copy2(file_path, temp_file)

            # Formatear el archivo temporal
            success = self.format_excel(temp_file, format_options)

            if success:
                # Notificar a la vista de previsualización que hay un nuevo archivo
                # (esto debe implementarse en el controlador principal)
                self.main_controller.view.preview_view.set_preview_file(
                    temp_file, "excel")
                return temp_file
            else:
                return None

        except Exception as e:
            print(f"Error al generar vista previa: {e}")
            return None

    def get_sheet_names(self, file_path):
        """
        Obtiene los nombres de las hojas en un archivo Excel.
        
        Args:
            file_path (str): Ruta del archivo Excel
        
        Returns:
            list: Lista de nombres de hojas, o None si falló
        """
        try:
            return self.excel_model.get_sheet_names(file_path)
        except Exception as e:
            print(f"Error al obtener nombres de hojas: {e}")
            return None

    def export_to_csv(self, excel_file, output_path, sheet_name=None):
        """
        Exporta una hoja de Excel a CSV.
        
        Args:
            excel_file (str): Ruta del archivo Excel
            output_path (str): Ruta donde guardar el CSV
            sheet_name (str, opcional): Nombre de la hoja a exportar
        
        Returns:
            bool: True si la exportación fue exitosa, False en caso contrario
        """
        try:
            return self.excel_model.export_to_csv(excel_file, output_path, sheet_name)
        except Exception as e:
            print(f"Error al exportar a CSV: {e}")
            return False

    def cleanup_temp_files(self):
        """
        Limpia los archivos temporales generados.
        
        Returns:
            bool: True si la limpieza fue exitosa, False en caso contrario
        """
        try:
            # Verificar si está activada la limpieza automática
            app_config = self.main_controller.get_config("app")
            if app_config and not app_config.get("auto_cleanup", True):
                return True

            # Eliminar archivos en el directorio temporal
            for file in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print(f"Error al eliminar {file_path}: {e}")

            return True
        except Exception as e:
            print(f"Error al limpiar archivos temporales: {e}")
            return False
