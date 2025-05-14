from controllers.main_controller import MainController
import customtkinter as ctk
import sys
import os

# Agregar la carpeta del proyecto al path para poder importar los módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def main():
    """
    Función principal que inicia la aplicación.
    Configura el tema, crea la instancia del controlador principal y ejecuta el loop principal.
    """

    # Configuración de CustomTkinter
    # Modes: "System" (standard), "Dark", "Light"
    # ctk.set_appearance_mode("Dark")
    # Themes: "blue" (standard), "green", "dark-blue"
    # ctk.set_default_color_theme("dark-blue")

    # Crear y configurar la ventana raíz
    app = ctk.CTk()
    app.title("Herramienta de Automatización")
    app.geometry("1200x700")
    app.minsize(900, 600)

    # Inicializar el controlador principal
    controller = MainController(app)

    # Ejecutar la aplicación
    app.mainloop()


if __name__ == "__main__":
    main()
