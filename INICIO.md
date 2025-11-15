# 🚀 Guía de Inicio Rápido

## Pasos para iniciar la aplicación

### 1. Verificar que Docker Desktop esté corriendo

**En Windows:**
- Abre Docker Desktop desde el menú de inicio
- Espera a que aparezca el ícono de Docker en la bandeja del sistema (tray)
- Debe decir "Docker Desktop is running"

### 2. Crear archivo de variables de entorno

```powershell
# Si no existe .env, créalo desde el ejemplo
Copy-Item env.example .env
```

O manualmente:
- Copia `env.example` y renómbralo a `.env`

### 3. Construir las imágenes Docker

```powershell
docker-compose build
```

O usando Make:
```powershell
make build
```

**⏱️ Esto puede tardar varios minutos la primera vez** (descarga Python, PostgreSQL, instala dependencias)

### 4. Levantar los servicios

```powershell
docker-compose up -d
```

O usando Make:
```powershell
make up
```

Esto levanta:
- ✅ PostgreSQL (puerto 5432)
- ✅ Django app (puerto 8000)

### 5. Ejecutar migraciones (crear tablas en la BD)

```powershell
docker-compose run --rm web python manage.py migrate
```

O usando Make:
```powershell
make migrate
```

### 6. Verificar que todo funciona

**Health check:**
```powershell
curl http://localhost:8000/healthz
```

O abre en el navegador: http://localhost:8000/healthz

**Readiness check:**
```powershell
curl http://localhost:8000/readyz
```

O abre en el navegador: http://localhost:8000/readyz

### 7. Acceder a la API

**Documentación Swagger:**
http://localhost:8000/api/docs/

**Admin de Django:**
http://localhost:8000/admin/

**API de Personas:**
http://localhost:8000/api/v1/persons/

**API de Productos:**
http://localhost:8000/api/v1/products/

---

## Comandos útiles

### Ver logs
```powershell
docker-compose logs -f web
# O
make logs
```

### Detener servicios
```powershell
docker-compose down
# O
make down
```

### Crear superusuario (para admin)
```powershell
docker-compose run --rm web python manage.py createsuperuser
# O
make superuser
```

### Ver estado de contenedores
```powershell
docker-compose ps
```

### Reiniciar servicios
```powershell
docker-compose restart
```

---

## Solución de problemas

### Error: "Docker daemon is not running"
- Inicia Docker Desktop
- Espera a que esté completamente iniciado

### Error: "Port already in use"
- Alguien más está usando el puerto 8000 o 5432
- Cambia el puerto en `.env`: `WEB_PORT=8001`

### Error: "Cannot connect to database"
- Verifica que el servicio `db` esté corriendo: `docker-compose ps`
- Espera unos segundos después de `docker-compose up` para que PostgreSQL inicie

### Ver logs de errores
```powershell
docker-compose logs web
docker-compose logs db
```

---

## Prueba rápida de la API

### Crear una Persona:
```powershell
curl -X POST http://localhost:8000/api/v1/persons/ `
  -H "Content-Type: application/json" `
  -d '{\"first_name\": \"Juan\", \"last_name\": \"Pérez\", \"email\": \"juan@example.com\"}'
```

### Listar Personas:
```powershell
curl http://localhost:8000/api/v1/persons/
```

### Crear un Producto:
```powershell
curl -X POST http://localhost:8000/api/v1/products/ `
  -H "Content-Type: application/json" `
  -d '{\"name\": \"Laptop\", \"sku\": \"LAP-001\", \"price\": \"999.99\"}'
```

---

## ✅ Checklist de inicio

- [ ] Docker Desktop está corriendo
- [ ] Archivo `.env` creado
- [ ] Imágenes construidas (`docker-compose build`)
- [ ] Servicios levantados (`docker-compose up -d`)
- [ ] Migraciones ejecutadas (`make migrate`)
- [ ] Health check funciona (`/healthz`)
- [ ] API responde (`/api/v1/persons/`)

¡Listo! 🎉

