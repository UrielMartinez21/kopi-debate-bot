# Kopi Debate Bot 🤖

Un chatbot persuasivo de IA que puede mantener debates e intentar convencer al otro lado de sus puntos de vista, independientemente de cuán irracional sea el punto.

## 📋 Características

- **API REST completa** construida con FastAPI
- **Debates inteligentes** que mantienen posiciones firmes y persuasivas
- **Persistencia de conversaciones** usando PostgreSQL/SQLite
- **Containerización completa** con Docker y Docker Compose
- **Tests comprehensivos** con pytest y cobertura de código
- **Documentación automática** con Swagger UI
- **Respuestas bajo 30 segundos** como se requiere
- **Historial de conversación** con las últimas 5 interacciones

## 🏗️ Arquitectura

### Decisiones de Diseño

**FastAPI**: Elegido por su excelente rendimiento, documentación automática con OpenAPI, y soporte nativo para async/await.

**SQLAlchemy con AsyncIO**: Para manejo eficiente de base de datos con operaciones no bloqueantes.

**PostgreSQL en producción, SQLite en desarrollo**: PostgreSQL para robustez en producción, SQLite para facilidad de desarrollo.

**Estrategia de Debate Modular**: El `DebateBot` utiliza diferentes tácticas de persuasión basadas en el contexto de la conversación.

**Containerización**: Docker garantiza consistencia entre entornos y facilita el despliegue.

### Estructura del Proyecto

```
kopi-debate-bot/
├── src/
│   └── kopi_bot/
│       ├── __init__.py          # Inicialización del paquete
│       ├── main.py              # Aplicación FastAPI principal
│       ├── schemas.py           # Modelos Pydantic para request/response
│       ├── models.py            # Modelos SQLAlchemy para base de datos
│       ├── database.py          # Servicio de base de datos
│       ├── debate_bot.py        # Lógica principal del bot de debate
│       └── config.py            # Configuración de la aplicación
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Configuración y fixtures de pytest
│   ├── test_api.py             # Tests de endpoints de API
│   ├── test_debate_bot.py      # Tests de lógica del bot
│   └── test_database.py        # Tests de operaciones de base de datos
├── requirements.txt            # Dependencias de producción
├── requirements-dev.txt        # Dependencias de desarrollo
├── Dockerfile                  # Configuración de container
├── docker-compose.yml          # Orquestación de servicios
├── Makefile                    # Comandos de automatización
├── .env.example               # Variables de entorno de ejemplo
├── .gitignore                 # Archivos a ignorar en Git
└── README.md                  # Este archivo
```

## 🚀 Inicio Rápido

### Prerrequisitos

- **Python 3.12.8** (requerido)
- **Docker** y **Docker Compose**
- **Git** (para clonar el repositorio)

En Windows, puedes instalar estos desde:
- Python: https://www.python.org/downloads/release/python-3128/
- Docker Desktop: https://www.docker.com/products/docker-desktop/

### 1. Clonar el Repositorio

```bash
git clone <repository-url>
cd kopi-debate-bot
```

### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env con tus valores (opcional para el funcionamiento básico)
```

**Variables de Entorno Requeridas:**

| Variable | Descripción | Valor por Defecto | Requerido |
|----------|-------------|-------------------|-----------|
| `DATABASE_URL` | URL de conexión a la base de datos | `postgresql://postgres:password@db:5432/kopi_debate` | No |
| `DEBUG` | Modo debug (true/false) | `false` | No |
| `LOG_LEVEL` | Nivel de logging | `INFO` | No |
| `OPENAI_API_KEY` | Clave API de OpenAI (para funcionalidad extendida) | None | No |

### 3. Ejecutar con Docker (Recomendado)

**En Windows (PowerShell):**
```powershell
# Instalar dependencias y verificar requisitos
.\run.ps1 install

# Ejecutar todos los servicios
.\run.ps1 run
```

**En Windows (CMD):**
```cmd
# Instalar dependencias y verificar requisitos
run.bat install

# Ejecutar todos los servicios
run.bat run
```

**En Linux/Mac:**
```bash
# Instalar dependencias y verificar requisitos
make install

# Ejecutar todos los servicios
make run
```

