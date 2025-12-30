import os  # Lectura de variables de entorno
from datetime import datetime, timedelta  # Para calcular expiracion del token
from typing import Optional  # Tipado opcional

from fastapi import Depends, HTTPException, status  # Dependencias y errores HTTP
from fastapi.security import OAuth2PasswordBearer  # Esquema OAuth2 Bearer
from jose import JWTError, jwt  # Para crear y verificar tokens JWT
from passlib.context import CryptContext  # Para hashear contraseñas con bcrypt
from sqlalchemy.orm import Session  # Sesion de SQLAlchemy

from database import get_db  # Dependencia para obtener la sesion
from model import User  # Modelo de usuario

# Configuración de seguridad (leer de variables de entorno)
SECRET_KEY = os.getenv("SECRET_KEY", "cambia_esta_clave_en_prod")  # Clave JWT
ALGORITHM = "HS256"  # Algoritmo de encriptación para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))  # Expiracion del token

# Contexto de bcrypt para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Configuracion de bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # Esquema Bearer para extraer el token


def hash_password(password: str) -> str:  # Hashea una contraseña en texto plano
    """Convierte una contraseña en texto plano a un hash seguro"""
    return pwd_context.hash(password)  # Retorna el hash bcrypt


def verify_password(plain_password: str, hashed_password: str) -> bool:  # Verifica si la contraseña coincide
    """Compara una contraseña en texto plano con un hash"""
    return pwd_context.verify(plain_password, hashed_password)  # True si coincide, False si no


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:  # Crea un token JWT
    """Genera un token JWT con los datos proporcionados y una fecha de expiración"""
    to_encode = data.copy()  # Copia los datos para no modificar el original
    if expires_delta:  # Si se proporciona un tiempo de expiracion
        expire = datetime.utcnow() + expires_delta  # Calcula la fecha de expiracion
    else:  # Si no se proporciona tiempo
        expire = datetime.utcnow() + timedelta(minutes=15)  # Expira en 15 minutos por defecto
    to_encode.update({"exp": expire})  # Agrega la fecha de expiracion al payload
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  # Crea el token JWT
    return encoded_jwt  # Retorna el token generado


def get_current_user(  # Obtiene el usuario actual a partir del token JWT
    token: str = Depends(oauth2_scheme),  # Extrae el token del header Authorization
    db: Session = Depends(get_db)  # Sesion de BD para buscar al usuario
) -> User:  # Devuelve la instancia de usuario
    credentials_exception = HTTPException(  # Error 401 en caso de token invalido
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas o token expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  # Decodifica el token
        username: Optional[str] = payload.get("sub")  # Obtiene el subject (username)
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()  # Busca el usuario en BD
    if user is None:
        raise credentials_exception
    return user  # Usuario autenticado
