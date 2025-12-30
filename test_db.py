from sqlalchemy import create_engine, text  # Utilidades de SQLAlchemy para conexiones y SQL crudo

DATABASE_URL = "mysql+pymysql://root:@localhost/api_database"  # Cadena de conexion a MySQL

engine = create_engine(DATABASE_URL)  # Crea el engine de SQLAlchemy

try:  # Intenta conectarse a la BD
    with engine.connect() as connection:  # Abre una conexion
        connection.execute(text("SELECT 1"))  # Ejecuta un ping simple
        print("Conexión exitosa a la base de datos")  # Mensaje de exito
except Exception as e:  # Si ocurre un error
    print("Error al conectar a la base de datos:", e)  # Muestra el error
