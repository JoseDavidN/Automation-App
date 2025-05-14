automationApp/
│
├── main.py                     # Punto de entrada de la aplicación
│
├── config/
│   ├── __init__.py
│   ├── config_manager.py       # Gestión de configuraciones (JSON)
│   └── default_config.json     # Configuraciones predeterminadas
│
├── models/                     # Capa de datos y lógica de negocio
│   ├── __init__.py
│   ├── database_model.py       # Manejo de conexiones y consultas a BD
│   ├── excel_model.py          # Procesamiento y formateo de Excel
│   └── email_model.py          # Lógica de envío de correos
│
├── controllers/                # Intermediarios entre vistas y modelos
│   ├── __init__.py
│   ├── main_controller.py      # Controlador principal
│   ├── config_controller.py    # Controlador de configuraciones
│   ├── database_controller.py  # Controlador de operaciones de BD
│   ├── excel_controller.py     # Controlador de operaciones Excel
│   └── email_controller.py     # Controlador de operaciones de correo
│
├── views/                      # Interfaz de usuario
│   ├── __init__.py
│   ├── app.py                  # Ventana principal y gestión de tabs
│   ├── config_tab.py           # Tab de configuraciones
│   ├── connection_tab.py       # Tab de conexión a BD
│   ├── excel_tab.py            # Tab de formateo Excel
│   ├── email_tab.py            # Tab de automatización de correos
│   └── preview_tab.py          # Tab de vista previa de archivos
│
└── utils/                      # Funciones y clases auxiliares
    ├── __init__.py
    ├── file_manager.py         # Gestión de archivos temporales
    ├── validators.py           # Validaciones de formularios y datos
    └── constants.py            # Constantes utilizadas en la aplicación
