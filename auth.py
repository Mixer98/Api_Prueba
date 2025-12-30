from datetime import datetime, timedelta  # Para calcular expiracion del token
from typing import Optional  # Tipado opcional

from jose import JWTError, jwt  # Para crear y verificar tokens JWT
from passlib.context import CryptContext  # Para hashear contraseñas con bcrypt

# Configuración de seguridad
SECRET_KEY = "tu_clave_secreta_muy_segura_cambiala_en_produccion"  # CAMBIAR en producción
ALGORITHM = "HS256"  # Algoritmo de encriptación para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Tiempo de vida del token en minutos

# Contexto de bcrypt para hashear contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  # Configuracion de bcrypt


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
