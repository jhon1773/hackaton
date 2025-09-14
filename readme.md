<!--
proyecto con Jinja2 para usar un template base, uso de bootstrap y separar el CSS en un archivo externo.
-->

# correr el programa

# eliminar entorno virtual antiguo

elimina la carpeta .venv

# -- Entorno virtual

py -m venv .venv

# -- Acceso al entorno virtual

.venv\Scripts\Activate.ps1

pip install flask

# instalar las librerias

pip install -r requirements.txt

# descargar manual si no funciona_____________________________________________________

pip install numpy
pip install matplotlib
pip install kiwisolver
pip install flask
pip install pandas
pip install openpyxl
pip install reportlab
pip install matplotlib
pip install Pillow
pip install kiwisolver

# ejecutar la base de datos______________________________________________________________________________

copiar el sql.txt en tu administrador de base de datos preferida

añadir IMPORTANTE:

ALTER TABLE pqrsd ADD COLUMN respuesta TEXT;

# insertar un funcionario

INSERT INTO usuarios (nombre, email, password, area_id, rol_id)
VALUES ("NOMBRE_FUNCIONARIO", "EMAIL_FUNCIONARIO", "PASSWORD_HASH", "ID_AREA", "ID_ROL_FUNCIONARIO");

EJEMPLO
VALUES ("funcionario1", "emailfuncionario@gmail.com", "123456789", "(1-8)", "2");

# agregar un admin

INSERT INTO usuarios (nombre, email, password, area_id, rol_id)
VALUES ("NOMBRE_ADMIN", "EMAIL_ADMIN", "PASSWORD_HASH", "ID_AREA", "ID_ROL_ADMINISTRADOR");

EJEMPLO
VALUES ("admin", "emailadmin@gmail.com", "123456789", "(1-8)", "1");

# ___________________________________________________________________________________________________

# ejecución

python app.py

## para salir del entorno virtual (.venv)

deactivate

# ------ COMANDOS A TENER EN CUENTA___________________________________________________________________

# para validar y mostrar información detallada del paquete python-dotenv

pip show python-dotenv

# listar las instalaciones

pip list

# Ver ruta de instalación

pip show flask | findstr Location

# para generar un archivo de dependencias

pip freeze > requirements.txt

# para instalar el archivo de dependencias generado

pip install -r requirements.txt

# Actualizar el archivo al agregar paquetes nuevos

pip freeze > requirements.txt


# _____________________________________________________________________________________________________