# Django Microservice

Microservicio Django + PostgreSQL listo para producción con API REST para gestión de Personas y Productos.

## 🚀 Características

- **Django 4+** con Django REST Framework
- **PostgreSQL** como base de datos
- **Docker** y **docker-compose** para despliegue
- **API REST** completa con CRUD para Personas y Productos
- **Filtros y paginación** en todos los endpoints
- **Health checks** (`/healthz`, `/readyz`)
- **Métricas Prometheus** (`/metrics`)
- **Documentación OpenAPI/Swagger** (`/api/docs/`)
- **Autenticación JWT** opcional
- **Logs estructurados** (JSON en producción)
- **Tests** con pytest (cobertura ≥65%)
- **Linting** con ruff y black
- **CI/CD** con GitLab CI

## 📋 Requisitos

- Python 3.11+
- Docker y docker-compose
- PostgreSQL 15+ (si no usas Docker)

## 🛠️ Instalación

### Opción 1: Docker (Recomendado)

1. Clona el repositorio:
```bash
git clone <repo-url>
cd django-microservice
```

2. Copia el archivo de variables de entorno:
```bash
cp .env.example .env
```

3. Edita `.env` con tus configuraciones (opcional):
```bash
# Edita SECRET_KEY, DATABASE_URL, etc.
```

4. Construye y levanta los servicios:
```bash
make build
make up
```

O usando docker-compose directamente:
```bash
docker-compose up -d
```

5. Ejecuta las migraciones:
```bash
make migrate
# O
docker-compose run --rm web python manage.py migrate
```

6. Crea un superusuario (opcional):
```bash
make superuser
# O
docker-compose run --rm web python manage.py createsuperuser
```

### Opción 2: Instalación Local

1. Crea un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instala las dependencias:
```bash
make install
# O
pip install -r requirements.txt
```

3. Configura las variables de entorno:
```bash
cp .env.example .env
# Edita .env con tus configuraciones
```

4. Ejecuta las migraciones:
```bash
make migrate
```

5. Inicia el servidor de desarrollo:
```bash
python manage.py runserver
```

## 📚 Uso de la API

### Endpoints Disponibles

#### Personas

- `POST /api/v1/persons/` - Crear persona
- `GET /api/v1/persons/` - Listar personas (paginado, filtros: `email`, `last_name`, orden: `ordering=created_at`)
- `GET /api/v1/persons/{id}/` - Obtener persona
- `PUT /api/v1/persons/{id}/` - Actualizar persona (completo)
- `PATCH /api/v1/persons/{id}/` - Actualizar persona (parcial)
- `DELETE /api/v1/persons/{id}/` - Eliminar persona

#### Productos

- `POST /api/v1/products/` - Crear producto
- `GET /api/v1/products/` - Listar productos (paginado, filtros: `sku`, `price_min`, `price_max`, `q` (búsqueda por nombre), orden: `ordering=price` o `ordering=created_at`)
- `GET /api/v1/products/{id}/` - Obtener producto
- `PUT /api/v1/products/{id}/` - Actualizar producto (completo)
- `PATCH /api/v1/products/{id}/` - Actualizar producto (parcial)
- `DELETE /api/v1/products/{id}/` - Eliminar producto

#### Health Checks

- `GET /healthz` - Verifica que la aplicación esté viva
- `GET /readyz` - Verifica que la base de datos esté conectada
- `GET /metrics` - Métricas Prometheus

#### Documentación

- `GET /api/docs/` - Swagger UI
- `GET /api/redoc/` - ReDoc
- `GET /api/schema/` - Schema OpenAPI (JSON)

### Ejemplos de Uso

#### Crear una Persona

```bash
curl -X POST http://localhost:8000/api/v1/persons/ \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }'
```

#### Listar Personas con Filtros

```bash
curl "http://localhost:8000/api/v1/persons/?email=john&ordering=-created_at"
```

#### Crear un Producto

```bash
curl -X POST http://localhost:8000/api/v1/products/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "sku": "LAP-001",
    "price": "999.99",
    "owner_id": "uuid-de-la-persona"
  }'
```

