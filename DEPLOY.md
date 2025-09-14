# 🚀 Despliegue en Azure - Guía Paso a Paso

## Requisitos Previos

1. **Azure for Students Account**: https://azure.microsoft.com/en-us/free/students/
2. **Azure CLI** instalado: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli
3. **Repositorio en GitHub** (ya tienes esto ✅)

## 🛠️ Paso 1: Configurar Azure

### Opción A: Azure Cloud Shell (Más Fácil)
1. Ve a https://shell.azure.com
2. Selecciona PowerShell
3. Ejecuta el script de setup:

```bash
# Descargar y ejecutar setup
curl -O https://raw.githubusercontent.com/UrielMartinez21/kopi-debate-bot/main/azure-setup.ps1
./azure-setup.ps1
```

### Opción B: Azure CLI Local
```powershell
# Login a Azure
az login

# Ejecutar script de setup
.\azure-setup.ps1
```

## 🔑 Paso 2: Configurar GitHub Secrets

Ve a tu repositorio en GitHub:
`Settings > Secrets and variables > Actions > New repository secret`

Agrega estos **3 secrets**:

1. **AZURE_CREDENTIALS**
   - Obtén del output del script azure-setup.ps1
   - Es un JSON con las credenciales del service principal

2. **AZURE_REGISTRY_USERNAME**
   - Usuario del Azure Container Registry

3. **AZURE_REGISTRY_PASSWORD**
   - Contraseña del Azure Container Registry

## 🚀 Paso 3: Desplegar

¡Simplemente haz push a tu repositorio!

```bash
git add .
git commit -m "Setup Azure deployment"
git push origin main
```

GitHub Actions automáticamente:
1. ✅ Ejecutará tests
2. 🏗️ Construirá la imagen Docker
3. 📤 La subirá a Azure Container Registry
4. 🌐 Desplegará en Azure Container Instances

## 🌐 Resultado

Tu API estará disponible en:
- **URL**: `http://kopi-debate-bot-{run-number}.eastus.azurecontainer.io:8000`
- **Docs**: `http://kopi-debate-bot-{run-number}.eastus.azurecontainer.io:8000/docs`

El `{run-number}` será el número de ejecución de GitHub Actions.

## 📊 Monitoreo

- **GitHub Actions**: Ve el progreso en la pestaña "Actions" de tu repo
- **Azure Portal**: Monitorea recursos en https://portal.azure.com
- **Logs**: Ve logs del container en Azure Portal > Container Instances

## 💰 Costos

Con Azure for Students ($100 USD gratuitos):
- **Container Registry**: ~$0.167/día
- **Container Instance**: ~$1/día (1 vCPU, 1GB RAM)
- **Total**: ~$35/mes (dentro de tu crédito gratuito)

## 🛠️ Comandos Útiles

```bash
# Ver status del deployment
az container show --resource-group kopi-debate-bot-rg --name kopi-debate-bot-ci

# Ver logs
az container logs --resource-group kopi-debate-bot-rg --name kopi-debate-bot-ci

# Detener container (para ahorrar dinero)
az container stop --resource-group kopi-debate-bot-rg --name kopi-debate-bot-ci

# Reiniciar container
az container restart --resource-group kopi-debate-bot-rg --name kopi-debate-bot-ci
```

## 🎯 Para el Desafío Kopi

Una vez desplegado, tendrás:
✅ **URL pública de la API en ejecución** - Para enviar en tu submission
✅ **API completamente funcional** - Lista para ser probada
✅ **Documentación automática** - En `/docs`
✅ **Deployment automatizado** - Con GitHub Actions

¡Perfecto para cumplir con el requisito de "una URL pública de la API en ejecución que se puede probar"! 🎉