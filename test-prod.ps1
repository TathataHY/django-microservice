# Script para probar configuración de producción
# Ejecutar con: .\test-prod.ps1

Write-Host "🧪 Probando configuración de producción..." -ForegroundColor Cyan

# 1. Verificar que los servicios están corriendo
Write-Host "`n1. Verificando servicios..." -ForegroundColor Yellow
docker-compose ps

# 2. Health checks
Write-Host "`n2. Probando health checks..." -ForegroundColor Yellow
Write-Host "Healthz:"
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/healthz -UseBasicParsing
    Write-Host $response.Content -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

Write-Host "`nReadyz:"
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/readyz -UseBasicParsing
    Write-Host $response.Content -ForegroundColor Green
} catch {
    Write-Host "❌ Error: $_" -ForegroundColor Red
}

# 3. Verificar DEBUG
Write-Host "`n3. Verificando DEBUG=False..." -ForegroundColor Yellow
try {
    $debug = docker-compose exec -T web python -c "from django.conf import settings; print(settings.DEBUG)"
    if ($debug -match "False") {
        Write-Host "✅ DEBUG está en False (correcto para producción)" -ForegroundColor Green
    } else {
        Write-Host "⚠️  DEBUG está en True (debería ser False)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error verificando DEBUG: $_" -ForegroundColor Red
}

# 4. Verificar settings module
Write-Host "`n4. Verificando settings module..." -ForegroundColor Yellow
try {
    $settings = docker-compose exec -T web python -c "import os; print(os.getenv('DJANGO_SETTINGS_MODULE'))"
    if ($settings -match "prod") {
        Write-Host "✅ Usando settings de producción: $settings" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Usando: $settings (debería ser core.settings.prod)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error verificando settings: $_" -ForegroundColor Red
}

# 5. Verificar usuario no-root
Write-Host "`n5. Verificando usuario no-root..." -ForegroundColor Yellow
try {
    $user = docker-compose exec -T web whoami
    if ($user -match "appuser") {
        Write-Host "✅ Ejecutando como usuario no-root: $user" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Ejecutando como: $user" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error verificando usuario: $_" -ForegroundColor Red
}

# 6. Verificar Gunicorn
Write-Host "`n6. Verificando Gunicorn..." -ForegroundColor Yellow
try {
    $gunicorn = docker-compose exec -T web ps aux | Select-String "gunicorn"
    if ($gunicorn) {
        Write-Host "✅ Gunicorn está corriendo" -ForegroundColor Green
        Write-Host $gunicorn -ForegroundColor Gray
    } else {
        Write-Host "⚠️  Gunicorn no encontrado" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error verificando Gunicorn: $_" -ForegroundColor Red
}

# 7. Probar API
Write-Host "`n7. Probando API..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri http://localhost:8000/api/v1/persons/ -UseBasicParsing
    Write-Host "✅ API respondiendo correctamente (Status: $($response.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "❌ Error en API: $_" -ForegroundColor Red
}

# 8. Verificar métricas
Write-Host "`n8. Verificando métricas..." -ForegroundColor Yellow
try {
    $metrics = Invoke-WebRequest -Uri http://localhost:8000/metrics -UseBasicParsing
    if ($metrics.Content -match "http_requests_total") {
        Write-Host "✅ Métricas disponibles" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Métricas no encontradas" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error verificando métricas: $_" -ForegroundColor Red
}

# 9. Verificar logs (formato JSON)
Write-Host "`n9. Verificando formato de logs..." -ForegroundColor Yellow
Write-Host "Revisa los logs con: make logs" -ForegroundColor Cyan
Write-Host "En producción deberían estar en formato JSON" -ForegroundColor Cyan

Write-Host "`nPruebas completadas!" -ForegroundColor Green
Write-Host "`nRevisa los resultados arriba. Todo deberia estar en verde" -ForegroundColor Cyan