#### Buscar Productos

```bash
curl "http://localhost:8000/api/v1/products/?q=laptop&price_min=500&price_max=1500&ordering=price"
```

## 🧪 Testing

Ejecutar tests:

```bash
make test
# O
pytest
```

Ejecutar tests con cobertura:

```bash
make test-cov
# O
pytest --cov=api --cov=health --cov-report=html
```

Ver reporte de cobertura:
```bash
# Abre htmlcov/index.html en tu navegador
```

## 🔍 Linting y Formato

Formatear código:
```bash
make fmt
# O
black .
```

Linting:
```bash
make lint
# O
ruff check .
```

Linting con auto-fix:
```bash
make lint-fix
# O
ruff check --fix .
```

## 🐳 Comandos Docker

```bash
make build          # Construir imágenes
make up             # Levantar servicios
make down           # Detener servicios
make logs           # Ver logs
make docker-test    # Ejecutar tests en Docker
make docker-lint    # Ejecutar linter en Docker
make docker-migrate # Ejecutar migraciones en Docker
```

## 📝 Variables de Entorno

Principales variables de entorno (ver `.env.example`):

- `DJANGO_SETTINGS_MODULE` - Módulo de settings (dev/prod)
- `SECRET_KEY` - Clave secreta de Django
- `DEBUG` - Modo debug (True/False)
- `ALLOWED_HOSTS` - Hosts permitidos (separados por comas)
- `DATABASE_URL` - URL de conexión a PostgreSQL
- `CORS_ALLOWED_ORIGINS` - Orígenes permitidos para CORS
- `LOG_LEVEL` - Nivel de logging (DEBUG, INFO, WARNING, ERROR)
- `ENABLE_JWT` - Habilitar autenticación JWT (True/False)
- `JWT_ACCESS_TTL_MIN` - Tiempo de vida del token JWT en minutos

## 🔐 Autenticación JWT (Opcional)

Para habilitar JWT, configura en `.env`:

```env
ENABLE_JWT=True
```

Luego, usa el endpoint de login:

```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "tu_usuario",
    "password": "tu_contraseña"
  }'
```

Respuesta:
```json
{
  "refresh": "...",
  "access": "..."
}
```

Usa el token en las peticiones:
```bash
curl -H "Authorization: Bearer <token>" http://localhost:8000/api/v1/persons/
```

## 🏗️ Estructura del Proyecto

```
django-microservice/
├── api/                    # App principal de la API
│   ├── models.py          # Modelos Person y Product
│   ├── serializers.py     # Serializers DRF
│   ├── views.py           # ViewSets
│   ├── filters.py         # Filtros
│   ├── urls.py            # URLs de la API
│   └── tests/             # Tests
├── health/                 # Health checks y métricas
│   ├── views.py
│   └── tests/
├── core/                   # Configuración del proyecto
│   ├── settings/
│   │   ├── base.py        # Settings base
│   │   ├── dev.py         # Settings desarrollo
│   │   └── prod.py        # Settings producción
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── Makefile
└── README.md
```

## 🚀 Despliegue en Producción

1. Configura las variables de entorno de producción en `.env`
2. Asegúrate de que `DEBUG=False`
3. Configura `ALLOWED_HOSTS` con tu dominio
4. Genera una `SECRET_KEY` segura
5. Configura `SECURE_SSL_REDIRECT=True` si usas HTTPS
6. Construye y despliega:

```bash
docker-compose -f docker-compose.yml up -d
```

El servicio estará disponible en `http://localhost:8000` (o el puerto configurado).

## 📊 Métricas y Observabilidad

- **Health Check**: `GET /healthz`
- **Readiness Check**: `GET /readyz`
- **Métricas Prometheus**: `GET /metrics`

Los logs están en formato estructurado (JSON en producción) y se pueden configurar con `LOG_LEVEL`.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👤 Autor

Tu nombre aquí

## 🙏 Agradecimientos

- Django y Django REST Framework
- Comunidad de Python

