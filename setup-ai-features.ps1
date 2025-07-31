# Azure Cosmos DB AI Features Quick Start Script - PowerShell Version
# This script helps set up the environment for testing new AI features

Write-Host "=== Azure Cosmos DB AI Features Quick Start ===" -ForegroundColor Cyan
Write-Host ""

# Check if Azure CLI is installed
try {
    az --version | Out-Null
    Write-Host "✅ Azure CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Azure CLI is not installed. Please install it first:" -ForegroundColor Red
    Write-Host "   https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
}

# Login check
try {
    az account show | Out-Null
    Write-Host "✅ Azure login verified" -ForegroundColor Green
} catch {
    Write-Host "🔐 Please login to Azure first:" -ForegroundColor Yellow
    az login
}

# Set variables (user should modify these)
$RESOURCE_GROUP = "cosmosdb-ai-workshop"
$COSMOS_ACCOUNT = "smartbooking-ai-$(Get-Date -Format 'yyyyMMddHHmmss')"
$LOCATION = "East US"
$DATABASE_NAME = "AIWorkshopDB"

Write-Host ""
Write-Host "📋 Configuration:" -ForegroundColor Cyan
Write-Host "   Resource Group: $RESOURCE_GROUP"
Write-Host "   Cosmos Account: $COSMOS_ACCOUNT"
Write-Host "   Location: $LOCATION"
Write-Host "   Database: $DATABASE_NAME"
Write-Host ""

$confirmation = Read-Host "Continue with this configuration? (y/n)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Host "❌ Setup cancelled" -ForegroundColor Red
    exit 1
}

# Create resource group
Write-Host "📦 Creating resource group..." -ForegroundColor Yellow
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Cosmos DB account with AI features
Write-Host "🚀 Creating Cosmos DB account with AI features (this may take 5-10 minutes)..." -ForegroundColor Yellow
$createResult = az cosmosdb create `
    --resource-group $RESOURCE_GROUP `
    --name $COSMOS_ACCOUNT `
    --kind GlobalDocumentDB `
    --locations regionName=$LOCATION failoverPriority=0 isZoneRedundant=False `
    --default-consistency-level Session `
    --enable-free-tier true `
    --capabilities EnableServerless EnableNoSQLVectorSearch

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Cosmos DB account created successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Failed to create Cosmos DB account" -ForegroundColor Red
    exit 1
}

# Create database
Write-Host "📊 Creating database..." -ForegroundColor Yellow
az cosmosdb sql database create `
    --resource-group $RESOURCE_GROUP `
    --account-name $COSMOS_ACCOUNT `
    --name $DATABASE_NAME

# Create container with vector indexing
Write-Host "📁 Creating container with vector indexing..." -ForegroundColor Yellow
$indexingPolicy = @'
{
    "indexingMode": "consistent",
    "automatic": true,
    "includedPaths": [{"path": "/*"}],
    "excludedPaths": [{"path": "/_etag/?"}],
    "vectorIndexes": [{"path": "/vectorProperty", "type": "diskANN"}]
}
'@

az cosmosdb sql container create `
    --resource-group $RESOURCE_GROUP `
    --account-name $COSMOS_ACCOUNT `
    --database-name $DATABASE_NAME `
    --name "AIContainer" `
    --partition-key-path "/tenantId" `
    --indexing-policy $indexingPolicy

# Get connection strings
Write-Host "🔑 Retrieving connection strings..." -ForegroundColor Yellow
$PRIMARY_CONNECTION = az cosmosdb keys list --resource-group $RESOURCE_GROUP --name $COSMOS_ACCOUNT --type connection-strings --query 'connectionStrings[0].connectionString' -o tsv

Write-Host ""
Write-Host "🎉 Setup Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Your AI-Enhanced Cosmos DB Setup:" -ForegroundColor Cyan
Write-Host "   Account Name: $COSMOS_ACCOUNT"
Write-Host "   Database: $DATABASE_NAME"
Write-Host "   Container: AIContainer"
Write-Host "   Resource Group: $RESOURCE_GROUP"
Write-Host ""
Write-Host "🔑 Connection String:" -ForegroundColor Cyan
Write-Host "   $PRIMARY_CONNECTION"
Write-Host ""
Write-Host "📝 Next Steps:" -ForegroundColor Yellow
Write-Host "   1. Set up Dedicated Gateway for Integrated Cache:"
Write-Host "      - Go to Azure Portal > Your Cosmos DB > Settings > Dedicated Gateway"
Write-Host "      - Configure D4s SKU with 1 instance"
Write-Host ""
Write-Host "   2. Enable Query Copilot Preview:"
Write-Host "      - Enroll in Microsoft Copilot for Azure preview"
Write-Host "      - Access via Data Explorer in Azure Portal"
Write-Host ""
Write-Host "   3. Try the sample applications:"
Write-Host "      - C#: samples/CosmosDB_AI_Features_Demo.cs"
Write-Host "      - Python: samples/cosmos_ai_demo.py"
Write-Host ""
Write-Host "   4. Load sample AI data:"
Write-Host "      - Use data/AI_Enhanced_Hotel_Data.json"
Write-Host ""
Write-Host "📚 Documentation:" -ForegroundColor Cyan
Write-Host "   - Implementation Guide: AI-Features-Implementation-Guide.md"
Write-Host "   - Workshop README: README.md (Challenge 6)"
Write-Host ""

# Create environment file for easy reference
$envContent = @"
# Azure Cosmos DB AI Features Environment Variables
COSMOS_ACCOUNT_NAME=$COSMOS_ACCOUNT
COSMOS_DATABASE_NAME=$DATABASE_NAME
COSMOS_CONTAINER_NAME=AIContainer
COSMOS_RESOURCE_GROUP=$RESOURCE_GROUP
COSMOS_CONNECTION_STRING="$PRIMARY_CONNECTION"

# Instructions:
# 1. Get dedicated gateway connection string from Azure Portal
# 2. Replace COSMOS_CONNECTION_STRING with dedicated gateway string for cache features
# 3. Install Python requirements: pip install -r samples/requirements.txt
# 4. Run samples with these environment variables
"@

$envContent | Out-File -FilePath ".env" -Encoding UTF8

Write-Host "💾 Environment variables saved to .env file" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  Important: To use Integrated Cache, replace the connection string in .env" -ForegroundColor Yellow
Write-Host "   with the Dedicated Gateway connection string from Azure Portal"
Write-Host ""
Write-Host "🔧 To set up Dedicated Gateway via CLI (optional):" -ForegroundColor Cyan
Write-Host "   az cosmosdb service create \"
Write-Host "     --resource-group $RESOURCE_GROUP \"
Write-Host "     --account-name $COSMOS_ACCOUNT \"
Write-Host "     --kind DedicatedGateway \"
Write-Host "     --count 1 \"
Write-Host "     --size Cosmos.D4s"
Write-Host ""
Write-Host "Happy coding with Azure Cosmos DB AI features! 🚀" -ForegroundColor Green