La API estará disponible en:
- **API Principal**: http://localhost:8000
- **Documentación Swagger**: http://localhost:8000/docs
- **Documentación ReDoc**: http://localhost:8000/redoc

### 4. Ejecutar en Modo Desarrollo

**En Windows (PowerShell):**
```powershell
# Instalar dependencias
.\run.ps1 install

# Ejecutar en modo desarrollo (con recarga automática)
.\run.ps1 dev
```

**En Windows (CMD):**
```cmd
# Instalar dependencias
run.bat install

# Ejecutar en modo desarrollo (con recarga automática)
run.bat dev
```

**En Linux/Mac:**
```bash
# Instalar dependencias
make install

# Ejecutar en modo desarrollo (con recarga automática)
make dev
```

## 🧪 Testing

**En Windows (PowerShell/CMD):**
```powershell
# Ejecutar todos los tests
.\run.ps1 test
# o
run.bat test
```

**En Linux/Mac:**
```bash
# Ejecutar todos los tests
make test
```

Los tests incluyen:
- **Tests unitarios** para la lógica del bot
- **Tests de integración** para la API
- **Tests de base de datos** para persistencia
- **Tests de flujo completo** para conversaciones

## 📚 Uso de la API

### Iniciar Nueva Conversación

```bash
curl -X POST "http://localhost:8000/conversation" \
     -H "Content-Type: application/json" \
     -d '{
       "conversation_id": null,
       "message": "I think climate change is not real"
     }'
```

**Respuesta:**
```json
{
  "conversation_id": "conv_abc123",
  "messages": [
    {
      "role": "user",
      "message": "I think climate change is not real"
    },
    {
      "role": "bot",
      "message": "I understand your perspective, but let me share compelling evidence that climate change is indeed happening..."
    }
  ]
}
```

### Continuar Conversación

```bash
curl -X POST "http://localhost:8000/conversation" \
     -H "Content-Type: application/json" \
     -d '{
       "conversation_id": "conv_abc123",
       "message": "But what about natural climate cycles?"
     }'
```

### Obtener Historial de Conversación

```bash
curl -X GET "http://localhost:8000/conversation/conv_abc123"
```

### Verificar Estado de la API

```bash
curl -X GET "http://localhost:8000/health"
```

## 🤖 Comportamiento del Bot

### Estrategias de Debate

El bot utiliza múltiples estrategias persuasivas:

1. **Reconocer y Contrarrestar**: Reconoce puntos válidos pero presenta contraargumentos
2. **Proporcionar Evidencia**: Presenta datos y investigación científica
3. **Apelación Emocional**: Conecta con valores humanos y consecuencias reales
4. **Progresión Lógica**: Construye argumentos paso a paso

### Temas Soportados

El bot está especialmente entrenado para debatir sobre:
- **Cambio climático** (posición pro-ciencia)
- **Vacunas** (posición pro-vacunas)
- **Forma de la Tierra** (posición pro-ciencia)
- **Evolución** (posición pro-ciencia)
- **Temas generales** (toma posición contraria para generar debate)

### Mantenimiento de Posición

- El bot **mantiene posiciones firmes** a lo largo de toda la conversación
- **No cambia de opinión** independientemente de los argumentos del usuario
- **Utiliza evidencia científica** para respaldar sus posiciones
- **Aplica tácticas de persuasión** para intentar convencer al usuario

## 🛠️ Comandos de Desarrollo

```bash
# Mostrar ayuda
make help

# Instalar dependencias
make install

# Ejecutar tests
make test

# Ejecutar en Docker
make run

# Detener servicios
make down

# Limpiar completamente (contenedores, volúmenes, imágenes)
make clean

# Ejecutar en modo desarrollo
make dev

# Ver logs de servicios
make logs

# Ver estado de servicios
make status

# Reconstruir sin cache
make rebuild
```

## 🔧 Configuración Avanzada

### Base de Datos

**Desarrollo (SQLite):**
```bash
DATABASE_URL=sqlite:///./kopi_debate.db
```

**Producción (PostgreSQL):**
```bash
DATABASE_URL=postgresql://user:password@host:port/database
```

### Configuración de Logging

```bash
LOG_LEVEL=INFO    # DEBUG, INFO, WARNING, ERROR
DEBUG=true        # Habilita logs detallados
```

