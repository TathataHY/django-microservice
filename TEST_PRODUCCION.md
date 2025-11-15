# 🧪 Guía para Probar Producción Localmente

Esta guía te muestra cómo probar la configuración de producción en tu máquina local usando Docker.

## 📋 Pasos para Probar Producción

### 1. Crear archivo .env para producción

Crea un archivo `.env` basado en `env.example` pero con configuración de producción:

```bash
# Copiar el ejemplo
cp env.example .env
```

Luego edita `.env` con estos valores de **producción**:

```env
# Django Settings - PRODUCCIÓN
DJANGO_SETTINGS_MODULE=core.settings.prod
SECRET_KEY=tu-clave-secreta-super-segura-aqui-genera-una-nueva
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://postgres:postgres@db:5432/app
POSTGRES_DB=app
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# JWT (Optional)
ENABLE_JWT=False
JWT_ACCESS_TTL_MIN=60

# Logging
LOG_LEVEL=INFO

# Server
WEB_PORT=8000

# Security (Production) - Descomentar para probar
# SECURE_SSL_REDIRECT=False  # False para local, True en producción real
```

### 2. Generar SECRET_KEY segura

```bash
# En PowerShell
python scripts/generate_secret_key.py
```

O manualmente, copia la clave generada y pégala en `.env` como `SECRET_KEY=...`

### 3. Construir y levantar servicios

```powershell
# Construir imágenes
make build

# Levantar servicios
make up
```

### 4. Ejecutar migraciones

```powershell
# Ejecutar migraciones
docker-compose run --rm --profile migrations migrations
```

O manualmente:
```powershell
docker-compose run --rm web python manage.py migrate
```

### 5. Verificar que está en modo producción

#### Verificar logs (deben estar en formato JSON)
```powershell
make logs
```

Deberías ver logs en formato JSON (no en formato texto plano).

#### Verificar que DEBUG está desactivado
```powershell
# Hacer una petición que cause error (debe mostrar página de error genérica, no detallada)
curl http://localhost:8000/api/v1/persons/99999999-9999-9999-9999-999999999999/
```

Si está en producción, verás un error genérico, no el detallado de Django.

### 6. Probar Health Checks

```powershell
# Health check
curl http://localhost:8000/healthz

# Debe responder: {"status":"ok","service":"django-microservice"}

# Readiness check
curl http://localhost:8000/readyz

# Debe responder: {"status":"ready","database":"connected"}
```

### 7. Probar API en modo producción

```powershell
# Crear una persona
curl -X POST http://localhost:8000/api/v1/persons/ `
  -H "Content-Type: application/json" `
  -d '{\"first_name\":\"Test\",\"last_name\":\"Production\",\"email\":\"test@prod.com\"}'

# Listar personas
curl http://localhost:8000/api/v1/persons/

# Ver métricas
curl http://localhost:8000/metrics
```

### 8. Verificar seguridad

#### Verificar que las cabeceras de seguridad están activas

En PowerShell, puedes usar:
```powershell
$response = Invoke-WebRequest -Uri http://localhost:8000/healthz
$response.Headers
```

O usar curl con verbose:
```powershell
curl -v http://localhost:8000/healthz
```

Deberías ver cabeceras como:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`

### 9. Verificar logs estructurados

Los logs en producción deben estar en formato JSON. Verifica con:

```powershell
make logs
```

Deberías ver algo como:
```json
{"asctime": "2025-01-15 10:30:45", "name": "django", "levelname": "INFO", "message": "..."}
```

En lugar de:
```
level=INFO timestamp=2025-01-15T10:30:45 logger=django message=...
```

## 🔍 Verificaciones Específicas de Producción

### ✅ Verificar que Gunicorn está corriendo

```powershell
docker-compose exec web ps aux | grep gunicorn
```

Deberías ver procesos de gunicorn con workers.

### ✅ Verificar que DEBUG=False

```powershell
docker-compose exec web python -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)"
```

Debería mostrar: `DEBUG: False`

### ✅ Verificar settings de producción

```powershell
docker-compose exec web python -c "from django.conf import settings; print('Settings module:', settings.SETTINGS_MODULE)"
```

Debería mostrar: `Settings module: core.settings.prod`

### ✅ Verificar usuario no-root

```powershell
docker-compose exec web whoami
```

Debería mostrar: `appuser` (no `root`)

## 🧪 Script de Prueba Completo

Crea un archivo `test-prod.ps1`:

```powershell
# Script para probar producción
Write-Host "🧪 Probando configuración de producción..." -ForegroundColor Cyan

