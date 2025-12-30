from sqlalchemy import create_engine, text

DATABASE_URL = "mysql+pymysql://root:@localhost/api_database"

engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
        print("Conexión exitosa a la base de datos")
except Exception as e:
    print("Error al conectar a la base de datos:", e)
