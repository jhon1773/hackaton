import os
from dotenv import load_dotenv


load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "pqrsd-secret-key-2023")
    
    # Configuración de la base de datos
    DB_HOST = os.getenv("MYSQL_HOST", "localhost")
    DB_USER = os.getenv("MYSQL_USER", "pqrsd_user")
    DB_PASSWORD = os.getenv("MYSQL_PASSWORD", "pqrsd_password_2023")
    DB_NAME = os.getenv("MYSQL_DB", "sistema_pqrsd")
    DB_PORT = os.getenv("MYSQL_PORT", "3306")
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False