# 1. Verificar que los servicios están corriendo
Write-Host "`n1. Verificando servicios..." -ForegroundColor Yellow
docker-compose ps

# 2. Health checks
Write-Host "`n2. Probando health checks..." -ForegroundColor Yellow
Write-Host "Healthz:"
curl http://localhost:8000/healthz
Write-Host "`nReadyz:"
curl http://localhost:8000/readyz

# 3. Verificar DEBUG
Write-Host "`n3. Verificando DEBUG=False..." -ForegroundColor Yellow
docker-compose exec web python -c "from django.conf import settings; print('DEBUG:', settings.DEBUG)"

# 4. Verificar settings module
Write-Host "`n4. Verificando settings module..." -ForegroundColor Yellow
docker-compose exec web python -c "import os; print('DJANGO_SETTINGS_MODULE:', os.getenv('DJANGO_SETTINGS_MODULE'))"

# 5. Probar API
Write-Host "`n5. Probando API..." -ForegroundColor Yellow
curl http://localhost:8000/api/v1/persons/

# 6. Verificar métricas
Write-Host "`n6. Verificando métricas..." -ForegroundColor Yellow
curl http://localhost:8000/metrics | Select-String "http_requests_total"

Write-Host "`n✅ Pruebas completadas!" -ForegroundColor Green
```

Ejecuta con:
```powershell
.\test-prod.ps1
```

## 🐛 Solución de Problemas

### Si los logs no están en JSON

Verifica que `DJANGO_SETTINGS_MODULE=core.settings.prod` en `.env`

### Si DEBUG sigue en True

1. Verifica `.env` tiene `DEBUG=False`
2. Reinicia los contenedores: `make down && make up`

### Si hay errores de ALLOWED_HOSTS

Agrega `localhost` y `127.0.0.1` a `ALLOWED_HOSTS` en `.env`:
```env
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Si no puedes acceder a la API

1. Verifica que el puerto 8000 está libre
2. Verifica que los contenedores están corriendo: `docker-compose ps`
3. Revisa los logs: `make logs`

## 📊 Comparación Dev vs Prod

| Aspecto | Desarrollo | Producción |
|---------|-----------|------------|
| Settings | `core.settings.dev` | `core.settings.prod` |
| DEBUG | `True` | `False` |
| Logs | Texto (key=value) | JSON |
| CORS | Todos los orígenes | Solo permitidos |
| Security Headers | Básicos | Completos (HSTS, etc.) |
| Server | runserver | Gunicorn |
| User | root (dev) | appuser (prod) |

## ✅ Checklist de Verificación

- [ ] `.env` configurado con `DJANGO_SETTINGS_MODULE=core.settings.prod`
- [ ] `DEBUG=False` en `.env`
- [ ] `SECRET_KEY` segura generada
- [ ] `ALLOWED_HOSTS` configurado
- [ ] Servicios levantados con `make up`
- [ ] Migraciones ejecutadas
- [ ] Health checks funcionando (`/healthz`, `/readyz`)
- [ ] API respondiendo correctamente
- [ ] Logs en formato JSON
- [ ] Gunicorn corriendo con workers
- [ ] Usuario no-root (`appuser`)
- [ ] Cabeceras de seguridad activas
- [ ] Métricas disponibles (`/metrics`)

## 🎯 Siguiente Paso

Una vez que todo funcione localmente en modo producción, estás listo para desplegar en un servidor real. Solo necesitas:

1. Configurar las variables de entorno del servidor
2. Configurar el dominio en `ALLOWED_HOSTS`
3. Configurar HTTPS y `SECURE_SSL_REDIRECT=True`
4. Desplegar con `docker-compose up -d`

