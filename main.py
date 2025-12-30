from fastapi import FastAPI  # Importa el framework FastAPI
from database import engine  # Engine de SQLAlchemy para conectar a la BD
from model import Base  # Base de modelos ORM (no se usa aún en este archivo)


# Crea la instancia principal de la aplicación FastAPI
app = FastAPI()



@app.on_event("startup")
def on_startup():
    try:
        Base.metadata.create_all(bind=engine)
    except Exception as exc:
        # registra o imprime el error para depurar
        print(f"Error creando tablas: {exc}")


# Ruta raíz que responde con un mensaje simple
@app.get("/")
def root():
    return {"message": "API funcionando"}