### Límites de Conversación

```bash
MAX_CONVERSATION_HISTORY=5    # Mensajes por lado a mantener
MAX_MESSAGE_LENGTH=2000       # Caracteres máximos por mensaje
RESPONSE_TIMEOUT=30           # Segundos máximo para respuesta
```

## 🚀 Despliegue en Producción

### Variables de Entorno de Producción

```bash
DATABASE_URL=postgresql://user:password@host:port/database
DEBUG=false
LOG_LEVEL=WARNING
OPENAI_API_KEY=your_production_key
```

### Consideraciones de Seguridad

1. **Usar PostgreSQL** en lugar de SQLite
2. **Configurar CORS** apropiadamente en `main.py`
3. **Usar HTTPS** con un proxy reverso (nginx)
4. **Limitar rate limiting** en el proxy
5. **Monitorear logs** para detectar abusos

### Docker en Producción

```bash
# Construir imagen de producción
docker build -t kopi-debate-bot:latest .

# Ejecutar con variables de entorno de producción
docker run -d \
  -p 8000:8000 \
  -e DATABASE_URL=postgresql://... \
  -e DEBUG=false \
  kopi-debate-bot:latest
```

## 🧪 Ejemplos de Uso

### Ejemplo 1: Debate sobre Cambio Climático

```json
{
  "conversation_id": null,
  "message": "El cambio climático es una mentira inventada por los políticos"
}
```

**Respuesta del bot:** Proporcionará evidencia científica sobre el cambio climático y mantendrá una posición pro-ciencia.

### Ejemplo 2: Debate sobre Vacunas

```json
{
  "conversation_id": null,
  "message": "Las vacunas causan autismo"
}
```

**Respuesta del bot:** Citará estudios científicos que desmienten esta afirmación y promoverá la vacunación.

### Ejemplo 3: Conversación Larga

El bot puede mantener conversaciones de más de 5 intercambios, manteniendo consistencia en su posición y recordando el contexto de la conversación.

## 🤝 Contribución

### Estructura de Commits

```bash
git commit -m "feat: añadir nueva estrategia de persuasión"
git commit -m "fix: corregir problema de persistencia de conversaciones"
git commit -m "docs: actualizar README con ejemplos"
```

### Agregar Nuevos Temas de Debate

1. Editar `src/kopi_bot/debate_bot.py`
2. Agregar el nuevo tema en `_load_debate_topics()`
3. Añadir lógica de detección en `analyze_first_message()`
4. Crear tests correspondientes

### Ejecutar Tests Antes de Commit

```bash
make test
make lint
make format
```

## 📊 Monitoreo y Logs

### Métricas Importantes

- **Tiempo de respuesta** (debe ser < 30 segundos)
- **Tasa de error** de la API
- **Longitud promedio** de conversaciones
- **Tipos de temas** más debatidos

### Logs Estructurados

El sistema utiliza `structlog` para logging estructurado:

```python
logger.info("Processing conversation", 
           conversation_id=conv_id,
           message_length=len(message))
```

## ❓ Resolución de Problemas

### Problemas Comunes

**Error: "No se puede conectar a la base de datos"**
```bash
# Verificar que PostgreSQL esté ejecutándose
make status

# Recrear servicios
make down
make run
```

**Error: "Puerto 8000 ya está en uso"**
```bash
# Encontrar el proceso que usa el puerto
netstat -ano | findstr :8000

# Detener servicios existentes
make down
```

**Tests fallando**
```bash
# Asegurar que las dependencias de desarrollo estén instaladas
make install

# Ejecutar tests con más verbosidad
venv\Scripts\python -m pytest tests/ -v -s
```

### Logs de Debug

```bash
# Ver logs en tiempo real
make logs

# Ver logs de un servicio específico
docker-compose logs -f api
docker-compose logs -f db
```

## 📄 Licencia

Este proyecto está desarrollado para el desafío Kopi. Todos los derechos reservados.

---

## 📞 Soporte

Para preguntas o problemas:

1. Verificar esta documentación
2. Revisar los logs con `make logs`
3. Ejecutar tests con `make test`
4. Verificar el estado con `make status`

**¡El bot está listo para debates intensos y persuasivos! 🚀**