# API de Prueba (FastAPI)

CRUD de tareas con autenticación JWT.

## Requisitos
- Python 3.11+ (usando venv)
- Base de datos: MySQL local (actual) usando PyMySQL
- XAMPP: activar el servicio MySQL (no es necesario Apache para la API)
- SQL inicial: importar `api_database.sql` en tu MySQL (phpMyAdmin o consola) para crear la base y datos de arranque si aplica
- Variables de entorno:
  - `SECRET_KEY` (obligatoria para JWT)
  - `ACCESS_TOKEN_EXPIRE_MINUTES` (opcional, por defecto 30)
  - `DATABASE_URL` (opcional; si no se define, usa la cadena en `database.py`)
    - Formato MySQL: `mysql+pymysql://USER:PASSWORD@HOST:PORT/NOMBRE_BD`
    - Ejemplo local (XAMPP): `mysql+pymysql://root:@localhost:3306/api_database`

## Instalación
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Ejecutar
```bash
uvicorn main:app --reload
```
La API queda en `http://127.0.0.1:8000` y la documentación en `http://127.0.0.1:8000/docs`.

## Autenticación
- Registro: `POST /auth/register` (JSON)
- Login: `POST /auth/login` (form-data `username`, `password`)
- Usa el token en los endpoints protegidos con el header:
  ```
  Authorization: Bearer <token>
  ```
- En `/docs`, pulsa **Authorize**, ingresa `username` y `password`, y Swagger inyecta el token.

## Endpoints principales
- `POST /tasks` (protegido): crea tarea.
- `GET /tasks`: lista con paginación (`page`, `page_size`).
- `GET /tasks/{id}`: obtiene tarea.
- `PUT /tasks/{id}` (protegido): actualiza tarea.
- `DELETE /tasks/{id}` (protegido): elimina tarea.

## Ejemplos curl
Registrar:
```bash
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","password":"secreto123"}'
```
Login (form-data):
```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=secreto123"
```
Crear tarea (requiere token):
```bash
curl -X POST http://127.0.0.1:8000/tasks \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"titulo":"Comprar pan","descripcion":"Integral","estado":"pending"}'
```
Listar con paginación:
```bash
curl "http://127.0.0.1:8000/tasks?page=1&page_size=5"
```

## Modelos
- Task: `id`, `titulo`, `descripcion`, `estado`, `fecha` (timestamp), estados: `pending|in_progress|done`.
- User: `id`, `username` (único), `hashed_password`.

## Errores esperados
- 401: sin token o credenciales inválidas.
- 404: tarea no encontrada.
- 422: validación (campos faltantes o longitud mínima/ máxima).


