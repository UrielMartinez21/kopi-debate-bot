# 🚂 Despliegue en Railway - Guía Súper Fácil

## 🎯 ¿Por qué Railway?

- ✅ **Gratis** para empezar (500 horas/mes)
- ✅ **Despliegue automático** desde GitHub
- ✅ **URL pública inmediata**
- ✅ **Logs en tiempo real**
- ✅ **HTTPS automático**

## 🚀 Pasos para Desplegar (5 minutos)

### **1. Crear cuenta en Railway**
- Ve a https://railway.app
- Haz clic en "Login with GitHub"
- Autoriza Railway a acceder a tus repos

### **2. Crear nuevo proyecto**
- Clic en "New Project"
- Selecciona "Deploy from GitHub repo"
- Busca y selecciona `UrielMartinez21/kopi-debate-bot`
- Clic en "Deploy Now"

### **3. Configurar variables de entorno (Opcional)**
Railway detectará automáticamente tu `railway.toml`, pero puedes ajustar:

- `DATABASE_URL`: `sqlite:///./kopi_debate.db` (ya configurado)
- `DEBUG`: `false` (ya configurado)
- `LOG_LEVEL`: `INFO` (ya configurado)

### **4. ¡Listo!**
Railway automáticamente:
- ✅ Detecta que es una app FastAPI
- ✅ Instala dependencias de `requirements.txt`
- ✅ Ejecuta el comando de start
- ✅ Te da una URL pública

## 🌐 Tu API estará disponible en:

```
https://tu-proyecto-production.up.railway.app
```

**Endpoints principales:**
- `GET /` - Estado de la API
- `GET /health` - Health check
- `GET /docs` - Documentación interactiva Swagger
- `POST /conversation` - Endpoint principal del chatbot

## 📊 Monitoreo

En el dashboard de Railway puedes ver:
- ✅ **Logs en tiempo real**
- ✅ **Métricas de CPU/RAM**
- ✅ **Status del deployment**
- ✅ **URL pública**

## 🧪 Probar tu API

Una vez desplegada, prueba con:

```bash
# Health check
curl https://tu-proyecto-production.up.railway.app/health

# Iniciar conversación
curl -X POST "https://tu-proyecto-production.up.railway.app/conversation" \
     -H "Content-Type: application/json" \
     -d '{"conversation_id": null, "message": "I think climate change is fake"}'
```

## 🎯 Para el Desafío Kopi

✅ **URL pública**: `https://tu-proyecto-production.up.railway.app`
✅ **API funcionando**: Lista para ser probada
✅ **Documentación**: En `/docs`

¡Perfecto para enviar en tu submission! 🎉

## 💰 Costos

- **Plan gratuito**: 500 horas/mes (suficiente para el desafío)
- **Si necesitas más**: $5/mes por servicio

## 🛠️ Comandos Útiles

Para actualizaciones futuras:
```bash
git add .
git commit -m "Update API"
git push origin main
```

Railway redesplegará automáticamente con cada push a `main`.

## 🔧 Troubleshooting

**Si algo no funciona:**

1. **Check logs** en Railway dashboard
2. **Verifica variables de entorno**
3. **Confirma que requirements.txt está correcto**

**Problemas comunes:**
- Si no inicia: Verifica el comando start en `railway.toml`
- Si no responde: Verifica que esté usando `PORT` environment variable
- Si errores de DB: SQLite debería funcionar out-of-the-box

¡Railway es súper confiable y fácil de usar! 🚂