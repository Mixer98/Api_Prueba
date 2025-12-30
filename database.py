from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator

# Cadena de conexión a MySQL usando PyMySQL
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:@localhost/api_database"

# Crea el engine que gestionará las conexiones a la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Genera una sesión por petición con commit/control manual
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para declarar los modelos ORM
Base = declarative_base()


def get_db() -> Generator:  # Dependencia de FastAPI para inyectar una sesion por solicitud
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()