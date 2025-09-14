# Kopi Debate Bot - Azure Setup Script
# Run this in Azure Cloud Shell or with Azure CLI installed

# Variables
$RESOURCE_GROUP = "kopi-debate-bot-rg"
$LOCATION = "East US"
$ACR_NAME = "kopidebatebotregistry"
$SUBSCRIPTION_ID = "your-subscription-id"

Write-Host "🚀 Setting up Azure resources for Kopi Debate Bot..." -ForegroundColor Green

# 1. Create Resource Group
Write-Host "📁 Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. Create Azure Container Registry
Write-Host "🗃️ Creating Azure Container Registry..." -ForegroundColor Yellow
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# 3. Get ACR credentials
Write-Host "🔑 Getting ACR credentials..." -ForegroundColor Yellow
$ACR_USERNAME = az acr credential show --name $ACR_NAME --query username --output tsv
$ACR_PASSWORD = az acr credential show --name $ACR_NAME --query passwords[0].value --output tsv

# 4. Create Service Principal for GitHub Actions
Write-Host "👤 Creating service principal..." -ForegroundColor Yellow
$SP_OUTPUT = az ad sp create-for-rbac --name "kopi-debate-bot-sp" --role contributor --scopes "/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP" --sdk-auth

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Add these secrets to your GitHub repository:" -ForegroundColor Cyan
Write-Host "Settings > Secrets and variables > Actions > New repository secret"
Write-Host ""
Write-Host "Secret Name: AZURE_CREDENTIALS" -ForegroundColor Yellow
Write-Host "Secret Value:"
Write-Host $SP_OUTPUT
Write-Host ""
Write-Host "Secret Name: AZURE_REGISTRY_USERNAME" -ForegroundColor Yellow
Write-Host "Secret Value: $ACR_USERNAME"
Write-Host ""
Write-Host "Secret Name: AZURE_REGISTRY_PASSWORD" -ForegroundColor Yellow
Write-Host "Secret Value: $ACR_PASSWORD"
Write-Host ""
Write-Host "🌐 Once deployed, your API will be available at:" -ForegroundColor Green
Write-Host "http://kopi-debate-bot-{run-number}.eastus.azurecontainer.io:8000"